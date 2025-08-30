from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
import math, random

app = FastAPI(title="Kogenta Explorer Lite")

# Serve static frontend
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

# --- Demo POI data ---
POIS = [
    {"name":"ASDA Peckham", "lat":51.4747, "lon":-0.0695},
    {"name":"ASDA Lewisham", "lat":51.4616, "lon":-0.0102},
    {"name":"Tesco Superstore Brixton", "lat":51.4631, "lon":-0.1149},
    {"name":"Oxford Circus", "lat":51.5154, "lon":-0.1410},
    {"name":"Canary Wharf", "lat":51.5054, "lon":-0.0235},
]

def seeded(lat: float, lon: float, salt: int = 0) -> random.Random:
    seed = int((lat*10000)%100000) ^ int((lon*10000)%100000) ^ salt
    return random.Random(seed)

@app.get("/api/poi")
def poi_search(q: str = Query("", description="keyword e.g. 'ASDA'")):
    ql = q.lower().strip()
    results = [p for p in POIS if ql in p["name"].lower()] if ql else POIS
    return {"results": results}

@app.get("/api/busyness")
def busyness(lat: float, lon: float):
    rnd = seeded(lat, lon, 42)
    base = 50 + 40*math.sin((lat+lon)*3.14) + rnd.randint(-10, 10)
    return {"score": max(0, min(100, int(base))), "ts": datetime.utcnow().isoformat()+"Z"}

@app.get("/api/flows")
def flows(lat: float, lon: float):
    rnd = seeded(lat, lon, 7)
    areas = ["SE15","SE1","SE8","SE16","SE5","SE14","SE4"]
    data = [{"origin": a, "visitors": rnd.randint(50, 400)} for a in areas]
    return {"results": sorted(data, key=lambda x:x["visitors"], reverse=True)}

@app.get("/api/forecast")
def forecast(lat: float, lon: float):
    rnd = seeded(lat, lon, 99)
    now = datetime.utcnow()
    series = []
    base = rnd.randint(30,70)
    for h in range(24):
        val = base + int(25*math.sin((h/24)*2*math.pi)) + rnd.randint(-8,8)
        series.append({"t": (now + timedelta(hours=h)).isoformat()+"Z",
                       "score": max(0, min(100, val))})
    return {"series": series}

# ✅ Redirect root → /web/
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/web/")
