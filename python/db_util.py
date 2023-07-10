import mysql.connector
import config_util

# MariaDB 연결 설정

def excuteQuery(query, param) :
    cnx = mysql.connector.connect(**config_util.getConfig('mysql'))

    cursor = cnx.cursor()   

    cursor.execute(query, param)

    cnx.commit()

    cursor.close()
    cnx.close()