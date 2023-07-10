import configparser
import util


# 설정 파일 읽기
config = configparser.ConfigParser()
config.read(util.getReadFile('config.ini'))

def getConfig(confName) :
    return config[confName]

