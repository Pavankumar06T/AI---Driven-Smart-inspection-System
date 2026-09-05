import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print(f"Starting PS-05 Document Intelligence Module Backend on http://{HOST}:{PORT}")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
