import { AuthConfig } from "./auth.js";
export declare class DNSEOpenAPIClient {
    private config;
    constructor(config: AuthConfig);
    private request;
    private buildUrl;
    get<T>(path: string, query?: Record<string, string | number | undefined>): Promise<{
        status: number;
        body: T;
    }>;
    post<T>(path: string, body?: unknown, query?: Record<string, string | number | undefined>, extraHeaders?: Record<string, string>): Promise<{
        status: number;
        body: T;
    }>;
    delete<T>(path: string, query?: Record<string, string | number | undefined>, extraHeaders?: Record<string, string>): Promise<{
        status: number;
        body: T;
    }>;
    put<T>(path: string, body?: unknown, query?: Record<string, string | number | undefined>, extraHeaders?: Record<string, string>): Promise<{
        status: number;
        body: T;
    }>;
}
