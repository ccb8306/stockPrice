import os

def getRealPath() :
    return os.path.dirname(os.path.abspath(__file__))

def getReadFile(fileName) :
    return os.path.join(getRealPath(), fileName)