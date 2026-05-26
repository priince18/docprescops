import os
import joblib
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict
from pathlib import Path

MODEL_DIR = Path("/mnt/efs/ml-data/models")
MODEL_FILE = MODEL_DIR / "model.pkl"


# Map label -> medicine info payload used by Node backend/FE
LABEL_TO_MEDICINE: Dict[str, Dict] = {
    'paracetamol': {
        'name': 'Paracetamol', 'genericName': 'Acetaminophen', 'category': 'Antipyretic/Analgesic',
        'dosage': '500-1000mg every 4-6 hours', 'sideEffects': 'Nausea, stomach upset, liver risk (high dose)',
        'precautions': 'Max 4g/day; avoid alcohol'
    },
    'ibuprofen': {
        'name': 'Ibuprofen', 'genericName': 'Ibuprofen', 'category': 'NSAID',
        'dosage': '200-400mg every 4-6 hours with food', 'sideEffects': 'Stomach irritation, bleeding risk',
        'precautions': 'Avoid with ulcers; take with food'
    },
    'antacid': {
        'name': 'Antacid', 'genericName': 'Al/Mg hydroxide', 'category': 'Antacid',
        'dosage': '1-2 tablets as needed', 'sideEffects': 'Diarrhea/constipation',
        'precautions': 'Separate from other meds by 1-2h'
    },
    'omeprazole': {
        'name': 'Omeprazole', 'genericName': 'Omeprazole', 'category': 'PPI',
        'dosage': '20mg once daily before food', 'sideEffects': 'Headache, GI upset',
        'precautions': 'Short-term use; consult for long-term'
    },
    'cetirizine': {
        'name': 'Cetirizine', 'genericName': 'Cetirizine', 'category': 'Antihistamine',
        'dosage': '10mg once daily', 'sideEffects': 'Drowsiness, dry mouth',
        'precautions': 'Caution with driving/alcohol'
    },
    'loratadine': {
        'name': 'Loratadine', 'genericName': 'Loratadine', 'category': 'Antihistamine (non-drowsy)',
        'dosage': '10mg once daily', 'sideEffects': 'Headache, fatigue',
        'precautions': 'Generally well tolerated'
    },
    'dextromethorphan': {
        'name': 'Dextromethorphan', 'genericName': 'Dextromethorphan', 'category': 'Antitussive',
        'dosage': '15-30mg every 4-6 hours', 'sideEffects': 'Drowsiness, nausea',
        'precautions': 'Avoid alcohol; do not drive'
    },
    'guaifenesin': {
        'name': 'Guaifenesin', 'genericName': 'Guaifenesin', 'category': 'Expectorant',
        'dosage': '200-400mg every 4 hours', 'sideEffects': 'Nausea, headache',
        'precautions': 'Hydration recommended'
    },
}

class PredictRequest(BaseModel):
    symptoms: str
    age: int | None = None
    gender: str | None = None
    medicalHistory: str | None = None


model = None
if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)

async def predict(req_data: dict):
    global model
    
    # જો મેમરીમાં મોડેલ ન હોય, તો EFS માંથી લોડ કરો
    if model is None:
        if MODEL_FILE.exists():
            print(f"Loading model from EFS: {MODEL_FILE}")
            model = joblib.load(MODEL_FILE)
        else:
            raise HTTPException(status_code=503, detail='Model pkl file not found on EFS. Train first.')

    # જો ઇનપુટ ડાયરેક્ટ ડિક્શનરી હોય તો તેને ટેક્સ્ટમાં કન્વર્ટ કરો
    symptoms_text = req_data.get("symptoms", "")
    text = str(symptoms_text).strip().lower()
    
    if not text:
        raise HTTPException(status_code=400, detail='symptoms is required')

    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba([text])[0]
        labels = list(model.classes_)
        scored = sorted(zip(labels, proba), key=lambda x: x[1], reverse=True)
    else:
        # fallback to decision_function/predict
        pred = model.predict([text])[0]
        scored = [(pred, 1.0)]

    top = scored[:3]
    recommendations: List[Dict] = []

    for label, score in top:
        info = LABEL_TO_MEDICINE.get(label, {
            'name': label.title(), 'genericName': label.title(), 'category': 'General',
            'dosage': 'See package insert', 'sideEffects': 'Varies', 'precautions': 'Consult professional'
        })
        rec = {
            **info,
            'confidence': int(round(float(score) * 100)) if score is not None else 60
        }
        recommendations.append(rec)

    # Simple age/history heuristics could be applied here if needed
    return {"success": True, "recommendations": recommendations}


import os
import joblib
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict
from pathlib import Path

# EFS પાથ
MODEL_DIR = Path("/mnt/efs/ml-data/models")
MODEL_FILE = MODEL_DIR / "model.pkl"

# ... (તમારો LABEL_TO_MEDICINE અને PredictRequest ક્લાસ અહીં સમાન રહેશે) ...

model = None

async def predict(req_data: dict):
    global model
    
    # જો મેમરીમાં મોડેલ ન હોય, તો EFS માંથી લોડ કરો
    if model is None:
        if MODEL_FILE.exists():
            print(f"Loading model from EFS: {MODEL_FILE}")
            model = joblib.load(MODEL_FILE)
        else:
            raise HTTPException(status_code=503, detail='Model pkl file not found on EFS. Train first.')

    # જો ઇનપુટ ડાયરેક્ટ ડિક્શનરી હોય તો તેને ટેક્સ્ટમાં કન્વર્ટ કરો
    symptoms_text = req_data.get("symptoms", "")
    text = str(symptoms_text).strip().lower()
    
    if not text:
        raise HTTPException(status_code=400, detail='symptoms is required')

    # પ્રેડિક્શન લોજિક
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba([text])[0]
        labels = list(model.classes_)
        scored = sorted(zip(labels, proba), key=lambda x: x[1], reverse=True)
    else:
        pred = model.predict([text])[0]
        scored = [(pred, 1.0)]

    top = scored[:3]
    recommendations = []

    for label, score in top:
        info = LABEL_TO_MEDICINE.get(label, {
            'name': label.title(), 'genericName': label.title(), 'category': 'General',
            'dosage': 'See package insert', 'sideEffects': 'Varies', 'precautions': 'Consult professional'
        })
        rec = {
            **info,
            'confidence': int(round(float(score) * 100)) if score is not None else 60
        }
        recommendations.append(rec)

    return {"success": True, "recommendations": recommendations}
