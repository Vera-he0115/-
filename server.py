import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agentic_workflow import Agent
import uvicorn

# 创建FastAPI应用
app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求模型
class WorkflowRequest(BaseModel):
    user_input: str

# 定义响应模型
class WorkflowResponse(BaseModel):
    status: str
    message: str
    report_path: str = None
    logs: list = []

# 全局日志存储
logs = []

# 自定义日志函数
def custom_log(role, message):
    """
    自定义日志函数，同时输出到控制台和日志列表
    """
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{role}] {message}"
    print(log_message)
    logs.append({
        "timestamp": timestamp,
        "role": role,
        "message": message
    })

# 替换默认的log函数
import agentic_workflow
agentic_workflow.log = custom_log

# 创建智能体实例
agent = Agent(api_key="sk-ffcedad879664de9805ddaa89af44484")

@app.post("/run-workflow", response_model=WorkflowResponse)
async def run_workflow(request: WorkflowRequest):
    """
    运行智能体工作流
    """
    global logs
    logs = []  # 清空之前的日志
    
    try:
        # 运行智能体工作流
        result = await agent.run(request.user_input)
        
        # 提取报告路径
        report_path = None
        if "报告已生成：" in result:
            report_path = result.replace("报告已生成：", "")
        
        return WorkflowResponse(
            status="success",
            message="工作流执行完成",
            report_path=report_path,
            logs=logs
        )
    except Exception as e:
        return WorkflowResponse(
            status="error",
            message=f"工作流执行失败: {str(e)}",
            logs=logs
        )

@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)