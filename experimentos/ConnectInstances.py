import paramiko
from configparser import ConfigParser
import scp
from scp import SCPClient
import json
import os
import subprocess
import datetime

class ConnectInstances():
    def __init__(self):
        pass

    def readConfigFile(self):
        parser = ConfigParser()
        # parser.read("C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\config.ini")
        # parser.read("/home/gribeiro/logs/Honeypots/experimentos/config.ini")
        parser.read("/mnt/c/gabriel/UFU/honeypots/Honeypots/experimentos/config.ini")

        db = {}
        if parser.has_section("credentials"):
            params = parser.items("credentials")
            for param in params:
                db[param[0]] = param[1]

            self.defaultSSHPort = db["defaultSSHPort".lower()]
            self.defaultSSHUsername = db["defaultSSHUsername".lower()]
            self.defaultSSHPassword = db["defaultSSHPassword".lower()]
            # self.dateLog = db["dateLog".lower()]
            self.dateLog = datetime.datetime.now().strftime("%Y-%m-%d")
            self.jsonFilePath = db["jsonFilePath".lower()]

        # read connection values from all instances
        # self.getInstancesData()
        f = open(self.jsonFilePath, "r")
        self.instances = json.load(f)
        f.close()
        # print(self.instances)

    def getInstancesData(self):
        regions = ['us-west2', 'southamerica-east1', 'europe-west3', 'me-west1', 'asia-east2']
        intancesData = subprocess.Popen("gcloud compute instances list | grep -v 'NAME'", shell=True, stdout=subprocess.PIPE).stdout
        print("gcloud compute instances list")
        print(1, intancesData)

    def getRemoteData(self, ipAddress, region, instanceName, flag = False):
        def createSSHClient(server, port, user, password):
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, port, user, password)
            return client

        ssh = createSSHClient(ipAddress, self.defaultSSHPort, self.defaultSSHUsername, self.defaultSSHPassword)

        # verificacao se existe arquivo de log para ser baixado
        _, stdout, _ = ssh.exec_command("find /home/cowrie/cowrie/var/log/cowrie/ -name 'cowrie.json.2*'")
        output = stdout.read()
        resposta_busca = output.decode("utf-8")
        scpCon = scp.SCPClient(ssh.get_transport())

        if resposta_busca == "": #se nao encontrar dados de log por dia, baixa o arquivo de log existente
            scpCon.get('/home/cowrie/cowrie/var/log/cowrie/cowrie.json', "/data/honeypots/ipv6/exp_1/logsColeta/" + instanceName + "-cowrie.json." + self.dateLog + ".empty")
        else: #senao, baixara todos os arquivos de log existentes
            arquivos_log = resposta_busca.split("\n")
            for arquivo in arquivos_log:
                log_arquivo_nome = arquivo.split("/")[len(arquivo.split("/")) - 1]
                print(log_arquivo_nome)
                scpCon.get(arquivo, "/data/honeypots/ipv6/exp_1/logsColeta/" + instanceName + "-" + log_arquivo_nome)

        scpCon.close()

    def connectInstances(self):
        for i in self.instances:
            print("\nRegiao: " + i)
            for j in self.instances[i]:
                print("Instancia: " + j["name"] + " (" + j["ip"] + ")")
                self.getRemoteData(j["ip"], i, j["name"])
