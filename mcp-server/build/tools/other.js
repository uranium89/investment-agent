import { z } from "zod";
export function getOtherTools(client) {
    return [
        {
            name: "fireant_instruments",
            description: "Get list of all securities codes",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/instruments");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_screener",
            description: "Filter stocks by JSON conditions",
            inputSchema: {
                conditions: z.record(z.unknown()).describe("JSON filter conditions"),
            },
            handler: async (args) => {
                const data = await client.post("/me/screeners/filter", args.conditions);
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
    ];
}
