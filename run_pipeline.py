import os
import sys

# Ensure the project root is in the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.tools.fetch_reviews import fetch_reviews
from src.tools.scrubber import scrub_pii
from src.tools.cluster_themes import cluster_themes
from src.tools.generate_pulse import generate_pulse

def main():
    print("🚀 Running Phase 2: Fetching Reviews...")
    raw_reviews = fetch_reviews.invoke({
        "app_id": "com.nextbillion.groww",
        "weeks": 8
    })
    print(f"Fetched {len(raw_reviews)} raw reviews.")

    print("\n🧹 Running Phase 2: Scrubbing PII and Filtering...")
    clean_reviews = scrub_pii.invoke({
        "raw_reviews": raw_reviews
    })
    print(f"Filtered down to {len(clean_reviews)} valid, clean English reviews.")

    print("\n🧠 Running Phase 3: Clustering Themes (Groq LLM)...")
    if not clean_reviews:
        print("No reviews to cluster.")
        return

    # Cap to top 200 reviews max to save tokens just in case
    clustering_input = clean_reviews[:200]
    
    themes_result = cluster_themes.invoke({
        "reviews": clustering_input
    })
    num_themes = len(themes_result.get("themes", []))
    print(f"Identified {num_themes} themes.")

    print("\n📝 Running Phase 4: Generating Pulse Report (Groq LLM)...")
    pulse_report = generate_pulse.invoke({
        "themes_result": themes_result
    })

    print("\n" + "="*50)
    print("📊 GENERATED PULSE REPORT")
    print("="*50 + "\n")
    print(pulse_report)
    print("\n" + "="*50)
    
    # Save to file
    out_dir = "data/exports"
    os.makedirs(out_dir, exist_ok=True)
    report_path = os.path.join(out_dir, "weekly_pulse.md")
    with open(report_path, "w") as f:
        f.write(pulse_report)
    print(f"Pulse report saved to {report_path}")

if __name__ == "__main__":
    main()
