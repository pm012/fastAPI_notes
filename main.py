from fastapi import FastAPI
from src.routes.notes import router as notes_router
from src.routes.tags import router as tags_router

app = FastAPI()

# Підключаємо роутери з їхніми новими змінними
app.include_router(tags_router, prefix='/api')
app.include_router(notes_router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}
