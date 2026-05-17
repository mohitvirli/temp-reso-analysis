import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import torch
import torchaudio
from allin1 import Allin1

app = FastAPI(title="Music Structure Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    model = Allin1()
except Exception as e:
    print(f"Warning: Could not initialize Allin1 model: {e}")
    model = None


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "music-analysis-api"}


@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not initialized")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    allowed_extensions = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported format")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name

        waveform, sr = torchaudio.load(tmp_path)

        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            waveform = resampler(waveform)
            sr = 16000

        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        with torch.no_grad():
            results = model.analyze(waveform, sr)

        analysis_result = {
            "filename": file.filename,
            "duration_seconds": float(waveform.shape[1] / sr),
            "sample_rate": sr,
            "bpm": float(results.get("bpm", 0)) if results.get("bpm") is not None else None,
            "segments": results.get("segments", []),
            "beats": results.get("beats", []),
            "downbeats": results.get("downbeats", []),
        }

        return JSONResponse(content=analysis_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.get("/")
async def root():
    return {
        "service": "Music Structure Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze (POST)",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
