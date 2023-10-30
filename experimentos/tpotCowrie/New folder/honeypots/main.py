import json


def getCowrieLogsInformation(nameFile):
    with open(nameFile + ".json", encoding='utf-8') as meu_json:
        dados = [json.loads(line) for line in open(nameFile + '.json', 'r')]

    count = 0
    eventIdTypes = set()

    cowrieClientFingerprint = []
    cowrieLoginSuccess = []
    cowrieLoginFailed = []
    cowrieClientSize = []
    cowrieSessionFileUpload = []
    cowrieCommandInput = []
    cowrieVirustotalScanfile = []
    cowrieSessionConnect = []
    cowrieClientVersion = []
    cowrieClientKex = []
    cowrieSessionClosed = []
    cowrieLogClosed = []
    cowrieDirectTcpipRequest = []
    cowrieDirectTcpipData = []
    cowrieClientVar = []
    cowrieSessionParams = []
    cowrieCommandFailed = []

    cowrieSessionDuration = (0, [])
    usedCommands = set()
    srcIps = set()

    for i in dados:
        if i["eventid"] == 'cowrie.client.fingerprint':
            cowrieClientFingerprint.append(i)
        elif i["eventid"] == 'cowrie.login.success':
            cowrieLoginSuccess.append(i)
        elif i["eventid"] == 'cowrie.login.failed':
            cowrieLoginFailed.append(i)
        elif i["eventid"] == 'cowrie.client.size':
            cowrieClientSize.append(i)
        elif i["eventid"] == 'cowrie.session.file_upload':
            cowrieSessionFileUpload.append(i)
        elif i["eventid"] == 'cowrie.command.input':
            cowrieCommandInput.append(i)
            usedCommands.add(i["input"])
        elif i["eventid"] == 'cowrie.virustotal.scanfile':
            cowrieVirustotalScanfile.append(i)
        elif i["eventid"] == 'cowrie.session.connect':
            cowrieSessionConnect.append(i)
            srcIps.add(i["src_ip"])
        elif i["eventid"] == 'cowrie.client.version':
            cowrieClientVersion.append(i)
        elif i["eventid"] == 'cowrie.client.kex':
            cowrieClientKex.append(i)
        elif i["eventid"] == 'cowrie.session.closed':
            cowrieSessionClosed.append(i)
            cowrieSessionDuration = (
                float(i["duration"]) + cowrieSessionDuration[0], cowrieSessionDuration[1] + [float(i["duration"])])
        elif i["eventid"] == 'cowrie.log.closed':
            cowrieLogClosed.append(i)
        elif i["eventid"] == 'cowrie.direct-tcpip.request':
            cowrieDirectTcpipRequest.append(i)
        elif i["eventid"] == 'cowrie.direct-tcpip.data':
            cowrieDirectTcpipData.append(i)
        elif i["eventid"] == 'cowrie.client.var':
            cowrieClientVar.append(i)
        elif i["eventid"] == 'cowrie.session.params':
            cowrieSessionParams.append(i)
        elif i["eventid"] == 'cowrie.command.failed':
            cowrieCommandFailed.append(i)
            usedCommands.add(i["input"])

        eventIdTypes.add(i["eventid"])
        count = count + 1
        # print(i)

    arquivo = open('report' + nameFile + '.txt', 'w')
    arquivo.write('---- SEÇÕES ----')
    arquivo.write('\nIniciadas: ' + str(len(cowrieSessionConnect)))
    arquivo.write('\nEncerradas: ' + str(len(cowrieSessionClosed)))
    arquivo.write('\nDuração média: ' + str(cowrieSessionDuration[0] / len(cowrieSessionDuration[1])))
    arquivo.write('\nIPs doa atacantes: ' + str(srcIps))

    arquivo.write('\n\n---- LOGINS ----')
    arquivo.write('\nCom sucesso: ' + str(len(cowrieLoginSuccess)))
    arquivo.write('\nSem sucesso: ' + str(len(cowrieLoginFailed)))

    arquivo.write('\n\n---- COMANDOS ----')
    arquivo.write('\nInseridos : ' + str(len(cowrieCommandInput)))
    arquivo.write('\nFalharam: ' + str(len(cowrieCommandFailed)))
    arquivo.write('\nLista de comandos:' + str(usedCommands))

    arquivo = open('report' + nameFile + '.json', 'w')
    arquivo.write('{')
    arquivo.write('"averageCowrieSessionConnect": ' + str(len(cowrieSessionConnect)))
    arquivo.write(',"averageCowrieSessionClosed": ' + str(len(cowrieSessionClosed)))
    arquivo.write(',"averageCowrieSessionDuration": ' + str(cowrieSessionDuration[0] / len(cowrieSessionDuration[1])))
    arquivo.write(',"sourceIPs": ' + str(srcIps))

    arquivo.write(',"averageCowrieLoginSuccess": ' + str(len(cowrieLoginSuccess)))
    arquivo.write(',"cowrieLoginFailed": ' + str(len(cowrieLoginFailed)))

    arquivo.write(',"averageCowrieCommandInput": ' + str(len(cowrieCommandInput)))
    arquivo.write(',"averageCowrieCommandFailed": ' + str(len(cowrieCommandFailed)))
    arquivo.write(',"usedCommands":' + str(usedCommands))
    arquivo.write('}')

    """
        print(eventIdTypes)
        print(len(dados))
        print(len(cowrieClientFingerprint))
        print(len(cowrieClientSize))
        print(len(cowrieSessionFileUpload))
        print(len(cowrieVirustotalScanfile))
        print(len(cowrieClientVar))
        print(len(cowrieDirectTcpipRequest))
        print(len(cowrieDirectTcpipData))
        print(len(cowrieSessionParams))
        print(len(cowrieClientVersion))
        print(len(cowrieClientKex))
    """

    return (
        len(cowrieSessionConnect), len(cowrieSessionClosed), cowrieSessionDuration[0] / len(cowrieSessionDuration[1]),
        srcIps, len(cowrieLoginSuccess), len(cowrieLoginFailed), len(cowrieCommandInput), len(cowrieCommandFailed),
        usedCommands)


def getCowrieAverageLogsInformation(reportData):
    totalCowrieSessionConnect = 0
    totalCowrieSessionClosed = 0
    cowrieSessionDuration = (0, [])
    srcIps = set()
    totalCowrieLoginSuccess = 0
    totalCowrieLoginFailed = 0
    totalCowrieCommandInput = 0
    totalCowrieCommandFailed = 0
    usedCommands = set()

    for reportItem in reportData:
        totalCowrieSessionConnect = totalCowrieSessionConnect + reportItem[0]
        totalCowrieSessionClosed = totalCowrieSessionClosed + reportItem[1]
        cowrieSessionDuration = (cowrieSessionDuration[0] + reportItem[2], cowrieSessionDuration[1] + [reportItem[2]])
        for x in reportItem[3]: srcIps.add(x)
        totalCowrieLoginSuccess = totalCowrieLoginSuccess + reportItem[4]
        totalCowrieLoginFailed = totalCowrieLoginFailed + reportItem[5]
        totalCowrieCommandInput = totalCowrieCommandInput + reportItem[6]
        totalCowrieCommandFailed = totalCowrieCommandFailed + reportItem[7]
        for x in reportItem[8]: usedCommands.add(x)


    arquivo = open('avreageReport.txt', 'w')
    arquivo.write('---- SEÇÕES ----')
    arquivo.write('\nIniciadas: ' + str(totalCowrieSessionConnect))
    arquivo.write('\nEncerradas: ' + str(totalCowrieSessionClosed))
    arquivo.write('\nDuração média: ' + str(cowrieSessionDuration[0] / len(cowrieSessionDuration[1])))
    arquivo.write('\nIPs doa atacantes: ' + str(srcIps))

    arquivo.write('\n\n---- LOGINS ----')
    arquivo.write('\nCom sucesso: ' + str(totalCowrieLoginSuccess))
    arquivo.write('\nSem sucesso: ' + str(totalCowrieLoginFailed))

    arquivo.write('\n\n---- COMANDOS ----')
    arquivo.write('\nInseridos : ' + str(totalCowrieCommandInput))
    arquivo.write('\nFalharam: ' + str(totalCowrieCommandFailed))
    arquivo.write('\nLista de comandos:' + str(usedCommands))

    arquivo = open('avreageReport.json', 'w')
    arquivo.write('{')
    arquivo.write('"averageCowrieSessionConnect": ' + str(totalCowrieSessionConnect))
    arquivo.write(',"averageCowrieSessionClosed": ' + str(totalCowrieSessionClosed))
    arquivo.write(',"averageCowrieSessionDuration": ' + str(cowrieSessionDuration[0] / len(cowrieSessionDuration[1])))
    arquivo.write(',"sourceIPs": ' + str(srcIps))

    arquivo.write(',"averageCowrieLoginSuccess": ' + str(totalCowrieLoginSuccess))
    arquivo.write(',"averageCowrieLoginFailed": ' + str(totalCowrieCommandFailed))

    arquivo.write(',"averageCowrieCommandInput": ' + str(totalCowrieCommandInput))
    arquivo.write('"averageCowrieCommandFailed": ' + str(totalCowrieCommandFailed))
    arquivo.write('"usedCommands":' + str(usedCommands))


reportData = []
for x in range(16, 23, 1):
    reportData.append(getCowrieLogsInformation('sensor02-2022-09-' + str(x)))

getCowrieAverageLogsInformation(reportData)
