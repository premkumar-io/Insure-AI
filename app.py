import os
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse, ErrorResponse
from model.predict import predict_output, model

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("insure_ai")

APP_VERSION = "2.0.0"

app = FastAPI(
    title="Insure AI Risk Prediction API",
    description="Production-grade AI/ML API to assess and predict insurance premium risk categories based on demographic & physical indicators.",
    version=APP_VERSION
)

# Environment-based CORS configuration
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env and allowed_origins_env != "*":
    origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
elif os.getenv("ENVIRONMENT") == "production":
    origins = [os.getenv("FRONTEND_ORIGIN", "http://localhost:8501")]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vercel Serverless Path Rewriter Middleware
@app.middleware("http")
async def vercel_scope_fix(request: Request, call_next):
    path = request.scope.get("path", "")
    forwarded = request.headers.get("x-vercel-forwarded-path") or request.headers.get("x-forwarded-uri")
    
    if forwarded and forwarded.startswith("/"):
        clean_fwd = forwarded.split("?")[0]
        if clean_fwd in ["/api/index.py", "/api/index"]:
            if request.method.upper() == "POST":
                request.scope["path"] = "/predict"
            else:
                request.scope["path"] = "/"
        else:
            request.scope["path"] = clean_fwd
    elif path in ["", "/api/index.py", "/api/index"]:
        if request.method.upper() == "POST":
            request.scope["path"] = "/predict"
        else:
            request.scope["path"] = "/"

    return await call_next(request)

# Custom Validation Error Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc}")
    error_details = []
    for err in exc.errors():
        field = " -> ".join([str(x) for x in err.get("loc", []) if x != "body"])
        error_details.append({
            "field": field or "payload",
            "message": err.get("msg", "Invalid value"),
            "type": err.get("type", "validation_error")
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Please check the highlighted input fields.",
                "details": error_details
            }
        }
    )

# Custom General Exception Handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error processing {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred while generating prediction. Please try again later."
            }
        }
    )

from fastapi.responses import JSONResponse, HTMLResponse

@app.get('/', response_class=HTMLResponse)
@app.get('/api/index.py', response_class=HTMLResponse)
@app.get('/api/index', response_class=HTMLResponse)
def home():
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    return HTMLResponse(content="<h1>Insure AI Platform</h1>", status_code=200)

@app.get('/json')
def api_info():
    return {
        'message': 'Insure AI Risk Analytics API',
        'status': 'active',
        'version': APP_VERSION,
        'docs_url': '/docs'
    }

@app.get("/health")
def health_check():
    import model.predict as mp
    current_model = mp.get_model()
    return {
        "status": "OK" if current_model is not None else "DEGRADED",
        "model_loaded": current_model is not None,
        "model_path": mp.MODEL_PATH,
        "model_error": mp.model_load_error,
        "version": APP_VERSION
    }

@app.post('/predict', response_model=PredictionResponse)
@app.post('/api/index.py', response_model=PredictionResponse)
@app.post('/api/index', response_model=PredictionResponse)
def predict_premium(data: UserInput):
    try:
        user_input = {
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }

        logger.info(f"Predicting premium category for city_tier={data.city_tier}, age_group={data.age_group}")
        prediction = predict_output(user_input)
        return prediction
    
    except Exception as e:
        logger.error(f"Prediction execution failed: {e}", exc_info=True)
        raise e