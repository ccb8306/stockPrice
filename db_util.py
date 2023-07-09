import mysql.connector
import configUtil

# MariaDB 연결 설정

def excuteQuery(query, param) :
    cnx = mysql.connector.connect(**configUtil.getConfig('mysql'))

    cursor = cnx.cursor()   

    cursor.execute(query, param)

    cnx.commit()

    cursor.close()
    cnx.close()