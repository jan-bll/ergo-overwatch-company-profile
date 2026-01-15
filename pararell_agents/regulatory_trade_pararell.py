from parallel import Parallel
import json


def create_regulatory_trade_task(client: Parallel, company: str):
    """Create the regulatory/trade task and return the task_run object (non-blocking)."""
    with open('prompts/regulatory_trade_prompt.md', 'r') as f:
        system_prompt_base = f.read()
    system_prompt = f"##For company: {company} find this information\n\n{system_prompt_base}"

    processor = "ultra"
    print(f"[Regulatory/Trade] Creating task with processor: {processor}")
        
    return client.task_run.create(
        input=system_prompt,
        processor=processor,
        task_spec={
            "output_schema": {
                "json_schema": {
                    "type": "object",
                    "description": "Research-only schema capturing factual regulatory and competitive signals relevant to Dell, without analysis or interpretation.",
                    "properties": {
                        "policy_constraints": {
                            "type": "array",
                            "description": "Documented regulatory or policy constraints that affect technology, trade, or market access in a specific jurisdiction.",
                            "items": {
                                "type": "object",
                                "description": "A single observed policy or regulatory constraint issued by a governing authority.",
                                "properties": {
                                "policy_type": {
                                    "type": "string",
                                    "description": "The category of policy instrument that imposes constraints or requirements."
                                },
                                "issuing_authority": {
                                    "type": "string",
                                    "description": "The government body or authority that issued the policy."
                                },
                                "jurisdiction": {
                                    "type": "string",
                                    "description": "The legal jurisdiction under which the policy is enforced."
                                },
                                "affected_regions": {
                                    "type": "array",
                                    "description": "Geographic regions explicitly impacted by the policy.",
                                    "items": {
                                        "type": "string",
                                        "description": "A country or region affected by the policy."
                                    }
                                },
                                "affected_product_categories": {
                                    "type": "array",
                                    "description": "Product or technology categories explicitly covered by the policy.",
                                    "items": {
                                        "type": "string",
                                        "description": "A specific product or technology category affected by the policy."
                                    }
                                },
                                "policy_description": {
                                    "type": "string",
                                    "description": "A concise factual description of what the policy restricts or requires."
                                },
                                "effective_date": {
                                    "type": "string",
                                    "format": "date",
                                    "description": "The date on which the policy became or will become effective."
                                },
                                "status": {
                                    "type": "string",
                                    "enum": ["active", "proposed", "amended", "repealed"],
                                    "description": "The current legal status of the policy."
                                },
                                "source_ref": {
                                    "type": "string",
                                    "description": "Reference ID linking this policy to a specific source in regulatory_trade_sources."
                                }
                                },
                                "required": [
                                "policy_type",
                                "issuing_authority",
                                "jurisdiction",
                                "policy_description",
                                "effective_date",
                                "status",
                                "source_ref"
                                ]
                            }
                        },
                        "regional_demand_signals": {
                            "type": "array",
                            "description": "Observed signals indicating regional or government-led demand for digital or AI infrastructure.",
                            "items": {
                                "type": "object",
                                "description": "A single factual demand-related signal observed in a specific region.",
                                "properties": {
                                "region": {
                                    "type": "string",
                                    "description": "The geographic region where the demand signal is observed."
                                },
                                "signal_type": {
                                    "type": "string",
                                    "description": "The type of demand signal indicating infrastructure or technology investment."
                                },
                                "initiator": {
                                    "type": "string",
                                    "description": "The entity that initiated or announced the demand-related activity."
                                },
                                "description": {
                                    "type": "string",
                                    "description": "A brief factual description of the observed demand signal."
                                },
                                "public_amount_disclosed": {
                                    "type": "boolean",
                                    "description": "Indicates whether a public investment amount was disclosed."
                                },
                                "amount_usd": {
                                    "type": ["number", "null"],
                                    "description": "The disclosed investment amount expressed in USD, if available."
                                },
                                "timeframe": {
                                    "type": "string",
                                    "description": "The announced or implied timeframe of the demand initiative."
                                },
                                "observed_date": {
                                    "type": "string",
                                    "description": "The date when the demand signal was publicly observed."
                                },
                                },
                                "required": [
                                "region",
                                "signal_type",
                                "description",
                                "public_amount_disclosed",
                                "observed_date"                                ]
                            }
                        },
                        "competitor_factual_moves": {
                            "type": "array",
                            "description": "Publicly reported factual actions taken by Dell’s competitors.",
                            "items": {
                                "type": "object",
                                "description": "A single observed competitive move without interpretation or impact assessment.",
                                "properties": {
                                    "competitor": {
                                        "type": "string",
                                        "description": "The name of the competitor that executed the action."
                                    },
                                    "move_type": {
                                        "type": "string",
                                        "description": "The category of the competitive action taken by the competitor."
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "A factual description of the competitive action taken by the competitor."
                                    },
                                    "regions_affected": {
                                        "type": "array",
                                        "description": "The geographic region or regions impacted by the action.",
                                        "items": {
                                            "type": "string",
                                            "description": "A region affected by the competitive move."
                                        }
                                    },
                                    "date_announced": {
                                        "type": "string",
                                        "description": "The date when the competitive action was publicly announced."
                                    },
                                },
                                "required": [
                                "competitor",
                                "move_type",
                                "description",
                                "date_announced"]
                            }
                        },
                        "factual_actions": {
                            "type": "array",
                            "description": "Publicly disclosed factual actions taken by Dell, without interpretation or strategic assessment.",
                            "items": {
                                "type": "object",
                                "description": "A single factual action announced or executed by Dell.",
                                "properties": {
                                "action_type": {
                                    "type": "string",
                                    "description": "The category of action taken by Dell."
                                },
                                "description": {
                                    "type": "string",
                                    "description": "A concise factual description of Dell’s action."
                                },
                                "regions_affected": {
                                    "type": "array",
                                    "description": "The geographic scope of the action.",
                                    "items": {
                                        "type": "string",
                                        "description": "A region where the action applies."
                                    }
                                },
                                "date_announced": {
                                    "type": "string",
                                    "description": "The date the action was publicly announced."
                                },
                                "public_statement": {
                                    "type": "boolean",
                                    "description": "Indicates whether the action was communicated via a public statement."
                                },
                                },
                                "required": [
                                "action_type",
                                "description",
                                "date_announced",
                                "public_statement"                                ]
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
                        }, 
                    },
                    "required": [
                        "policy_constraints",
                        "regional_demand_signals",
                        "competitor_factual_moves",
                        "factual_actions",
                        "sources"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )


def save_regulatory_trade_result(run_result) -> bool:
    """Save the regulatory/trade result to a JSON file."""
    try:
        with open("data/regulatory_trade.json", "w") as f:
            f.write(json.dumps(run_result.output.content, indent=4))
        print("[Regulatory/Trade] Data saved successfully")
        return True
    except Exception as e:
        print(f"[Regulatory/Trade] Error saving data: {e}")
        return False