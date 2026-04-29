import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List

class APIClient:
    def __init__(self, api_key: str, api_url: str = "https://api.deepseek.com/v1/chat/completions"):
        self.api_key = api_key
        self.api_url = api_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def call_deepseek(self, prompt: str, model: str = "deepseek-chat", max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        调用DeepSeek API
        :param prompt: 提示词
        :param model: 模型名称
        :param max_tokens: 最大 tokens
        :param temperature: 温度参数
        :return: API响应
        """
        await self._ensure_session()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        start_time = time.time()
        try:
            async with self.session.post(self.api_url, headers=headers, json=data) as response:
                response.raise_for_status()
                result = await response.json()
                end_time = time.time()
                
                # 处理响应
                if "choices" in result and len(result["choices"]) > 0:
                    return {
                        "success": True,
                        "content": result["choices"][0]["message"]["content"],
                        "usage": result.get("usage", {}),
                        "time": end_time - start_time
                    }
                else:
                    return {
                        "success": False,
                        "error": "No choices in response",
                        "time": end_time - start_time
                    }
        except Exception as e:
            end_time = time.time()
            return {
                "success": False,
                "error": str(e),
                "time": end_time - start_time
            }
    
    async def process_long_text(self, text: str, max_length: int = 4000) -> str:
        """
        处理长文本，进行截断
        :param text: 原始文本
        :param max_length: 最大长度
        :return: 截断后的文本
        """
        if len(text) > max_length:
            return text[:max_length] + "... [文本已截断]"
        return text
    
    async def batch_call(self, prompts: List[str], max_concurrent: int = 3) -> List[Dict[str, Any]]:
        """
        批量调用API，支持并发
        :param prompts: 提示词列表
        :param max_concurrent: 最大并发数
        :return: 响应列表
        """
        await self._ensure_session()
        
        # 限制并发数
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def call_with_semaphore(prompt):
            async with semaphore:
                # 添加延迟，避免API限流
                await asyncio.sleep(0.5)
                return await self.call_deepseek(prompt)
        
        tasks = [call_with_semaphore(prompt) for prompt in prompts]
        return await asyncio.gather(*tasks)

# 示例用法
async def main():
    api_key = "sk-ffcedad879664de9805ddaa89af44484"
    async with APIClient(api_key) as client:
        # 测试单个调用
        prompt = "请简要介绍DPO算法的原理"
        result = await client.call_deepseek(prompt)
        print(f"单个调用结果: {result}")
        
        # 测试批量调用
        prompts = [
            "请介绍DPO算法的优点",
            "请介绍DPO算法的应用场景",
            "请介绍DPO算法的最新进展"
        ]
        results = await client.batch_call(prompts)
        print(f"批量调用结果: {results}")

if __name__ == "__main__":
    asyncio.run(main())