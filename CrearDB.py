import mysql.connector
import xlrd
import numpy as np

class DB:
    def __init__(self):
        self.conexion = 0
        self.cursor = 0
    
    def iniciarConexion(self, host, user, password, DB=""):
        self.conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=DB
        )
        self.cursor = self.conexion.cursor()

class hojaExcel:
    def __init__(self):
        self.book = 0
        self.sheet = 0

    def cargarHoja(self, book):
        self.book = xlrd.open_workbook(book + ".xlsx")
        self.sheet = self.book.sheet_by_index(0)
        columnas = []
        filas = []
        for i in range(1, self.sheet.nrows):
            for j in range(0, self.sheet.ncols):
                columnas.append(str(self.sheet.cell_value(rowx=i, colx=j))) #Va agregando las columnas a una lista
            filas.append(columnas) #Cuando termina de recorrer columnas, agrega esa lista a una lista filas
            columnas = [] #Se borra el valor de columnas para que guarde las de la siguiente fila
        return(filas)


myDB = DB()
myDB.iniciarConexion("localhost", "David", "12345")
myDB.cursor.execute("CREATE DATABASE PAISES")

myDB.iniciarConexion("localhost", "David", "12345", "PAISES")
myDB.cursor.execute("CREATE TABLE PAISES (ID_COUNTRY INT, NAME_COUNTRY VARCHAR(255), ID_STATE INT, NAME_STATE VARCHAR(255),\
                    ID_CITY INT, NAME_CITY VARCHAR(255), POPULATION INT)")

Se parte de las ciudades puesto que estas determinan el número de filas de la BD
hojaExcel = hojaExcel()
ciudades = hojaExcel.cargarHoja("cities")

myDB.cursor.executemany("INSERT INTO PAISES (ID_CITY, NAME_CITY, ID_STATE, POPULATION) VALUES (%s, %s, %s, %s)", ciudades) #Se insertan en la DB
myDB.conexion.commit()

estados = hojaExcel.cargarHoja("states") #Se recorren los estados y se actualizan las ciudades según el ID_STATE
for estado in estados:
    myDB.cursor.execute("UPDATE PAISES SET NAME_STATE = %s, ID_COUNTRY = %s WHERE ID_STATE = %s", (estado[1], estado[2], estado[0]))
myDB.conexion.commit()

            
paises = hojaExcel.cargarHoja("countries") #Se recorren los paises y se actualizan las ciudades según el ID_COUNTRY
for pais in paises:
    myDB.cursor.execute("UPDATE PAISES SET NAME_COUNTRY = %s WHERE ID_COUNTRY = %s", (pais[1], pais[0]))
myDB.conexion.commit()

##Con esto se ingresan los países que no tienen registrado algún Estado, pero que igual están en la base de datos
for pais in paises:
    myDB.cursor.execute("SELECT NAME_COUNTRY FROM PAISES.PAISES WHERE ID_COUNTRY = %s", (pais[0],))
    Resultado = myDB.cursor.fetchall()
    if Resultado == []:
        myDB.cursor.execute("INSERT INTO PAISES (ID_COUNTRY, NAME_COUNTRY) VALUES (%s, %s)", (pais[0], pais[1]))
myDB.conexion.commit()

