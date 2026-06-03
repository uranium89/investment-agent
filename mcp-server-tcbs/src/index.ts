import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { TCBSOpenAPIClient } from "./client.js";
import { getAuthConfig } from "./auth.js";
import { getAccountTools } from "./tools/account.js";
import { getOrderTools } from "./tools/orders.js";
import { getDerivativeTools } from "./tools/derivative.js";
import { safeHandler } from "./tools/types.js";

function main() {
  // Pass getAuthConfig as a function so client can dynamically fetch the latest runtime token
  const client = new TCBSOpenAPIClient(getAuthConfig);

  const server = new McpServer(
    { name: "tcbs-mcp-server", version: "1.0.0" },
    { capabilities: { tools: {} } },
  );

  const tools = [
    ...getAccountTools(client),
    ...getOrderTools(client),
    ...getDerivativeTools(client),
  ];

  for (const tool of tools) {
    server.registerTool(
      tool.name,
      {
        description: tool.description,
        inputSchema: tool.inputSchema,
      },
      safeHandler(tool.handler) as any,
    );
  }

  const transport = new StdioServerTransport();
  server.connect(transport).catch((err) => {
    console.error("Fatal error starting TCBS MCP Server:", err);
    process.exit(1);
  });
}

main();
