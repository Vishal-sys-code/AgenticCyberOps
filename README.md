# AgenticCyberOps

AgenticCyberOps is an autonomous cybersecurity pipeline built using LangGraph and LangChain. It is designed as an intelligent agent that decomposes high-level security tasks, enforces target scope constraints, executes security scans using tools like nmap and gobuster, and generates a comprehensive security audit report with detailed logs.

---

## System Architecture

The system is composed of several key components:

- **CyberSecurityState Model:**  
  A Pydantic model that defines the internal state of the agent. It includes:
  - **task:** The high-level security task (e.g., "Scan example.com for open ports and directories").
  - **task_list:** A list of decomposed tasks (e.g., "nmap scan on example.com", "gobuster scan on example.com directories").
  - **results:** The outputs from executing the scan commands.
  - **allowed_scope:** The domains or IP ranges within which the agent is authorized to scan.
  - **logs:** A detailed log of each step in the pipeline.
  - **final_report:** A consolidated security audit report generated from the scan results and logs.

- **LangGraph Workflow:**  
  A state graph that integrates multiple nodes, each responsible for a specific function:
  - **Task Decomposition:** Breaks down a high-level task into actionable scanning tasks.
  - **Scope Constraints:** Filters tasks based on an allowed scope to prevent unauthorized scans.
  - **Task Execution & Retry Logic:** Executes the scan commands using external tools (nmap, gobuster) with built-in retry mechanisms.
  - **Logging & Reporting:** Aggregates scan results and logs, producing a final audit report.

- **Integration with External Tools and APIs:**  
  The agent utilizes external security tools and Google’s Gemini API for natural language processing. The API key is securely loaded from a `.env` file.

- **Flowchart or Architecture**
![Flowchart_of_AgenticCyberOps](https://github.com/Vishal-sys-code/AgenticCyberOps/blob/main/Flowchart.jpg)

---

## Agent Roles and Responsibilities

The agent in AgenticCyberOps performs the following roles:

- **Task Analyzer:**  
  Receives a high-level security instruction and decomposes it into a list of actionable tasks.

- **Scope Enforcer:**  
  Ensures that all scanning tasks are executed only on targets that fall within the allowed scope. This is crucial to prevent unauthorized scanning.

- **Scanner:**  
  Executes security scans using tools such as nmap and gobuster. It includes retry logic to handle transient failures or errors during execution.

- **Logger and Reporter:**  
  Records detailed logs for each step of the process and generates a comprehensive final report that includes both the scan outputs and execution logs.

---

## Scope Enforcement Strategy

The **allowed_scope** is defined in the `CyberSecurityState` model through the `allowed_scope` field. By default, the scope is set to:

- `example.com`
- `192.168.1.0/24`

This means the agent will only execute scanning tasks on targets that contain these strings. Any tasks referencing targets outside of this allowed scope are skipped or flagged, ensuring that the agent operates only within authorized boundaries.

---

## Steps to Replicate and Run the Project

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **nmap** and **gobuster** installed and added to your system’s PATH
- [Optional] Virtual environment (e.g., `venv`)

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/AgenticCyberOps.git
cd AgenticCyberOps
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
Ensure that requirements.txt includes the following packages:
- `python-dotenv`
- `google-generativeai`
- `langgraph`
- `pydantic`
- `streamlit`

### 4. Configure Environment Variables
Create a `.env` file in the root of the project with the following content:
```
GOOGLE_API_KEY='your_own_api_key'
```
**Important:** 
Make sure to add `.env` to your `.gitignore` to keep your API key private.

### 5. Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

- The Streamlit dashboard will open in your browser.
- Use the sidebar to enter your target (e.g., `example.com`) and click Run Security Scan.
- The final security audit report and detailed execution logs will be displayed.

### 6. Testing with Different Domains
- You can test the pipeline with different targets (within the allowed scope). For example, change the target to `google.com` if you update the allowed scope accordingly.
- The pipeline will generate a security audit report based on the scan outputs and execution logs.

**Additional Notes**
- **Error Handling:** The pipeline includes retry logic. If a scan command fails, it will automatically retry using alternate parameters.
- **Customization:** You can modify the allowed scope, add more scanning tools, or extend the workflow with additional nodes as needed.
- **Permissions:** Ensure you have explicit permission to scan any target. Unauthorized scanning may have legal consequences.
- 

## **Screenshots**
### **Running on `example.com`**
![first_screenshot](https://github.com/Vishal-sys-code/AgenticCyberOps/blob/main/Images/example-1-ss.png)
![second_screenshot](https://github.com/Vishal-sys-code/AgenticCyberOps/blob/main/Images/example-2-ss.png)
![third_screenshot](https://github.com/Vishal-sys-code/AgenticCyberOps/blob/main/Images/example-3-ss.png)
