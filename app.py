from flask import Flask, render_template, request
import requests #biblioteca para fazer requisições HTTP à API

app = Flask(__name__)

API_ENDPOINT = "https://brasilapi.com.br/api/cep/v1/"

Sudeste = ["SP", "RJ", "MG", "ES"]
Sul = ["PR", "SC", "RS"]
CentroOeste = ["MT", "MS", "GO", "DF"]
Nordeste =["BA", "SE", "AL", "PE", "PB", "RN", "CE", "PI", "MA"]
Norte = ["AM", "RR", "AP", "PA", "TO", "RO", "AC"]

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        cep = request.form.get('cep', default=0)
        peso = request.form.get('peso', type=float, default=0)
        response = requests.get(API_ENDPOINT + cep)

        if peso <= 0:
            return render_template('index.html', erro = "Peso inválido!")

        if response.status_code == 200: #tipo erro 404, 200 é que deu certo
            data = response.json() #convertendo para json
            destino = data['city']
            estado = data['state'] #pegando a cotação
            print(estado)
            if estado in Sudeste:
                frete = 0.05
                tempo = 3
            elif estado in Sul:
                frete = 0.06
                tempo = 7
            elif estado in CentroOeste:
                frete = 0.07
                tempo = 5
            elif estado in Nordeste:
                frete = 0.08
                tempo = 10
            elif estado in Norte:
                frete = 0.10
                tempo = 12
            else:
                print("frete 0 ")
            valor_final = peso * frete #calculando o valor final
            return render_template('index.html', valor_final=f'{valor_final:.2f}', tempo=tempo, destino=destino, estado=estado)
        elif response.status_code == 400:
            return render_template('index.html', erro = "CEP inválido!")
        else:
            return render_template('index.html', erro = "Falha de API, volte mais tarde!") #tratando erro de api
    return render_template('index.html') #se for get
app.run(debug=True)
