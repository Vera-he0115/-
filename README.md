# Agentic Workflow 智能体工作流系统

一个基于大语言模型（LLM）的智能体工作流系统，能够根据用户输入的研究需求，自动进行文献搜索、信息提取、摘要生成，并最终生成结构化的研究报告。

## 功能特点

- **智能需求识别**：能够识别用户的具体研究领域需求，包括但不限于：
  - DPO算法研究进展
  - 人工智能领域进展
  - 金融行业舆情分析
  - 手游热度排行分析
  - 医疗、教育、环境、科技、经济等领域调研

- **工具调用能力**：通过Function Calling机制，赋予大模型"联网与行动"的能力
  - Arxiv论文搜索：连接真实的学术论文数据库
  - 网页内容抓取：获取论文详细信息
  - 报告生成工具：生成结构化Markdown报告

- **异步并发处理**：使用Asyncio实现多篇文献的并行处理，提高效率
  - 异步API请求
  - API限流处理
  - 长文本上下文截断

- **Chain-of-Thought日志**：在前端清晰展示智能体的思考链路
  - 规划步骤展示
  - API调用记录
  - 执行时间统计
  - 关键信息提取

- **可视化界面**：
  - 实时执行日志追踪
  - 报告内容展示
  - Chain-of-Thought可视化

## 项目结构

```
.
├── agentic_workflow.py          # 核心智能体工作流实现
├── api_client.py               # API客户端（DeepSeek/Kimi）
├── server.py                   # FastAPI后端服务
├── web_interface.html          # Web前端界面
├── run_agent.py                # 命令行运行脚本
├── requirements.txt            # 项目依赖
├── README.md                   # 项目说明文档
└── .gitignore                  # Git忽略文件
```

## 环境依赖

- Python 3.8+
- 主要依赖库：
  - `fastapi` - Web框架
  - `uvicorn` - ASGI服务器
  - `aiohttp` - 异步HTTP请求
  - `requests` - HTTP请求库
  - `beautifulsoup4` - 网页解析
  - `lxml` - XML/HTML解析

## 安装指南

### 1. 克隆项目

```bash
git clone <repository_url>
cd sy1-2
```

### 2. 创建虚拟环境（推荐）

```bash
# 使用conda
conda create -n agentic_workflow python=3.8
conda activate agentic_workflow

# 或使用venv
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置API密钥

本项目支持DeepSeek和Kimi两个大模型API。您需要在代码中设置相应的API密钥：

- **DeepSeek API**：访问 [DeepSeek开放平台](https://platform.deepseek.com/) 获取API密钥
- **Kimi API**：访问 [Moonshot开放平台](https://platform.moonshot.cn/) 获取API密钥

在 `agentic_workflow.py` 或 `api_client.py` 中修改API密钥配置：

```python
# DeepSeek配置
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"

# Kimi配置
KIMI_API_KEY = "your_kimi_api_key_here"
```

如果未配置API密钥，系统将使用模拟数据进行演示。

## 快速开始

### 启动后端服务

```bash
python server.py
```

服务启动后，访问 http://localhost:8000 查看服务状态。

### 启动前端界面

直接打开 `web_interface.html` 文件，或在浏览器中打开该文件。

### 使用方法

1. 在"研究需求"输入框中输入您的研究问题，例如：
   - "帮我分析国内手游的热度排行"
   - "调研人工智能领域的最新进展"
   - "分析金融行业的整体舆情"
   - "帮我调研生态环境领域的最新进展"
   - "帮我调研2026年关于DPO算法的最新进展"

2. 点击"启动工作流"按钮

3. 查看执行日志和生成的报告

### 使用命令行运行

```bash
python run_agent.py
```

## 工作流程

1. **需求分析**：分析用户输入，提取关键领域信息
2. **文献搜索**：调用Arxiv API搜索相关论文
3. **论文筛选**：分析搜索结果，选取最相关的论文
4. **内容获取**：抓取选定论文的详细信息
5. **智能分析**：使用大模型API分析论文内容（并发处理）
6. **报告生成**：整合所有信息，生成结构化报告

## Chain-of-Thought展示

系统在前端展示智能体的完整思考链路：

- 分析步骤
- 调用的API
- 执行时间
- 提取的关键信息

## 技术栈

- **大语言模型**：DeepSeek-V3, Kimi
- **Web框架**：FastAPI, Uvicorn
- **前端**：HTML5, CSS3, JavaScript
- **异步处理**：Asyncio, aiohttp
- **API协议**：OpenAI兼容API格式
- **论文数据库**：ArXiv API

## 注意事项

- 请确保网络连接正常，以便访问Arxiv API和外部工具
- 如遇到API限流，请稍后重试
- 报告内容取决于搜索到的论文质量
- 建议使用真实的API密钥以获得更准确的分析结果
- 启动前端前请确保后端服务正在运行

## 许可证

MIT License

## 作者

Agentic Workflow Team

## 联系方式

如有问题或建议，请通过GitHub Issues提交。
