import { z } from "zod";
import type { FireAntClient } from "../client.js";
import type { ToolDefinition } from "./types.js";

export function getSearchTools(client: FireAntClient): ToolDefinition[] {
  return [
    {
      name: "fireant_search",
      description: "Search stock market data by keyword",
      inputSchema: { q: z.string().describe("Search keyword") },
      handler: async (args: { q: string }) => {
        const data = await client.get("/search", { q: args.q });
        return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
      },
    },
    {
      name: "fireant_exact_search",
      description: "Exact search by keyword",
      inputSchema: { q: z.string().describe("Search keyword") },
      handler: async (args: { q: string }) => {
        const data = await client.get("/search/exact", { q: args.q });
        return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
      },
    },
  ];
}
