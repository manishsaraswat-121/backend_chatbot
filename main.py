from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from db import insert_complaint, get_complaint_by_id, get_complaint_by_mobile

app = FastAPI()

# ✅ Root route to confirm server is live
@app.get("/")
def root():
    return {"message": "✅ Complaint API Server is running"}

# Request model for complaint registration
class RegisterRequest(BaseModel):
    name: str
    mobile: str
    complaint: str

@app.post("/register")
def register_complaint(data: RegisterRequest):
    complaint_id = str(uuid4())[:8]
    complaint_data = {
        "complaint_id": complaint_id,
        "name": data.name,
        "mobile": data.mobile,
        "complaint": data.complaint,
        "status": "Pending"
    }
    insert_complaint(complaint_data)
    return {"message": "Complaint registered successfully", "complaint_id": complaint_id}

@app.get("/status/{query}")
def get_status(query: str):
    result = get_complaint_by_id(query)
    if result:
        return result
    result = get_complaint_by_mobile(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Complaint not found")
