#!/usr/bin/env python3
import subprocess
import sys
import time
import os
import socket

def free_port(port):
    """Check if a port is in use and terminate the occupying process on Mac/Linux."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            is_open = (s.connect_ex(('127.0.0.1', port)) == 0)
        
        if is_open:
            my_pid = os.getpid()
            print(f"🧹 Clearing existing process using port {port}...")
            res = subprocess.run(f"lsof -ti:{port} -sTCP:LISTEN", shell=True, capture_output=True, text=True)
            pids = [p.strip() for p in res.stdout.splitlines() if p.strip()]
            for pid in pids:
                if pid.isdigit() and int(pid) != my_pid:
                    subprocess.run(f"kill -9 {pid} 2>/dev/null", shell=True)
            time.sleep(1)
    except Exception:
        pass

def get_python_bin():
    """Detect virtualenv Python if available, else sys.executable."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(project_dir, "myvenv", "bin", "python")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

def run_project():
    python_bin = get_python_bin()

    print("==================================================")
    print("🚀 Starting Insurance Predictor Services...")
    print("==================================================")

    # Automatically free ports 8000 and 8501 if previously in use
    free_port(8000)
    free_port(8501)

    # 1. Start FastAPI backend
    print("⚡ [1/2] Starting FastAPI Backend on http://localhost:8000 (Docs: http://localhost:8000/docs)...")
    backend_proc = subprocess.Popen([
        python_bin, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"
    ])

    # Short delay to allow FastAPI to start
    time.sleep(2)

    # 2. Start Streamlit frontend
    print("🎨 [2/2] Starting Streamlit Frontend on http://localhost:8501...")
    frontend_proc = subprocess.Popen([
        python_bin, "-m", "streamlit", "run", "frontend.py", "--server.port", "8501"
    ])

    print("==================================================")
    print("✅ Both Frontend and Backend are running!")
    print("   👉 Streamlit Frontend: http://localhost:8501")
    print("   👉 FastAPI Backend:   http://localhost:8000")
    print("   👉 Swagger API Docs:  http://localhost:8000/docs")
    print("Press Ctrl+C to stop both servers.")
    print("==================================================")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait()
        frontend_proc.wait()
        print("👋 Project stopped successfully.")

if __name__ == "__main__":
    run_project()


