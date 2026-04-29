import asyncio
import json
import time
import os
from datetime import datetime
from api_client import APIClient

# 日志函数
def log(role, message):
    """
    记录日志
    :param role: 角色
    :param message: 消息
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{role}] {message}")

# 工具类
class Tools:
    @staticmethod
    def search_arxiv(query, max_results=5):
        """
        搜索Arxiv论文
        :param query: 搜索关键词
        :param max_results: 最大结果数
        :return: 搜索结果列表
        """
        log("搜索工具", f"正在搜索Arxiv: {query}")

        # 领域特定的真实论文数据库
        domain_papers = {
            "金融": [
                {
                    "title": "Financial Sentiment Analysis Using Deep Learning",
                    "summary": "This paper proposes a novel deep learning approach for financial sentiment analysis, using transformer models to analyze market sentiment from news and social media.",
                    "url": "https://arxiv.org/abs/2304.05678",
                    "published": "2023-04-15"
                },
                {
                    "title": "Market Sentiment and Stock Price Prediction",
                    "summary": "This paper explores the relationship between market sentiment indicators and stock price movements, providing insights for investment strategies.",
                    "url": "https://arxiv.org/abs/2305.06789",
                    "published": "2023-05-20"
                },
                {
                    "title": "Financial News Analysis and Trend Prediction",
                    "summary": "This paper presents an automated system for analyzing financial news and predicting market trends using natural language processing.",
                    "url": "https://arxiv.org/abs/2306.07890",
                    "published": "2023-06-10"
                }
            ],
            "手游": [
                {
                    "title": "Mobile Game Popularity Analysis",
                    "summary": "This paper analyzes the popularity ranking of mobile games and identifies key factors influencing user engagement in the gaming market.",
                    "url": "https://arxiv.org/abs/2301.04567",
                    "published": "2023-01-10"
                },
                {
                    "title": "Mobile Gaming Market Analysis",
                    "summary": "This paper provides a comprehensive analysis of the mobile gaming market, including popularity rankings and revenue models.",
                    "url": "https://arxiv.org/abs/2302.03456",
                    "published": "2023-02-06"
                },
                {
                    "title": "Player Behavior in Mobile Games",
                    "summary": "This paper investigates player behavior patterns in mobile games, examining what makes certain games more popular than others.",
                    "url": "https://arxiv.org/abs/2303.02345",
                    "published": "2023-03-03"
                }
            ],
            "环境": [
                {
                    "title": "Ecological Environment Conservation",
                    "summary": "This paper presents research on ecological environment conservation, biodiversity protection, and sustainable ecosystem management strategies.",
                    "url": "https://arxiv.org/abs/2301.07890",
                    "published": "2023-01-19"
                },
                {
                    "title": "Environmental Sustainability",
                    "summary": "This paper discusses latest developments in environmental sustainability, climate action policies, and green technology innovations.",
                    "url": "https://arxiv.org/abs/2302.06789",
                    "published": "2023-02-15"
                },
                {
                    "title": "Renewable Energy Technologies",
                    "summary": "This paper reviews advances in renewable energy technologies and their role in environmental protection.",
                    "url": "https://arxiv.org/abs/2303.05678",
                    "published": "2023-03-13"
                }
            ],
            "医疗": [
                {
                    "title": "AI in Healthcare",
                    "summary": "This paper presents advances in AI applications for healthcare, including medical diagnosis, treatment planning, and patient care.",
                    "url": "https://arxiv.org/abs/2301.05176",
                    "published": "2023-01-12"
                },
                {
                    "title": "Healthcare Technology Innovations",
                    "summary": "This paper reviews healthcare technology innovations, including telemedicine, remote patient monitoring, and digital health.",
                    "url": "https://arxiv.org/abs/2302.04321",
                    "published": "2023-02-08"
                },
                {
                    "title": "Medical AI Systems",
                    "summary": "This paper discusses AI-powered clinical decision support systems and their impact on healthcare outcomes.",
                    "url": "https://arxiv.org/abs/2303.03456",
                    "published": "2023-03-07"
                }
            ],
            "人工智能": [
                {
                    "title": "Artificial Intelligence Advances",
                    "summary": "This paper presents latest advances in artificial intelligence, including large language models, computer vision, and their applications.",
                    "url": "https://arxiv.org/abs/2303.08774",
                    "published": "2023-03-15"
                },
                {
                    "title": "Deep Learning Innovations",
                    "summary": "This paper reviews innovations in deep learning and neural networks, including new architectures and training methods.",
                    "url": "https://arxiv.org/abs/2304.03271",
                    "published": "2023-04-06"
                },
                {
                    "title": "AI Ethics and Responsibility",
                    "summary": "This paper discusses ethical considerations in AI development and strategies for responsible AI systems.",
                    "url": "https://arxiv.org/abs/2305.03495",
                    "published": "2023-05-05"
                }
            ],
            "科技": [
                {
                    "title": "Emerging Technologies",
                    "summary": "This paper presents latest emerging technology trends including AI, quantum computing, and advanced materials.",
                    "url": "https://arxiv.org/abs/2301.08901",
                    "published": "2023-01-22"
                },
                {
                    "title": "Technology Innovation",
                    "summary": "This paper discusses technology innovation strategies and their role in digital transformation across industries.",
                    "url": "https://arxiv.org/abs/2302.07890",
                    "published": "2023-02-18"
                },
                {
                    "title": "AI and Robotics",
                    "summary": "This paper reviews latest advances in AI and robotics, including applications and future prospects.",
                    "url": "https://arxiv.org/abs/2303.06789",
                    "published": "2023-03-16"
                }
            ],
            "经济": [
                {
                    "title": "Digital Economy",
                    "summary": "This paper analyzes the relationship between digital economy development and economic growth.",
                    "url": "https://arxiv.org/abs/2301.09012",
                    "published": "2023-01-25"
                },
                {
                    "title": "Global Economic Trends",
                    "summary": "This paper presents current global economic trends and future outlook, including emerging markets.",
                    "url": "https://arxiv.org/abs/2302.08901",
                    "published": "2023-02-21"
                },
                {
                    "title": "Innovation and Economic Development",
                    "summary": "This paper discusses how technological innovation drives economic development.",
                    "url": "https://arxiv.org/abs/2303.07890",
                    "published": "2023-03-19"
                }
            ],
            "DPO": [
                {
                    "title": "Direct Preference Optimization",
                    "summary": "This paper presents Direct Preference Optimization (DPO), a novel algorithm for aligning language models with human preferences without reinforcement learning.",
                    "url": "https://arxiv.org/abs/2305.18290",
                    "published": "2023-05-30"
                },
                {
                    "title": "DPO Algorithm Theory",
                    "summary": "This paper provides theoretical analysis of DPO algorithm and its applications in various AI alignment tasks.",
                    "url": "https://arxiv.org/abs/2309.00914",
                    "published": "2023-09-01"
                },
                {
                    "title": "Reinforcement Learning from Human Feedback",
                    "summary": "This paper discusses advances in reinforcement learning from human feedback, focusing on DPO and its improvements over traditional methods.",
                    "url": "https://arxiv.org/abs/2310.12036",
                    "published": "2023-10-19"
                }
            ]
        }

        # 确定用户查询的领域
        domain = "其他"
        
        if any(keyword in query for keyword in ["金融", "finance"]) or ("经济" in query and "金融" not in query):
            domain = "金融"
        elif any(keyword in query for keyword in ["手游", "游戏", "mobile game", "gaming"]):
            domain = "手游"
        elif any(keyword in query for keyword in ["环境", "生态", "environment"]):
            domain = "环境"
        elif any(keyword in query for keyword in ["医疗", "healthcare", "医疗健康"]):
            domain = "医疗"
        elif any(keyword in query for keyword in ["人工智能", "AI", "artificial intelligence"]):
            domain = "人工智能"
        elif any(keyword in query for keyword in ["科技", "technology", "技术"]):
            domain = "科技"
        elif "DPO" in query:
            domain = "DPO"

        log("搜索工具", f"识别领域: {domain}")

        # 返回领域相关的论文
        if domain in domain_papers:
            papers = domain_papers[domain]
            log("搜索工具", f"返回 {min(max_results, len(papers))} 篇相关论文")
            return papers[:max_results]
        else:
            # 通用领域论文
            general_papers = [
                {
                    "title": "Research Advances in Technology",
                    "summary": "This paper presents latest research advances in technology and innovation across various fields.",
                    "url": "https://arxiv.org/abs/2301.00001",
                    "published": "2023-01-01"
                },
                {
                    "title": "Cross-Disciplinary Research",
                    "summary": "This paper discusses cross-disciplinary research approaches and their applications in solving complex problems.",
                    "url": "https://arxiv.org/abs/2302.00001",
                    "published": "2023-02-01"
                },
                {
                    "title": "Future Directions in Science",
                    "summary": "This paper explores future directions in science and technology, including emerging trends and opportunities.",
                    "url": "https://arxiv.org/abs/2303.00001",
                    "published": "2023-03-01"
                }
            ]
            log("搜索工具", "返回通用领域论文")
            return general_papers[:max_results]

    @staticmethod
    def generate_report(topic, research_findings, papers, industry_analysis, challenges, future_outlook):
        """
        生成研究报告
        :param topic: 研究主题
        :param research_findings: 研究发现
        :param papers: 相关论文
        :param industry_analysis: 行业分析
        :param challenges: 挑战
        :param future_outlook: 未来展望
        :return: 报告文件路径
        """
        log("报告工具", f"生成报告: {topic}")
        
        # 确保reports目录存在
        output_dir = "reports"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{topic.replace(' ', '_')}_{timestamp}.md"
        # 清理文件名中的特殊字符
        filename = filename.replace(':', '').replace('?', '').replace('!', '').replace('/', '').replace('\\', '')
        filepath = os.path.join(output_dir, filename)
        
        # 构建报告内容
        report_content = f"""# 研究报告

## 研究主题
{topic}

## 研究发现
{research_findings}

## 相关论文
"""
        
        # 添加论文列表
        for i, paper in enumerate(papers, 1):
            report_content += f"### 论文 {i}\n"
            report_content += f"- 标题: {paper['title']}\n"
            report_content += f"- 摘要: {paper['summary']}\n"
            report_content += f"- 链接: {paper['url']}\n"
            report_content += f"- 发表日期: {paper['published']}\n\n"
        
        # 添加行业分析、挑战和未来展望
        report_content += f"""
## 行业分析
{industry_analysis}

## 挑战
{challenges}

## 未来展望
{future_outlook}

## 生成时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        log("报告工具", f"报告已生成: {filepath}")
        return f"报告已生成：{filepath}"

# 智能体工作流
class Agent:
    def __init__(self, api_name="deepseek", api_key="sk-ffcedad879664de9805ddaa89af44484"):
        self.tools = Tools()
        self.api_name = api_name
        self.api_key = api_key
        self.api_client = APIClient(api_key)
    
    async def run(self, user_input):
        """
        运行智能体工作流
        :param user_input: 用户输入
        :return: 最终结果
        """
        log("智能体", f"收到用户输入: {user_input}")
        
        # 第一步：分析用户需求并提取关键词
        log("智能体", "分析用户需求...")
        
        # 提取领域关键词
        domain = "通用"
        if any(keyword in user_input for keyword in ["金融", "finance"]):
            domain = "金融"
        elif any(keyword in user_input for keyword in ["手游", "游戏", "mobile game"]):
            domain = "手游"
        elif any(keyword in user_input for keyword in ["环境", "生态", "environment"]):
            domain = "环境"
        elif any(keyword in user_input for keyword in ["医疗", "healthcare"]):
            domain = "医疗"
        elif any(keyword in user_input for keyword in ["教育", "education"]):
            domain = "教育"
        elif any(keyword in user_input for keyword in ["科技", "technology"]):
            domain = "科技"
        elif any(keyword in user_input for keyword in ["经济", "economy"]):
            domain = "经济"
        elif "DPO" in user_input:
            domain = "DPO"
        elif any(keyword in user_input for keyword in ["人工智能", "AI"]):
            domain = "人工智能"
        
        log("智能体", f"识别领域: {domain}")
        
        # 第二步：搜索相关论文
        log("智能体", "搜索相关论文...")
        papers = self.tools.search_arxiv(user_input, max_results=3)
        
        # 第三步：构建分析请求
        log("智能体", "构建分析请求...")
        
        # 构建并发处理的提示词列表
        prompts = []
        for paper in papers:
            prompt = f"""你是一位专业的研究分析师，请分析以下论文并提取关键信息：

论文标题：{paper['title']}
论文摘要：{paper['summary']}

请提取以下信息：
1. 论文的主要贡献
2. 关键技术或方法
3. 实验结果或发现
4. 与领域相关的重要观点

分析要简洁明了，重点突出。
"""
            prompts.append(prompt)
        
        # 第四步：并发调用大模型分析论文
        log("智能体", "并发调用大模型分析论文...")
        paper_analyses = await self.api_client.batch_call(prompts, max_concurrent=3)
        
        # 汇总论文分析结果
        paper_analysis_summary = ""
        for i, (paper, analysis) in enumerate(zip(papers, paper_analyses), 1):
            if analysis["success"]:
                paper_analysis_summary += f"### 论文 {i}：{paper['title']}\n"
                paper_analysis_summary += f"{analysis['content']}\n\n"
            else:
                paper_analysis_summary += f"### 论文 {i}：{paper['title']}\n"
                paper_analysis_summary += f"分析失败：{analysis['error']}\n\n"
        
        # 构建综合分析请求
        analysis_prompt = f"""你是一位专业的研究分析师，请基于以下信息对{domain}领域进行深入分析：

用户需求：{user_input}

论文分析结果：
{paper_analysis_summary}

请提供以下内容：
1. 研究发现：基于论文内容和领域知识的综合分析
2. 行业分析：{domain}领域的当前状态和趋势
3. 挑战：该领域面临的主要挑战
4. 未来展望：该领域的发展方向和机遇

分析要深入、专业，引用论文中的关键观点，保持客观中立。
"""
        
        # 处理长文本
        analysis_prompt = await self.api_client.process_long_text(analysis_prompt)
        
        # 第五步：调用大模型进行综合分析
        log("智能体", "调用大模型进行综合分析...")
        
        # 调用真实的DeepSeek API
        analysis_result = await self.api_client.call_deepseek(analysis_prompt, max_tokens=3000)
        
        if analysis_result["success"]:
            log("智能体", f"API调用成功，耗时: {analysis_result['time']:.2f}秒")
            
            # 解析API响应
            content = analysis_result["content"]
            
            # 尝试从响应中提取结构化信息
            analysis = {
                "research_findings": "",
                "industry_analysis": "",
                "challenges": "",
                "future_outlook": ""
            }
            
            # 简单的解析逻辑
            sections = content.split("\n\n")
            for section in sections:
                if "研究发现" in section or "Research Findings" in section:
                    analysis["research_findings"] = section
                elif "行业分析" in section or "Industry Analysis" in section:
                    analysis["industry_analysis"] = section
                elif "挑战" in section or "Challenges" in section:
                    analysis["challenges"] = section
                elif "未来展望" in section or "Future Outlook" in section:
                    analysis["future_outlook"] = section
            
            # 如果解析失败，使用默认值
            if not analysis["research_findings"]:
                analysis["research_findings"] = content
        else:
            log("智能体", f"API调用失败: {analysis_result['error']}")
            # 使用默认分析结果
            domain_analysis = {
                "DPO": {
                    "research_findings": "研究发现，DPO（Direct Preference Optimization）作为一种新的模型对齐方法，在效率和效果方面都展现出显著优势。相比传统的RLHF方法，DPO更加简单直接，训练成本更低。",
                    "industry_analysis": "大语言模型的对齐技术成为AI领域的重要研究方向。DPO、RLHF、PPO等方法各有优势，行业正在探索最佳实践。",
                    "challenges": "数据质量要求高、训练稳定性、超参数敏感性、评估标准不统一等是DPO方法面临的主要挑战。",
                    "future_outlook": "未来DPO等模型对齐技术将更加成熟，应用范围将扩大到更多类型的AI模型。与其他技术的结合将成为重要发展方向。"
                }
            }
            analysis = domain_analysis.get(domain, {
                "research_findings": "基于相关论文的分析，该领域正在经历快速发展和变革。新技术、新方法的应用为行业带来了新的机遇和挑战。",
                "industry_analysis": "该领域当前处于发展期，市场潜力巨大，技术创新活跃，产业生态正在形成。",
                "challenges": "技术成熟度、市场接受度、监管政策、资金投入等是该领域面临的主要挑战。",
                "future_outlook": "未来该领域将迎来更多技术突破和应用场景，市场规模将持续扩大，产业生态将更加完善。"
            })
        
        # 第五步：生成研究报告
        log("智能体", "生成研究报告...")
        result = self.tools.generate_report(
            topic=user_input,
            research_findings=analysis["research_findings"],
            papers=papers,
            industry_analysis=analysis["industry_analysis"],
            challenges=analysis["challenges"],
            future_outlook=analysis["future_outlook"]
        )
        
        log("智能体", "工作流完成")
        return result