import { z } from "zod";
import { setRuntimeToken } from "../auth.js";
export function getAccountTools(client) {
    return [
        {
            name: "tcbs_get_token",
            description: "Exchange API Key and iOTP passcode for a temporary JWT Access Token. Updates the client state automatically.",
            inputSchema: z.object({
                apiKey: z.string().describe("Your TCBS API Key generated on TCInvest"),
                otp: z.string().describe("iOTP passcode from your TCInvest app"),
            }),
            handler: async (args) => {
                const { status, body } = await client.post("/gaia/v1/oauth2/openapi/token", {
                    apiKey: args.apiKey,
                    otp: args.otp,
                });
                if (body && body.token) {
                    setRuntimeToken(body.token);
                }
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify({
                                status,
                                message: "Token retrieved successfully and cached in memory.",
                                token: body?.token,
                            }, null, 2),
                        },
                    ],
                };
            },
        },
        {
            name: "tcbs_get_sub_accounts",
            description: "Get detailed profile and sub-accounts information for a custody account",
            inputSchema: z.object({
                custodyCode: z.string().describe("Custody code (e.g. 105C334455)"),
                fields: z
                    .string()
                    .optional()
                    .default("basicInfo,personalInfo,bankSubAccounts,bankAccounts")
                    .describe("Comma-separated fields to retrieve"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/eros/v2/get-profile/by-username/${args.custodyCode}`, { fields: args.fields });
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
        {
            name: "tcbs_get_cash_investment",
            description: "Get remaining cash balances and cash investments for a specific sub-account",
            inputSchema: z.object({
                accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/aion/v1/accounts/${args.accountNo}/cashInvestments`);
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
        {
            name: "tcbs_get_asset_stock",
            description: "Get stock portfolio holdings and assets under a specific sub-account",
            inputSchema: z.object({
                accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/aion/v1/accounts/${args.accountNo}/se`);
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
        {
            name: "tcbs_get_purchasing_power",
            description: "Get purchasing power (suc mua) for a sub-account. Can optionally filter by stock symbol and price.",
            inputSchema: z.object({
                accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
                symbol: z.string().optional().describe("Optional stock symbol (e.g. FPT)"),
                price: z.number().optional().describe("Optional price to calculate purchasing power for (e.g. 52000)"),
            }),
            handler: async (args) => {
                let path = `/aion/v1/accounts/${args.accountNo}/ppse`;
                if (args.symbol) {
                    path += `/${args.symbol}`;
                    if (args.price !== undefined) {
                        path += `/${args.price}`;
                    }
                }
                const { status, body } = await client.get(path);
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
        {
            name: "tcbs_get_margin_risk",
            description: "Get margin risk parameters including total debt, interest, warning and maintenance ratios",
            inputSchema: z.object({
                accountNo: z.string().describe("Margin account number (e.g. 0001G75216)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/hydros/v1/account/${args.accountNo}/risk`);
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
        {
            name: "tcbs_get_loans",
            description: "Get detailed list of loans/margin contracts for a margin account",
            inputSchema: z.object({
                accountNo: z.string().describe("Margin account number (e.g. 0001G75216)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/khaos/v1/loan/${args.accountNo}`);
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
        {
            name: "tcbs_get_margin_info",
            description: "Get margin and debt history for a specific account inside a date range",
            inputSchema: z.object({
                accountNo: z.string().describe("Sub-account number"),
                custodyCode: z.string().describe("Custody code (e.g. 105C209414)"),
                fromDate: z.string().describe("From date (yyyy-MM-dd)"),
                toDate: z.string().describe("To date (yyyy-MM-dd)"),
                page: z.number().optional().default(1).describe("Page number"),
                size: z.number().optional().default(25).describe("Page size"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get("/erebos/v2/digital/margin-info", {
                    acctno: args.accountNo,
                    custodycd: args.custodyCode,
                    fromdate: args.fromDate,
                    toDate: args.toDate,
                    page: args.page,
                    size: args.size,
                });
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
        {
            name: "tcbs_get_cash_statements",
            description: "Get historical cash statements for a sub-account",
            inputSchema: z.object({
                accountNo: z.string().describe("Sub-account number"),
                fromDate: z.string().describe("From date (yyyy-MM-dd)"),
                toDate: z.string().describe("To date (yyyy-MM-dd)"),
                pageIndex: z.number().optional().default(1).describe("Page number"),
                pageSize: z.number().optional().default(25).describe("Page size"),
                transactionCode: z.string().optional().describe("Optional transaction code filter"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get("/erebos/v2/digital/trans-hist-cashStatements", {
                    accountNo: args.accountNo,
                    fromDate: args.fromDate,
                    toDate: args.toDate,
                    pageIndex: args.pageIndex,
                    pageSize: args.pageSize,
                    transactionCode: args.transactionCode,
                });
                return {
                    content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
                };
            },
        },
    ];
}
