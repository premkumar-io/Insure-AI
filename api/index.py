import sys
import os
import logging

# Setup logger for Vercel Serverless Function
logger = logging.getLogger("insure_ai.vercel")

# Ensure root directory is at the top of sys.path for Vercel
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app import app
    logger.info("Successfully imported FastAPI app for Vercel Serverless deployment.")
except Exception as ex:
    logger.error(f"Critical error importing app in api/index.py: {ex}", exc_info=True)
    from fastapi import FastAPI
    app = FastAPI(title="Insure AI - Vercel Serverless Initialization Error")

    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
    def error_fallback(path: str):
        return {
            "status": "error",
            "message": "Vercel Serverless Function Initialization Failed",
            "detail": str(ex),
            "python_path": sys.path,
            "root_dir": root_dir
        }

# Export app and handler for Vercel ASGI serverless runner
handler = app
__all__ = ["app", "handler"]
