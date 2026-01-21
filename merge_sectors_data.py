from pathlib import Path
from datetime import datetime
import json
import asyncio
from parallel import Parallel
import os

from pararell_agents.financial_pararell import create_financial_task, save_financial_result
from pararell_agents.supply_chain_pararell import create_supply_chain_task, save_supply_chain_result
from pararell_agents.customers_markets_pararell import create_customers_markets_task, save_customers_markets_result
from pararell_agents.regulatory_trade_pararell import create_regulatory_trade_task, save_regulatory_trade_result

client = Parallel(api_key=os.getenv("PARALLEL_API_KEY"))

def collect_sources(data):
    """Collect all sources from the data"""
    sources = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "sources" and isinstance(value, list):
                sources.extend(value)
            elif isinstance(value, (dict, list)):
                sources.extend(collect_sources(value))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                sources.extend(collect_sources(item))
    return sources

def calculate_confidence(data):
    """Calculate overall confidence score"""
    # Simple heuristic: count non-null values
    sources = collect_sources(data)
    if sources:
        return min(len(sources) * 0.1, 1.0)
    return 0.5

def generate_concentration_flags(data):
    """Generate concentration risk flags"""
    flags = []
    # Add logic here to identify concentration risks
    return flags

def assess_data_quality(data):
    """Assess data quality"""
    sources = collect_sources(data)
    return {
        "source_summary": {
            "tier_1_count": len([s for s in sources if s.get("type") == "10-K"]),
            "tier_2_count": len([s for s in sources if s.get("type") in ["annual_report", "investor_presentation"]]),
            "tier_3_count": len([s for s in sources if s.get("type") in ["earnings_call", "press_release"]]),
            "tier_4_count": len([s for s in sources if s.get("type") == "news"])
        },
        "data_gaps": [],
        "stale_data_warnings": []
    }

def merge_sectors_data():
    files = ["financial.json", "supply_chain.json", "customers_markets.json", "regulatory_trade.json"]
    merged_data = {}
    
    for file in files:
        try:
            with open(f'data/{file}', 'r') as f:
                file_data = json.load(f)
                merged_data.update(file_data)
        except FileNotFoundError:
            print(f"Warning: {file} not found, skipping...")
            continue
    
    company_name = merged_data.get("company_overview", {}).get("name", "Unknown Company")
    ticker = merged_data.get("company_overview", {}).get("ticker", "UNKNOWN")
    profile = {
        "meta": {
            "company_name": company_name,
            "ticker": ticker,
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "baseline_fiscal_year": merged_data.get("financial_baseline", {}).get("fiscal_year"),
            "data_freshness_note": f"Compiled from {len(files)} data sources",
            "confidence_overall": calculate_confidence(merged_data),
            "primary_sources": [s.get("name", "") for s in collect_sources(merged_data)[:10]]
        },

        "company_overview": merged_data.get("company_overview", {}),

        "financial": {
            "business_segments": merged_data.get("business_segments", []),
            "revenue_by_region": merged_data.get("revenue_by_region", []),
            "financial_baseline": merged_data.get("financial_baseline", []),
            "sources": merged_data.get("sources", [])
        },

        "supply_chain": {
            "company_owned_facilities": merged_data.get("company_owned_facilities", []),
            "contract_manufacturers": merged_data.get("contract_manufacturers", []),
            "critical_suppliers": merged_data.get("critical_suppliers", []),
            "supplier_concentration": merged_data.get("supplier_concentration", {}),
            "supply_corridors": merged_data.get("supply_corridors", []),
            "supply_chain_initiatives": merged_data.get("supply_chain_initiatives", []),
            "sources": merged_data.get("sources", [])
        },

        "customer_profile": {
            "segment_mix": merged_data.get("segment_mix", []),
            "customer_concentration": merged_data.get("customer_concentration", {}),
            "top_customers": merged_data.get("top_customers", []),
            "industry_exposure": merged_data.get("industry_exposure", []),
            "customer_characteristics": merged_data.get("customer_characteristics", []),
            "sources": merged_data.get("sources", [])
        },

        "regulatory_footprint": {
            "policy_constraints": merged_data.get("policy_constraints", []),
            "regional_demand_signals": merged_data.get("regional_demand_signals", []),
            "competitor_factual_moves": merged_data.get("competitor_factual_moves", []),
            "factual_actions": merged_data.get("factual_actions", []),
            "sources": merged_data.get("sources", [])
        },

        # "strategic_initiatives": merged_data.get("strategic_initiatives", []),

        # "concentration_flags": generate_concentration_flags(merged_data),

        "data_quality": assess_data_quality(merged_data)
    }

    return profile, company_name, ticker

def merge_sectors_data_for_company():
    try:
        sectors_data, company_name, ticker = merge_sectors_data()
        with open(f'data/{ticker}_profile.json', 'w') as f:
            json.dump(sectors_data, f, indent=4)
        print(f"Successfully merged data for {company_name} into {company_name}_profile.json")
        return sectors_data, ticker
    except Exception as e:
        print(f"Error merging sectors data: {e}")
        import traceback
        traceback.print_exc()
        return None, None

async def run_all_agents(client: Parallel, company: str):
    """
    Run all agents in parallel using Option 2:
    1. Create all tasks first (fast, sync) - tasks start running on Parallel API immediately
    2. Poll all results in parallel using asyncio.to_thread
    """
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)

    print("Creating all tasks...")

    # Step 1: Create all tasks (these start immediately on the Parallel API)
    tasks = [
        ("financial", create_financial_task(client, company), save_financial_result),
        ("supply_chain", create_supply_chain_task(client, company), save_supply_chain_result),
        ("customers_markets", create_customers_markets_task(client, company), save_customers_markets_result),
        ("regulatory_trade", create_regulatory_trade_task(client, company), save_regulatory_trade_result),
    ]

    print(f"All {len(tasks)} tasks created. Waiting for results in parallel...")

    # Step 2: Poll all results in parallel using asyncio.to_thread
    async def get_and_save_result(name: str, task_run, save_func) -> bool:
        try:
            print(f"[{name}] Waiting for result (run_id: {task_run.run_id})...")

            # Poll with timeout to keep Streamlit alive
            max_wait_time = 1800  # 10 minutes
            poll_interval = 5  # Check every 5 seconds
            elapsed = 0

            while elapsed < max_wait_time:
                try:
                    # Try to get result with short timeout
                    result = await asyncio.wait_for(
                        asyncio.to_thread(client.task_run.result, task_run.run_id),
                        timeout=poll_interval
                    )
                    print(f"[{name}] Result received!")
                    return save_func(result)
                except asyncio.TimeoutError:
                    # Still waiting, keep Streamlit alive
                    elapsed += poll_interval
                    print(f"[{name}] Still waiting... ({elapsed}s elapsed)")
                    await asyncio.sleep(0.1)  # Brief pause

        except Exception as e:
            print(f"[{name}] Error: {e}")
            return False

    results = await asyncio.gather(*[
        get_and_save_result(name, task_run, save_func)
        for name, task_run, save_func in tasks
    ])

    return results

def pull_data_for_company(company: str):
    results = asyncio.run(run_all_agents(client, company))

    print(f"DEBUG: results type={type(results)}, results={results}")
    success_count = sum(results)
    print(f"\n{success_count}/{len(results)} agents completed successfully")

    if not all(results):
        agent_names = ["financial", "supply_chain", "customers_markets", "regulatory_trade"]
        for name, success in zip(agent_names, results):
            if not success:
                print(f"  - {name} failed")

    return merge_sectors_data_for_company()

# if __name__ == "__main__":
#     merge_sectors_data_for_company('DELL', 'DELL')
