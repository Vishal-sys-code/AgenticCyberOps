import subprocess

NMAP_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"
GOBUSTER_PATH = r"C:\Users\YourUsername\gobuster\gobuster.exe"

def run_nmap(target):
    try:
        result = subprocess.check_output([NMAP_PATH, "-Pn", target], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"nmap error: {e.output}"
    except FileNotFoundError:
        return "nmap command not found!"

def run_gobuster(target):
    try:
        result = subprocess.check_output([GOBUSTER_PATH, "dir", "-u", f"http://{target}", "-w", "wordlist.txt"], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"gobuster error: {e.output}"
    except FileNotFoundError:
        return "gobuster command not found!"