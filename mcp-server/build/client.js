import { getToken, clearToken } from "./auth.js";
const BASE_URL = "https://api.fireant.vn";
export class FireAntClient {
    async request(method, path, query, body) {
        const token = await getToken();
        const url = new URL(`${BASE_URL}${path}`);
        if (query) {
            for (const [key, value] of Object.entries(query)) {
                if (value !== undefined) {
                    url.searchParams.set(key, String(value));
                }
            }
        }
        const headers = {
            Authorization: `Bearer ${token}`,
        };
        if (body !== undefined) {
            headers["Content-Type"] = "application/json";
        }
        const response = await fetch(url.toString(), {
            method,
            headers,
            body: body !== undefined ? JSON.stringify(body) : undefined,
        });
        if (response.status === 401) {
            clearToken();
            const newToken = await getToken();
            headers.Authorization = `Bearer ${newToken}`;
            const retryResponse = await fetch(url.toString(), {
                method,
                headers,
                body: body !== undefined ? JSON.stringify(body) : undefined,
            });
            if (!retryResponse.ok) {
                throw new Error(`API error: ${retryResponse.status} ${retryResponse.statusText}`);
            }
            const text = await retryResponse.text();
            return text ? JSON.parse(text) : null;
        }
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        const text = await response.text();
        return text ? JSON.parse(text) : null;
    }
    async get(path, query) {
        return this.request("GET", path, query);
    }
    async post(path, body) {
        return this.request("POST", path, undefined, body);
    }
}
