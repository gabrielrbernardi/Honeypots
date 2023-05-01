import logging
import traceback
from ConnectInstances import ConnectInstances
from AnalyseLogs import AnalyseLogs

logging.basicConfig(filename="logs.log", format='%(levelname)s - %(asctime)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s', datefmt='%d/%m/%Y %H:%M:%S %z', level=logging.DEBUG)

try:
    print("MENU".center(50, "="))
    print("1 - Get Logs")
    print("2 - Analyse Logs")
    # choose = int(input("Option: "))
    choose = 2

    if(choose == 1):
        ci = ConnectInstances()
        ci.readConfigFile()
        ci.connectInstances()
    else:
        al = AnalyseLogs()
        al.readConfigFile()
        al.openLogFiles()
        al.exportLogData()
except:
    print(traceback.format_exc())
    logging.error("Erro na execucao")