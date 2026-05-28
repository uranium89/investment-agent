# dnse-mcp-server

MCP server that bridges AI assistants to the [DNSE OpenAPI](https://developers.dnse.com.vn) — Vietnamese stock market data.

## Features

- **7 market data tools** — security definitions, instruments, OHLC, trades, latest trade, close price, working dates
- **HMAC-SHA256 authentication** — implements DNSE's request signing protocol
- **No OTP required** — market data endpoints are read-only

## Prerequisites

- DNSE API credentials ([register here](https://entradex.dnse.com.vn/thong-tin-ca-nhan/light-speed))
- Node.js 22+

## Installation

```bash
cd mcp-server-dnse
npm install
npm run build
```

## Configuration

Set these environment variables:

| Variable           | Description                       | Default                       |
| ------------------ | --------------------------------- | ----------------------------- |
| `DNSE_API_KEY`     | Your DNSE API key                 | **(required)**                |
| `DNSE_API_SECRET`  | Your DNSE API secret              | **(required)**                |
| `DNSE_BASE_URL`    | API base URL                      | `https://openapi.dnse.com.vn` |
| `DNSE_API_VERSION` | API version header                | `2026-05-07`                  |
| `DNSE_HMAC_NONCE`  | Enable/disable nonce in signature | `true`                        |

## Usage

Add to your MCP host configuration:

```json
{
  "mcpServers": {
    "dnse-mcp-server": {
      "command": "node",
      "args": ["/path/to/mcp-server-dnse/build/index.js"],
      "env": {
        "DNSE_API_KEY": "your-api-key",
        "DNSE_API_SECRET": "your-api-secret"
      }
    }
  }
}
```

## Tools

| Tool                       | Description                                              |
| -------------------------- | -------------------------------------------------------- |
| `dnse_security_definition` | Get security trading parameters (price limits, lot size) |
| `dnse_instruments`         | Search/filter available instruments                      |
| `dnse_ohlc`                | Get historical OHLC price bars                           |
| `dnse_trades`              | Get historical trade executions                          |
| `dnse_latest_trade`        | Get most recent trade                                    |
| `dnse_close_price`         | Get previous session closing price                       |
| `dnse_working_dates`       | Get valid trading days                                   |

## Tech Stack

TypeScript, Node.js, MCP SDK, Zod
