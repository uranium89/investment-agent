import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { getIndustryTools } from "./tools/knowledge.js";
import { safeHandler } from "./tools/types.js";
const server = new McpServer({ name: "industry-mcp-server", version: "1.0.0" }, { capabilities: { tools: {} } });
const allTools = [
    ...getIndustryTools(), // Industry Knowledge Base tools
];
for (const tool of allTools) {
    server.registerTool(tool.name, {
        description: tool.description,
        inputSchema: tool.inputSchema,
    }, safeHandler(tool.handler));
}
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}
main().catch((err) => {
    console.error("Fatal error:", err);
    process.exit(1);
});
