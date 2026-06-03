import type { z } from "zod";

export type ToolCallback = (args: any) => Promise<{
  content: Array<{ type: "text"; text: string }>;
  isError?: boolean;
}>;

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: z.ZodTypeAny;
  handler: ToolCallback;
}

/**
 * Wraps a tool handler with try/catch block to prevent server from crashing when APIs fail.
 * Standardizes the error response format returned to the MCP client.
 */
export function safeHandler(
  handler: (args: any) => Promise<{ content: Array<{ type: string; text: string }> }>,
): ToolCallback {
  return async (args: any) => {
    try {
      const result = await handler(args);
      return {
        content: result.content.map((c) => ({ type: "text" as const, text: c.text })),
      };
    } catch (error: any) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: "text" as const,
            text: `Error executing tool: ${errorMessage}`,
          },
        ],
        isError: true,
      };
    }
  };
}
