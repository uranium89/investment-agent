import { createHmac, randomUUID } from "node:crypto";
export function getDateHeaderName() {
    return process.env["DNSE_DATE_HEADER"] || "Date";
}
function formatDate(date) {
    return date.toUTCString();
}
function encodeSignature(data) {
    return encodeURIComponent(data.toString("base64"));
}
export function buildSignature(secret, method, path, dateValue, algorithm, nonce) {
    const headerName = getDateHeaderName();
    const headerKey = headerName.toLowerCase();
    const headers = `(request-target) ${headerKey}`;
    let signatureString = `(request-target): ${method.toLowerCase()} ${path}\n${headerKey}: ${dateValue}`;
    if (nonce) {
        signatureString += `\nnonce: ${nonce}`;
    }
    let hashAlgo;
    if (algorithm === "hmac-sha256")
        hashAlgo = "sha256";
    else if (algorithm === "hmac-sha384")
        hashAlgo = "sha384";
    else if (algorithm === "hmac-sha512")
        hashAlgo = "sha512";
    else
        hashAlgo = "sha1";
    const mac = createHmac(hashAlgo, secret);
    mac.update(signatureString);
    const encoded = encodeSignature(mac.digest());
    return { headers, signature: encoded };
}
export function getAuthConfig() {
    const apiKey = process.env["DNSE_API_KEY"];
    const apiSecret = process.env["DNSE_API_SECRET"];
    if (!apiKey || !apiSecret) {
        throw new Error("Missing DNSE API credentials. Set DNSE_API_KEY and DNSE_API_SECRET environment variables.");
    }
    return {
        apiKey,
        apiSecret,
        baseUrl: process.env["DNSE_BASE_URL"] || "https://openapi.dnse.com.vn",
        algorithm: process.env["DNSE_ALGORITHM"] || "hmac-sha256",
        hmacNonceEnabled: process.env["DNSE_HMAC_NONCE"] !== "false",
        apiVersion: process.env["DNSE_API_VERSION"] || "2026-05-07",
    };
}
export function generateSignatureHeaders(config, method, path) {
    const dateValue = formatDate(new Date());
    const nonce = config.hmacNonceEnabled ? randomUUID().replace(/-/g, "") : undefined;
    const { headers, signature } = buildSignature(config.apiSecret, method, path, dateValue, config.algorithm, nonce);
    let signatureHeader = `Signature keyId="${config.apiKey}",algorithm="${config.algorithm}",headers="${headers}",signature="${signature}"`;
    if (nonce) {
        signatureHeader += `,nonce="${nonce}"`;
    }
    return { dateValue, signatureHeader };
}
