import { z } from "zod";
import type { FireAntClient } from "../client.js";
import type { ToolDefinition } from "./types.js";

function symHandler(client: FireAntClient, suffix: string) {
  return async (args: { symbol: string }) => {
    const data = await client.get(`/symbols/${args.symbol}${suffix}`);
    return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
  };
}

function simpleHandler(client: FireAntClient, path: string) {
  return async () => {
    const data = await client.get(path);
    return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
  };
}

export function getSymbolTools(client: FireAntClient): ToolDefinition[] {
  return [
    {
      name: "fireant_symbol_info",
      description: "Get basic stock info for a symbol (e.g. ACB, VNM)",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, ""),
    },
    {
      name: "fireant_search_symbols",
      description: "Search stock symbols by keyword",
      inputSchema: { q: z.string().describe("Search keyword") },
      handler: async (args: { q: string }) => {
        const data = await client.get("/symbols/search", { q: args.q });
        return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
      },
    },
    {
      name: "fireant_top_movers",
      description: "Get top moving stocks",
      inputSchema: {},
      handler: simpleHandler(client, "/symbols/movers"),
    },
    {
      name: "fireant_company_profile",
      description: "Get company profile for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/profile"),
    },
    {
      name: "fireant_fundamental",
      description: "Get fundamental info for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/fundamental"),
    },
    {
      name: "fireant_historical_quotes",
      description: "Get historical price data for a symbol",
      inputSchema: {
        symbol: z.string().describe("Stock symbol"),
        startDate: z.string().optional().describe("Start date (yyyy-MM-dd)"),
        endDate: z.string().optional().describe("End date (yyyy-MM-dd)"),
        offset: z.number().optional().describe("Pagination offset"),
        limit: z.number().optional().describe("Number of records (default 20)"),
      },
      handler: async (args: { symbol: string; startDate?: string; endDate?: string; offset?: number; limit?: number }) => {
        const data = await client.get(`/symbols/${args.symbol}/historical-quotes`, {
          startDate: args.startDate,
          endDate: args.endDate,
          offset: args.offset,
          limit: args.limit,
        });
        return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
      },
    },
    {
      name: "fireant_financial_reports",
      description: "Get summary financial reports for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/financial-reports"),
    },
    {
      name: "fireant_full_financial_reports",
      description: "Get full financial reports for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/full-financial-reports"),
    },
    {
      name: "fireant_financial_indicators",
      description: "Get financial indicators for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/financial-indicators"),
    },
    {
      name: "fireant_financial_data",
      description: "Get full financial info for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/financial-data"),
    },
    {
      name: "fireant_financial_data_by_period",
      description: "Get financial data by reporting period for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/financial-data-by-period"),
    },
    {
      name: "fireant_dynamic_financial_data",
      description: "Compare financial data across multiple companies",
      inputSchema: {},
      handler: simpleHandler(client, "/symbols/dynamic-financial-data"),
    },
    {
      name: "fireant_all_financial_data",
      description: "Get financial data for all companies",
      inputSchema: {},
      handler: simpleHandler(client, "/symbols/all-financial-data"),
    },
    {
      name: "fireant_estimated_price",
      description: "Get valuation/target price for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/estimated-price"),
    },
    {
      name: "fireant_dividends",
      description: "Get dividend statistics for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/dividends"),
    },
    {
      name: "fireant_rrg",
      description: "Get RRG (Relative Rotation Graph) statistics for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/rrg"),
    },
    {
      name: "fireant_holders",
      description: "Get list of major shareholders for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/holders"),
    },
    {
      name: "fireant_officers",
      description: "Get management board for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/officers"),
    },
    {
      name: "fireant_subsidiaries",
      description: "Get subsidiaries and affiliates for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/subsidiaries"),
    },
    {
      name: "fireant_transactions",
      description: "Get institutional transactions for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/transactions"),
    },
    {
      name: "fireant_holder_transactions",
      description: "Get major shareholder transactions for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/holder-transactions"),
    },
    {
      name: "fireant_timescale_marks",
      description: "Get timeline events/marks for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/timescale-marks"),
    },
    {
      name: "fireant_symbol_posts",
      description: "Get posts related to a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/posts"),
    },
    {
      name: "fireant_bonds",
      description: "Get corporate bonds for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/bonds"),
    },
    {
      name: "fireant_warrant_info",
      description: "Get covered warrant info for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/warrant-info"),
    },
    {
      name: "fireant_commodity_contract",
      description: "Get commodity futures contract info for a symbol",
      inputSchema: { symbol: z.string().describe("Stock symbol") },
      handler: symHandler(client, "/commodity-contract"),
    },
    {
      name: "fireant_commodities_by_category",
      description: "Get futures contracts by category",
      inputSchema: { category: z.string().describe("Category code") },
      handler: async (args: { category: string }) => {
        const data = await client.get(`/symbols/commodities/${args.category}`);
        return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
      },
    },
  ];
}
