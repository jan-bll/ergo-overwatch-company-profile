from parallel import Parallel
import json


def create_supply_chain_task(client: Parallel, company: str):
    """Create the supply chain task and return the task_run object (non-blocking)."""
    with open('prompts/supply_chain_prompt.md', 'r') as f:
        system_prompt_base = f.read()
    system_prompt = f"##For company: {company} find this information\n\n{system_prompt_base}"

    processor = "ultra"
    print(f"[Supply Chain] Creating task with processor: {processor}")
        
    return client.task_run.create(
        input=system_prompt,
        processor=processor,
        task_spec={
            "output_schema": {
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "company_owned_facilities": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "country": {
                                        "type": "string",
                                        "description": "Country where Dell's owned facility is located"
                                    },
                                    "city": {
                                        "type": "string",
                                        "description": "City location (if available)"
                                    },
                                    "roles": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": ["assembly", "L10", "L11", "L12", "testing", "config"]
                                        },
                                        "description": "Operational roles at this Dell-owned site"
                                    },
                                    "region_served": {
                                        "type": "string",
                                        "enum": ["Americas", "EMEA", "APJ"],
                                        "description": "Primary region served"
                                    },
                                    "products": {
                                        "type": "string",
                                        "description": "Product lines handled at this facility"
                                    },
                                    "source": {
                                        "type": "string",
                                        "description": "Source of information (10-K, investor materials, etc.)"
                                    }
                                },
                                "required": ["country", "roles", "region_served"]
                            }
                        },
                        
                        
                        "contract_manufacturers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "manufacturer_name": {
                                        "type": "string",
                                        "description": "The name of the contract manufacturer"
                                    },
                                    "headquarters_country": {
                                        "type": "string",
                                        "description": "Country where the contract manufacturer is headquartered"
                                    },
                                    "relationship_type": {
                                        "type": "string",
                                        "enum": ["ODM", "EMS", "both"],
                                        "description": "The type of relationship with Dell"
                                    },
                                    "production_countries": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "Countries where the contract manufacturer produces"
                                    },
                                    "products_manufactured": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "The product that the contract manufacturer makes"
                                    },
                                    "functions": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": ["assembly", "L10", "L11", "L12", "PCB", "cooling", "sub-assembly", "components", "testing", "config", "other"]
                                        },
                                        "description": "Functions performed by this contract manufacturer"
                                    },
                                    "dependency_level": {
                                        "type": "string",
                                        "enum": ["critical", "high", "medium"],
                                        "description": "The level of dependency on this supplier"
                                    },
                                    "notes": {
                                        "type": "string",
                                        "description": "Additional notes about the contract manufacturer"
                                    }
                                },
                                "required": ["manufacturer_name", "relationship_type", "production_countries", "products_manufactured", "notes"],
                                "additionalProperties": False
                            }
                        },
                        
                        "critical_suppliers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "supplier_name": {
                                        "type": "string",
                                        "description": "The name of the supplier"
                                    },
                                    "headquarters_country": {
                                        "type": "string",
                                        "description": "The country of the supplier's headquarters"
                                    },
                                    "provides": {
                                        "type": "string",
                                        "description": "The components or services the supplier provides"
                                    },
                                    "component_category": {
                                        "type": "string",
                                        "enum": ["CPU", "GPU", "memory", "storage", "display", "software", "other"],
                                        "description": "The category of the component or service"
                                    },
                                    "dependency_level": {
                                        "type": "string",
                                        "enum": ["critical", "high", "medium"],
                                        "description": "The level of dependency on this supplier"
                                    },
                                    "single_source": {
                                        "type": "boolean",
                                        "description": "Whether the supplier is a single source"
                                    },
                                    "manufacturing_locations": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "Countries where the supplier produces"
                                    },
                                    "notes": {
                                        "type": "string",
                                        "description": "Additional context about the supplier"
                                    }
                                },
                                "required": ["supplier_name", "headquarters_country", "provides", "component_category", "dependency_level", "single_source", "manufacturing_locations", "notes"],
                                "additionalProperties": False
                            }
                        },
                        
                        "supplier_concentration": {
                            "type": "object",
                            "properties": {
                                "top_country": {
                                    "type": "string",
                                    "description": "The country with the highest supplier concentration"
                                },
                                "top_country_percent": {
                                    "type": ["integer", "null"],
                                    "description": "The percentage of suppliers from the top country"
                                },
                                "top_3_countries": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "The top 3 countries by supplier concentration"
                                },
                                "concentration_notes": {
                                    "type": "string",
                                    "description": "Analysis of supplier concentration risk"
                                }
                            },
                            "required": ["top_country", "top_country_percent", "top_3_countries", "concentration_notes"],
                            "additionalProperties": False
                        },
                        
                        "supply_corridors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "corridor": {
                                        "type": "string",
                                        "description": "The supply chain corridor route (e.g., 'Asia → Mexico → US', 'China → EMEA', 'Taiwan → Americas')"
                                    },
                                    "purpose": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": ["assembly", "config", "distribution", "component_sourcing", "final_assembly", "regional_finishing"]
                                        },
                                        "description": "Primary purposes of this corridor"
                                    },
                                    "flow_description": {
                                        "type": "string",
                                        "description": "Additional details about what flows through this corridor and logistics dependencies"
                                    }
                                },
                                "required": ["corridor", "purpose", "flow_description"],
                                "additionalProperties": False
                            }
                        },
                        
                        "supply_chain_initiatives": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "initiative": {
                                        "type": "string",
                                        "description": "The supply chain initiative or diversification effort"
                                    },
                                    "purpose": {
                                        "type": "string",
                                        "description": "The purpose or goal of the initiative"
                                    },
                                    "status": {
                                        "type": "string",
                                        "enum": ["announced", "in_progress", "completed"],
                                        "description": "Current status of the initiative"
                                    },
                                    "target_regions": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "Geographic regions affected by this initiative"
                                    }
                                },
                                "required": ["initiative", "purpose", "status"],
                                "additionalProperties": False
                            }
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
                                        "enum": ["10-K", "industry_report", "news", "company_statement"],
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
                    "required": ["company_owned_facilities", "contract_manufacturers", "critical_suppliers", "supplier_concentration", "supply_corridors", "supply_chain_initiatives", "sources"],
                    "additionalProperties": False
                },
                "type": "json"
            }
        }
    )


def save_supply_chain_result(run_result) -> bool:
    """Save the supply chain result to a JSON file."""
    try:
        with open("data/supply_chain.json", "w") as f:
            f.write(json.dumps(run_result.output.content, indent=4))
        print("[Supply Chain] Data saved successfully")
        return True
    except Exception as e:
        print(f"[Supply Chain] Error saving data: {e}")
        return False