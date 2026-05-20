import type { z } from "zod";

export type ToolCallback = (args: any) => Promise<{
  content: Array<{ type: "text"; text: string }>;
}>;

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: Record<string, z.ZodTypeAny>;
  handler: ToolCallback;
}
