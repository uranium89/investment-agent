const BASE_URL = "https://api.fireant.vn";
const ANONYMOUS_LOGIN_URL = `${BASE_URL}/authentication/anonymous-login`;
let cachedToken = null;
let tokenExpiry = null;
export async function getToken() {
    if (cachedToken && tokenExpiry && Date.now() < tokenExpiry) {
        return cachedToken;
    }
    const response = await fetch(ANONYMOUS_LOGIN_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://fireant.vn/",
            "Origin": "https://fireant.vn"
        },
        body: "{}",
    });
    if (!response.ok) {
        throw new Error(`Login failed: ${response.status} ${response.statusText}`);
    }
    const data = (await response.json());
    const token = data.accessToken;
    if (!token) {
        throw new Error("No access_token in login response");
    }
    cachedToken = token;
    tokenExpiry = Date.now() + ((data.expires_in ?? 3600) - 60) * 1000;
    return token;
}
export function clearToken() {
    cachedToken = null;
    tokenExpiry = null;
}
