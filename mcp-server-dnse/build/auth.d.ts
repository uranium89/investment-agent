export declare function getDateHeaderName(): string;
export declare function buildSignature(secret: string, method: string, path: string, dateValue: string, algorithm: string, nonce?: string): {
    headers: string;
    signature: string;
};
export interface AuthConfig {
    apiKey: string;
    apiSecret: string;
    baseUrl: string;
    algorithm: string;
    hmacNonceEnabled: boolean;
    apiVersion: string;
}
export declare function getAuthConfig(): AuthConfig;
export declare function generateSignatureHeaders(config: AuthConfig, method: string, path: string): {
    dateValue: string;
    signatureHeader: string;
};
