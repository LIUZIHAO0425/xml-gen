import asyncio  
import os
from openai import OpenAI
from dotenv import load_dotenv
from contextlib import AsyncExitStack  #资源管理，退出后释放资源

# 加载 .venv文件，确保apikey收到保护
load_dotenv() 

class MCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()    
        """ 初始化退出栈 """
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  #读取openai key
        self.base_url = os.getenv("BASE_URL")  #读取base url
        self.model = os.getenv("MODEL")

        required_vars = {
          "OPENAI_API_KEY": self.openai_api_key,
          "BASE_URL": self.base_url,
          "MODEL": self.model,
        }
        #dict，进行一下检查
        for var_name, var_value in required_vars.items():
          if not var_value:
            raise ValueError(f"环境变量错误: {var_name} 未设置")

        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url) #创建客户端

    async def process_query(self, query:str) -> str:
        messages = [
            {"role": "system", "content": "你是一个智能助手，根据输入的需求，总结内容生成相应的json文件"},
            {"role": "user", "content": query},
        ]
        try:
            #开始引入大模型，调用api
            response = await asyncio.get_event_loop().run_in_executor(   #防止堵塞
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                ),
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"调用出现Error: {e}")
              
            
    async def chat_loop(self):
        """ run 聊天循环 """
        print("\nMCP 客户端已启动！输入 'quit' 退出")

        while True:
            try:
                query = input("请输入问题: ").strip()
                if query.lower() == "quit":
                    print("退出客户端")
                    break
                response = await self.process_query(query)
                print(f"\n 🤖OpenAI：{response}")
            except Exception as e:
                print(f"\n ⚠️[Error] {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        await client.chat_loop()
    finally:
        await client.cleanup()
   



if __name__ == "__main__":
    asyncio.run(main())