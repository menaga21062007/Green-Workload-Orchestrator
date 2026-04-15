from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# ✅ CORS (important for Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage
tasks = []
co2_saved = 0

# Home
@app.get("/")
def home():
    return {"message": "Backend running"}

# Get tasks
@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks}

# 🔥 Dynamic carbon intensity
@app.get("/carbon")
def get_carbon():
    value = random.randint(100, 500)

    if value < 200:
        status = "GREEN"
    elif value < 350:
        status = "YELLOW"
    else:
        status = "RED"

    return {
        "carbon_intensity": value,
        "status": status
    }

# CO2 savings
@app.get("/savings")
def get_savings():
    return {"co2_saved": co2_saved}

# Add task
@app.post("/task")
def add_task(task: dict):
    global co2_saved

    task["status"] = "RUNNING"
    task["carbon_at_submission"] = random.randint(100, 500)

    tasks.append(task)

    # simulate saving
    co2_saved += random.randint(1, 10)

    return {"message": "Task added"}