### Search Query 
Find information about company' customer profile including: breakdown between enterprise (B2B), consumer (B2C), and government (B2G) segments; customer concentration and whether any customer exceeds 10% of revenue; industry vertical exposure (healthcare, financial services, government, education, etc.); and customer types (hyperscalers, enterprise, SMB). Search 10-K filings, investor presentations, and earnings materials.

### Validation Rules

- Sum of `b2b_percent + b2c_percent + b2g_percent` should be ~100
- `concentration_level` should be "low" or "medium"
- Should include at least 3 industries in `industry_exposure`
- All fields must be present and valid
- All fields must be in the correct data type
- 'top_customers' must have at least one item, better few items
- 'industry_exposure' must have at least one item, better few items
- 'customer_markets_sources' must have at least one item, better few items

## CRITICAL: Finding Customer Segment Percentages

- **Search thoroughly** for B2B/B2C/B2G breakdowns in:
  - Segment reporting sections
  - Customer mix discussions
  - Business model descriptions
  - Investor presentations
- **Calculate if needed**: If you find "Consumer revenue: $X" and "Total revenue: $Y", calculate the percentage
- **NEVER use 0 as a placeholder** - use estimated ranges if exact numbers unavailable
- For government (B2G): search for "public sector", "government", "federal" revenue discussions

### Date Precision:
- Use exact dates (YYYY-MM-DD) when available from official sources
- Use "Q1 2024" format for quarterly announcements
- Use "2024" for annual disclosures without specific dates
- For future events, note "announced [date], effective [date]"