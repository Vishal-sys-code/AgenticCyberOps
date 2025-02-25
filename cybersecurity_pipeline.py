# cybersecurity_pipeline.py

import os
from dotenv import load_dotenv
import subprocess
import shlex
from pydantic import BaseModel
from typing import List
import langgraph
from langgraph.graph import StateGraph
import google.generativeai as genai

# -----------------------------------------------------------------------------
# Step 1: Setup Environment & API Configuration
# -----------------------------------------------------------------------------
# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables.")

# Configure Gemini with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------------------------------------------------------------
# Step 2: Define Core Architecture (State Model & LangGraph Workflow)
# -----------------------------------------------------------------------------
class CyberSecurityState(BaseModel):
    task: str
    task_list: List[str] = []
    results: List[str] = []
    allowed_scope: List[str] = ["example.com", "192.168.1.0/24"]
    logs: List[str] = []
    final_report: str = ""  # Field for the final report

# -----------------------------------------------------------------------------
# Step 4: Helper Function for Task Execution & Retry Logic
# -----------------------------------------------------------------------------
def execute_command_with_retry(cmd: str, alternate_cmd: str = None, max_retries: int = 2) -> str:
    attempt = 0
    while attempt < max_retries:
        try:
            output = subprocess.check_output(
                shlex.split(cmd),
                stderr=subprocess.STDOUT,
                timeout=60,
                universal_newlines=True
            )
            return output
        except Exception as e:
            attempt += 1
            if attempt >= max_retries:
                if alternate_cmd:
                    try:
                        output = subprocess.check_output(
                            shlex.split(alternate_cmd),
                            stderr=subprocess.STDOUT,
                            timeout=60,
                            universal_newlines=True
                        )
                        return output
                    except Exception as e2:
                        return f"Command failed after retries: {str(e2)}"
                else:
                    return f"Command failed after retries: {str(e)}"
            if alternate_cmd:
                cmd = alternate_cmd
    return "Unknown error"

# -----------------------------------------------------------------------------
# Step 3: Implement the Agent Workflow
# -----------------------------------------------------------------------------
# 3.1 Build Task Decomposition
def task_decomposition(state: dict) -> dict:
    state_obj = CyberSecurityState.model_validate(state)
    # For simplicity, extract target from the task description (assumes target is the second word)
    target = state_obj.task.split()[1]
    state_obj.task_list = [
        f"nmap scan on {target}",
        f"gobuster scan on {target} directories"
    ]
    state_obj.logs.append(f"[Task Decomposition] Decomposed task into: {state_obj.task_list}")
    return state_obj.model_dump()

# 3.3 Implement Scope Constraints
def apply_scope_constraints(state: dict) -> dict:
    state_obj = CyberSecurityState.model_validate(state)
    filtered_tasks = []
    for task in state_obj.task_list:
        if any(scope in task for scope in state_obj.allowed_scope):
            filtered_tasks.append(task)
        else:
            filtered_tasks.append(f"Task '{task}' skipped (outside allowed scope)")
    state_obj.task_list = filtered_tasks
    state_obj.logs.append(f"[Scope Constraints] Filtered tasks: {state_obj.task_list}")
    return state_obj.model_dump()

# Step 4 (continued): Execute Tasks with Retry Logic
def execute_tasks_with_retry(state: dict) -> dict:
    state_obj = CyberSecurityState.model_validate(state)
    results = []
    target = state_obj.task.split()[1]
    for task in state_obj.task_list:
        if "nmap" in task:
            primary_cmd = f"nmap -p- {target}"
            alternate_cmd = f"nmap -sV {target}"
            output = execute_command_with_retry(primary_cmd, alternate_cmd, max_retries=2)
            results.append(f"nmap result for {target}:\n{output}")
            state_obj.logs.append(f"[Execute Tasks] nmap scan executed for {target}")
        elif "gobuster" in task:
            primary_cmd = f"gobuster dir -u https://{target} -w wordlist.txt"
            alternate_cmd = f"gobuster dir -u http://{target} -w wordlist.txt"
            output = execute_command_with_retry(primary_cmd, alternate_cmd, max_retries=2)
            results.append(f"gobuster result for {target}:\n{output}")
            state_obj.logs.append(f"[Execute Tasks] gobuster scan executed for {target}")
        else:
            results.append(f"Unknown task: {task}")
            state_obj.logs.append(f"[Execute Tasks] Unknown task encountered: {task}")
    state_obj.results = results
    return state_obj.model_dump()

# Step 5: Implement Logging & Reporting
def generate_report(state: dict) -> dict:
    state_obj = CyberSecurityState.model_validate(state)
    report_lines = ["=== Security Audit Report ==="]
    report_lines.extend(state_obj.results)
    report_lines.append("\n=== Execution Logs ===")
    report_lines.extend(state_obj.logs)
    final_report = "\n".join(report_lines)
    state_obj.logs.append("[Generate Report] Final report generated.")
    state_obj.final_report = final_report
    return state_obj.model_dump()

# -----------------------------------------------------------------------------
# Build the LangGraph Workflow (Integrating Steps 2–5)
# -----------------------------------------------------------------------------
workflow = StateGraph(CyberSecurityState)
workflow.add_node("Task Decomposition", task_decomposition)
workflow.add_node("Apply Scope Constraints", apply_scope_constraints)
workflow.add_node("Execute Tasks with Retry", execute_tasks_with_retry)
workflow.add_node("Generate Report", generate_report)
workflow.set_entry_point("Task Decomposition")
workflow.add_edge("Task Decomposition", "Apply Scope Constraints")
workflow.add_edge("Apply Scope Constraints", "Execute Tasks with Retry")
workflow.add_edge("Execute Tasks with Retry", "Generate Report")
agent = workflow.compile()

# -----------------------------------------------------------------------------
# Public Function to Run the Security Pipeline
# -----------------------------------------------------------------------------
def run_security_pipeline(task_description: str) -> dict:
    """
    Initializes the state with the provided high-level task, runs the workflow,
    and returns the final state (including the final report and logs).
    """
    initial_state = CyberSecurityState(task=task_description)
    final_state = agent.invoke(initial_state.model_dump())
    return final_state