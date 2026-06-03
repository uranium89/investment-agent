import { z } from "zod";
import { TCBSOpenAPIClient } from "../client.js";
import type { ToolDefinition } from "./types.js";

export function getOrderTools(client: TCBSOpenAPIClient): ToolDefinition[] {
  return [
    {
      name: "tcbs_place_order",
      description: "Place a new stock order (co so) for buying or selling.",
      inputSchema: z.object({
        accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
        execType: z.enum(["NB", "NS"]).describe("NB = Buy, NS = Sell"),
        symbol: z.string().describe("Stock symbol (e.g. VNM, FPT)"),
        price: z.number().describe("Trading price (e.g. 10000)"),
        quantity: z.number().describe("Trading quantity (e.g. 100)"),
        priceType: z
          .enum(["LO", "ATO", "ATC", "PLO", "MP", "MTL", "MOK", "MAK"])
          .default("LO")
          .describe("Price type (default LO)"),
      }),
      handler: async (args) => {
        const { status, body } = await client.post(`/akhlys/v1/accounts/${args.accountNo}/orders`, {
          execType: args.execType as string,
          symbol: args.symbol as string,
          price: args.price as number,
          quantity: args.quantity as number,
          priceType: args.priceType as string,
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_update_order",
      description: "Modify a pending stock order's price or quantity.",
      inputSchema: z.object({
        accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
        orderId: z.string().describe("Order ID to modify"),
        price: z.number().describe("New trading price"),
        quantity: z.number().describe("New trading quantity"),
      }),
      handler: async (args) => {
        const { status, body } = await client.put(
          `/akhlys/v1/accounts/${args.accountNo}/orders/${args.orderId}`,
          {
            price: args.price as number,
            quantity: args.quantity as number,
          },
        );
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_cancel_order",
      description: "Cancel one or more pending stock orders.",
      inputSchema: z.object({
        accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
        orderIds: z.array(z.string()).describe("List of Order IDs to cancel"),
      }),
      handler: async (args) => {
        const ordersList = (args.orderIds as string[]).map((id) => ({
          orderID: id,
        }));

        const { status, body } = await client.put(
          `/akhlys/v1/accounts/${args.accountNo}/cancel-orders`,
          {
            ordersList,
          },
        );
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_get_orders",
      description: "Retrieve list of today's stock orders or details for a specific order ID.",
      inputSchema: z.object({
        accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
        orderId: z.string().optional().describe("Optional specific Order ID to query"),
      }),
      handler: async (args) => {
        let path = `/aion/v1/accounts/${args.accountNo}/orders`;
        if (args.orderId) {
          path += `/${args.orderId}`;
        }
        const { status, body } = await client.get(path);
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },

    {
      name: "tcbs_get_matching_details",
      description: "Get trade execution/matching details for a stock sub-account.",
      inputSchema: z.object({
        accountNo: z.string().describe("Sub-account number (e.g. 0001170730)"),
      }),
      handler: async (args) => {
        const { status, body } = await client.get(
          `/aion/v1/accounts/${args.accountNo}/matching-details`,
        );
        return {
          content: [{ type: "text", text: JSON.stringify({ status, data: body }, null, 2) }],
        };
      },
    },
  ];
}
