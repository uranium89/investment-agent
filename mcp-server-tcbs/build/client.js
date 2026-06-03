import { getActiveToken } from "./auth.js";
export class TCBSOpenAPIClient {
    configGetter;
    constructor(configGetter) {
        this.configGetter = configGetter;
    }
    async request(method, path, query, body, extraHeaders) {
        const config = this.configGetter();
        const url = this.buildUrl(config.baseUrl, path, query);
        const headers = {};
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
        let parsedBody;
        try {
            parsedBody = text ? JSON.parse(text) : null;
        }
        catch {
            parsedBody = text;
        }
        if (!response.ok) {
            throw new Error(`TCBS API error (${response.status}): ${JSON.stringify(parsedBody)}`);
        }
        return { status: response.status, body: parsedBody };
    }
    buildUrl(baseUrl, path, query) {
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
