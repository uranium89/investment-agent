import type { z } from "zod";
export type ToolCallback = (args: any) => Promise<{
    content: Array<{
        type: "text";
        text: string;
    }>;
    isError?: boolean;
}>;
export interface ToolDefinition {
    name: string;
    description: string;
    inputSchema: Record<string, z.ZodTypeAny>;
    handler: ToolCallback;
}
/**
 * Wraps a tool handler with try/catch block to prevent server from crashing when APIs fail.
 * Standardizes the error response format returned to the MCP client.
 */
export declare function safeHandler(handler: (args: any) => Promise<{
    content: Array<{
        type: "text";
        text: string;
    }>;
}>): ToolCallback;
