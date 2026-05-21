import { z } from "zod";
export function getAccountTools(client) {
    return [
        {
            name: "dnse_get_accounts",
            description: "Get list of all trading accounts associated with the API key",
            inputSchema: z.object({}),
            handler: async () => {
                const { status, body } = await client.get("/accounts");
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_balances",
            description: "Get cash and asset balances for a specific account (co so & phai sinh)",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/balances`);
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_loan_packages",
            description: "Get available loan/margin packages for an account by market type",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                symbol: z.string().optional().describe("Filter by stock symbol"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/loan-packages`, {
                    marketType: args.marketType,
                    symbol: args.symbol,
                });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_ppse",
            description: "Calculate purchasing power (suc mua, suc ban) for a symbol",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                symbol: z.string().describe("Stock symbol"),
                price: z.number().describe("Price to calculate purchasing power"),
                loanPackageId: z.number().describe("Loan package ID"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/ppse`, {
                    marketType: args.marketType,
                    symbol: args.symbol,
                    price: String(args.price),
                    loanPackageId: String(args.loanPackageId),
                });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_orders",
            description: "Get today's order list (so lenh) for an account by market type",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/orders`, { marketType: args.marketType });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_order_detail",
            description: "Get detailed status of a specific order by order ID",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                orderId: z.string().describe("Order ID"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/orders/${args.orderId}`, { marketType: args.marketType });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_execution_detail",
            description: "Get execution/trade history for an order (phai sinh only)",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                orderId: z.string().describe("Order ID"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                orderCategory: z.string().optional().default("NORMAL").describe("Order category (default: NORMAL)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/executions/${args.orderId}`, {
                    marketType: args.marketType,
                    orderCategory: args.orderCategory || "NORMAL",
                });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_order_history",
            description: "Get historical orders within a date range (max 1 year)",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                from: z.string().optional().describe("Start date (yyyy-MM-dd)"),
                to: z.string().optional().describe("End date (yyyy-MM-dd)"),
                pageSize: z.number().optional().describe("Page size"),
                pageIndex: z.number().optional().describe("Page index"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/orders/history`, {
                    marketType: args.marketType,
                    from: args.from,
                    to: args.to,
                    pageSize: args.pageSize,
                    pageIndex: args.pageIndex,
                });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_get_positions",
            description: "Get all open positions (vi the nam giu) for an account by market type",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
            }),
            handler: async (args) => {
                const { status, body } = await client.get(`/accounts/${args.accountNo}/positions`, { marketType: args.marketType });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_post_order",
            description: "Place a new order (requires trading-token from OTP)",
            inputSchema: z.object({
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                tradingToken: z.string().describe("Trading token from OTP authentication"),
                payload: z.any().describe("Order payload object"),
            }),
            handler: async (args) => {
                const { status, body } = await client.post("/accounts/orders", args.payload, { marketType: args.marketType, orderCategory: "NORMAL" }, { "trading-token": args.tradingToken });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_put_order",
            description: "Modify an existing pending order (requires trading-token)",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                orderId: z.string().describe("Order ID to modify"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                tradingToken: z.string().describe("Trading token from OTP authentication"),
                payload: z.any().describe("Updated order payload"),
            }),
            handler: async (args) => {
                const { status, body } = await client.put(`/accounts/${args.accountNo}/orders/${args.orderId}`, args.payload, { marketType: args.marketType }, { "trading-token": args.tradingToken });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_cancel_order",
            description: "Cancel a pending order (requires trading-token)",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                orderId: z.string().describe("Order ID to cancel"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                tradingToken: z.string().describe("Trading token from OTP authentication"),
            }),
            handler: async (args) => {
                const { status, body } = await client.delete(`/accounts/${args.accountNo}/orders/${args.orderId}`, { marketType: args.marketType }, { "trading-token": args.tradingToken });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_close_position",
            description: "Close an open position (requires trading-token)",
            inputSchema: z.object({
                accountNo: z.string().describe("Account number"),
                positionId: z.string().describe("Position ID to close"),
                marketType: z.enum(["STOCK", "DERIVATIVE"]).describe("Market type (STOCK or DERIVATIVE)"),
                tradingToken: z.string().describe("Trading token from OTP authentication"),
                payload: z.any().describe("Close position payload"),
            }),
            handler: async (args) => {
                const { status, body } = await client.post(`/accounts/${args.accountNo}/positions/${args.positionId}/close`, args.payload, { "trading-token": args.tradingToken, marketType: args.marketType });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_create_trading_token",
            description: "Create a trading token via OTP authentication",
            inputSchema: z.object({
                otpType: z.enum(["email_otp", "smart_otp"]).describe("OTP type: email_otp or smart_otp"),
                passcode: z.string().describe("OTP passcode from email or SmartOTP app"),
            }),
            handler: async (args) => {
                const { status, body } = await client.post("/registration/trading-token", {
                    otpType: args.otpType,
                    passcode: args.passcode,
                });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
        {
            name: "dnse_send_email_otp",
            description: "Send OTP code to registered email for authentication",
            inputSchema: z.object({
                email: z.string().describe("Registered email address"),
            }),
            handler: async (args) => {
                const { status, body } = await client.post("/registration/send-email-otp", {
                    email: args.email,
                    otpType: "email_otp",
                });
                return { content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }] };
            },
        },
    ];
}
