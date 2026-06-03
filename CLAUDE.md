# 🤖 AI Investment Agent — Developer Guidelines

This repository contains Model Context Protocol (MCP) servers for the Vietnamese Stock Market.

## 🏗️ Core Workspaces
- **`mcp-server`**: MCP server for FireAnt.vn APIs (market data, financials, symbol search, posts, etc.)
- **`mcp-server-dnse`**: MCP server for DNSE OpenAPI (ohlcv, trades, portfolio, order placement)

## ⚡ Command Reference (Run from Root)
- **Install dependencies for all workspaces**:
  ```bash
  npm run install:all
  ```
- **Build all workspaces**:
  ```bash
  npm run build
  ```
- **Typecheck code**:
  ```bash
  npm run typecheck
  ```
- **Lint code**:
  ```bash
  npm run lint
  ```
- **Format code**:
  ```bash
  npm run format
  ```

## 🛠️ Individual Workspace Start/Test
- **FireAnt server**:
  - Start: `npm run start --workspace=mcp-server`
  - Build: `npm run build --workspace=mcp-server`
- **DNSE server**:
  - Start: `npm run start --workspace=mcp-server-dnse`
  - Build: `npm run build --workspace=mcp-server-dnse`

## 📝 Code Style Guidelines
- **Type Safety**: TypeScript is strictly enforced. Avoid `any` where possible (unless working with external raw API payloads).
- **Zod schemas**: Always define input schemas for MCP tools using Zod so clients understand parameter requirements.
- **Error Handling**: Use the `safeHandler` helper to catch API and runtime errors gracefully so they return as MCP error messages rather than crashing the stdio transport.
- **Imports**: Use ESM imports with `.js` extensions for relative TypeScript files (e.g., `import { client } from "./client.js"`).
