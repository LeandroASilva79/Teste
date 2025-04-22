from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

def buscar_preventiva(placa):
    df = pd.read_excel('preventivas.xlsx', sheet_name='CONTROLE DE PREVENTIVAS - GERAL', header=1)
    df.columns = df.iloc[0]
    df = df[1:]

    df = df.rename(columns={
        'Placa': 'Placa',
        'DATA ÚLTIMA REVISÃO ': 'Data_20k',
        'KM ULTIMA REVISÃO ': 'KM_20k',
        'Data_Rodagem': 'Data_Rodagem',
        'KM_Rodagem': 'KM_Rodagem'
    })

    resultado = df[df['Placa'].astype(str).str.upper() == placa.upper()]
    if resultado.empty:
        return f"Veículo {placa.upper()} não encontrado."

    dados = resultado.iloc[0]
    return f"""Veículo: {dados['Placa']}
Revisão 20k - Data: {dados['Data_20k']} | KM: {dados['KM_20k']}
Rodagem - Data: {dados['Data_Rodagem']} | KM: {dados['KM_Rodagem']}"""

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    placa = request.values.get('Body', '').strip().upper()
    resposta = buscar_preventiva(placa)
    msg = MessagingResponse()
    msg.message(resposta)
    return str(msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
