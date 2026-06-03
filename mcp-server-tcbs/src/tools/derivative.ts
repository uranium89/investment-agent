import { z } from "zod";
import { randomUUID } from "node:crypto";
import { TCBSOpenAPIClient } from "../client.js";
import type { ToolDefinition } from "./types.js";

// Helper to generate a unique refId in the format H.sequence
function generateRefId(): string {
  const uuid = randomUUID().replace(/-/g, "").substring(0, 16);
  return `H.${uuid}`;
}

export function getDerivativeTools(client: TCBSOpenAPIClient): ToolDefinition[] {
  return [
    {
      name: "tcbs_get_derivative_cash_margin",
      description: "Get derivative account status including cash overview and margin requirements.",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        subAccountId: z.string().describe("Derivative sub-account number (e.g. 105C031402A)"),
        getType: z.enum(["0", "1"]).default("0").describe("0 = Get all, 1 = Only money"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get("/khronos/v1/account/status", {
          accountId: args.accountId as string,
          subAccountId: args.subAccountId as string,
          getType: args.getType as string,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_get_derivative_positions_open",
      description: "Get list of open derivative positions and asset status.",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        subAccountId: z.string().describe("Derivative sub-account number (e.g. 105C031402A)"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get("/khronos/v1/account/portfolio/status", {
          accountId: args.accountId as string,
          subAccountId: args.subAccountId as string,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_get_derivative_positions_close",
      description: "Get historical closed derivative positions with realized PnL, fees and taxes.",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        subAccountId: z.string().describe("Derivative sub-account number (e.g. 105C031402A)"),
        symbol: z.string().optional().describe("Optional stock / derivative contract symbol"),
        pageNo: z.number().optional().default(1).describe("Page number"),
        pageSize: z.number().optional().default(20).describe("Page size"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get("/khronos/v1/account/portfolio/position/close", {
          accountId: args.accountId as string,
          subAccountId: args.subAccountId as string,
          symbol: args.symbol as string | undefined,
          pageNo: args.pageNo as number,
          pageSize: args.pageSize as number,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_place_derivative_order",
      description: "Place a new normal derivative order (Long or Short).",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        subAccountId: z.string().describe("Derivative sub-account number (e.g. 105C031402A)"),
        symbol: z.string().describe("Derivative contract symbol (e.g. VN30F2303)"),
        side: z.enum(["B", "S"]).describe("B = Buy/Long, S = Sell/Short"),
        price: z.number().describe("Order price (e.g. 1198.7)"),
        volume: z.number().describe("Order quantity/volume"),
        orderType: z
          .string()
          .default("0")
          .describe("0 = Normal order, SLP=1.0,0.8 = StopLoss/TakeProfit, ABI = Arbitrage"),
        refId: z
          .string()
          .optional()
          .describe("Optional unique random ID. If not set, one will be generated."),
        pin: z.string().optional().default("H").describe("Order channel"),
      }),
      handler: async (args) => {
        const refId = (args.refId as string) || generateRefId();
        const { status, body } = await client.post("/khronos/v1/order/place", {
          accountId: args.accountId as string,
          subAccountId: args.subAccountId as string,
          symbol: args.symbol as string,
          side: args.side as string,
          price: args.price as number,
          volume: args.volume as number,
          orderType: args.orderType as string,
          refId,
          pin: args.pin as string,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, refId, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_place_derivative_conditional_order",
      description: "Place a conditional derivative order (Stop Order or Trailing Stop).",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        subAccountId: z.string().describe("Derivative sub-account number (e.g. 105C031402A)"),
        symbol: z.string().describe("Derivative contract symbol (e.g. VN30F2303)"),
        side: z.enum(["B", "S"]).describe("B = Buy/Long, S = Sell/Short"),
        price: z.number().describe("Order price"),
        volume: z.number().describe("Order quantity/volume"),
        orderType: z
          .enum(["SOU", "SOL", "TSO"])
          .describe("SOU = price <= activation, SOL = price >= activation, TSO = Trailing Stop"),
        activationPrice: z.number().describe("Activation price for stop condition"),
        soPrice: z.number().describe("Activation price for trailing stop condition"),
        callbackPoint: z.number().default(0.1).describe("Trailing step deviation (e.g. 0.1)"),
        refId: z
          .string()
          .optional()
          .describe("Optional unique random ID. If not set, one will be generated."),
        pin: z.string().optional().default("H").describe("Order channel"),
      }),
      handler: async (args) => {
        const refId = (args.refId as string) || generateRefId();
        const { status, body } = await client.post("/khronos/v1/order/condition/place", {
          accountId: args.accountId as string,
          subAccountId: args.subAccountId as string,
          symbol: args.symbol as string,
          side: args.side as string,
          price: args.price as number,
          volume: args.volume as number,
          orderType: args.orderType as string,
          activationPrice: args.activationPrice as number,
          soPrice: args.soPrice as number,
          callbackPoint: args.callbackPoint as number,
          refId,
          pin: args.pin as string,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, refId, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_cancel_derivative_order",
      description: "Cancel a pending normal derivative order.",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        orderNo: z.string().describe("Order number to cancel (retrieved from the order book)"),
        cmd: z.string().optional().default("Web.cancelOrder").describe("Business type command"),
        refId: z.string().optional().describe("Optional reference ID"),
      }),
      handler: async (args) => {
        const { status, body } = await client.put("/khronos/v1/order/cancel", {
          accountId: args.accountId as string,
          orderNo: args.orderNo as string,
          cmd: args.cmd as string,
          refId: args.refId as string | undefined,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_cancel_derivative_conditional_order",
      description: "Cancel a pending conditional derivative order.",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        orderNo: z
          .string()
          .describe("Order number to cancel (retrieved from conditional order book)"),
        cmd: z
          .string()
          .optional()
          .default("Web.cancelActivatedOrder")
          .describe("Business type command"),
      }),
      handler: async (args) => {
        const { status, body } = await client.put("/khronos/v1/order/condition/cancel", {
          accountId: args.accountId as string,
          orderNo: args.orderNo as string,
          cmd: args.cmd as string,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_get_derivative_orders",
      description: "Retrieve list of today's normal derivative orders.",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        symbol: z
          .string()
          .optional()
          .default("ALL,ALL")
          .describe("Filter contract & side (e.g. ALL,ALL or VN30F2303,B)"),
        status: z
          .enum(["0", "1", "2"])
          .default("0")
          .describe("0 = All, 1 = Waiting for match, 2 = Matched"),
        orderType: z
          .string()
          .optional()
          .default("")
          .describe("Empty = All, 3 = Arbitrage, 4 = SL/TP, 5 = ForceClose, 6 = Normal"),
        pageNo: z.number().optional().default(1).describe("Page number"),
        pageSize: z.number().optional().default(20).describe("Page size"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get("/khronos/v1/order/in-day", {
          accountId: args.accountId as string,
          symbol: args.symbol as string,
          status: args.status as string,
          orderType: args.orderType as string,
          pageNo: args.pageNo as number,
          pageSize: args.pageSize as number,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_get_derivative_conditional_orders",
      description: "Retrieve list of derivative conditional orders.",
      inputSchema: z.object({
        accountId: z.string().describe("Custody account number (e.g. 105C031402)"),
        subAccountId: z.string().describe("Derivative sub-account number (e.g. 105C031402A)"),
        orderStatus: z
          .enum(["0", "1", "2", "3"])
          .default("0")
          .describe("0 = All, 1 = Waiting for activation, 2 = Activated, 3 = Rejected"),
        orderType: z
          .string()
          .optional()
          .default("ALL,ALL")
          .describe("ALL,ALL = All, 3 = Arbitrage, 4 = SL/TP, 5 = stopOrder"),
        symbol: z
          .string()
          .optional()
          .default("")
          .describe("Filter contract & side (e.g. VN30F2303,B)"),
        pageNo: z.number().optional().default(1).describe("Page number"),
        pageSize: z.number().optional().default(25).describe("Page size"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get("/khronos/v1/order/condition/detail", {
          accountId: args.accountId as string,
          subAccountID: args.subAccountId as string,
          orderStatus: args.orderStatus as string,
          orderType: args.orderType as string,
          Symbol: args.symbol as string,
          pageNo: args.pageNo as number,
          PageSize: args.pageSize as number,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },
  ];
}
