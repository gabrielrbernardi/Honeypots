import json
import requests
import time

#API Docs: https://ip-api.com/

apiUrl = "http://ip-api.com/json/"

pathFiles01 = []
pathFiles02 = []

folderPath01 = "./Logs/log-sensor1/log/"
folderPath02 = "./Logs/log-sensor2/log/"

attackersCountries = []
attackersCountriesUniques = []

pathFiles01.append(folderPath01 + "cowrie.json.2022-09-16.json")
pathFiles01.append(folderPath01 + "cowrie.json.2022-09-17.json")
pathFiles01.append(folderPath01 + "cowrie.json.2022-09-18.json")
pathFiles01.append(folderPath01 + "cowrie.json.2022-09-19.json")
pathFiles01.append(folderPath01 + "cowrie.json.2022-09-20.json")
pathFiles01.append(folderPath01 + "cowrie.json.2022-09-21.json")
pathFiles01.append(folderPath01 + "cowrie.json.2022-09-22.json")

pathFiles02.append(folderPath02 + "cowrie.json.2022-09-16.json")
pathFiles02.append(folderPath02 + "cowrie.json.2022-09-17.json")
pathFiles02.append(folderPath02 + "cowrie.json.2022-09-18.json")
pathFiles02.append(folderPath02 + "cowrie.json.2022-09-19.json")
pathFiles02.append(folderPath02 + "cowrie.json.2022-09-20.json")
pathFiles02.append(folderPath02 + "cowrie.json.2022-09-21.json")
pathFiles02.append(folderPath02 + "cowrie.json.2022-09-22.json")


relatorio = ""

def searchIp(ip):
    cont = 0
    tInit = time.time()
    for x in ip:
        part01 = time.time()
        time.sleep(1.1)
        # print(".", end="", flush=True)
        response = requests.get(apiUrl + x)
        res = response.json()
        if res:
            country = res["country"]
        attackersCountries.append(country)
        if country not in attackersCountriesUniques:
            attackersCountriesUniques.append(country)
        cont += 1
        part02 = time.time()
        # print(chr(27) + "[2J")
        # print()
        print(str(round(part02 - part01, 4)) + " ", end="", flush=True)
    tEnd = time.time()
    if cont <= 0:
        cont = 1
    print("Tempo medio por requisicao: " + str((tEnd - tInit) / cont))

def openLogFile(files):
    connectionsSuccessfully = 0
    connectionsNotSuccessfully = 0

    connectionDuration = 0.0

    protocolTelnet = 0
    protocolSSH = 0

    inputCommandsSuccessfully = 0
    inputCommandsNotSuccessfully = 0
    inputCommands = []

    srcIp = []
    srcPort = []
    dstPort = []
    jsonContentFiles = []


    for file in files:
        tempFile = open(file)
        jsonContentFiles.append(json.load(tempFile))
        for jsonFileConverted in jsonContentFiles:
            keysList = []
            for x in jsonFileConverted["data"]:
                for y in x:
                    
                    if y not in keysList:
                        keysList.append(y)
            
                    if y == "eventid":
                        if x[y] == "cowrie.session.connect":
                            connectionsSuccessfully += 1
                        if x[y] == "cowrie.login.failed":
                            connectionsNotSuccessfully += 1
                        if x[y] == "cowrie.command.input":
                            inputCommands.append(x["input"])
                            inputCommandsSuccessfully += 1
                        if x[y] == "cowrie.command.failed":
                            inputCommands.append(x["input"])
                            inputCommandsNotSuccessfully += 1
                    
                    if y == "duration":
                        connectionDuration += x[y]

                    if y == "protocol":
                        if x[y] == "telnet":
                            protocolTelnet += 1
                        if x[y] == "ssh":
                            protocolSSH += 1
                    
                    if y == "src_ip" and x[y] not in srcIp:
                        srcIp.append(x[y])
                    
                    if y == "src_port" and x[y] not in srcPort:
                        srcPort.append(x[y])
                    
                    if y == "dst_port" and x[y] not in dstPort:
                        dstPort.append(x[y])

    global relatorio
    relatorio += ("Quantidade total de conexoes: " + str(connectionsSuccessfully + connectionsNotSuccessfully)) + "\n"
    relatorio += ("Conexoes bem sucedidas: " + str(connectionsSuccessfully)) + "\n"
    relatorio += ("Conexoes mal sucedidas: " + str(connectionsNotSuccessfully)) + "\n"
    if connectionsSuccessfully == 0:
        divisor = 1
    else:
        divisor = connectionsSuccessfully
    relatorio += ("Tempo medio por conexao: " + str(connectionDuration/divisor)) + "\n"
    relatorio += ("Quantidade conexoes Telnet: " + str(protocolTelnet) + " Porcentagem: " + str(round(protocolTelnet/divisor * 100, 2)) + "%") + "\n"
    relatorio += ("Quantidade conexoes SSH: " + str(protocolSSH) + " Porcentagem: " + str(round(protocolSSH/divisor * 100, 2)) + "%") + "\n"
    
    # for x in inputCommands:
    #     relatorio += (x + ": " + str(inputCommands.count(x))) + "\n"
    relatorio += ("Quantidade comandos inseridos: " + str(len(inputCommands))) + "\n"
    relatorio += ("Quantidade comandos bem sucedidos: " + str(inputCommandsSuccessfully)) + "\n"
    relatorio += ("Quantidade comandos mal sucedidos: " + str(inputCommandsNotSuccessfully)) + "\n"
    
    choose01 = input("Deseja visualizar os comandos? (S/N) ")
    if choose01 == "S" or choose01 == "s":
        relatorio += ("Comandos Executados: " + str(inputCommands)) + "\n"
        
    relatorio += ("Quantidade de diferentes atacantes: " + str(len(srcIp))) + "\n"

    choose02 = input("Procurar Paises? (S/N) ")
    if choose02 == "S" or choose02 == "s":
        searchIp(srcIp)

    relatorio += ("Paises:\n" + str(attackersCountries)) + "\n"
    relatorio += ("Paises unicos:\n" + str(attackersCountriesUniques)) + "\n"

    choose03 = input("Ver lista de portas de origem? (S/N) ")
    if choose03 == "S" or choose03 == "s":
        srcPort.sort()
        relatorio += ("Portas de origem: " + str(srcPort)) + "\n"
    
    dstPort.sort()
    relatorio += ("Portas de destino: " + str(dstPort)) + "\n"

t0 = time.time()
relatorio += "Maquina 01" + "\n"
openLogFile(pathFiles01)
relatorio += "\n\nMaquina 02" + "\n"
openLogFile(pathFiles02)
fileOutput = open("saida.txt", "w")
fileOutput.write(relatorio)

t1 = time.time()
final = t1 - t0
print("Tempo execucao: " + str(final))
