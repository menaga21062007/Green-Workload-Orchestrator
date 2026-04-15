from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []
co2_saved = 0

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks}

@app.get("/carbon")
def get_carbon():
    return {"carbon_intensity": 50, "status": "GREEN"}

@app.get("/savings")
def get_savings():
    return {"co2_saved": co2_saved}

@app.post("/task")
def add_task(task: dict):
    global co2_saved

    task["status"] = "RUNNING"
    task["carbon_at_submission"] = 50

    tasks.append(task)
    co2_saved += 5

    return {"message": "Task added"}