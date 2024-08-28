# Install Mysql on your computer
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python
#APPARENTLY WE DONT NEED THIS FILE AFTER CREATING THE APP
import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
   password='Element99@@@',
    auth_plugin='mysql_native_password' 
     

)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE fhdb3039")


print("All Done!")

