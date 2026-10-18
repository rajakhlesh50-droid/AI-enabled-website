def score(data):
    total = 0
    course = str(data.get("course", "")).lower()
    if any(k in course for k in ["b.tech", "cse", "ece", "mechanical", "civil", "engineering"]):
        total += 50
    elif "nursing" in course:
        total += 45
    elif "agriculture" in course:
        total += 45
    elif "bba" in course:
        total += 40
    elif "diploma" in course:
        total += 35
    else:
        total += 30

    phone = "".join(character for character in str(data.get("phone", "")) if character.isdigit())
    if len(phone) == 10:
        total += 25

    try:
        marks = float(data.get("marks", 0))
        if marks >= 80:
            total += 25
        elif marks >= 60:
            total += 15
        elif marks >= 45:
            total += 10
    except (TypeError, ValueError):
        pass

    return total

def predict_admission(marks, course):
    if marks >= 80:
        prediction = "High"
        scholarship = "Eligible for 50% - 100% Merit Scholarship"
        message = "Outstanding score! Very high chance of direct admission in 1st Merit List."
    elif marks >= 60:
        prediction = "High"
        scholarship = "Eligible for 25% Merit Scholarship"
        message = "Great score! High chance of admission in your selected course."
    elif marks >= 45:
        prediction = "Moderate"
        scholarship = "Standard Merit Seat"
        message = "Eligible for counseling round and seat confirmation."
    else:
        prediction = "Low"
        scholarship = "Counseling Recommended"
        message = "Marks below minimum criteria (45%). Please contact admission counselor."

    return {
        "prediction": prediction,
        "marks": marks,
        "course": course,
        "scholarship": scholarship,
        "message": message
    }

