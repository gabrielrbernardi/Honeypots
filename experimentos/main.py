import paramiko
from configparser import ConfigParser
from scp import SCPClient

class Main():
    def __init__(self):
        # Configuracoes de conexao as instancias
        self.instances = {
            "europe-west1-b": [
                {
                    "name": "europe-west-1-maquina-01",
                    "ip": "34.140.133.163",
                },
            ],
            "southamerica-east1": [],
            "us-west2": [],
            "europe-west3": [],
            "me-west1": [],
            "asia-east2": []
        }
    
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
                print("Instancia: " + j["name"])
                self.getRemoteData(j["ip"], i, j["name"])

main = Main()
main.readConfigFile()
main.connectInstances()