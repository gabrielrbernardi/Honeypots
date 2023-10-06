import sqlite3
import pandas as pd
class AnalyseLogs():
    def __init__(self):
        self.con = sqlite3.connect("honeypotLogs.sqlite")
        self.cur = self.con.cursor()

    def fetchData(self):        
        self.regioes = [
            "asia_east2",
            "europe_west3",
            "me_west1",
            "southamerica_east1",
            "us_west2"
        ]

        for regiao in self.regioes:
            self.df = pd.DataFrame()
            self.df = pd.read_sql_query(f"select * from {regiao}", self.con)
            print()
            print(".", end=" ", flush=True)
            # self.linhas = self.df
            self.ipv6 = self.df.loc[(self.df["dst_ip"].str.contains("[a-z A-Z 0-9]+::", regex=True)) & (self.df["eventid"] == "cowrie.session.connect")]
            print(".", end=" ", flush=True)
            self.conexoesGerais = self.df.loc[(self.df["eventid"] == "cowrie.session.connect")]
            print(".", end=" ", flush=True)
            self.conexoesSSH = self.df.loc[(self.df["eventid"] == "cowrie.session.connect") & (self.df["protocol"] == "ssh")]
            print(".", end=" ", flush=True)
            self.conexoesTelnet = self.df.loc[(self.df["eventid"] == "cowrie.session.connect") & (self.df["protocol"] == "telnet")]
            print(".", end=" ", flush=True)
            self.conexoesSucesso = self.df.loc[(self.df["eventid"] == "cowrie.login.success")]
            print(".", end=" ", flush=True)
            self.conexoesSucessoAleatorio = self.df.loc[(self.df["eventid"] == "cowrie.login.success") & (self.df["sensor"].str.contains("[a-z A-Z 0-9]+-instance-01", regex=True))]
            print(".", end=" ", flush=True)
            self.conexoesSucessoPasslist = self.df.loc[(self.df["eventid"] == "cowrie.login.success") & (self.df["sensor"].str.contains("[a-z A-Z 0-9]+-instance-02", regex=True))]
            print(".", end=" ", flush=True)
            self.conexoesFalha = self.df.loc[(self.df["eventid"] == "cowrie.login.failed")]
            print(".", end=" ", flush=True)
            self.conexoesFalhaAleatorio = self.df.loc[(self.df["eventid"] == "cowrie.login.failed") & (self.df["sensor"].str.contains("[a-z A-Z 0-9]+-instance-01", regex=True))]
            print(".", end=" ", flush=True)
            self.conexoesFalhaPasslist = self.df.loc[(self.df["eventid"] == "cowrie.login.failed") & (self.df["sensor"].str.contains("[a-z A-Z 0-9]+-instance-02", regex=True))]
            
            self.showData(regiao)
            
    def showData(self, nomeRegiao):
        print()
        print(f"Regiao: {nomeRegiao}")
        # print(self.ipv6)
        print(f"{'Quantidade IPv6:':<30} \033[36m{str(len(self.ipv6)):>30}\033[0m")
        if(len(self.ipv6)):
            self.sessionsIpv6 = []
            self.ipv6.apply(self.getSessionIpv6, axis=1)
            print(self.sessionsIpv6)
        print(f"{'Conexoes Gerais:':<30} {str(len(self.conexoesGerais)):>30}")
        print(f"{'SSH':<30} {str(len(self.conexoesSSH)):>30}")
        print(f"{'Telnet':<30} {str(len(self.conexoesTelnet)):>30}")
        print(f"{'Conexoes Sucesso':<30} \033[92m{str(len(self.conexoesSucesso)):>30}\033[0m")
        print(f"{'Conexoes Sucesso Aleatorio':<30} {str(len(self.conexoesSucessoAleatorio)):>30}")
        print(f"{'Conexoes Sucesso Passlist':<30} {str(len(self.conexoesSucessoPasslist)):>30}")
        print(f"{'Conexoes Falha':<30} \033[91m{str(len(self.conexoesFalha)):>30}\033[0m")
        print(f"{'Conexoes Falha Aleatorio':<30} {str(len(self.conexoesFalhaAleatorio)):>30}")
        print(f"{'Conexoes Falha Passlist':<30} {str(len(self.conexoesFalhaPasslist)):>30}")

    def getSessionIpv6(self, linha):
        self.sessionsIpv6.append(linha["session"])
        return linha