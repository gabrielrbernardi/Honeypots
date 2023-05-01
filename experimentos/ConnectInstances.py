import paramiko
from configparser import ConfigParser
from scp import SCPClient
import json

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
        f = open(self.jsonFilePath, "r")
        self.instances = json.load(f)
        f.close()
        print(self.instances)

    def getRemoteData(self, ipAddress, region, instanceName):
        def createSSHClient(server, port, user, password):
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, port, user, password)
            return client

        ssh = createSSHClient(ipAddress, self.defaultSSHPort, self.defaultSSHUsername, self.defaultSSHPassword)
        scp = SCPClient(ssh.get_transport())

        scp.get('/home/cowrie/cowrie/var/log/cowrie/cowrie.json.' + self.dateLog, "C:\\Users\\gabri\\Documentos\\UFU\\Honeypots\\experimentos\\logs\\"+ region + "\\" + instanceName + "-cowrie.json." + self.dateLog)

        scp.close()
    
    def connectInstances(self):
        for i in self.instances:
            print("\nRegiao: " + i)
            for j in self.instances[i]:
                print("Instancia: " + j["name"] + " (" + j["ip"] + ")")
                self.getRemoteData(j["ip"], i, j["name"])