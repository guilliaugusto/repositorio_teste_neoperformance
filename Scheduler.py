import schedule
import time as tm
from datetime import time, timedelta, datetime
from Main_etl import Export_Data_Sheets


#Agendamento configurado para rodar diariamente às 22h
schedule.every().day.at("22:00").do(Export_Data_Sheets);


while True:
    schedule.run_pending()
    tm.sleep(1)