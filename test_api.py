from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

app = FastAPI()

class Complaint(BaseModel):
    name: str
    mobile: str
    message: str

complaints = {}

@app.post("/register")
def register_complaint(complaint: Complaint):
    complaint_id = str(uuid4())[:8]
    complaints[complaint_id] = {
        "id": complaint_id,
        "name": complaint.name,
        "mobile": complaint.mobile,
        "message": complaint.message,
        "timestamp": datetime.now().isoformat(),
        "status": "Pending"
    }
    return {"complaint_id": complaint_id, "message": "Complaint registered successfully."}

@app.get("/status/{query}")
def get_status(query: str):
    # Search by complaint ID first, then by mobile
    for comp_id, details in complaints.items():
        if query == comp_id or query == details["mobile"]:
            return details
    return {"message": "No complaint found for the given input."}
