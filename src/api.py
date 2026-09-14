from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import glob

app = FastAPI(title="Groww Weekly Pulse API")

# Allow all origins for the Vercel frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Groww Weekly Pulse Backend"}

@app.get("/api/reviews")
def get_reviews():
    filepath = "data/reviews.json"
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/themes")
def get_themes():
    filepath = "data/themes.json"
    if not os.path.exists(filepath):
        return {"themes": []}
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pulse/latest")
def get_latest_pulse():
    # Find all pulse markdown files in the output directory
    output_dir = "output"
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="No pulse reports generated yet.")
        
    pulse_files = glob.glob(f"{output_dir}/pulse_*.md")
    if not pulse_files:
        raise HTTPException(status_code=404, detail="No pulse reports found.")
        
    # Sort by filename descending to get the latest (since format is pulse_YYYY-WNN.md)
    latest_file = sorted(pulse_files, reverse=True)[0]
    
    try:
        with open(latest_file, "r") as f:
            content = f.read()
            return {
                "filename": os.path.basename(latest_file),
                "content": content
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
