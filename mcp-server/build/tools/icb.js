import { z } from "zod";
export function getIcbTools(client) {
    return [
        {
            name: "fireant_icb_list",
            description: "List all industries (ICB classification)",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/icb");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_icb_symbols",
            description: "Get stock symbols in an industry",
            inputSchema: { industryCode: z.string().describe("Industry code (e.g. 60101000)") },
            handler: async (args) => {
                const data = await client.get(`/icb/${args.industryCode}/symbols`);
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_icb_statistics",
            description: "Get current statistics for an industry",
            inputSchema: { industryCode: z.string().describe("Industry code") },
            handler: async (args) => {
                const data = await client.get(`/icb/${args.industryCode}/statistics`);
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_all_icb_statistics",
            description: "Get statistics for all industries",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/icb/statistics");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_icb_financial_data",
            description: "Get financial data for an industry",
            inputSchema: { industryCode: z.string().describe("Industry code") },
            handler: async (args) => {
                const data = await client.get(`/icb/${args.industryCode}/financial-data`);
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_all_icb_financial_data",
            description: "Get latest financial data for all industries",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/icb/financial-data");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_icb_historical_index",
            description: "Get historical index for an industry",
            inputSchema: { industryCode: z.string().describe("Industry code") },
            handler: async (args) => {
                const data = await client.get(`/icb/${args.industryCode}/historical-index`);
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_latest_icb_index",
            description: "Get latest index for all industries",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/icb/latest-index");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
    ];
}
