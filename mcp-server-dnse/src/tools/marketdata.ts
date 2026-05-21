import { z } from "zod";
import { DNSEOpenAPIClient } from "../client.js";

interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: z.ZodTypeAny;
  handler: (args: Record<string, unknown>) => Promise<{ content: Array<{ type: string; text: string }> }>;
}

export function getMarketDataTools(client: DNSEOpenAPIClient): ToolDefinition[] {
  return [
    {
      name: "dnse_security_definition",
      description: "Get security definition & trading parameters (price limits, lot size, board info) for a symbol",
      inputSchema: z.object({
        symbol: z.string().describe("Stock symbol (e.g. HPG, VNM, FPT)"),
        boardId: z.string().optional().describe("Trading board ID (e.g. G1)"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get(
          `/price/${args.symbol}/secdef`,
          args.boardId ? { boardId: args.boardId as string } : undefined,
        );
        return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
      },
    },

    {
      name: "dnse_instruments",
      description: "Search/filter available trading instruments with metadata",
      inputSchema: z.object({
        symbol: z.string().optional().describe("Comma-separated symbols (e.g. SSI,SHS,ACB)"),
        marketId: z.string().optional().describe("Market exchange filter"),
        securityGroupId: z.string().optional().describe("Security group filter"),
        indexName: z.string().optional().describe("Index name filter"),
        limit: z.number().optional().describe("Page size"),
        page: z.number().optional().describe("Page number"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get("/instruments", {
          symbol: args.symbol as string | undefined,
          marketId: args.marketId as string | undefined,
          securityGroupId: args.securityGroupId as string | undefined,
          indexName: args.indexName as string | undefined,
          limit: args.limit as number | undefined,
          page: args.page as number | undefined,
        });
        return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
      },
    },

    {
      name: "dnse_ohlc",
      description: "Get historical OHLC (Open, High, Low, Close) price bars for a symbol",
      inputSchema: z.object({
        symbol: z.string().describe("Stock symbol (e.g. HPG)"),
        resolution: z.string().describe("Bar interval: 1, 5, 15, 30, 1H, 4H, 1D, 1W, 1M"),
        from: z.number().describe("Start time as Unix timestamp (seconds)"),
        to: z.number().describe("End time as Unix timestamp (seconds)"),
        barType: z.string().optional().default("STOCK").describe("Bar type (default: STOCK)"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get("/price/ohlc", {
          symbol: args.symbol as string,
          resolution: args.resolution as string,
          from: args.from as number,
          to: args.to as number,
          type: (args.barType as string) || "STOCK",
        });
        return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
      },
    },

    {
      name: "dnse_trades",
      description: "Get historical trade executions for a symbol",
      inputSchema: z.object({
        symbol: z.string().describe("Stock symbol (e.g. GAS)"),
        boardId: z.string().optional().describe("Trading board ID (e.g. G1)"),
        fromDate: z.number().optional().describe("Start time as Unix timestamp (seconds)"),
        toDate: z.number().optional().describe("End time as Unix timestamp (seconds)"),
        limit: z.number().optional().describe("Number of records (max 100)"),
        order: z.enum(["ASC", "DESC"]).optional().describe("Sort order (ASC or DESC)"),
        nextPageToken: z.string().optional().describe("Cursor for pagination"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get(`/price/${args.symbol}/trades`, {
          boardId: args.boardId as string | undefined,
          from: args.fromDate as number | undefined,
          to: args.toDate as number | undefined,
          limit: args.limit as number | undefined,
          order: args.order as string | undefined,
          nextPageToken: args.nextPageToken as string | undefined,
        });
        return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
      },
    },

    {
      name: "dnse_latest_trade",
      description: "Get the most recent trade for a symbol",
      inputSchema: z.object({
        symbol: z.string().describe("Stock symbol (e.g. HPG)"),
        boardId: z.string().optional().describe("Trading board ID (e.g. G1)"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get(
          `/price/${args.symbol}/trades/latest`,
          args.boardId ? { boardId: args.boardId as string } : undefined,
        );
        return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
      },
    },

    {
      name: "dnse_close_price",
      description: "Get the previous session closing price for a symbol",
      inputSchema: z.object({
        symbol: z.string().describe("Stock symbol (e.g. HPG)"),
        boardId: z.string().optional().describe("Trading board ID (e.g. G1)"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get(
          `/price/${args.symbol}/close`,
          args.boardId ? { boardId: args.boardId as string } : undefined,
        );
        return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
      },
    },

    {
      name: "dnse_working_dates",
      description: "Get list of valid trading days on the exchange",
      inputSchema: z.object({}),
      handler: async () => {
        const { status, body } = await client.get("/market/working-dates");
        return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
      },
    },
  ];
}
