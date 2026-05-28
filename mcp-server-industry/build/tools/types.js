export function safeHandler(handler) {
    return async (args) => {
        try {
            return await handler(args);
        }
        catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            return {
                content: [
                    {
                        type: "text",
                        text: `Error executing tool: ${errorMessage}`,
                    },
                ],
                isError: true,
            };
        }
    };
}
