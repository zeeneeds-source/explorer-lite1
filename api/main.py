from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Serve static files from web folder
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/")
async def root():
    return {"message": "Kogenta Explorer Lite API running"}

@app.get("/web/index")
async def get_index():
    return FileResponse("web/index.html")
