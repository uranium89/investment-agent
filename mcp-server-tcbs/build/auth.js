import { z } from "zod";
const envSchema = z.object({
    TCBS_TOKEN: z.string().optional(),
    TCBS_BASE_URL: z.string().default("https://openapi.tcbs.com.vn"),
});
// In-memory token store for JWT tokens exchanged dynamically at runtime
let runtimeToken = undefined;
export function getAuthConfig() {
    const result = envSchema.safeParse({
        TCBS_TOKEN: process.env["TCBS_TOKEN"],
        TCBS_BASE_URL: process.env["TCBS_BASE_URL"],
    });
    if (!result.success) {
        console.error("⚠️ WARNING: TCBS MCP Server configuration validation failed!");
        result.error.errors.forEach((err) => {
            console.error(`   - ${err.path.join(".")}: ${err.message}`);
        });
        return {
            token: runtimeToken || process.env["TCBS_TOKEN"],
            baseUrl: process.env["TCBS_BASE_URL"] || "https://openapi.tcbs.com.vn",
        };
    }
    const data = result.data;
    return {
        token: runtimeToken || data.TCBS_TOKEN,
        baseUrl: data.TCBS_BASE_URL,
    };
}
/**
 * Update the in-memory token.
 */
export function setRuntimeToken(token) {
    runtimeToken = token;
}
/**
 * Helper to check if credentials or token is available
 */
export function hasToken(config) {
    return !!(config.token || runtimeToken);
}
/**
 * Retrieve the active token
 */
export function getActiveToken(config) {
    const token = runtimeToken || config.token;
    if (!token) {
        throw new Error("TCBS Access Token is not set. Please either set the TCBS_TOKEN environment variable or run the 'tcbs_get_token' tool with your API Key and OTP to authenticate.");
    }
    return token;
}
