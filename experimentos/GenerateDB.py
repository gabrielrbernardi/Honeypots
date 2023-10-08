import pandas as pd
import json
from configparser import ConfigParser
# import openpyxl
from sqlalchemy import create_engine
import sqlite3

class GenerateDB():
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
        # for i in range(1,12):
        for i in range(1,12):
            logFilename.append(defaultValue + str(i).zfill(2))

        print(logFilename)
        
        self.logContents = []
        instanceLabel = "-instance-0"

        tempDataFrames = []
        self.qtdIpv6 = 0
        for idx, region in enumerate(self.regions):
            # quantidade de tipos de acesso
            for idx2 in range(2):
                for _, tempFilename in enumerate(logFilename):
                    tempLogFilename = self.logsPath + region + "\\" + (region + instanceLabel + str((idx2 % 2) + 1) + "-" + tempFilename)
                    print(tempLogFilename)
                    tempVar = pd.read_json(tempLogFilename, lines=True)
                    tempDataFrames.append(tempVar)
                    tempVar.apply(self.checkValues, axis = 1)
        
        
        cont = 0
        for i in range(5):
            tempList = []
            for _ in range(2):
                tempList.append(tempDataFrames[cont])
                cont+=1
            # Juntando dataframes por regiao
            tempDf = pd.concat(tempList)
            tempDf = tempDf.astype(str)
            # print(tempDf[tempDf["eventid"] == "cowrie.session.connect" return tempDf["dst_ip"]])
            # tempDf.apply(lambda x: (qtdIpv6+=1) if (x["dst_ip"].find("2600:190") != -1 and x["eventid"] == "cowrie.session.connect") else "", axis = 1)
            self.logContents.append(tempDf)
        print(self.qtdIpv6)

        # print(self.logContents[4]["sensor"])
        # exit()

        # print(type(self.logContents[0]))
            
        # for idx, elem in enumerate(self.logContents):
        #     self.logContents[idx] = elem.set_index(["session", "eventid"])
        #     print(self.logContents[i])

    def checkValues(self, linha):
        if linha["eventid"] == "cowrie.session.connect" and linha["dst_ip"].find("2600:190") != -1:
            self.qtdIpv6 += 1

    def exportLogData(self):
        # disk_engine = create_engine('sqlite:///my_lite_store.sqlite')
        conn = sqlite3.connect('honeypotLogs.sqlite')

        for idx, elem in enumerate(self.logContents):
            table_name = self.regions[idx].replace("-","_")
            # table_name = 'df_' + str(idx)
            # print(elem["sensor"])
            schema = ','.join(['{} TEXT'.format(col) for col in elem.columns])
            # conn.execute('DROP  TABLE {}'.format(table_name))
            conn.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, schema))

            # insert the data into the table
            for row in elem.itertuples(index=False):
                placeholders = ','.join(['?'] * len(row))
                try:
                    conn.execute('INSERT INTO {} VALUES ({})'.format(table_name, placeholders), row)
                except:
                    print(row)
                    exit()

        conn.commit()
        conn.close()
                
            # for row in elem.itertuples(index=False):
            #     conn.execute('INSERT INTO {} VALUES ({})'.format("tabela_"+str(idx)), row)
            # elem.to_sql(name=str(idx), con=disk_engine, if_exists='append', escapechar='\\')


        # with pd.ExcelWriter(self.outputExcelPath + self.outputExcelFile) as writter:
                # elem.to_excel(writter, str(idx), index=True)
                # elem.to_csv(self.outputExcelPath +"resultado" + str(idx) + ".csv", index=True)
