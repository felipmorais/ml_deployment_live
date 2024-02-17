import streamlit as st
import data_handler
import util
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import requests
import json

if not util.check_password():
    st.stop()  # Do not continue if check_password is not True.

API_URL = "http://localhost:8000"

# dados = data_handler.load_data()
dados = None
response = requests.get(API_URL + "/get_titanic_data")
if response.status_code == 200:
    dados_json = json.loads(response.json())
    
    dados = pd.DataFrame(dados_json)
else:
    print("Erro no request do get_titanic_data")

# model = pickle.load(open('./models/model.pkl', 'rb'))

data_analyses_on = st.toggle("Exibir análise dos dados")

if data_analyses_on:
    
    st.dataframe(dados)
    
    st.header("Histrograma das idades")
    fig = plt.figure()
    plt.hist(dados['Age'], bins=30)
    plt.xlabel("Idade")
    plt.ylabel("Quantidade")
    st.pyplot(fig)

    st.header("Sobreviventes")
    st.bar_chart(dados.Survived.value_counts())
    
st.header("Preditor de sobrevivência")

col1, col2, col3 = st.columns(3)

with col1:
    classes = ["1st", "2nd", "3rd"]
    p_class = st.selectbox("Ticket class", classes)

with col2:
    classes = ['Male', 'Female']
    sex = st.selectbox('Sex', classes)
    
with col3:
    age = st.number_input("Age in years", step=1)
    

col1, col2, col3 = st.columns([2,2,1])

with col1:
    sib_sp = st.number_input("Number of siblings / spouses aboard", step=1)
    
with col2: 
    par_ch = st.number_input("Number of parents / children aboard", step=1)
    
with col3: 
    fare = st.number_input("Passenger Fare")

col1, col2 = st.columns(2)
with col1:
    classes = ['Cherbourg', 'Queenstown', 'Southampton']
    embarked = st.selectbox('Port of Embarkation', classes)
    
with col2:    
    submit = st.button("Verificar")
    
if submit or 'survived' in st.session_state:

    passageiro = {
        'Pclass': p_class,
        'Sex': sex,
        'Age': age,
        'SibSp': sib_sp,
        'Parch': par_ch,
        'Fare': fare,
        'Embarked': embarked
    }

    st.write(passageiro)
    
    # values = pd.DataFrame([passageiro])
    
    # st.dataframe(values)
    
    # results = model.predict(values)
    
    passageiro_json = json.dumps(passageiro)
    
    response = requests.post(API_URL + "/predict", json=passageiro_json)
    result = None
    if response.status_code == 200:
        result = response.json()
    else:
        print("Erro no request do predict")
    
    if result is not None:
        survided = result
        
        if survided == 1:
            st.subheader('Passageiro SOBREVIVEU! 😃🙌🏻')
            if 'survived' not in st.session_state:
                st.balloons()
            
        else:
            st.subheader('Passageiro NÃO sobreviveu! 😢')
            if 'survived' not in st.session_state:
                st.snow()
            
        st.session_state['survived'] = survided
            
    if passageiro and 'survived' in st.session_state:
        st.write("A predição está correta?")
        
        col1, col2, col3 = st.columns([1,1,5])
        
        with col1:
            correct_prediction = st.button('👍🏻')
            
        with col2:
            wrong_prediction = st.button('👎🏻')
            
        if correct_prediction or wrong_prediction:
            message = "Muito obrigado pelo feedback"
            if wrong_prediction:
                message += ", iremos usar esses dados para melhorar nosso modelo"
                
            if correct_prediction:
                passageiro['CorrectPrediction'] = True
            elif wrong_prediction:
                passageiro['CorrectPrediction'] = False
                
            passageiro['Survived'] = st.session_state['survived']
            
            st.write(message)
            
            # data_handler.save_prediction(passageiro)
            passageiro_json = json.dumps(passageiro)
            
            response = requests.post(API_URL + "/save_prediction", json=passageiro_json)
            
            if response.status_code == 200:
                print("Predicao salva")
            else:
                print("Erro no request do save_prediction")
            
    col1, col2, col3 = st.columns(3)
    
    with col2:
        new_test = st.button("Iniciar nova análise")
        
        if new_test and 'survived' in st.session_state:
            del st.session_state['survived']
            st.rerun()
            
accuracy_predictions_on = st.toggle("Exibir acurácia")

if accuracy_predictions_on:
    # predictions = data_handler.get_all_predictions()
    predictions = None
    response = requests.get(API_URL + "/get_all_predictions")
    if response.status_code == 200:
        predictions = response.json()
    else:
        print("Erro no request do get_all_predictions")
    
    num_total_predictions = len(predictions)
    correct_predictions = 0
    accuracy_hist = [0]
    for index, passageiro in enumerate(predictions):
        total = index + 1
        if passageiro['CorrectPrediction'] == True:
            correct_predictions += 1
            
        temp_acurracy = correct_predictions / total if total else 0
        accuracy_hist.append(round(temp_acurracy, 2))
        
    accuracy = correct_predictions / num_total_predictions if num_total_predictions else 0
    
    st.metric('Acurácia', round(accuracy, 2))
    
    # st.write(accuracy_hist)
    
    st.subheader('Histórico de acurácia')
    st.line_chart(accuracy_hist)
            
        
    
    
    
    