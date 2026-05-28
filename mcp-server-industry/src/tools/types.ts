import type { z } from "zod";

export type ToolCallback = (args: any) => Promise<{
  content: Array<{ type: "text"; text: string }>;
  isError?: boolean;
}>;

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: Record<string, z.ZodTypeAny>;
  handler: ToolCallback;
}

export function safeHandler(
  handler: (args: any) => Promise<{ content: Array<{ type: "text"; text: string }> }>,
): ToolCallback {
  return async (args: any) => {
    try {
      return await handler(args);
    } catch (error: any) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: "text",
            text: `Error executing tool: ${errorMessage}`,
          },
        ],
        isError: true,
      };
    }
  };
}
