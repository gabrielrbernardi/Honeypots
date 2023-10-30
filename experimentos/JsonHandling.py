import pandas as pd
import json
import fileinput
import os, glob
from configparser import ConfigParser

class JsonHandling():
    def __init__(self):
        parser = ConfigParser()
        parser.read("/mnt/c/gabriel/UFU/honeypots/Honeypots/experimentos/config.ini")

        db = {}
        if parser.has_section("logs"):
            params = parser.items("logs")
            for param in params:
                db[param[0]] = param[1]

            self.logsPath = db["logspath".lower()]

    def readFiles(self):
        self.files = []
        
        os.chdir(self.logsPath)
        for file in glob.glob("*.json*"):
            if os.stat(file).st_size > 0: #arquivos nao vazios
                self.files.append(self.logsPath + "/" + file)

    def modifyJsonFiles(self):
        fileContent = []
        
        for file in self.files:
            print(file)
            for line in fileinput.input(file, inplace=True):
                if 1 != fileinput.filelineno():
                    print(',{}'.format(line), end='')
                else:
                    print('[{}'.format(line), end='')
            open(file,"a").write(']')

            # f = open(file, "r")
            # content = f.readlines()
            # qtdLines = len(content)
            # print(file, "linhas", qtdLines)
            # for i in range(qtdLines - 1):
            #     fileContent.append(content[i][:-1] + ",\n")
            # fileContent.append(content[qtdLines - 1])
            # f.close()
            
            # f = open(file, "w")
            # f.write('[\n')
            # for i in fileContent:
            #     f.write(i)

            # f.write("]")
            # f.close()

    def readJsonFiles(self):
        self.dataframes = []
        for i in range(len(self.files)):
            print(self.files[i])
            self.dataframes.append(pd.read_json(self.files[i], orient=str))
        
        # df = self.dataframes[0].append(self.dataframes[1], ignore_index=True)
        df = pd.concat([self.dataframes[0], self.dataframes[1]])
        for i in range(2, len(self.dataframes)):
            df = pd.concat([df, self.dataframes[i]])
        
        df.to_csv("/mnt/c/gabriel/UFU/honeypots/Honeypots/experimentos/saida.csv", index=False)
        