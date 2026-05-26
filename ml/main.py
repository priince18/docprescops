from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from train import train_model
from serve import predict
from pathlib import Path
import uvicorn

app = FastAPI(
    title="ML Service",
    root_path="/ml"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# સાચો EFS માઉન્ટ પાથ
BASE_PATH = Path("/mnt/efs/ml-data")

# જો ફોલ્ડર ન હોય તો EFS પર ઓટોમેટિક બનાવી દેશે
for folder in ["models", "artifacts", "logs"]:
    (BASE_PATH / folder).mkdir(parents=True, exist_ok=True)

# જો EFS પર મોડેલ ફાઇલ ન હોય તો જ ટ્રેનિંગ શરૂ થશે
model_file = BASE_PATH / "models" / "model.pkl"
if not model_file.exists():
    print("Model missing on EFS, training starting...")
    train_result = train_model()
    print("Training finished.")

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
async def prediction(request: Request):
    try:
        # રિક્વેસ્ટ ડેટા પાસ કરવો
        req_data = await request.json()
        
        # serve.py ના કન્વર્ઝન માટે Pydantic મોડેલ સ્ટ્રક્ચર જરૂરી હોઈ શકે છે
        # જો ડાયરેક્ટ ડિક્શનરી મોકલવી હોય તો serve.py ને તે મુજબ એડજસ્ટ કરવું
        result = await predict(req_data) 
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False)
