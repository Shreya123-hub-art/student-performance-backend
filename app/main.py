from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from pymongo import MongoClient

app = FastAPI()

# -------------------------
# MongoDB Atlas Connection
# -------------------------
client = MongoClient("mongodb+srv://tantryshreya352_db_user:shreya123@cluster0.nthtnx2.mongodb.net/")
db = client["student_db"]
collection = db["predictions"]

# -------------------------
# Input Schema
# -------------------------
class StudentInput(BaseModel):
    attendance: float
    assignment_score: float
    internal_marks: float
    participation: float
    previous_score: float

# -------------------------
# Home
# -------------------------
@app.get("/")
def home():
    return {"message": "Student Performance API Running"}

# -------------------------
# Predict API (LOGIC BASED)
# -------------------------
@app.post("/predict")
def predict_performance(data: StudentInput):
    try:
        # Simple intelligent logic
        if data.attendance > 90 and data.assignment_score > 85:
            result = "Excellent"
        elif data.attendance > 60:
            result = "Average"
        else:
            result = "At Risk"

        # Save to MongoDB
        record = {
            "attendance": data.attendance,
            "assignment_score": data.assignment_score,
            "internal_marks": data.internal_marks,
            "participation": data.participation,
            "previous_score": data.previous_score,
            "prediction": result
        }

        collection.insert_one(record)

        return {"prediction": result}

    except Exception as e:
        return {"error": str(e)}

# -------------------------
# History API
# -------------------------
@app.get("/history")
def get_history():
    try:
        data = list(collection.find({}, {"_id": 0}))
        return {"history": data}
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Analytics API
# -------------------------
@app.get("/analytics")
def analytics():
    try:
        total = collection.count_documents({})
        excellent = collection.count_documents({"prediction": "Excellent"})
        average = collection.count_documents({"prediction": "Average"})
        risk = collection.count_documents({"prediction": "At Risk"})

        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avg_attendance": {"$avg": "$attendance"},
                    "avg_assignment": {"$avg": "$assignment_score"},
                    "avg_internal": {"$avg": "$internal_marks"},
                    "avg_participation": {"$avg": "$participation"},
                    "avg_previous": {"$avg": "$previous_score"}
                }
            }
        ]

        avg_data = list(collection.aggregate(pipeline))

        return {
            "total_students": total,
            "performance_distribution": {
                "excellent": excellent,
                "average": average,
                "at_risk": risk
            },
            "average_scores": avg_data[0] if avg_data else {}
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Graph Data API
# -------------------------
@app.get("/graph-data")
def graph_data():
    try:
        data = list(collection.find({}, {"_id": 0})

        attendance = [d["attendance"] for d in data]
        assignment = [d["assignment_score"] for d in data]
        internal = [d["internal_marks"] for d in data]

        return {
            "attendance": attendance,
            "assignment_scores": assignment,
            "internal_marks": internal
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Risk Summary API
# -------------------------
@app.get("/risk-summary")
def risk_summary():
    try:
        risky_students = list(collection.find({"prediction": "At Risk"}, {"_id": 0}))

        return {
            "count": len(risky_students),
            "students": risky_students[:5]
        }

    except Exception as e:
        return {"error": str(e)}