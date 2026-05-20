import { z } from "zod";
export function getPostsTools(client) {
    return [
        {
            name: "fireant_news_feed",
            description: "Get news feed",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/posts/feed");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_posts",
            description: "Get list of posts",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/posts");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_popular_posts",
            description: "Get popular posts",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/posts/popular");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_experts",
            description: "Get list of experts",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/posts/experts");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_expert_ideas",
            description: "Get expert opinions/ideas",
            inputSchema: {},
            handler: async () => {
                const data = await client.get("/posts/expert-ideas");
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
        {
            name: "fireant_popular_symbols",
            description: "Get most shared symbols in a period",
            inputSchema: { period: z.string().describe("Period (e.g. day, week, month)") },
            handler: async (args) => {
                const data = await client.get(`/posts/popular-symbols/${args.period}`);
                return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
            },
        },
    ];
}
