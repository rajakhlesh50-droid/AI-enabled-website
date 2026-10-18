import sys
import os

sys.path.insert(0, os.path.abspath("backend"))

import config
import database
import auth
import scoring
import ai_service
import models
from app import app

client = app.test_client()

# 1. Test Static / HTML View Pages
pages = ["/", "/login", "/admissions", "/courses", "/dashboard", "/contact", "/gallery", "/overview"]
for page in pages:
    res = client.get(page)
    print(f"Page {page}: HTTP {res.status_code}")
    assert res.status_code == 200, f"Failed on {page}"

# 2. Test Course Catalog API
courses_res = client.get("/api/courses")
print(f"API /api/courses: HTTP {courses_res.status_code}, count: {len(courses_res.json)}")
assert courses_res.status_code == 200

# 3. Test AI Merit Predictor API
predict_res = client.post("/predict", json={"marks": 85, "course": "B.Tech CSE"})
print(f"API /predict: HTTP {predict_res.status_code}, prediction: {predict_res.json.get('prediction')}")
assert predict_res.status_code == 200

# 4. Test AI Chatbot API
chat_res = client.post("/chat", json={"message": "Tell me about CSE course"})
print(f"API /chat: HTTP {chat_res.status_code}, mode: {chat_res.json.get('mode')}")
assert chat_res.status_code == 200

print("\n>>> ALL BACKEND MODULES AND ROUTES VERIFIED SUCCESSFULLY! <<<")

