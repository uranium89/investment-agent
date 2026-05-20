import { z } from "zod";
export function getSearchTools(client) {
    return [
        {
            name: "fireant_search",
            description: "Search stock market data by keyword",
            inputSchema: { q: z.string().describe("Search keyword") },
            handler: async (args) => {
                const data = await client.get("/search", { q: args.q });
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_exact_search",
            description: "Exact search by keyword",
            inputSchema: { q: z.string().describe("Search keyword") },
            handler: async (args) => {
                const data = await client.get("/search/exact", { q: args.q });
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
    ];
}
