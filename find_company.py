from parallel import Parallel
import json

client = Parallel(api_key="Bpx8ahd-2RcYB8wXLnIsbSaEWGTvu8lYGTnIlJeU")


system_prompt = """
# Company Intelligence Agent - Deep Research Prompt

**Purpose:** This prompt is used with Parallel API's Deep Research to extract comprehensive company data for geopolitical exposure analysis.

**Output Format:** Structured JSON for downstream UI display and FLOS analysis

---

## System Prompt

```
You are a Company Intelligence Analyst specializing in geopolitical and macroeconomic exposure mapping. Your task is to build a comprehensive FACTUAL profile of a company's operations, dependencies, and exposure points.

## CRITICAL CONSTRAINTS

This is DATA EXTRACTION, not ANALYSIS.

DO NOT:
- Score risks or opportunities (no -1.0 to +1.0 scores)
- Apply the 40/40/20 balance framework
- Assess impact severity or likelihood
- Link data to geopolitical scenarios
- Provide strategic recommendations
- Speculate or infer data that isn't sourced

DO:
- Extract verifiable facts from sources
- Flag data gaps explicitly with [DATA UNAVAILABLE]
- Apply source tiering (Tier 1-4)
- Maintain data provenance for every fact
- Note confidence levels based on source quality

## SOURCE TIERING

| Tier | Source Type | Confidence Weight |
|------|-------------|-------------------|
| 1 | SEC filings (10-K, 10-Q), audited financials | Highest |
| 2 | Investor presentations, earnings calls, official press releases | High |
| 3 | Industry reports, analyst coverage, reputable news | Medium |
| 4 | Marketing materials, data >2 years old | Low - reference only |

## OUTPUT FORMAT

You MUST return a valid JSON object following the exact schema provided. Do not include markdown formatting, code blocks, or explanatory text outside the JSON structure.
```

---

## User Prompt Template

```
Extract a comprehensive company profile for: Dell Technologies Inc.

Focus areas for geopolitical exposure analysis:
1. Where does this company operate? (facilities, manufacturing, offices)
2. Who does this company depend on? (suppliers, contract manufacturers, technology platforms)
3. Where does revenue come from? (geographic breakdown)
4. Who are the customers? (concentration, segments)
5. What regulatory jurisdictions apply?
6. What is the financial baseline? (size, margins, balance sheet strength)

Return the data as a JSON object following this exact schema:

{
  "meta": {
    "company_name": "string",
    "ticker": "string or null",
    "extraction_date": "YYYY-MM-DD",
    "baseline_fiscal_year": number,
    "data_freshness_note": "string (e.g., 'Based on FY2024 10-K filed February 2024')",
    "confidence_overall": number (0.0-1.0),
    "primary_sources": ["array of source descriptions"]
  },

  "company_overview": {
    "headquarters": {"city": "string", "country": "string"},
    "founded": number,
    "employees": number,
    "business_description": "string (2-3 sentences)",
    "business_model": "asset_heavy | asset_light | platform | hybrid",
    "primary_segments": [
      {"name": "string", "revenue_percent": number, "description": "string"}
    ],
    "value_chain_position": "upstream | midstream | downstream | integrated"
  },

  "geographic_exposure": {
    "revenue_by_region": [
      {
        "region": "string",
        "percent_of_total": number,
        "revenue_usd_millions": number or null,
        "yoy_growth": number or null,
        "source_tier": 1|2|3|4
      }
    ],
    "manufacturing_footprint": [
      {
        "country": "string",
        "percent_of_production": number or null,
        "facility_types": ["array"],
        "notes": "string",
        "source_tier": 1|2|3|4
      }
    ],
    "key_facilities": [
      {
        "name": "string",
        "location": {"city": "string", "country": "string"},
        "type": "manufacturing | r_and_d | datacenter | distribution | headquarters | office",
        "function": "string",
        "significance": "string (why this facility matters)",
        "source_tier": 1|2|3|4
      }
    ]
  },

  "supply_chain": {
    "critical_suppliers": [
      {
        "name": "string (actual company name)",
        "headquarters_country": "string",
        "provides": "string (specific components/services)",
        "dependency_level": "critical | high | medium",
        "single_source": true|false,
        "notes": "string",
        "source_tier": 1|2|3|4
      }
    ],
    "contract_manufacturers": [
      {
        "name": "string",
        "headquarters_country": "string",
        "production_countries": ["array"],
        "products_manufactured": "string",
        "source_tier": 1|2|3|4
      }
    ],
    "supplier_geography_concentration": {
      "top_country": "string",
      "top_country_percent": number or null,
      "top_3_countries": ["array"],
      "concentration_note": "string"
    }
  },

  "customer_profile": {
    "segment_mix": {
      "b2b_percent": number,
      "b2c_percent": number,
      "b2g_percent": number
    },
    "top_customers": [
      {
        "name": "string (or 'Undisclosed - Customer A')",
        "percent_of_revenue": number or null,
        "industry": "string",
        "source_tier": 1|2|3|4
      }
    ],
    "customer_concentration": {
      "top_customer_percent": number or null,
      "top_10_percent": number or null,
      "concentration_level": "high | medium | low",
      "note": "string"
    },
    "industry_exposure": [
      {"industry": "string", "percent_of_revenue": number}
    ]
  },

  "regulatory_footprint": {
    "primary_jurisdictions": [
      {
        "jurisdiction": "string",
        "regulatory_bodies": ["array"],
        "key_requirements": ["array"],
        "exposure_level": "high | medium | low"
      }
    ],
    "trade_exposure": {
      "tariff_exposure": {
        "level": "high | medium | low",
        "key_tariffs": ["array of specific tariffs affecting company"],
        "notes": "string"
      },
      "export_controls": {
        "level": "high | medium | low",
        "applicable_regimes": ["array (e.g., 'EAR', 'ITAR')"],
        "notes": "string"
      },
      "sanctions_exposure": {
        "level": "high | medium | low",
        "notes": "string"
      }
    },
    "compliance_domains": ["array (e.g., 'data_privacy', 'environmental', 'labor')"]
  },

  "financial_baseline": {
    "fiscal_year": number,
    "revenue_usd_millions": number,
    "gross_margin": number (0.0-1.0),
    "operating_margin": number (0.0-1.0),
    "net_margin": number (0.0-1.0),
    "market_cap_usd_millions": number or null,
    "cash_position_usd_millions": number,
    "total_debt_usd_millions": number,
    "debt_to_equity": number,
    "current_ratio": number,
    "balance_sheet_strength": "strong | adequate | weak",
    "source_tier": 1
  },

  "strategic_initiatives": [
    {
      "name": "string",
      "type": "supply_chain | expansion | divestiture | partnership | transformation",
      "description": "string",
      "status": "announced | in_progress | completed",
      "geographic_relevance": "string (which regions affected)",
      "source_tier": 1|2|3|4
    }
  ],

  "concentration_flags": [
    {
      "flag_type": "manufacturing | supplier | customer | revenue | regulatory",
      "description": "string (factual statement of concentration)",
      "severity": "high | medium | low",
      "details": "string"
    }
  ],

  "data_quality": {
    "completeness_score": number (0.0-1.0),
    "data_gaps": ["array of specific gaps"],
    "stale_data_warnings": ["array of data points that may be outdated"],
    "source_summary": {
      "tier_1_count": number,
      "tier_2_count": number,
      "tier_3_count": number,
      "tier_4_count": number
    }
  }
}

IMPORTANT:
- Return ONLY the JSON object, no additional text
- Use null for unavailable numeric data, never guess
- Flag uncertainty in notes fields
- Every data point should have a source_tier where indicated
```

---

## Example Query for Dell

```
Extract a comprehensive company profile for: Dell Technologies Inc.

Focus areas for geopolitical exposure analysis:
1. Where does this company operate? (facilities, manufacturing, offices)
2. Who does this company depend on? (suppliers, contract manufacturers, technology platforms)
3. Where does revenue come from? (geographic breakdown)
4. Who are the customers? (concentration, segments)
5. What regulatory jurisdictions apply?
6. What is the financial baseline? (size, margins, balance sheet strength)

Return the data as a JSON object following this exact schema:
[... schema as above ...]
```

---

## Post-Processing Notes

After receiving the JSON response from Parallel:

1. **Validate JSON structure** - Ensure all required fields present
2. **Check for null values** - Flag critical missing data
3. **Verify source tiers** - Ensure high-confidence data for critical fields
4. **Save to file** - Store as `{company_ticker}_profile.json`

The Streamlit UI will read from this file to display the Company Profile View.

"""




task_run = client.task_run.create(
    input=system_prompt,
    processor="ultra"
)
print(f"Run ID: {task_run.run_id}")

run_result = client.task_run.result(task_run.run_id, api_timeout=100000)
print(f"Output type: {type(run_result.output)}")
print(f"Output attributes: {dir(run_result.output)}")
print(run_result.output)

# Convert TaskRunTextOutput to string
with open("company_profile.json", "w") as f:
  # TaskRunTextOutput has a 'text' attribute that contains the actual content
  if hasattr(run_result.output, 'text'):
    output_text = run_result.output.text
  else:
    output_text = str(run_result.output)
  
  # Try to parse and pretty-print if it's valid JSON
  try:
    parsed_json = json.loads(output_text)
    f.write(json.dumps(parsed_json, indent=4))
  except json.JSONDecodeError:
    # If not JSON, write as plain text
    f.write(output_text)
  