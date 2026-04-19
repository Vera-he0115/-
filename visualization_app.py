import gradio as gr
import asyncio
import time
import json
from datetime import datetime
from agentic_workflow import Agent, set_log_manager

class LogManager:
    """日志管理器，用于收集和管理执行日志"""
    def __init__(self):
        self.logs = []
        self.running = False
    
    def add_log(self, step, message, duration=None, api_call=None, key_info=None):
        """
        添加日志
        :param step: 步骤名称
        :param message: 消息内容
        :param duration: 耗时（秒）
        :param api_call: API调用信息
        :param key_info: 关键信息
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "message": message,
            "duration": duration,
            "api_call": api_call,
            "key_info": key_info
        }
        self.logs.append(log_entry)
        return log_entry
    
    def get_logs(self):
        """获取所有日志"""
        return self.logs
    
    def clear_logs(self):
        """清空日志"""
        self.logs = []
    
    def set_running(self, running):
        """设置运行状态"""
        self.running = running
    
    def is_running(self):
        """获取运行状态"""
        return self.running

# 创建全局日志管理器
log_manager = LogManager()

# 设置日志管理器到agentic_workflow
set_log_manager(log_manager)

# 重定向print函数，将输出同时添加到日志
original_print = print
def log_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = " ".join(str(arg) for arg in args)
    log_manager.add_log("系统", message)

# 替换print函数
print = log_print

def run_agent_workflow(user_input):
    """
    运行智能体工作流
    :param user_input: 用户输入
    :return: 最终结果
    """
    log_manager.clear_logs()
    log_manager.set_running(True)
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 创建事件循环并运行异步任务
        async def main():
            # 创建Agent实例
            agent = Agent()
            # 运行工作流
            result = await agent.run(user_input)
            return result
        
        # 运行异步任务
        result = asyncio.run(main())
        
        # 记录总耗时
        total_duration = time.time() - start_time
        log_manager.add_log("完成", f"工作流执行完成，总耗时: {total_duration:.2f}秒")
        
        return result
    except Exception as e:
        error_msg = f"执行失败: {str(e)}"
        log_manager.add_log("错误", error_msg)
        return error_msg
    finally:
        log_manager.set_running(False)

def format_logs(logs):
    """
    格式化日志为HTML
    :param logs: 日志列表
    :return: 格式化后的HTML
    """
    if not logs:
        return "<p>暂无执行日志</p>"
    
    html = "<div style='max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 5px;'>"
    
    for log in logs:
        timestamp = log.get("timestamp", "")
        step = log.get("step", "")
        message = log.get("message", "")
        duration = log.get("duration", "")
        api_call = log.get("api_call", "")
        key_info = log.get("key_info", "")
        
        # 格式化时间
        time_str = timestamp.split("T")[1].split(".")[0] if timestamp else ""
        
        # 构建日志条目
        html += f"<div style='margin-bottom: 10px; padding: 8px; background-color: #f9f9f9; border-radius: 4px;'>"
        html += f"<div style='font-size: 12px; color: #666;'>{time_str} - {step}</div>"
        html += f"<div style='margin-top: 4px;'>{message}</div>"
        
        if duration:
            html += f"<div style='font-size: 12px; color: #888; margin-top: 2px;'>耗时: {duration:.2f}秒</div>"
        
        if api_call:
            html += f"<div style='font-size: 12px; color: #0066cc; margin-top: 2px;'>API调用: {api_call}</div>"
        
        if key_info:
            html += f"<div style='font-size: 12px; color: #009933; margin-top: 2px;'>关键信息: {key_info}</div>"
        
        html += "</div>"
    
    html += "</div>"
    return html

def get_latest_logs():
    """
    获取最新的日志
    :return: 格式化后的日志HTML
    """
    logs = log_manager.get_logs()
    return format_logs(logs)

def start_workflow(user_input):
    """
    启动工作流
    :param user_input: 用户输入
    :return: 初始状态
    """
    try:
        # 直接调用run_agent_workflow函数
        result = run_agent_workflow(user_input)
        return result, get_latest_logs()
    except Exception as e:
        error_msg = f"启动失败: {str(e)}"
        log_manager.add_log("错误", error_msg)
        return error_msg, get_latest_logs()

def update_logs():
    """
    更新日志显示
    :return: 最新的日志HTML
    """
    return get_latest_logs()

# 创建Gradio界面
def create_interface():
    with gr.Blocks(title="智能体工作流可视化") as app:
        gr.Markdown("# 智能体工作流可视化与执行日志追踪")
        
        with gr.Row():
            with gr.Column(scale=1):
                user_input = gr.Textbox(
                    label="研究需求",
                    placeholder="请输入您的研究需求，例如：帮我调研2026年关于DPO算法的最新进展",
                    lines=3
                )
                start_button = gr.Button("启动工作流", variant="primary")
                status = gr.Textbox(label="状态", value="就绪", interactive=False)
            
            with gr.Column(scale=2):
                logs_output = gr.HTML(label="执行日志与思考链路")
                
        # 添加按钮用于手动更新日志
        update_button = gr.Button("更新日志")
        update_button.click(fn=update_logs, inputs=[], outputs=[logs_output])
        
        # 启动工作流
        start_button.click(
            fn=start_workflow,
            inputs=[user_input],
            outputs=[status, logs_output]
        )
        
        # 初始加载
        app.load(fn=get_latest_logs, inputs=[], outputs=[logs_output])
    
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(debug=True, share=False)
