import pandas as pd
import json
import pickle

def load_data():
    dados = pd.read_csv('./data/titanic.csv')
    
    return dados

def get_all_predictions():
    data = None
    with open('predictions.json', 'r') as f:
        data = json.load(f)
        
    return data

def save_prediction(passageiro):
    data = get_all_predictions()
    
    data.append(passageiro)
    
    with open('predictions.json', 'w') as f:
        json.dump(data, f)
        

P_CLASS_MAP = {
    '1st': 1,
    '2nd': 2,
    '3rd': 3
}
SEX_MAP = {
    'Male': 0,
    'Female': 1,
}
EMBARKED_MAP = {
    'Cherbourg': 0, 
    'Queenstown': 1, 
    'Southampton': 2
}

def survival_predictor(passageiro):
    
    passageiro['Pclass'] = P_CLASS_MAP[passageiro['Pclass']]
    passageiro['Sex'] = SEX_MAP[passageiro['Sex']]
    passageiro['Embarked'] = EMBARKED_MAP[passageiro['Embarked']]
    
    values = pd.DataFrame([passageiro])
    
    model = pickle.load(open('./models/model.pkl', 'rb'))
    
    results = model.predict(values)
    
    result = None
    
    if len(results) == 1:
        result = int(results[0])
    
    return result