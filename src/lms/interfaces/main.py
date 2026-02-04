from fastapi import FastAPI
from lms.interfaces.enrollment_router import router as enrollment_router
from lms.interfaces.progress_router import router as progress_router

app = FastAPI(title="LMS DDD API", version="0.1.0")

app.include_router(enrollment_router)
app.include_router(progress_router)


@app.get("/health")
def health_check():
    return {'status': "ok"}
