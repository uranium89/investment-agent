import { createHmac, randomUUID } from "node:crypto";
import { z } from "zod";

const envSchema = z.object({
  DNSE_API_KEY: z.string().min(1, "DNSE_API_KEY is required"),
  DNSE_API_SECRET: z.string().min(1, "DNSE_API_SECRET is required"),
  DNSE_BASE_URL: z.string().default("https://openapi.dnse.com.vn"),
  DNSE_ALGORITHM: z.string().default("hmac-sha256"),
  DNSE_HMAC_NONCE: z.preprocess((val) => val !== "false", z.boolean()).default(true),
  DNSE_API_VERSION: z.string().default("2026-05-07"),
});

export function getDateHeaderName(): string {
  return process.env["DNSE_DATE_HEADER"] || "Date";
}

function formatDate(date: Date): string {
  return date.toUTCString();
}

function encodeSignature(data: Buffer): string {
  return encodeURIComponent(data.toString("base64"));
}

export function buildSignature(
  secret: string,
  method: string,
  path: string,
  dateValue: string,
  algorithm: string,
  nonce?: string,
): { headers: string; signature: string } {
  const headerName = getDateHeaderName();
  const headerKey = headerName.toLowerCase();
  const headers = `(request-target) ${headerKey}`;

  let signatureString = `(request-target): ${method.toLowerCase()} ${path}\n${headerKey}: ${dateValue}`;
  if (nonce) {
    signatureString += `\nnonce: ${nonce}`;
  }

  let hashAlgo: string;
  if (algorithm === "hmac-sha256") hashAlgo = "sha256";
  else if (algorithm === "hmac-sha384") hashAlgo = "sha384";
  else if (algorithm === "hmac-sha512") hashAlgo = "sha512";
  else hashAlgo = "sha1";

  const mac = createHmac(hashAlgo, secret);
  mac.update(signatureString);
  const encoded = encodeSignature(mac.digest());

  return { headers, signature: encoded };
}

export interface AuthConfig {
  apiKey: string;
  apiSecret: string;
  baseUrl: string;
  algorithm: string;
  hmacNonceEnabled: boolean;
  apiVersion: string;
}

export function getAuthConfig(): AuthConfig {
  const result = envSchema.safeParse({
    DNSE_API_KEY: process.env["DNSE_API_KEY"],
    DNSE_API_SECRET: process.env["DNSE_API_SECRET"],
    DNSE_BASE_URL: process.env["DNSE_BASE_URL"],
    DNSE_ALGORITHM: process.env["DNSE_ALGORITHM"],
    DNSE_HMAC_NONCE: process.env["DNSE_HMAC_NONCE"],
    DNSE_API_VERSION: process.env["DNSE_API_VERSION"],
  });

  if (!result.success) {
    console.error("⚠️ WARNING: DNSE MCP Server configuration validation failed!");
    result.error.errors.forEach((err) => {
      console.error(`   - ${err.path.join(".")}: ${err.message}`);
    });
    console.error("   The server will start, but authenticated tools will fail when invoked.\n");

    return {
      apiKey: process.env["DNSE_API_KEY"] || "",
      apiSecret: process.env["DNSE_API_SECRET"] || "",
      baseUrl: process.env["DNSE_BASE_URL"] || "https://openapi.dnse.com.vn",
      algorithm: process.env["DNSE_ALGORITHM"] || "hmac-sha256",
      hmacNonceEnabled: process.env["DNSE_HMAC_NONCE"] !== "false",
      apiVersion: process.env["DNSE_API_VERSION"] || "2026-05-07",
    };
  }

  const data = result.data;
  return {
    apiKey: data.DNSE_API_KEY,
    apiSecret: data.DNSE_API_SECRET,
    baseUrl: data.DNSE_BASE_URL,
    algorithm: data.DNSE_ALGORITHM,
    hmacNonceEnabled: data.DNSE_HMAC_NONCE,
    apiVersion: data.DNSE_API_VERSION,
  };
}

export function generateSignatureHeaders(
  config: AuthConfig,
  method: string,
  path: string,
): { dateValue: string; signatureHeader: string } {
  if (!config.apiKey || !config.apiSecret) {
    throw new Error(
      "DNSE API credentials are not configured. Please set DNSE_API_KEY and DNSE_API_SECRET environment variables.",
    );
  }

  const dateValue = formatDate(new Date());
  const nonce = config.hmacNonceEnabled ? randomUUID().replace(/-/g, "") : undefined;

  const { headers, signature } = buildSignature(
    config.apiSecret,
    method,
    path,
    dateValue,
    config.algorithm,
    nonce,
  );

  let signatureHeader = `Signature keyId="${config.apiKey}",algorithm="${config.algorithm}",headers="${headers}",signature="${signature}"`;
  if (nonce) {
    signatureHeader += `,nonce="${nonce}"`;
  }

  return { dateValue, signatureHeader };
}
