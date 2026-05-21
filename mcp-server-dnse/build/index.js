import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { DNSEOpenAPIClient } from "./client.js";
import { getAuthConfig } from "./auth.js";
import { getMarketDataTools } from "./tools/marketdata.js";
import { getAccountTools } from "./tools/account.js";
function main() {
    const config = getAuthConfig();
    const client = new DNSEOpenAPIClient(config);
    const server = new McpServer({ name: "dnse-mcp-server", version: "1.0.0" }, { capabilities: { tools: {} } });
    const tools = [
        ...getMarketDataTools(client),
        ...getAccountTools(client),
    ];
    for (const tool of tools) {
        server.registerTool(tool.name, {
            description: tool.description,
            inputSchema: tool.inputSchema,
        }, tool.handler);
    }
    const transport = new StdioServerTransport();
    server.connect(transport).catch((err) => {
        console.error("Fatal error:", err);
        process.exit(1);
    });
}
main();
