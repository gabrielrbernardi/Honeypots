import pandas as pd
import json
from configparser import ConfigParser

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
            self.outputExcelPath = db["outputExcelPath".lower()]
            self.outputExcelFile = db["outputExcelFile".lower()]

    def openLogFiles(self):
        defaultValue = "cowrie.json.2023-04-"
        logFilename = []
        for i in range(29,31):
            logFilename.append(defaultValue + str(i))
        
        self.logContents = []

        for i in self.regions:
            for j in logFilename:
                tempLogFilename = self.logsPath + i + "\\" + j
                print(tempLogFilename)
                self.logContents.append(pd.read_json(tempLogFilename))
                # f = open(tempLogFilename)
                # self.logContents.append(json.load(f))
                # f.close()

        for idx, elem in enumerate(self.logContents):
            self.logContents[idx] = elem.set_index(["session", "eventid"])
            # print(self.logContents[i])

    def exportLogData(self):
        # with pd.ExcelWriter(self.outputExcelPath + self.outputExcelFile) as writter:
        for idx, elem in enumerate(self.logContents):
            elem.to_csv(self.outputExcelPath +"resultado" + str(idx) + ".csv", index=True)

        
