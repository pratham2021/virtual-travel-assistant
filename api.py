from app.schemas.input_schema import Preference
from app.schemas.output_schema import Itinerary
from app.itinerary_generator import generate_itinerary
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from app.schemas.input_schema import solo_backpacker

app = FastAPI() # the main entrypoint to use FastAPI

jobs = {} # each key will be a unique job ID (a string); each value will be another dictionary holding that job's current status and result/error

# {
#   "status": "pending", # "pending" | "running" | "complete" | "failed"
#   "result": None,      # will hold the Itinerary once complete
#   "error": None        # will hold an error message if failed
# }

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"], # list of frontend URLs allowed to make requests to this backend
  allow_credentials=True, # wrhter cookies/auth headers are allowed to be sent cross-origin. 
  allow_methods=["*"], # allows all HTTP methods from the allowed origins. POST is my only endpoint.
  allow_headers=["*"], # allows any request headers, including Content-Type: application/json, which your frontend will need to send JSON bodies
)

def run_itinerary_generation(job_id: str, preference: Preference):
    jobs[job_id]["status"] = "running"
    try:
        result = generate_itinerary(preference)
        jobs[job_id]["status"] = "complete"
        jobs[job_id]["result"] = result
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
      
@app.post("/generate-itinerary")
def start_generation(preference: Preference, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = { "status": "pending", "result": None, "error": None }
    background_tasks.add_task(run_itinerary_generation, job_id, preference) # after the POST request has been made, add this as a background task
    return { "job_id": job_id }
  
@app.get("/generate-itinerary/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

if __name__ == "__main__":
    test_job_id = "test-123"
    print("Entered")
    jobs[test_job_id] = {"status": "pending", "result": None, "error": None}
    run_itinerary_generation(test_job_id, solo_backpacker)
    print(jobs[test_job_id])