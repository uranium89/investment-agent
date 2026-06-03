# 🤖 AI Investment Agent — Vietnamese Stock Market MCP Servers

Vietnamese Stock Market MCP servers designed for integration with AI clients (like Claude Desktop, Cursor, etc.). This monorepo provides direct access to stock information, financial data, and market transaction capabilities.

## 🏗️ Project Structure (Monorepo)

- **`mcp-server` (FireAnt MCP)**: Provides 40+ tools to retrieve data from FireAnt.vn (company profile, financials, historical quotes, symbol posts, dividends, etc.).
- **`mcp-server-dnse` (DNSE MCP)**: Connects with DNSE OpenAPI to retrieve market data (OHLC, trades) and handle portfolio/orders (requires authentication).

## 🚀 Installation & Build

### Requirements
- Node.js (ESM-compatible version)
- npm

### Steps

1. **Install dependencies for all workspaces:**
   ```bash
   npm run install:all
   ```

2. **Build all MCP Servers:**
   ```bash
   npm run build
   ```

3. **Check for errors (Linting & Type Check):**
   ```bash
   npm run lint
   ```
   ```bash
   npm run typecheck
   ```

## 🔌 MCP Configuration (Model Context Protocol)

To integrate these servers with your AI Client (e.g., Claude Desktop, Cursor), add the following configuration to your `mcp.json` or equivalent client configuration file:

```json
{
  "mcpServers": {
    "fireant-mcp": {
      "type": "local",
      "command": ["node", "/path/to/investment-agent/mcp-server/build/index.js"]
    },
    "dnse-mcp": {
      "type": "local",
      "command": ["node", "/path/to/investment-agent/mcp-server-dnse/build/index.js"]
    }
  }
}
```

*Note: Replace `/path/to/` with the absolute path of the repository on your local machine.*

## 🛠️ Built With

- **TypeScript / Node.js**: Main language and runtime environment.
- **Model Context Protocol (MCP)**: Standardized protocol for AI tool-calling.
- **npm workspaces**: Monorepo workspace manager.
