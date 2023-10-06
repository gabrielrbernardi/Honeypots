import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import sqlite3
import os

class GenerateDB1():
    def __init__(self) -> None:
        self.directories = [
            'C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\asia-east2', 
            'C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\europe-west3', 
            'C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\me-west1', 
            'C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\southamerica-east1', 
            'C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\us-west2'
        ]
        
        self.json_files = []
        for directory in self.directories:
            self.json_files += [os.path.join(directory, file) for file in os.listdir(directory) if file.find('.json')]

        self.dataframes = {}
        for file in self.json_files:
            directory_name = os.path.dirname(file)
            if directory_name not in self.dataframes:
                self.dataframes[directory_name] = pd.DataFrame()
            print(file)
            tempVar = pd.read_json(file, lines=True)
            tempVar = tempVar.astype(str)
            self.dataframes[directory_name] = self.dataframes[directory_name].append(tempVar)

        # print(self.dataframes)

        conn = sqlite3.connect('honeypotLogs.sqlite')
        for directory_name, df in self.dataframes.items():
            table_name = os.path.basename(directory_name).replace("-", "_")
            df.to_sql(table_name, conn, if_exists='replace')

        conn.close()