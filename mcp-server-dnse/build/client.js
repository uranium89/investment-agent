import { generateSignatureHeaders, getDateHeaderName } from "./auth.js";
export class DNSEOpenAPIClient {
    config;
    constructor(config) {
        this.config = config;
    }
    async request(method, path, query, body, extraHeaders) {
        const { dateValue, signatureHeader } = generateSignatureHeaders(this.config, method, path);
        const dateHeaderName = getDateHeaderName();
        const url = this.buildUrl(path, query);
        const headers = {
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
        let parsedBody;
        try {
            parsedBody = text ? JSON.parse(text) : null;
        }
        catch {
            parsedBody = text;
        }
        if (!response.ok) {
            throw new Error(`DNSE API error (${response.status}): ${JSON.stringify(parsedBody)}`);
        }
        return { status: response.status, body: parsedBody };
    }
    buildUrl(path, query) {
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
    get(path, query) {
        return this.request("GET", path, query);
    }
    post(path, body, query, extraHeaders) {
        return this.request("POST", path, query, body, extraHeaders);
    }
    delete(path, query, extraHeaders) {
        return this.request("DELETE", path, query, undefined, extraHeaders);
    }
    put(path, body, query, extraHeaders) {
        return this.request("PUT", path, query, body, extraHeaders);
    }
}
