import paramiko
from configparser import ConfigParser
import SCPClient
import json
import os
class ConnectInstances():
    def __init__(self):
        pass
    
    def readConfigFile(self):
        parser = ConfigParser()
        parser.read("C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\config.ini")

        db = {}
        if parser.has_section("credentials"):
            params = parser.items("credentials")
            for param in params:
                db[param[0]] = param[1]
            
            self.defaultSSHPort = db["defaultSSHPort".lower()]
            self.defaultSSHUsername = db["defaultSSHUsername".lower()]
            self.defaultSSHPassword = db["defaultSSHPassword".lower()]
            self.dateLog = db["dateLog".lower()]
            self.jsonFilePath = db["jsonFilePath".lower()]

        # read connection values from all instances
        self.getInstancesData()
        # f = open(self.jsonFilePath, "r")
        # self.instances = json.load(f)
        # f.close()
        # print(self.instances)

    def getInstancesData(self):
        regions = ['us-west2', 'southamerica-east1', 'europe-west3', 'me-west1', 'asia-east2']
        intancesData = os.popen("gcloud compute instances list")
        print(intancesData)

    def getRemoteData(self, ipAddress, region, instanceName, flag = False):
        def createSSHClient(server, port, user, password):
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, port, user, password)
            return client

        ssh = createSSHClient(ipAddress, self.defaultSSHPort, self.defaultSSHUsername, self.defaultSSHPassword)
        scp = scp.SCPClient(ssh.get_transport())

        if flag:
            scp.get('/home/cowrie/cowrie/var/log/cowrie/cowrie.json', "C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\"+ region + "\\" + instanceName + "-cowrie.json." + self.dateLog.replace("10", "11"))
        else:
            for i in range(1,11):
                scp.get('/home/cowrie/cowrie/var/log/cowrie/cowrie.json.' + self.dateLog.replace("10", str(i).zfill(2)), "C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\"+ region + "\\" + instanceName + "-cowrie.json." + self.dateLog.replace("10", str(i).zfill(2)))

        scp.close()
    
    def connectInstances(self):
        for i in self.instances:
            print("\nRegiao: " + i)
            for j in self.instances[i]:
                print("Instancia: " + j["name"] + " (" + j["ip"] + ")")
                self.getRemoteData(j["ip"], i, j["name"])
                self.getRemoteData(j["ip"], i, j["name"], True)