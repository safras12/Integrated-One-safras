from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

try:
    from backend.schemas.prediction import EmploymentReadinessRequest
    from backend.services.model_service import (
        ModelLoadingError,
        ModelPredictionError,
        predict_employment_readiness,
    )
except ModuleNotFoundError:
    from schemas.prediction import EmploymentReadinessRequest
    from services.model_service import (
        ModelLoadingError,
        ModelPredictionError,
        predict_employment_readiness,
    )

app = FastAPI(title="Employment Readiness Prediction API")

app.add_middleware(
    CORSMiddleware,
       allow_origins=[
       "http://localhost:5173",
       "http://127.0.0.1:5173",
       "https://integrated-one-safras-app.vercel.app",
   ],
   allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Employment Readiness Prediction API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/health")
def legacy_health_check() -> dict[str, str]:
    return health_check()


@app.post("/predict/employment-readiness")
def employment_readiness_prediction(request: EmploymentReadinessRequest) -> dict[str, object]:
    try:
        return predict_employment_readiness(request.to_student_data())
    except ModelLoadingError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ModelPredictionError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
