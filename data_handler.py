import json
import hashlib
import os

def anonymize_data(candidate_info):
    """Masks PII (Personally Identifiable Information) for GDPR compliance."""
    anonymized = candidate_info.copy()
    
    # 1. Mask Email (e.g., test@gmail.com -> t***@gmail.com)
    if "email" in anonymized and "@" in anonymized["email"]:
        username, domain = anonymized["email"].split("@")
        anonymized["email"] = f"{username[0]}***@{domain}"
        
    # 2. Mask Phone (e.g., 1234567890 -> ******7890)
    if "phone" in anonymized and len(str(anonymized["phone"])) > 4:
        phone_str = str(anonymized["phone"])
        anonymized["phone"] = "*" * (len(phone_str) - 4) + phone_str[-4:]
        
    # 3. Hash Name to create a unique but anonymous Candidate ID
    if "name" in anonymized:
        name_hash = hashlib.sha256(str(anonymized["name"]).encode()).hexdigest()[:8]
        anonymized["candidate_id"] = f"Candidate_{name_hash}"
        del anonymized["name"] # Remove the real name completely
        
    return anonymized

def save_to_mock_db(anonymized_data):
    """Simulates storing data in a backend database (JSON file)."""
    db_file = "mock_database.json"
    
    # Load existing data or create an empty list
    if os.path.exists(db_file):
        with open(db_file, "r") as file:
            db = json.load(file)
    else:
        db = []
        
    # Append the new anonymous record and save
    db.append(anonymized_data)
    with open(db_file, "w") as file:
        json.dump(db, file, indent=4)