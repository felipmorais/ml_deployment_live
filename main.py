from fastapi import Body, FastAPI
from typing import Any
import data_handler
import json

# rodar a nossa api
# uvicorn main:api --reload

api = FastAPI()


@api.get("/hello_world")
def hello_world():
    return {"message": "Hello World!"}

@api.get("/")
def root():
    return {"message": "Root"}


@api.get("/get_titanic_data")
def get_titanic():
    dados = data_handler.load_data()
    
    dados_json = dados.to_json(orient='records')
    
    return dados_json

@api.get("/get_all_predictions")
def get_predictions():
    all_predictions = data_handler.get_all_predictions()
    
    return all_predictions

@api.post("/save_prediction")
def save_prediction(passageiro_json: Any = Body(None)):
    passageiro = json.loads(passageiro_json)
    
    result = data_handler.save_prediction(passageiro)
    
    return result

@api.post("/predict")
def predict(passageiro_json: Any = Body(None)):
    
    passageiro = json.loads(passageiro_json)
    
    result = data_handler.survival_predictor(passageiro)
    
    return result