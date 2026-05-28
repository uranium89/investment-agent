# fireant-mcp-server

MCP server that bridges AI assistants to the [FireAnt.vn](https://fireant.vn) Vietnamese stock market API. Exposes 48+ tools for querying equities, industry data, financials, news, and more.

## Features

- **48+ stock market tools** — symbols, quotes, financial reports, dividends, holders, officers, industry data, news, screener, and more
- **Zero configuration** — anonymous authentication, no API keys required
- **Full industry coverage** — ICB classification, statistics, historical indices
- **News & sentiment** — news feed, social posts, expert ideas, trending symbols

## Installation

```bash
cd mcp-server
npm install
npm run build
```

## Usage

Add to your MCP host configuration (Claude Desktop, VS Code, etc.):

```json
{
  "mcpServers": {
    "fireant-mcp-server": {
      "command": "node",
      "args": ["/path/to/mcp-server/build/index.js"]
    }
  }
}
```

The server communicates over stdio — no ports to configure.

## Tools

### Symbols (23)

`fireant_symbol_info`, `fireant_search_symbols`, `fireant_top_movers`, `fireant_company_profile`, `fireant_fundamental`, `fireant_historical_quotes`, `fireant_financial_reports`, `fireant_full_financial_reports`, `fireant_financial_indicators`, `fireant_financial_data`, `fireant_financial_data_by_period`, `fireant_dynamic_financial_data`, `fireant_all_financial_data`, `fireant_estimated_price`, `fireant_dividends`, `fireant_rrg`, `fireant_holders`, `fireant_officers`, `fireant_subsidiaries`, `fireant_transactions`, `fireant_holder_transactions`, `fireant_timescale_marks`, `fireant_symbol_posts`, `fireant_bonds`, `fireant_warrant_info`, `fireant_commodity_contract`, `fireant_commodities_by_category`

### Industry / ICB (8)

`fireant_icb_list`, `fireant_icb_symbols`, `fireant_icb_statistics`, `fireant_all_icb_statistics`, `fireant_icb_financial_data`, `fireant_all_icb_financial_data`, `fireant_icb_historical_index`, `fireant_latest_icb_index`

### News & Posts (6)

`fireant_news_feed`, `fireant_posts`, `fireant_popular_posts`, `fireant_experts`, `fireant_expert_ideas`, `fireant_popular_symbols`

### Search (2)

`fireant_search`, `fireant_exact_search`

### Other (2)

`fireant_instruments`, `fireant_screener`

## Examples

```text
Get stock info:     fireant_symbol_info({ symbol: "ACB" })
Price history:      fireant_historical_quotes({ symbol: "VNM", startDate: "2025-01-01", endDate: "2025-12-31" })
Financial reports:  fireant_financial_reports({ symbol: "FPT" })
Industry list:      fireant_icb_list({})
Search market:      fireant_search({ q: "banking" })
Stock screener:     fireant_screener({ conditions: { ... } })
```

## Tech Stack

TypeScript, Node.js, [MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk), Zod
