from celery import Celery
import pandas as pd

# Configurando o Celery com o broker RabbitMQ
app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672//')

@app.task
def processar_excel(arquivo='C:\\Users\\Igor Moreira\\Downloads\\dados_e_requirements\\data\\dados_dias_atras.csv'):
    # Carrega o arquivo Excel para um DataFrame
    df = pd.read_excel(arquivo)

    # Executa uma filtragem simples nos dados
    df_filtrado = df[df['coluna'] > 10]

    # Exporta o resultado para um novo arquivo Excel
    novo_caminho = 'caminho_processado.xlsx'
    df_filtrado.to_excel(novo_caminho, index=False)

    return f"Processamento concluído, arquivo salvo em {novo_caminho}"
