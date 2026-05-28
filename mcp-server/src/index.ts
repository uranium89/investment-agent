import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { FireAntClient } from "./client.js";
import { getSymbolTools } from "./tools/symbols.js";
import { getIcbTools } from "./tools/icb.js";
import { getPostsTools } from "./tools/posts.js";
import { getSearchTools } from "./tools/search.js";
import { getOtherTools } from "./tools/other.js";
import { safeHandler } from "./tools/types.js";

const client = new FireAntClient();

const server = new McpServer(
  { name: "fireant-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } },
);

const allTools = [
  ...getSymbolTools(client),
  ...getIcbTools(client),
  ...getPostsTools(client),
  ...getSearchTools(client),
  ...getOtherTools(client),
  // Knowledge tools moved to mcp-server-buffett and mcp-server-munger
];

for (const tool of allTools) {
  server.registerTool(
    tool.name,
    {
      description: tool.description,
      inputSchema: tool.inputSchema,
    },
    safeHandler(tool.handler) as any,
  );
}

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
