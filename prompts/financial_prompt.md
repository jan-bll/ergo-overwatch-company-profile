### Search Query
Identify authoritative sources describing company' corporate profile and financial performance. Prioritize SEC 10-K filings, annual reports, and investor presentations. Extract: headquarters location, employee count, business segment breakdown with revenue percentages, total revenue, gross/operating/net margins, cash position, and debt levels. Use only explicitly stated figures from official sources.

## Validation Rules

- `revenue_usd_millions` must be present (required field)
- All margin fields must be between 0.0 and 1.0
- All fields must be present and valid
- All fields must be in the correct data type
- 'business_segments' must have at least one item, better few items

## CRITICAL: Handling Unknown Values

- **NEVER use 0 or 0.0 as a placeholder for unknown values**
- Use `null` when you cannot find the actual value
- Only use 0 when the actual disclosed value is zero
- For `debt_to_equity` and `current_ratio`: search balance sheet data thoroughly - these are standard metrics
- Search multiple sections: financial statements, management discussion, investor presentations

### Date Precision:
- Use exact dates (YYYY-MM-DD) when available from official sources
- Use "Q1 2024" format for quarterly announcements
- Use "2024" for annual disclosures without specific dates
- For future events, note "announced [date], effective [date]"