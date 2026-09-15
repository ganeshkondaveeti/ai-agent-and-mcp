from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import glob
from src.main import main as run_pipeline

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

import sqlite3

def get_db_connection():
    if not os.path.exists("data/metrics.db"):
        raise HTTPException(status_code=404, detail="Metrics database not initialized yet.")
    conn = sqlite3.connect("data/metrics.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/analytics/trajectory")
def get_trajectory():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, 
                   SUM(positive_count) as positive,
                   SUM(neutral_count) as neutral,
                   SUM(negative_count) as negative
            FROM daily_metrics
            GROUP BY date
            ORDER BY date ASC
            LIMIT 30
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/kpis")
def get_kpis():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get total reviews, total score for Net Sentiment, Detractor Rate, Velocity
        cursor.execute('''
            SELECT 
                SUM(review_count) as total_reviews,
                SUM(positive_count) as total_positive,
                SUM(negative_count) as total_negative,
                SUM(total_score) as sum_scores,
                COUNT(DISTINCT date) as days
            FROM daily_metrics
        ''')
        row = cursor.fetchone()
        conn.close()
        
        if not row or not row['total_reviews']:
            return {"net_sentiment": 0, "velocity": 0, "detractor_rate": 0}
            
        total = row['total_reviews']
        avg_score = row['sum_scores'] / total
        # Scale score (1-5) to Net Sentiment (0-100)
        net_sentiment = ((avg_score - 1) / 4) * 100
        
        detractor_rate = (row['total_negative'] / total) * 100
        velocity = total / (row['days'] or 1)
        
        return {
            "net_sentiment": round(net_sentiment, 1),
            "velocity": round(velocity, 0),
            "detractor_rate": round(detractor_rate, 1)
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/feature-pods")
def get_feature_pods():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pod_name, 
                   SUM(positive_count) as positive,
                   SUM(negative_count) as negative,
                   SUM(review_count) as total
            FROM feature_pod_metrics
            GROUP BY pod_name
            ORDER BY total DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/store-ecology")
def get_store_ecology():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT store, 
                   SUM(review_count) as total_reviews,
                   SUM(total_score) as sum_scores
            FROM daily_metrics
            GROUP BY store
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        result = {}
        for r in rows:
            store = r['store']
            avg_score = r['sum_scores'] / r['total_reviews'] if r['total_reviews'] else 0
            result[store] = {
                "total_reviews": r['total_reviews'],
                "avg_rating": round(avg_score, 1)
            }
        return result
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pulse/trigger")
async def trigger_pulse(background_tasks: BackgroundTasks):
    """
    Manually triggers the weekly pulse pipeline in the background.
    """
    background_tasks.add_task(run_pipeline)
    return {"status": "accepted", "message": "Pipeline triggered successfully in the background."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
