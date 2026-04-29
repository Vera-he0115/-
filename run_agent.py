import asyncio
from agentic_workflow import Agent

async def main():
    # 创建智能体实例
    agent = Agent(api_key="sk-ffcedad879664de9805ddaa89af44484")
    
    # 示例用户输入
    user_input = "帮我调研2026年关于DPO算法的最新进展"
    
    print("智能体工作流启动中...")
    print(f"用户输入: {user_input}")
    print("=" * 80)
    
    # 运行智能体工作流
    result = await agent.run(user_input)
    
    print("=" * 80)
    print(f"工作流完成: {result}")

if __name__ == "__main__":
    asyncio.run(main())