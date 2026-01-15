from parallel import Parallel
import json


def create_financial_task(client: Parallel, company: str):
    """Create the financial task and return the task_run object (non-blocking)."""
    with open('prompts/financial_prompt.md', 'r') as f:
        system_prompt_base = f.read()
    system_prompt = f"##For company: {company} find this information\n\n{system_prompt_base}"
    
    processor = "ultra"
    print(f"[Financial] Creating task with processor: {processor}")

    return client.task_run.create(
        input=system_prompt,
        processor=processor,
        task_spec={
            "output_schema": {
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "company_overview": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The official legal name of the company"
                                },
                                "ticker": {
                                    "type": "string",
                                    "description": "The ticker symbol of the company"
                                },
                                "headquarters": {
                                    "type": "object",
                                    "properties": {
                                        "city": {
                                            "type": "string",
                                            "description": "The city of the company's headquarters"
                                        },
                                        "country": {
                                            "type": "string",
                                            "description": "The country of the company's headquarters"
                                        }
                                    },
                                    "required": ["city", "country"],
                                    "additionalProperties": False
                                },
                                "founded": {
                                    "type": "integer",
                                    "description": "The year the company was founded"
                                },
                                "employees": {
                                    "type": "integer",
                                    "description": "The number of employees the company has"
                                },
                                "business_description": {
                                    "type": "string",
                                    "description": "A description of the company's business"
                                },
                                "business_model": {
                                    "type": "string",
                                    "enum": [
                                        "vertically_integrated",
                                        "contract_manufacturing",
                                        "hybrid_manufacturing",
                                        "fabless",
                                        "ODM_reliant",
                                        "configure_to_order"
                                    ],
                                    "description": "The model of the company's business"
                                },
                                "value_chain_position": {
                                    "type": "string",
                                    "description": "Position in the technology value chain (e.g., component supplier, ODM/EMS, branded OEM, systems integrator, vertically integrated)"
                                }
                            },
                            "required": ["name", "ticker", "headquarters", "founded", "employees", "business_description", "business_model", "value_chain_position"],
                            "additionalProperties": False
                        },
                        "business_segments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the business segment (e.g., Infrastructure Solutions Group, Client Solutions Group)"
                                    },
                                    "revenue_usd_millions": {
                                        "type": ["number", "null"],
                                        "description": "Revenue in USD millions for this segment"
                                    },
                                    "revenue_percent": {
                                        "type": ["number", "null"],
                                        "description": "Percentage of total company revenue"
                                    },
                                    "operating_income_usd_millions": {
                                        "type": ["number", "null"],
                                        "description": "Operating income in USD millions"
                                    },
                                    "operating_margin_percent": {
                                        "type": ["number", "null"],
                                        "description": "Operating margin percentage for this segment"
                                    },
                                    "yoy_growth_percent": {
                                        "type": ["number", "null"],
                                        "description": "Year-over-year revenue growth percentage"
                                    },
                                    "fiscal_year": {
                                        "type": "string",
                                        "description": "Fiscal year for these metrics (e.g., FY2024, Q4 2024)"
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "Description of what this segment does and key products/services"
                                    }
                                },
                                "required": ["name", "description"],
                                "additionalProperties": False
                            }
                        },
                        "revenue_by_region": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "region": {
                                        "type": "string",
                                        "enum": ["Americas", "EMEA", "APJ", "Other"],
                                        "description": "The region"
                                    },
                                    "percent_of_total": {
                                        "type": "number",
                                        "description": "Percentage of total revenue (e.g., 47.9 for 47.9%)"
                                    },
                                    "revenue_usd_millions": {
                                        "type": ["number", "null"],
                                        "description": "Revenue in USD millions"
                                    },
                                    "yoy_growth_percent": {
                                        "type": ["number", "null"],
                                        "description": "Year-over-year growth percentage (e.g., -5.7 for -5.7%)"
                                    },
                                    "key_countries": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "Major countries in this region contributing significant revenue"
                                    }
                                },
                                "required": ["region", "percent_of_total"],
                                "additionalProperties": False
                            }
                        },
                        "financial_baseline": {
                            "type": "object",
                            "properties": {
                                "fiscal_year": {
                                    "type": "integer",
                                    "description": "The fiscal year of the company"
                                },
                                "revenue_usd_millions": {
                                    "type": "integer",
                                    "description": "The revenue of the company in USD millions"
                                },
                                "gross_margin": {
                                    "type": "number",
                                    "description": "The gross margin of the company (0.0-1.0)"
                                },
                                "operating_margin": {
                                    "type": "number",
                                    "description": "The operating margin of the company (0.0-1.0)"
                                },
                                "net_margin": {
                                    "type": "number",
                                    "description": "The net margin of the company (0.0-1.0)"
                                },
                                "market_cap_usd_millions": {
                                    "type": ["number", "null"],
                                    "description": "The market cap of the company in USD millions"
                                },
                                "cash_position_usd_millions": {
                                    "type": "integer",
                                    "description": "The cash position of the company in USD millions"
                                },
                                "total_debt_usd_millions": {
                                    "type": "integer",
                                    "description": "The total debt of the company in USD millions"
                                },
                                "debt_to_equity": {
                                    "type": ["number", "null"],
                                    "description": "The debt to equity ratio of the company"
                                },
                                "current_ratio": {
                                    "type": ["number", "null"],
                                    "description": "The current ratio of the company"
                                },
                                "balance_sheet_strength": {
                                    "type": "string",
                                    "enum": ["strong", "adequate", "weak"],
                                    "description": "The strength of the company's balance sheet"
                                }
                            },
                            "required": ["fiscal_year", "revenue_usd_millions", "gross_margin", "operating_margin", "net_margin", "market_cap_usd_millions", "cash_position_usd_millions", "total_debt_usd_millions", "debt_to_equity", "current_ratio", "balance_sheet_strength"],
                            "additionalProperties": False
                        },
                        "sources": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the source"
                                    },
                                    "type": {
                                        "type": "string",
                                        "enum": ["10-K", "annual_report", "investor_presentation", "earnings_call"],
                                        "description": "The type of the source"
                                    },
                                    "date": {
                                        "type": "string",
                                        "description": "The date of the source"
                                    }
                                },
                                "required": ["name", "type", "date"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["company_overview", "business_segments", "revenue_by_region", "financial_baseline", "sources"],
                    "additionalProperties": False
                },
                "type": "json"
            }
        }
    )


def save_financial_result(run_result) -> bool:
    """Save the financial result to a JSON file."""
    try:
        with open("data/financial.json", "w") as f:
            f.write(json.dumps(run_result.output.content, indent=4))
        print("[Financial] Data saved successfully")
        return True
    except Exception as e:
        print(f"[Financial] Error saving data: {e}")
        return False