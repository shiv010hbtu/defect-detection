import os
import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import uuid
from detector import DefectDetector
from database.db import DefectLogger

app = FastAPI(title="Surface Defect Detection System")

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory="templates")

detector = DefectDetector()
logger = DefectLogger()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    history = logger.get_all()
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"history": history}
)


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = f"static/uploads/{filename}"

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = detector.analyze(save_path)
    result["image_url"] = f"/static/uploads/{filename}"
    result["filename"] = file.filename

    logger.save(
        filename=file.filename,
        severity=result["severity"],
        defect_count=result["defect_count"],
        confidence=result["confidence"],
        anomaly=result["is_anomaly"]
    )

    return JSONResponse(content=result)


@app.get("/history")
def get_history():
    return logger.get_all()


@app.delete("/history")
def clear_history():
    logger.clear()
    return {"message": "History cleared"}
