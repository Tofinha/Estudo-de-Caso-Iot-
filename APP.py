from flask import Flask, request, jsonify
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Função para processar o arquivo e retornar os dados processados
def processar_arquivo(caminho_arquivo):
    try:
        file_ext = os.path.splitext(caminho_arquivo)[1].lower()

        # Ler o arquivo conforme a extensão
        if file_ext == '.csv':
            df = pd.read_csv(caminho_arquivo)
        elif file_ext in ('.xls', '.xlsx'):
            df = pd.read_excel(caminho_arquivo)
        else:
            return {'error': 'Formato não suportado'}

        # Processamento de dados
        if 'nome' in df.columns:
            df['nome'] = df['nome'].str.upper()

        if 'idade' in df.columns:
            df = df[df['idade'] > 18]
            df['categoria'] = df['idade'].apply(lambda x: 'Adulto' if x >= 18 else 'Menor')

        # Simular cálculo de probabilidade de chuva baseado na umidade
        if 'umidade' in df.columns:
            df['probabilidade_chuva'] = df['umidade'].apply(lambda x: round(x / 100, 2))

        return {'status': 'success', 'processed_data': df.to_dict(orient='records')}

    except Exception as e:
        return {'error': str(e)}

# Rota para upload de arquivo
@app.route('/upload', methods=['POST'])
def upload_arquivo():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    arquivo = request.files['file']
    
    if arquivo.filename == '':
        return jsonify({'error': 'Nome de arquivo inválido'}), 400

    try:
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, arquivo.filename)
        arquivo.save(caminho_arquivo)

        # Processar o arquivo e obter os dados processados
        resultado = processar_arquivo(caminho_arquivo)

        return jsonify(resultado), 200 if 'processed_data' in resultado else 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
