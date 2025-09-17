import asyncio  
from mcp import ClientSession  #mcp会话管理
from contextlib import AsyncExitStack  #资源管理，退出后释放资源

class MCPClient:
    def __init__(self):
        self.session = None     #先不链接mcp服务器
        self.exit_stack = AsyncExitStack()    
        """ 初始化退出栈 """

    async def connect_to_mcp_server(self):
        print("Connecting to MCP server...")  
        """ 连接到MCP服务器 """

    async def chat_loop(self):
        """ 聊天循环 """
        print("\nMCP 客户端已启动！输入 'quit' 退出")

    async def main(self):
        print("Starting MCP client...")  
        """ 启动MCP客户端 """

        while True:
            try:
                query = input("请输入问题: ").strip()
                if query.lower() == "quit":
                    print("退出客户端")
                    break
                print(f"\n [Mock Response] 你说的是：{query}")
            except Exception as e:
                print(f"\n [Error] {e}")
    
    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        await client.connect_to_mcp_server()
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(MCPClient().main())