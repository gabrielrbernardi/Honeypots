import logging
import traceback
from ConnectInstances import ConnectInstances
from GenerateDB import GenerateDB
from GenerateDB1 import GenerateDB1
from AnalyseLogs import AnalyseLogs

# logging.basicConfig(filename="logs.log", format='%(levelname)s - %(asctime)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s', datefmt='%d/%m/%Y %H:%M:%S %z', level=logging.DEBUG)

try:
    print("MENU".center(50, "="))
    print("1 - Get Logs")
    print("2 - Generate DB")
    print("3 - Analyse Values")
    # choose = int(input("Option: "))
    choose = 1
    # choose = 3

    if(choose == 1):
        ci = ConnectInstances()
        ci.readConfigFile()
        ci.connectInstances()
    # elif choose == 2:
    #     gd1 = GenerateDB1()
    #     # al = GenerateDB()
    #     # al.readConfigFile()
    #     # al.openLogFiles()
    #     # al.exportLogData()
    # elif choose == 3:
    #     al = AnalyseLogs()
    #     al.fetchData()
except:
    print(traceback.format_exc())
    # logging.error("Erro na execucao")