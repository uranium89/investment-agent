import { z } from "zod";
import type { FireAntClient } from "../client.js";
import type { ToolDefinition } from "./types.js";

export function getOtherTools(client: FireAntClient): ToolDefinition[] {
  return [
    {
      name: "fireant_instruments",
      description: "Get list of all securities codes",
      inputSchema: {},
      handler: async () => {
        const data = await client.get("/instruments");
        return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
      },
    },
    {
      name: "fireant_screener",
      description: "Filter stocks by JSON conditions",
      inputSchema: {
        conditions: z.record(z.unknown()).describe("JSON filter conditions"),
      },
      handler: async (args: { conditions: Record<string, unknown> }) => {
        const data = await client.post("/me/screeners/filter", args.conditions);
        return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
      },
    },
  ];
}
