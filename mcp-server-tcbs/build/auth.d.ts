export interface AuthConfig {
  token?: string;
  baseUrl: string;
}
export declare function getAuthConfig(): AuthConfig;
/**
 * Update the in-memory token.
 */
export declare function setRuntimeToken(token: string): void;
/**
 * Helper to check if credentials or token is available
 */
export declare function hasToken(config: AuthConfig): boolean;
/**
 * Retrieve the active token
 */
export declare function getActiveToken(config: AuthConfig): string;
