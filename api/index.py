import sys
import os

# Add root directory to sys.path so app, schema, model, config imports resolve correctly in Vercel Serverless
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app import app

# Export app for Vercel ASGI serverless handler
__all__ = ["app"]
