import { AuthConfig, generateSignatureHeaders, getDateHeaderName } from "./auth.js";

export class DNSEOpenAPIClient {
  private config: AuthConfig;

  constructor(config: AuthConfig) {
    this.config = config;
  }

  private async request<T>(
    method: string,
    path: string,
    query?: Record<string, string | number | undefined>,
    body?: unknown,
    extraHeaders?: Record<string, string>,
  ): Promise<{ status: number; body: T }> {
    const { dateValue, signatureHeader } = generateSignatureHeaders(this.config, method, path);

    const dateHeaderName = getDateHeaderName();
    const url = this.buildUrl(path, query);

    const headers: Record<string, string> = {
      [dateHeaderName]: dateValue,
      "X-Signature": signatureHeader,
      "x-api-key": this.config.apiKey,
      version: this.config.apiVersion,
    };

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
      throw new Error(`DNSE API error (${response.status}): ${JSON.stringify(parsedBody)}`);
    }

    return { status: response.status, body: parsedBody };
  }

  private buildUrl(path: string, query?: Record<string, string | number | undefined>): string {
    const url = new URL(`${this.config.baseUrl}${path}`);
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
