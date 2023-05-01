import json

keysList = []

dicionario = {}

file = open("./Logs/log-sensor1/log/cowrie.json.2022-09-16.json")
jsonFile = json.load(file)

for x in jsonFile["data"]:
    for y in x.keys():
        if y not in keysList:
            keysList.append(y)

print(keysList)

for chave in keysList:
    dicionario[chave] = []

for x in jsonFile["data"]:
    for valor in dicionario:
        if x.get(valor) != None:
            print(dicionario[valor])
            if str(x[valor]) not in dicionario[valor]:
                dicionario[valor].append({str(x[valor]): 0})
                # dicionario[valor].append({x[valor]: 0})
            else:
                dicionario[valor][str(x[valor])] += 1

        


# for x in jsonFile["data"]:
#     for valor in dicionario:
#         if x.get(valor) != None and x[valor] not in dicionario[valor]:
#             dicionario[valor].append(x[valor])

print(dicionario)
