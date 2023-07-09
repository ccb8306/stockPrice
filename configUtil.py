import configparser


# 설정 파일 읽기
config = configparser.ConfigParser()
config.read('config.ini')

def getConfig(confName) :
    return config[confName]

