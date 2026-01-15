### Search Query 
Identify company' critical supply chain dependencies including: major component suppliers (CPUs, GPUs, memory, storage), contract manufacturers and ODM partners, single-source dependencies, and geographic concentration of supply base. Search 10-K risk factors, supplier disclosures, industry analysis, and supply chain reports. Include information about where key suppliers manufacture (Taiwan, China, Korea, etc.).


### Validation Rules

- All fields must be present and valid
- All fields must be in the correct data type
- 'company_owned_facilities' must have at least one item, better few items
- 'contract_manufacturers' must have at least one item, better few items
- 'critical_suppliers' must have at least one item, better few items
- 'supply_corridors' must have at least one item, better few items
- 'supply_chain_initiatives' must have at least one item, better few items
- 'sources' must have at least one item, better few items

## CRITICAL: Finding Supplier Information

- **Search thoroughly** for supplier names in:
  - 10-K risk factors sections (supplier dependencies)
  - Supply chain disruption discussions
  - Critical vendor disclosures
  - Industry reports mentioning company's suppliers
- **For `top_country_percent`**: Look for geographic concentration statements
  - e.g., "X% of our suppliers are located in..."
  - Use `null` only if truly unavailable, not as a placeholder
- **Name actual companies** when possible (Intel, AMD, NVIDIA, etc.) rather than generic descriptions

### Date Precision:
- Use exact dates (YYYY-MM-DD) when available from official sources
- Use "Q1 2024" format for quarterly announcements
- Use "2024" for annual disclosures without specific dates
- For future events, note "announced [date], effective [date]"