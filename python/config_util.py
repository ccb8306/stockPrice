import configparser
import util


# 설정 파일 읽기
config = configparser.ConfigParser()
config.read(util.getReadFile('config.ini'))



def getConfig(confName, confSName = None) :
    if confSName is None :
        return config[confName]
    else :
        return config.get(confName, confSName)