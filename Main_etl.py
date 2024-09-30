from Google import Create_Service
import pandas as pd
import numpy as np


pd.set_option('display.max_columns', None)

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
gsheetId = '1mD2wNTGP0CphgHhO21rUTnJJFaC_tuU4Os-Jj1Bwqks'

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

def Export_Data_Sheet1():
    #Leitura de arquivo origem
    URL = r'https://raw.githubusercontent.com/guilliaugusto/repositorio_teste_neoperformance/refs/heads/main/base_camp_brasileiro1.csv'
    df = pd.read_csv(URL,sep=';',skiprows=0,decimal=',')
    

    #Tratamentos celulas vazias
    df.replace(np.nan,'',inplace=True)

    cols = ['arbitro','tecnico_mandante','tecnico_visitante']
    df[cols] = df[cols].replace('','Indefinido')

    
    cols = ['idade_media_titular_mandante', 'idade_media_titular_visitante','publico','publico_max','time_mandante','time_visitante','colocacao_mandante','colocacao_visitante','valor_equipe_titular_mandante','valor_equipe_titular_visitante','gols_mandante','gols_visitante','gols_1_tempo_mandante','gols_1_tempo_visitante','escanteios_mandante','escanteios_visitante','faltas_mandante','faltas_visitante','chutes_bola_parada_mandante','chutes_bola_parada_visitante','defesas_mandante','defesas_visitante','impedimentos_mandante','impedimentos_visitante','chutes_mandante','chutes_visitante','chutes_fora_mandante','chutes_fora_visitante']
    df[cols] = df[cols].replace('',0)


    #Tratamento data
    df['dia'] = df['data'].str.slice(8,10)
    df['mes'] = df['data'].str.slice(5,7)
    df['ano'] = df['data'].str.slice(0,4)
    df['ano_mes'] = df['ano'].astype(str) + df['mes'].astype(str)
    df['data'] = df['dia'].astype(str) + '/' + df['mes'].astype(str) + '/' + df['ano'].astype(str)

    del df['dia']
    del df['mes']
    del df['ano']

    #Exclusão dos dados de 2017 para tras, devido a ter muitos indicadores incompletos
    df = df.drop(df[df.ano_campeonato <= 2017].index)


    #Transferencia para planilha google
    service.spreadsheets().values().clear(
        spreadsheetId=gsheetId,
        range='base_brasileirao1'
    ).execute()

    response_date = service.spreadsheets().values().append(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range='base_brasileirao1!A1',
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()



def Export_Data_Sheet2():
    #Leitura de arquivo origem
    URL = r'https://raw.githubusercontent.com/guilliaugusto/repositorio_teste_neoperformance/refs/heads/main/base_camp_brasileiro2.csv'
    df = pd.read_csv(URL,sep=';',skiprows=0,decimal=',')
    

    #Tratamentos celulas vazias
    df.replace(np.nan,'',inplace=True)


    #Transferencia para planilha google
    service.spreadsheets().values().clear(
        spreadsheetId=gsheetId,
        range='base_brasileirao2'
    ).execute()

    response_date = service.spreadsheets().values().append(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range='base_brasileirao2!A1',
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()

def Export_Data_Sheets():
    Export_Data_Sheet1()
    Export_Data_Sheet2()


Export_Data_Sheets()