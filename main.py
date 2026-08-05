import asyncio
from client.session import create_session
from router import route_message
from mcp.types import CreateMessageRequestParams, CreateMessageResult, TextContent
from mcp.shared.context import RequestContext
from mcp import ClientSession

async def process_input(
        context: RequestContext[ClientSession, None],
        params: CreateMessageRequestParams
):
    message_text = params.messages[0].content.text.strip()
    result = await route_message(context, message_text)

    return result

async def main():
    # session = await create_session(callback=process_input)
    # try:
    #     await session.initialize()
    #     print("[The system launched] Enter your input (type 'exit' to quit):")
    #     while True:
    #         query = input("Email content> ").strip()
    #         if query.lower() == 'exit':
    #             break
    #         await session.inject_text(query)
    # finally:
    #     #await session.exit_stack.aclose()
    #     pass

    async with create_session() as session:
        await session.initialize()
        print("[The system launched] Enter your input (type 'exit' to quit):")
        while True:
            query = input("Email content> ").strip()
            if query.lower() == "exit":
                break

            response_text = await route_message(session, query)
            print("Assistant:", response_text or "<no content returned>")

if __name__ == "__main__":
    asyncio.run(main())
    