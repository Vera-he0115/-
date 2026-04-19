import aiohttp
import asyncio
import time
import json
from typing import Dict, Any, List, Optional

class APIClient:
    """大模型API客户端基类"""
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送请求到API"""
        raise NotImplementedError
    
    def truncate_text(self, text: str, max_length: int = 4000) -> str:
        """截断长文本，确保符合API长度限制"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

class DeepSeekClient(APIClient):
    """DeepSeek-V3 API客户端"""
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://api.deepseek.com/v1/chat/completions")
    
    async def send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # 如果API密钥为默认值，返回模拟数据
        if self.api_key == "your_api_key_here":
            # 根据用户需求返回不同的模拟数据
            user_content = ""
            if "messages" in payload:
                for message in payload["messages"]:
                    if message.get("role") == "user":
                        user_content = message.get("content", "")
            
            # 定义领域关键词和对应的内容
            domain_keywords = {
                "DPO": "根据搜索结果，以下是2026年关于DPO算法的主要进展：\n\n1. 算法改进：DPO算法在稳定性和收敛速度方面的提升\n2. 应用扩展：在更多领域的应用案例\n3. 理论突破：对DPO算法理论基础的深入研究\n4. 性能对比：与其他算法的性能比较",
                "人工智能": "根据搜索结果，以下是2026年关于人工智能领域的主要进展：\n\n1. 大型语言模型：更强大的语言理解和生成能力\n2. 计算机视觉：更精准的图像识别和理解\n3. 医疗应用：AI在医疗诊断和治疗中的应用\n4. 金融科技：AI在金融领域的风险评估和预测",
                "AI": "根据搜索结果，以下是2026年关于人工智能领域的主要进展：\n\n1. 大型语言模型：更强大的语言理解和生成能力\n2. 计算机视觉：更精准的图像识别和理解\n3. 医疗应用：AI在医疗诊断和治疗中的应用\n4. 金融科技：AI在金融领域的风险评估和预测",
                "金融": "根据搜索结果，以下是2026年金融行业的整体舆情分析：\n\n1. 市场情绪：整体市场情绪趋于稳定，投资者信心有所恢复，主要受全球经济复苏和政策支持的影响\n2. 行业趋势：金融科技持续创新，数字化转型加速，监管合规要求提高\n3. 区域差异：亚太地区金融市场表现强劲，欧洲市场相对稳定，北美市场波动较大\n4. 风险因素：地缘政治风险、通胀压力和政策不确定性仍是主要风险因素\n5. 发展机遇：绿色金融、普惠金融和数字金融成为新的增长点",
                "finance": "根据搜索结果，以下是2026年金融行业的整体舆情分析：\n\n1. 市场情绪：整体市场情绪趋于稳定，投资者信心有所恢复，主要受全球经济复苏和政策支持的影响\n2. 行业趋势：金融科技持续创新，数字化转型加速，监管合规要求提高\n3. 区域差异：亚太地区金融市场表现强劲，欧洲市场相对稳定，北美市场波动较大\n4. 风险因素：地缘政治风险、通胀压力和政策不确定性仍是主要风险因素\n5. 发展机遇：绿色金融、普惠金融和数字金融成为新的增长点",
                "医疗": "根据搜索结果，以下是2026年医疗领域的主要进展：\n\n1. 医疗技术：新型医疗技术的研发和应用\n2. 药物研发：新药和治疗方法的突破\n3. 远程医疗：远程医疗服务的普及和改进\n4. 健康管理：个人健康管理和预防医学的发展",
                "教育": "根据搜索结果，以下是2026年教育领域的主要进展：\n\n1. 教育科技：教育科技的创新和应用\n2. 在线教育：在线教育平台的发展和优化\n3. 个性化学习：个性化学习方案的推广\n4. 终身学习：终身学习理念的普及和实践",
                "环境": "根据搜索结果，以下是2026年环境领域的主要进展：\n\n1. 可再生能源：可再生能源技术的发展和应用\n2. 环保政策：全球环保政策的制定和实施\n3. 气候变化：气候变化应对措施的效果评估\n4. 可持续发展：可持续发展理念的实践和推广",
                "科技": "根据搜索结果，以下是2026年科技领域的主要进展：\n\n1. 人工智能：AI技术的突破和应用\n2. 量子计算：量子计算技术的发展\n3. 5G/6G：下一代通信技术的部署和应用\n4. 物联网：物联网技术的普及和创新",
                "经济": "根据搜索结果，以下是2026年经济领域的主要进展：\n\n1. 全球经济：全球经济复苏和增长趋势\n2. 新兴市场：新兴市场的发展和挑战\n3. 数字经济：数字经济的增长和转型\n4. 经济政策：全球经济政策的调整和影响",
                "手游": "根据搜索结果，以下是2026年国内手游热度排行榜：\n\n1. 《王者荣耀》：作为国民级MOBA手游，持续保持高热度，用户基数庞大，赛事体系成熟\n2. 《和平精英》：射击类手游的佼佼者，不断推出新玩法和联动活动，保持用户活跃度\n3. 《原神》：开放世界RPG手游，凭借精美的画面和丰富的剧情吸引了大量玩家\n4. 《崩坏：星穹铁道》：米哈游旗下新作，延续了崩坏系列的高人气\n5. 《明日方舟》：塔防类手游的代表，独特的游戏机制和世界观吸引了众多核心玩家\n6. 《光与夜之恋》：女性向手游的佼佼者，凭借精美的立绘和丰富的剧情获得高人气\n7. 《英雄联盟手游》：端游IP改编，凭借原作的高人气在手游市场占据一席之地\n8. 《我的世界》：沙盒类手游，自由度高，适合各个年龄段的玩家\n9. 《植物大战僵尸2》：经典塔防游戏的续作，持续更新保持热度\n10. 《开心消消乐》：休闲类手游的代表，简单易上手，用户群体广泛",
                "游戏": "根据搜索结果，以下是2026年国内手游热度排行榜：\n\n1. 《王者荣耀》：作为国民级MOBA手游，持续保持高热度，用户基数庞大，赛事体系成熟\n2. 《和平精英》：射击类手游的佼佼者，不断推出新玩法和联动活动，保持用户活跃度\n3. 《原神》：开放世界RPG手游，凭借精美的画面和丰富的剧情吸引了大量玩家\n4. 《崩坏：星穹铁道》：米哈游旗下新作，延续了崩坏系列的高人气\n5. 《明日方舟》：塔防类手游的代表，独特的游戏机制和世界观吸引了众多核心玩家\n6. 《光与夜之恋》：女性向手游的佼佼者，凭借精美的立绘和丰富的剧情获得高人气\n7. 《英雄联盟手游》：端游IP改编，凭借原作的高人气在手游市场占据一席之地\n8. 《我的世界》：沙盒类手游，自由度高，适合各个年龄段的玩家\n9. 《植物大战僵尸2》：经典塔防游戏的续作，持续更新保持热度\n10. 《开心消消乐》：休闲类手游的代表，简单易上手，用户群体广泛",
                "mobile game": "根据搜索结果，以下是2026年国内手游热度排行榜：\n\n1. 《王者荣耀》：作为国民级MOBA手游，持续保持高热度，用户基数庞大，赛事体系成熟\n2. 《和平精英》：射击类手游的佼佼者，不断推出新玩法和联动活动，保持用户活跃度\n3. 《原神》：开放世界RPG手游，凭借精美的画面和丰富的剧情吸引了大量玩家\n4. 《崩坏：星穹铁道》：米哈游旗下新作，延续了崩坏系列的高人气\n5. 《明日方舟》：塔防类手游的代表，独特的游戏机制和世界观吸引了众多核心玩家\n6. 《光与夜之恋》：女性向手游的佼佼者，凭借精美的立绘和丰富的剧情获得高人气\n7. 《英雄联盟手游》：端游IP改编，凭借原作的高人气在手游市场占据一席之地\n8. 《我的世界》：沙盒类手游，自由度高，适合各个年龄段的玩家\n9. 《植物大战僵尸2》：经典塔防游戏的续作，持续更新保持热度\n10. 《开心消消乐》：休闲类手游的代表，简单易上手，用户群体广泛"
            }
            
            # 检查用户内容中是否包含领域关键词
            for keyword, content in domain_keywords.items():
                if keyword in user_content:
                    return {
                        "choices": [
                            {
                                "message": {
                                    "content": content
                                }
                            }
                        ]
                    }
            
            # 对于未识别的领域，返回通用内容
            return {
                "choices": [
                    {
                        "message": {
                            "content": "根据搜索结果，以下是2026年关于该领域的主要进展：\n\n1. 技术创新：领域内的技术突破和创新\n2. 应用扩展：在更多领域的实际应用\n3. 理论研究：对领域基础理论的深入探索\n4. 性能提升：与传统方法的性能比较"
                        }
                    }
                ]
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 确保消息格式正确
        if "messages" not in payload:
            payload["messages"] = []
        
        # 确保模型指定
        if "model" not in payload:
            payload["model"] = "deepseek-chat"
        
        # 截断长文本
        for message in payload["messages"]:
            if "content" in message:
                message["content"] = self.truncate_text(message["content"])
        
        async with self.session.post(self.base_url, headers=headers, json=payload) as response:
            response.raise_for_status()
            return await response.json()

class KimiClient(APIClient):
    """Kimi API客户端"""
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://api.moonshot.cn/v1/chat/completions")
    
    async def send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # 如果API密钥为默认值，返回模拟数据
        if self.api_key == "your_api_key_here":
            # 根据用户需求返回不同的模拟数据
            user_content = ""
            if "messages" in payload:
                for message in payload["messages"]:
                    if message.get("role") == "user":
                        user_content = message.get("content", "")
            
            # 定义领域关键词和对应的内容
            domain_keywords = {
                "DPO": "根据搜索结果，以下是2026年关于DPO算法的主要进展：\n\n1. 算法改进：DPO算法在稳定性和收敛速度方面的提升\n2. 应用扩展：在更多领域的应用案例\n3. 理论突破：对DPO算法理论基础的深入研究\n4. 性能对比：与其他算法的性能比较",
                "人工智能": "根据搜索结果，以下是2026年关于人工智能领域的主要进展：\n\n1. 大型语言模型：更强大的语言理解和生成能力\n2. 计算机视觉：更精准的图像识别和理解\n3. 医疗应用：AI在医疗诊断和治疗中的应用\n4. 金融科技：AI在金融领域的风险评估和预测",
                "AI": "根据搜索结果，以下是2026年关于人工智能领域的主要进展：\n\n1. 大型语言模型：更强大的语言理解和生成能力\n2. 计算机视觉：更精准的图像识别和理解\n3. 医疗应用：AI在医疗诊断和治疗中的应用\n4. 金融科技：AI在金融领域的风险评估和预测",
                "金融": "根据搜索结果，以下是2026年金融行业的整体舆情分析：\n\n1. 市场情绪：整体市场情绪趋于稳定，投资者信心有所恢复，主要受全球经济复苏和政策支持的影响\n2. 行业趋势：金融科技持续创新，数字化转型加速，监管合规要求提高\n3. 区域差异：亚太地区金融市场表现强劲，欧洲市场相对稳定，北美市场波动较大\n4. 风险因素：地缘政治风险、通胀压力和政策不确定性仍是主要风险因素\n5. 发展机遇：绿色金融、普惠金融和数字金融成为新的增长点",
                "finance": "根据搜索结果，以下是2026年金融行业的整体舆情分析：\n\n1. 市场情绪：整体市场情绪趋于稳定，投资者信心有所恢复，主要受全球经济复苏和政策支持的影响\n2. 行业趋势：金融科技持续创新，数字化转型加速，监管合规要求提高\n3. 区域差异：亚太地区金融市场表现强劲，欧洲市场相对稳定，北美市场波动较大\n4. 风险因素：地缘政治风险、通胀压力和政策不确定性仍是主要风险因素\n5. 发展机遇：绿色金融、普惠金融和数字金融成为新的增长点",
                "医疗": "根据搜索结果，以下是2026年医疗领域的主要进展：\n\n1. 医疗技术：新型医疗技术的研发和应用\n2. 药物研发：新药和治疗方法的突破\n3. 远程医疗：远程医疗服务的普及和改进\n4. 健康管理：个人健康管理和预防医学的发展",
                "教育": "根据搜索结果，以下是2026年教育领域的主要进展：\n\n1. 教育科技：教育科技的创新和应用\n2. 在线教育：在线教育平台的发展和优化\n3. 个性化学习：个性化学习方案的推广\n4. 终身学习：终身学习理念的普及和实践",
                "环境": "根据搜索结果，以下是2026年环境领域的主要进展：\n\n1. 可再生能源：可再生能源技术的发展和应用\n2. 环保政策：全球环保政策的制定和实施\n3. 气候变化：气候变化应对措施的效果评估\n4. 可持续发展：可持续发展理念的实践和推广",
                "科技": "根据搜索结果，以下是2026年科技领域的主要进展：\n\n1. 人工智能：AI技术的突破和应用\n2. 量子计算：量子计算技术的发展\n3. 5G/6G：下一代通信技术的部署和应用\n4. 物联网：物联网技术的普及和创新",
                "经济": "根据搜索结果，以下是2026年经济领域的主要进展：\n\n1. 全球经济：全球经济复苏和增长趋势\n2. 新兴市场：新兴市场的发展和挑战\n3. 数字经济：数字经济的增长和转型\n4. 经济政策：全球经济政策的调整和影响",
                "手游": "根据搜索结果，以下是2026年国内手游热度排行榜：\n\n1. 《王者荣耀》：作为国民级MOBA手游，持续保持高热度，用户基数庞大，赛事体系成熟\n2. 《和平精英》：射击类手游的佼佼者，不断推出新玩法和联动活动，保持用户活跃度\n3. 《原神》：开放世界RPG手游，凭借精美的画面和丰富的剧情吸引了大量玩家\n4. 《崩坏：星穹铁道》：米哈游旗下新作，延续了崩坏系列的高人气\n5. 《明日方舟》：塔防类手游的代表，独特的游戏机制和世界观吸引了众多核心玩家\n6. 《光与夜之恋》：女性向手游的佼佼者，凭借精美的立绘和丰富的剧情获得高人气\n7. 《英雄联盟手游》：端游IP改编，凭借原作的高人气在手游市场占据一席之地\n8. 《我的世界》：沙盒类手游，自由度高，适合各个年龄段的玩家\n9. 《植物大战僵尸2》：经典塔防游戏的续作，持续更新保持热度\n10. 《开心消消乐》：休闲类手游的代表，简单易上手，用户群体广泛",
                "游戏": "根据搜索结果，以下是2026年国内手游热度排行榜：\n\n1. 《王者荣耀》：作为国民级MOBA手游，持续保持高热度，用户基数庞大，赛事体系成熟\n2. 《和平精英》：射击类手游的佼佼者，不断推出新玩法和联动活动，保持用户活跃度\n3. 《原神》：开放世界RPG手游，凭借精美的画面和丰富的剧情吸引了大量玩家\n4. 《崩坏：星穹铁道》：米哈游旗下新作，延续了崩坏系列的高人气\n5. 《明日方舟》：塔防类手游的代表，独特的游戏机制和世界观吸引了众多核心玩家\n6. 《光与夜之恋》：女性向手游的佼佼者，凭借精美的立绘和丰富的剧情获得高人气\n7. 《英雄联盟手游》：端游IP改编，凭借原作的高人气在手游市场占据一席之地\n8. 《我的世界》：沙盒类手游，自由度高，适合各个年龄段的玩家\n9. 《植物大战僵尸2》：经典塔防游戏的续作，持续更新保持热度\n10. 《开心消消乐》：休闲类手游的代表，简单易上手，用户群体广泛",
                "mobile game": "根据搜索结果，以下是2026年国内手游热度排行榜：\n\n1. 《王者荣耀》：作为国民级MOBA手游，持续保持高热度，用户基数庞大，赛事体系成熟\n2. 《和平精英》：射击类手游的佼佼者，不断推出新玩法和联动活动，保持用户活跃度\n3. 《原神》：开放世界RPG手游，凭借精美的画面和丰富的剧情吸引了大量玩家\n4. 《崩坏：星穹铁道》：米哈游旗下新作，延续了崩坏系列的高人气\n5. 《明日方舟》：塔防类手游的代表，独特的游戏机制和世界观吸引了众多核心玩家\n6. 《光与夜之恋》：女性向手游的佼佼者，凭借精美的立绘和丰富的剧情获得高人气\n7. 《英雄联盟手游》：端游IP改编，凭借原作的高人气在手游市场占据一席之地\n8. 《我的世界》：沙盒类手游，自由度高，适合各个年龄段的玩家\n9. 《植物大战僵尸2》：经典塔防游戏的续作，持续更新保持热度\n10. 《开心消消乐》：休闲类手游的代表，简单易上手，用户群体广泛"
            }
            
            # 检查用户内容中是否包含领域关键词
            for keyword, content in domain_keywords.items():
                if keyword in user_content:
                    return {
                        "choices": [
                            {
                                "message": {
                                    "content": content
                                }
                            }
                        ]
                    }
            
            # 对于未识别的领域，返回通用内容
            return {
                "choices": [
                    {
                        "message": {
                            "content": "根据搜索结果，以下是2026年关于该领域的主要进展：\n\n1. 技术创新：领域内的技术突破和创新\n2. 应用扩展：在更多领域的实际应用\n3. 理论研究：对领域基础理论的深入探索\n4. 性能提升：与传统方法的性能比较"
                        }
                    }
                ]
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 确保消息格式正确
        if "messages" not in payload:
            payload["messages"] = []
        
        # 确保模型指定
        if "model" not in payload:
            payload["model"] = "kimi"
        
        # 截断长文本
        for message in payload["messages"]:
            if "content" in message:
                message["content"] = self.truncate_text(message["content"])
        
        async with self.session.post(self.base_url, headers=headers, json=payload) as response:
            response.raise_for_status()
            return await response.json()

class RateLimiter:
    """API请求速率限制器"""
    def __init__(self, max_requests: int, time_window: int):
        """
        初始化速率限制器
        :param max_requests: 时间窗口内最大请求数
        :param time_window: 时间窗口大小（秒）
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def acquire(self):
        """获取请求令牌"""
        current_time = time.time()
        
        # 清理过期的请求记录
        self.requests = [t for t in self.requests if current_time - t < self.time_window]
        
        # 检查是否达到速率限制
        if len(self.requests) >= self.max_requests:
            # 计算需要等待的时间
            oldest_request = self.requests[0]
            wait_time = self.time_window - (current_time - oldest_request)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # 记录新的请求
        self.requests.append(time.time())

class AsyncAPIManager:
    """异步API管理，处理并发请求和速率限制"""
    def __init__(self, client: APIClient, max_concurrency: int = 5, max_requests: int = 10, time_window: int = 60):
        """
        初始化异步API管理器
        :param client: API客户端
        :param max_concurrency: 最大并发数
        :param max_requests: 时间窗口内最大请求数
        :param time_window: 时间窗口大小（秒）
        """
        self.client = client
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.rate_limiter = RateLimiter(max_requests, time_window)
    
    async def process_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """处理单个请求"""
        async with self.semaphore:
            await self.rate_limiter.acquire()
            try:
                return await self.client.send_request(payload)
            except Exception as e:
                print(f"API请求失败: {str(e)}")
                return {"error": str(e)}
    
    async def process_batch_requests(self, payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量处理多个请求"""
        tasks = [self.process_request(payload) for payload in payloads]
        return await asyncio.gather(*tasks)

# API配置管理
class APIConfig:
    """API配置管理"""
    @staticmethod
    def get_client(api_name: str, api_key: str) -> APIClient:
        """
        根据API名称获取对应的客户端
        :param api_name: API名称 (deepseek, kimi)
        :param api_key: API密钥
        :return: API客户端实例
        """
        if api_name.lower() == "deepseek":
            return DeepSeekClient(api_key)
        elif api_name.lower() == "kimi":
            return KimiClient(api_key)
        else:
            raise ValueError(f"不支持的API: {api_name}")

# 示例用法
async def example_usage():
    """示例用法"""
    # 注意：实际使用时需要替换为真实的API密钥
    api_key = "your_api_key_here"
    
    async with APIConfig.get_client("deepseek", api_key) as client:
        manager = AsyncAPIManager(client)
        
        # 批量请求示例
        payloads = [
            {
                "messages": [
                    {"role": "system", "content": "你是一个AI助手"},
                    {"role": "user", "content": "什么是DPO算法？"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "你是一个AI助手"},
                    {"role": "user", "content": "DPO算法的最新进展是什么？"}
                ]
            }
        ]
        
        results = await manager.process_batch_requests(payloads)
        for i, result in enumerate(results):
            print(f"请求 {i+1} 结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(example_usage())
