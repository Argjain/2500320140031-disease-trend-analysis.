from playwright.sync_api import sync_playwright
from pathlib import Path
import time

out_dir = Path("docs/screenshots")
out_dir.mkdir(parents=True, exist_ok=True)

pages_to_capture = [
    ("http://localhost:8501/", "01_cockpit_home.png"),
    ("http://localhost:8501/Overview", "02_overview_state_burden.png"),
    ("http://localhost:8501/Trends", "03_trends_seasonality.png"),
    ("http://localhost:8501/Regional_Analysis", "04_regional_cfr_recovery.png"),
    ("http://localhost:8501/Demographics", "05_demographics_cohorts.png"),
    ("http://localhost:8501/EDA_Statistics", "06_eda_urban_density.png"),
    ("http://localhost:8501/Data_Quality", "07_data_quality_ledger.png"),
]

print("Launching Playwright to capture high-res project screenshots...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    
    for url, filename in pages_to_capture:
        try:
            print(f"Navigating to {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(2.5)  # Allow Streamlit charts to render
            save_path = out_dir / filename
            page.screenshot(path=str(save_path))
            print(f"Captured: {filename} ({save_path.stat().st_size // 1024} KB)")
        except Exception as e:
            print(f"Error capturing {url}: {e}")
            
    browser.close()

print("All screenshots captured successfully!")
