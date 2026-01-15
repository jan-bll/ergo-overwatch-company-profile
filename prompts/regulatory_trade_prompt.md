### Search Query

Find factual information about geopolitical and regulatory factors affecting company' business. Focus on: export controls and trade restrictions (US-China tech policy, Entity List, advanced computing rules), regional demand signals (sovereign AI initiatives, data localization investments), competitor actions (market access restrictions, manufacturing relocations), and company's disclosed responses (supply chain moves, partnerships). Search 10-K filings, regulatory documents, government announcements, earnings transcripts, and industry news.

## Validation Rules

- 'policy_constraints' must have at least one item documenting export controls, tariffs, or procurement restrictions
- 'regional_demand_signals' must capture government-led or policy-driven infrastructure demand
- 'competitor_factual_moves' should include actions by major competitors (HPE, Lenovo, Supermicro)
- 'factual_actions' should document company's publicly disclosed responses to geopolitical shifts
- 'regulatory_trade_sources' must have at least one item, better few items
- All dates should be in ISO format (YYYY-MM-DD) when available
- Use `null` for optional fields when information is genuinely unavailable
- Do NOT include analysis, recommendations, or strategic assessments - facts only

## CRITICAL: Pure Research Guidelines

### What to Include (FACTS):
- **Policy Constraints**: Documented regulations with issuing authority, effective dates, affected products/regions
  - Example: "US BIS export controls on AI chips to China, effective October 17, 2023"
- **Regional Demand Signals**: Government announcements, public investments, disclosed amounts
  - Example: "EU AI Act requiring sovereign AI infrastructure, €10B budget announced March 2024"
- **Competitor Moves**: Public announcements, filings, press releases
  - Example: "Lenovo removed from UK government supplier list, announced August 2023"
- **Company Actions**: Company statements, 10-K disclosures, executive quotes from earnings calls
  - Example: "Comapny announced Mexico facility expansion, 30% capacity increase, Q2 2023 investor presentation"


### Search Strategy:
1. **For Policy Constraints**:
   - Search 10-K Risk Factors for "export control", "tariff", "trade restriction"
   - Check BIS (Bureau of Industry and Security) Federal Register postings
   - Look for government procurement rules (Buy American Act, etc.)
   
2. **For Regional Demand Signals**:
   - Search for "sovereign AI", "data localization", "digital sovereignty" + country names
   - Government budget announcements, infrastructure plans
   - Industry analyst reports citing specific government initiatives with dollar amounts
   
3. **For Competitor Moves**:
   - Competitor 10-Ks, press releases, earnings transcripts
   - News about manufacturing relocations, market access restrictions
   - Government contract awards/exclusions
   
4. **For Company Actions**:
   - Company 10-K, earnings call transcripts, investor presentations
   - Executive quotes (CEO, CFO) about geopolitical responses
   - Press releases about facility expansions, partnerships, supply chain changes


### Date Precision:
- Use exact dates (YYYY-MM-DD) when available from official sources
- Use "Q1 2024" format for quarterly announcements
- Use "2024" for annual disclosures without specific dates
- For future events, note "announced [date], effective [date]"
