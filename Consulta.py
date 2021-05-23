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

#Creamos un objeto de la clase DB para realizar las ejecuciones SQL
myDB = DB()
myDB.iniciarConexion("localhost", "David", "12345", "PAISES")
#Se describe lo que hace el programa
print("A continuación puede consultar la población de cada ciudad según la jerarquía\
          que deseé, de la siguiente manera: Si ingresa 1 podrá consultar por país, mostrándose\
          la población por ciudad y a qué estado pertenece. Si ingresa 2 podrá consultar por Estado\
          mostrándose todas las ciudades de este, con su respectiva población. Si ingresa 3, podrá consultar\
          por ciudad y se muestra la población de esta.")

while True:
    tipo=input("Escriba: \n 1 para consultar por país\n 2 para consultar por Estado\n 3 para consultar por Ciudad\n")
    tipo = int(tipo)
    #Se valida que tipo de búsqueda es
    if tipo == 1:
        busqueda=input("Ingrese el país: ")
        myDB.cursor.execute("SELECT NAME_STATE, NAME_CITY, POPULATION FROM PAISES WHERE NAME_COUNTRY = %s", (busqueda,)) 
        Resultado = myDB.cursor.fetchall() #Se busca en la base de datos el dato ingresado, si no está se avisa
        if Resultado != []:
            if Resultado != [(None, None, None)]: #Se valida que el pais tenga estados y ciudades puesto que hay unos que no tienen
                print(Resultado)
            else:
                print("El país se encuentra registrado en la base de datos pero no tiene Estados ni ciudades asociadas")
        else:
            print("El país no se encuentra registrado en la base de datos.")
    elif tipo == 2:
        busqueda=input("Ingrese el Estado: ")
        myDB.cursor.execute("SELECT NAME_CITY, POPULATION FROM PAISES WHERE NAME_STATE = %s", (busqueda,))
        Resultado = myDB.cursor.fetchall()
        if Resultado != []:
            print(Resultado)
        else:
            print("El Estado no se encuentra registrado en la base de datos.")
    elif tipo == 3:
        busqueda=input("Ingrese la ciudad: ")
        myDB.cursor.execute("SELECT POPULATION FROM PAISES WHERE NAME_CITY = %s", (busqueda,))
        Resultado = myDB.cursor.fetchall()
        if Resultado != []:
            print(Resultado)
        else:
            print("La ciudad no se encuentra registrado en la base de datos.")
    else:
        print("Consulta incorrecta")
