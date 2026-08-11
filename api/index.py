import sys
import os
import logging

logger = logging.getLogger("insure_ai.vercel")

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app import app
except Exception as ex:
    from fastapi import FastAPI
    app = FastAPI(title="Insure AI Error Handler")
    @app.api_route("/{path:path}", methods=["GET", "POST"])
    def error_fallback(path: str):
        return {"error": "Init Failed", "detail": str(ex)}

@app.get("/debug-fs")
def debug_filesystem():
    api_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(api_dir)
    return {
        "cwd": os.getcwd(),
        "api_dir": api_dir,
        "project_root": project_root,
        "cwd_files": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else [],
        "api_dir_files": os.listdir(api_dir) if os.path.exists(api_dir) else [],
        "project_root_files": os.listdir(project_root) if os.path.exists(project_root) else [],
        "sys_path": sys.path
    }

handler = app
__all__ = ["app", "handler"]
