from parallel import Parallel
import json


def create_customers_markets_task(client: Parallel, company: str):
    """Create the customers/markets task and return the task_run object (non-blocking)."""
    with open('prompts/customers_markets_prompt.md', 'r') as f:
        system_prompt_base = f.read()
    system_prompt = f"##For company: {company} find this information\n\n{system_prompt_base}"
    
    processor = "ultra"
    print(f"[Customers/Markets] Creating task with processor: {processor}")
    
    return client.task_run.create(
        input=system_prompt,
        processor=processor,
        task_spec={
            "output_schema": {
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "segment_mix": {
                            "type": "object",
                            "properties": {
                                "b2b_percent": {
                                    "type": ["number", "null"],
                                    "description": "The percentage of revenue from B2B customers (e.g., 67.3)"
                                },
                                "b2c_percent": {
                                    "type": ["number", "null"],
                                    "description": "The percentage of revenue from B2C customers (e.g., 22.1)"
                                },
                                "b2g_percent": {
                                    "type": ["number", "null"],
                                    "description": "The percentage of revenue from B2G customers (e.g., 10.6)"
                                },
                                "notes": {
                                    "type": "string",
                                    "description": "Notes about the segment mix"
                                }
                            },
                            "required": ["b2b_percent", "b2c_percent", "b2g_percent"],
                            "additionalProperties": False
                        },
                        "customer_concentration": {
                            "type": "object",
                            "properties": {
                                "any_customer_over_10_percent": {
                                    "type": ["boolean", "null"],
                                    "description": "Whether any customer exceeds 10% of revenue"
                                },
                                "top_customer_percent": {
                                    "type": ["number", "null"],
                                    "description": "The percentage of revenue from the top customer (e.g., 8.5)"
                                },
                                "top_10_customers_percent": {
                                    "type": ["number", "null"],
                                    "description": "The percentage of revenue from the top 10 customers (e.g., 32.7)"
                                },
                                "concentration_level": {
                                    "type": "string",
                                    "enum": ["high", "medium", "low"],
                                    "description": "The level of customer concentration"
                                },
                                "disclosure_notes": {
                                    "type": "string",
                                    "description": "Notes about customer concentration disclosures"
                                }
                            },
                            "required": ["concentration_level"],
                            "additionalProperties": False
                        },
                        "top_customers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the customer"
                                    },
                                    "type": {
                                        "type": "string",
                                        "enum": ["hyperscaler", "enterprise", "government", "distributor", "other"],
                                        "description": "The type of customer"
                                    },
                                    "percent_of_revenue": {
                                        "type": ["number", "null"],
                                        "description": "The percentage of revenue from the customer (e.g., 8.5)"
                                    },
                                    "industry": {
                                        "type": "string",
                                        "description": "The industry of the customer"
                                    },
                                    "notes": {
                                        "type": "string",
                                        "description": "Notes about the customer"
                                    }
                                },
                                "required": ["name", "type", "percent_of_revenue"],
                                "additionalProperties": False
                            }
                        },
                        "industry_exposure": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "industry": {
                                        "type": "string",
                                        "description": "The industry vertical"
                                    },
                                    "percent_of_revenue": {
                                        "type": ["number", "null"],
                                        "description": "The percentage of revenue from the industry (e.g., 15.3)"
                                    },
                                    "trend": {
                                        "type": "string",
                                        "enum": ["growing", "stable", "declining", "unknown"],
                                        "description": "The trend of the industry"
                                    },
                                    "notes": {
                                        "type": "string",
                                        "description": "Notes about the industry"
                                    }
                                },
                                "required": ["industry", "percent_of_revenue"],
                                "additionalProperties": False
                            }
                        },
                        "customer_characteristics": {
                            "type": "object",
                            "properties": {
                                "typical_contract_length": {
                                    "type": "string",
                                    "description": "The typical contract length"
                                },
                                "recurring_vs_transactional": {
                                    "type": "string",
                                    "description": "The recurring vs transactional nature of customer relationships"
                                },
                                "geographic_notes": {
                                    "type": "string",
                                    "description": "Notes about the geographic location of customers"
                                }
                            },
                            "required": [],
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
                                        "enum": ["10-K", "investor_presentation", "earnings_call", "news"],
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
                    "required": ["segment_mix", "customer_concentration", "top_customers", "industry_exposure", "customer_characteristics", "sources"],
                    "additionalProperties": False
                },
                "type": "json"
            }
        }
    )


def save_customers_markets_result(run_result) -> bool:
    """Save the customers/markets result to a JSON file."""
    try:
        with open("data/customers_markets.json", "w") as f:
            f.write(json.dumps(run_result.output.content, indent=4))
        print("[Customers/Markets] Data saved successfully")
        return True
    except Exception as e:
        print(f"[Customers/Markets] Error saving data: {e}")
        return False
