from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import threading
import time

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory task storage
tasks = []

# ---------------- ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/carbon")
def get_carbon():
    carbon_intensity = random.randint(100, 500)
    status = "GREEN" if carbon_intensity < 300 else "RED"

    return {
        "carbon_intensity": carbon_intensity,
        "status": status
    }

@app.post("/task")
def add_task(task: dict):
    carbon_intensity = random.randint(100, 500)
    status = "GREEN" if carbon_intensity < 300 else "RED"

    # Decision logic
    if status == "GREEN":
        decision = "RUNNING"
    else:
        decision = "WAITING"

    task["status"] = decision
    task["carbon_at_submission"] = carbon_intensity

    tasks.append(task)

    return {
        "message": "Task processed",
        "task": task
    }

@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks}

# ---------------- AUTO SCHEDULER ---------------- #

def scheduler():
    while True:
        carbon_intensity = random.randint(100, 500)
        status = "GREEN" if carbon_intensity < 300 else "RED"

        print("Scheduler check:", carbon_intensity, status)

        if status == "GREEN":
            for task in tasks:
                if task["status"] == "WAITING":
                    task["status"] = "RUNNING"
                    task["executed_at_carbon"] = carbon_intensity
                    print("Task executed:", task["name"])

        time.sleep(5)  # runs every 5 seconds

# Start background scheduler
threading.Thread(target=scheduler, daemon=True).start()

# ---------------- CO2 SAVINGS ---------------- #

@app.get("/savings")
def get_savings():
    saved = 0

    for task in tasks:
        if "executed_at_carbon" in task:
            # baseline = dirty grid (400)
            saved += max(0, 400 - task["executed_at_carbon"])

    return {
        "co2_saved": saved
    }
