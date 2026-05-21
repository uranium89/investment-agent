import { z } from "zod";
import { DNSEOpenAPIClient } from "../client.js";
interface ToolDefinition {
    name: string;
    description: string;
    inputSchema: z.ZodTypeAny;
    handler: (args: Record<string, unknown>) => Promise<{
        content: Array<{
            type: string;
            text: string;
        }>;
    }>;
}
export declare function getMarketDataTools(client: DNSEOpenAPIClient): ToolDefinition[];
export {};
