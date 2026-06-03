import { AuthConfig, getActiveToken } from "./auth.js";

export class TCBSOpenAPIClient {
  private configGetter: () => AuthConfig;

  constructor(configGetter: () => AuthConfig) {
    this.configGetter = configGetter;
  }

  private async request<T>(
    method: string,
    path: string,
    query?: Record<string, string | number | undefined>,
    body?: unknown,
    extraHeaders?: Record<string, string>,
  ): Promise<{ status: number; body: T }> {
    const config = this.configGetter();
    const url = this.buildUrl(config.baseUrl, path, query);

    const headers: Record<string, string> = {};

    // Only skip Authorization header for the authentication/token exchange endpoint
    if (path !== "/gaia/v1/oauth2/openapi/token") {
      const token = getActiveToken(config);
      headers["Authorization"] = `Bearer ${token}`;
    }

    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
    }

    if (extraHeaders) {
      Object.assign(headers, extraHeaders);
    }

    const response = await fetch(url, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });

    const text = await response.text();
    let parsedBody: T;

    try {
      parsedBody = text ? JSON.parse(text) : (null as T);
    } catch {
      parsedBody = text as unknown as T;
    }

    if (!response.ok) {
      throw new Error(`TCBS API error (${response.status}): ${JSON.stringify(parsedBody)}`);
    }

    return { status: response.status, body: parsedBody };
  }

  private buildUrl(
    baseUrl: string,
    path: string,
    query?: Record<string, string | number | undefined>,
  ): string {
    const url = new URL(`${baseUrl}${path}`);
    if (query) {
      for (const [key, value] of Object.entries(query)) {
        if (value !== undefined && value !== "") {
          url.searchParams.set(key, String(value));
        }
      }
    }
    return url.toString();
  }

  get<T>(
    path: string,
    query?: Record<string, string | number | undefined>,
  ): Promise<{ status: number; body: T }> {
    return this.request<T>("GET", path, query);
  }

  post<T>(
    path: string,
    body?: unknown,
    query?: Record<string, string | number | undefined>,
    extraHeaders?: Record<string, string>,
  ): Promise<{ status: number; body: T }> {
    return this.request<T>("POST", path, query, body, extraHeaders);
  }

  delete<T>(
    path: string,
    query?: Record<string, string | number | undefined>,
    extraHeaders?: Record<string, string>,
  ): Promise<{ status: number; body: T }> {
    return this.request<T>("DELETE", path, query, undefined, extraHeaders);
  }

  put<T>(
    path: string,
    body?: unknown,
    query?: Record<string, string | number | undefined>,
    extraHeaders?: Record<string, string>,
  ): Promise<{ status: number; body: T }> {
    return this.request<T>("PUT", path, query, body, extraHeaders);
  }
}
