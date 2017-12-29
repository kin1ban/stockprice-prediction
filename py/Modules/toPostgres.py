# -*- coding: utf-8 -*-
import psycopg2 as psy
import pandas as pd
import json

class accessDB:
    #DBÚ±
    db_settings = {
        "host": "ec2-107-20-250-195.compute-1.amazonaws.com",
        "database": "dft7cdnj89sr19",
        "user": "uucnfvpykhhesw",
        "password": "f9d4fb3bcff7513a6f59682364418a658cd6be45d9ed8807ddba39cad56b5236",
        "port":5432
    }

    
    def __init__(self, code, start):
        self.code = code
        self.start = start
        #Quandl登録後に発行されるやつ
        self.apikey = '7m8muCv78TurSwmB5FHd'


    def insertStockData(self):
        import requests
        from datetime import datetime
        
        code = self.code 
        start = self.start #データの取得開始日
        end = datetime.now()
        apikey = self.apikey
        market = "TSE"  #取引所のコード TSE=東京証券取引所
        
        #Quandl
        url = "https://www.quandl.com/api/v3/datasets/" + market + "/" + code
        params = {
          'start_date': start,
          'end_date': end,
          'api_key': apikey
        }
        
        #JSON取得
        r = requests.get(url, params=params)

        #DataFrame作成
        x = json.loads(r.text)
        df = pd.DataFrame(x['dataset']['data'], columns = x['dataset']['column_names'])
        
        #csv出力(不要)
        #df.to_csv(str(code) + ".csv", index=False)
        
        print('Quandlより情報を取得')
                
        #DBとのConnectionを取得
        connection = psy.connect("host={host} port={port} dbname={database} user={user} password={password}".format(**accessDB.db_settings))
        connection.get_backend_pid()
        cur = connection.cursor()
        #接続確認
        print(cur)
        
        #データ削除
        cur.execute("DELETE FROM stock_price")
        
        
        l = []
        
        for i,row in df.iterrows():
            #市場コード、株式コード、日付、始値、高値、安値、終値
            t = (market,code,row[0],row[1],row[2],row[3],row[4])
            l.append(t)
            
        #INSERT文発行
        cur.executemany("INSERT INTO stock_price (\"StockExchangeCode\",\"StockCode\",\"Date\",\"Open\",\"High\",\"Low\",\"Close\") " + 
                        "values(%s,%s,%s,%s,%s,%s,%s)"
                        ,l)
        connection.commit()
        cur = connection.cursor()
        l = []
        connection.close()

    def getData(self):
        print('DBからデータを取得します')
        connection = psy.connect("host={host} port={port} dbname={database} user={user} password={password}".format(**accessDB.db_settings))    
        # DataFrameでロード
        return pd.read_sql(sql="SELECT * FROM stock_price;", con=connection )