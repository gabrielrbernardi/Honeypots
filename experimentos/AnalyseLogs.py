import pandas as pd
import json
from configparser import ConfigParser
# import openpyxl
from sqlalchemy import create_engine
import sqlite3

class AnalyseLogs():
    def __init__(self) -> None:
        pass

    def readConfigFile(self):
        parser = ConfigParser()
        parser.read("C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\config.ini")

        db = {}
        if parser.has_section("logs"):
            params = parser.items("logs")
            for param in params:
                db[param[0]] = param[1]
            
            self.logsPath = db["logsPath".lower()]
            self.regions = []
            self.regions.append(db["region01".lower()])
            self.regions.append(db["region02".lower()])
            self.regions.append(db["region03".lower()])
            self.regions.append(db["region04".lower()])
            self.regions.append(db["region05".lower()])
            self.outputExcelPath = db["outputExcelPath".lower()]
            self.outputExcelFile = db["outputExcelFile".lower()]

    def openLogFiles(self):
        defaultValue = "cowrie.json.2023-05-"
        logFilename = []
        for i in range(1,3):
            logFilename.append(defaultValue + str(i).zfill(2))

        print(logFilename)
        
        self.logContents = []
        instanceLabel = "-instance-0"

        tempDataFrames = []
        for idx, region in enumerate(self.regions):
            # quantidade de tipos de acesso
            for idx2 in range(2):
                for _, tempFilename in enumerate(logFilename):
                    tempLogFilename = self.logsPath + region + "\\" + (region + instanceLabel + str((idx2 % 2) + 1) + "-" + tempFilename)
                    print(tempLogFilename)
                    tempDataFrames.append(pd.read_json(tempLogFilename, lines=True))
            
            # Juntando dataframes por regiao
            tempDf = pd.concat(tempDataFrames)
            tempDf = tempDf.astype(str)
            self.logContents.append(tempDf)
            
        # for idx, elem in enumerate(self.logContents):
        #     self.logContents[idx] = elem.set_index(["session", "eventid"])
            # print(self.logContents[i])

    def exportLogData(self):
        # disk_engine = create_engine('sqlite:///my_lite_store.sqlite')
        conn = sqlite3.connect('honeypotLogs.sqlite')

        for idx, elem in enumerate(self.logContents):
            table_name = 'df_' + str(idx)
            schema = ','.join(['{} TEXT'.format(col) for col in elem.columns])
            conn.execute('DROP  TABLE {}'.format(table_name))
            conn.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, schema))

            # insert the data into the table
            for row in elem.itertuples(index=False):
                placeholders = ','.join(['?'] * len(row))
                conn.execute('INSERT INTO {} VALUES ({})'.format(table_name, placeholders), row)

        conn.commit()
        conn.close()
                
            # for row in elem.itertuples(index=False):
            #     conn.execute('INSERT INTO {} VALUES ({})'.format("tabela_"+str(idx)), row)
            # elem.to_sql(name=str(idx), con=disk_engine, if_exists='append', escapechar='\\')


        # with pd.ExcelWriter(self.outputExcelPath + self.outputExcelFile) as writter:
                # elem.to_excel(writter, str(idx), index=True)
                # elem.to_csv(self.outputExcelPath +"resultado" + str(idx) + ".csv", index=True)
