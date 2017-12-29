# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:27:54 2017

@author: yuki.yamaguchi
"""
class main:

    from Modules import toPostgres
    from flask import Flask
    app = Flask(__name__)

    @app.route('/colectData')
    def addStock(code, start_date):                
        stockCodeData = main.toPostgres.accessDB(code,start_date)
        print('株価情報登録スタート:')
        stockCodeData.insertStockData()
        print('株価コード' + code + 'のデータが登録されました')
        
    
    @app.route('/train')
    def getStock():
        ins = main.toPostgres.accessDB('','')
        return ins.getData()
        


main.addStock('3915', '2017-12-01')
print(main.getStock())
