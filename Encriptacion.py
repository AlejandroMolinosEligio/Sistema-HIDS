import hashlib
import shutil
from datetime import datetime
import os
import hmac
import secrets
import random

hashes_route = './Record/Hashes/hashes.txt'
dict_nonces = dict()
dict_keys = dict()
dict_hashes = dict()

#########################################################################################################################
############################################# FUNCIONES DE HASH #########################################################
#########################################################################################################################

### Función para la creacion de hash SHA256 de un archivo

def hash_file_SHA256(file_path,nonce):
    hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    hash.update(nonce)
    hash = hash.hexdigest()

    return hash

### Función para la creacion de hash SHA1 de un archivo
def hash_file_SHA1(file_path,nonce):
    hash = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    hash.update(nonce)
    hash = hash.hexdigest()

    return hash
    
### Función para la creacion de hash HMACSHA1 de un archivo

def createHmacSha1(file_path,key):
    with open (file_path, "rb") as f:
        hashed = hmac.new(key=key,digestmod=hashlib.sha1)
        for chunk in iter(lambda: f.read(4096), b""):
            hashed.update(chunk)
        hashed_hmac= hashed.hexdigest()
    return hashed_hmac 
        
### Función para la creacion de hash HMACSHA256 de un archivo

def createHmacSHA256(file_path,key):
    with open (file_path, "rb") as f:
        hashed = hmac.new(key=key, digestmod=hashlib.sha256)
        for chunk in iter(lambda: f.read(4096), b""):
            hashed.update(chunk)
        hashed_hmac= hashed.hexdigest()
    return hashed_hmac 

### Función PRINCIPAL para hashear y guardar todos los elementos correspondientes

def hash_file(route,token,encryp,name):

    # Generamos un nonce en función del token

    nonce = generatoken(name,token)

    # Generamos key 

    key = generaClave(name)

    # Creamos el hash inicial con la encriptación señalada y el HMAC
    if(encryp == 'SHA256'):
        hash = hash_file_SHA256(route,nonce)
        hmac = createHmacSHA256(route,key)
    else:
        hash = hash_file_SHA1(route,nonce)
        hmac = createHmacSha1(route,key)

    # Guardamos en los archivos correspondientes

    save_record(route,hash,hmac,encryp)

    return 0


#########################################################################################################################
############################################# FUNCIONES AUXILIARES ######################################################
#########################################################################################################################


### Creamos una función para guarda la entrada nombre del archivo,hash,machash y ENCRIPTACIÓN
def save_record(file_path,hash,hmac,type):

    global hashes_route

    # Escogemos solo el nombre del archivo
    file_name = file_path.split("/")[-1]

    # Creamos una tupla la cuál va a guardar el nombre del fichero y su hash asociado
    entry = (file_name,hash,hmac,type)

    #Intentamos escribir en el archivo de hashes, si obtenemos un error este será capturado

    try:
        file = open(hashes_route,'a')
        file.write(str(entry)+'\n')
        file.close()
    
    except FileNotFoundError:
        print('El archivo no existe')

    return 0


### Creación de documentos
def create_file():

    # Preguntamos al usuario para confirmar la acción

    print('¿Quieres crear un archivo?[y/n]:')
    response = input()

    # En función de la respuesta haremos una cosa o otra
    # Tanto si es No como algo distinto la función termina, si es Y continuamos con la creación

    if(response == 'n'):
        return print('Gracias!')
    elif(response != 'y' and response=='n'):
        return print('Respuesta no válida.')
    else:
        # El usuario indica la ruta de su archivo la cual guardamos y nos quedamos tambien con el nombre
        print('Indica la ruta de tu archivo:')
        route = input()

        # Obtenemos el nombre del archivo
        name = route.split("/")[-1]

        # Pedimos al cliente que especifique un token para el posteiror challenge

        print('Indique su token (valor numérico):')
        token = input()
        if(token.isdigit()== False):
            print('No es un valor válido, porfavor asegurese de que sea un valor numérico')
        else:
            # El usuario elige método de encriptación
            print('Indica el tipo de encriptación[SHA256/SHA1]:')
            encryp = input()
            if(encryp != 'SHA256' and encryp != 'SHA1'):
                print('No es un tipo de encriptación')
                return 0

            # Intentamos copiar el archivo a nuestra carpeta contenedora
            try:
                shutil.copy(route,'./Documents/'+name)
            except FileNotFoundError:
                print('La ruta del fichero indicado no existe.')
                return 0

            # Guardamos el hash asociado al documento en función del tipo de encriptación escogido
            hash_file('./Documents/'+name,int(token),encryp,name)
            
    return 0

### Función para la creacion de hash SHA256 de un archivo
def generatoken(name,token):

    # Comprobamos si tenemos los diccionarios cargados correctamente

    check_dicts()
    global dict_nonces
    nonce = None

    # Comprobamos primero si el archivo ya está registrado en el diccionario de nonces

    if(name in dict_nonces):
        nonce = dict_nonces.get(name)[0]

    # En caso contrario tomamos este toke como challenge para decidir el tipo de nonce que se va a crear

    else:
        if(token%2==0):
            nonce = str(secrets.token_hex(16))
            nonce = nonce.replace(',','')
            dict_nonces[name]= (nonce,token)
        else:
            nonce = str(secrets.token_bytes(16))
            nonce = nonce.replace(',','')
            dict_nonces[name]= (nonce,token)

        # Escribimos la nueva entrada en el fichero de nonces (nombre_archivo, nonce, token)

        file = open('./Data/dataNonces','a')
        file.write(name+','+nonce+','+str(token)+'\n')
        file.close()

    # Como último parseamos de str a bytes

    return bytes(nonce,'utf-8')


### Función para generar key

def generaClave(name):

    # Comprobamos si tenemos los diccionarios cargados correctamente y declaramos el dict global para poder modificarlo
    
    check_dicts()
    global dict_keys
    
    # Comprobamos primero si el archivo ya está registrado en el diccionario de claves

    if(name in dict_keys):
        key = dict_keys.get(name)

    # En caso contrario generamos una clave nueva aleatoria

    else:
        key = str(os.urandom(8))
        key = key.replace(',','')
        dict_keys[name] = key

        # Escribimos en el archivo de claves la nueva entrada (nombre archivo, clave)

        file1 = open('./Data/dataClaves','a')
        file1.write(name+','+key+'\n')

    return bytes(key,'utf-8')

## Función para la lectura de dicc

def check_dicts():

    # Declaramos las variables diccionario como globales para poder modificarlas

    global dict_nonces
    global dict_keys
    global dict_hashes

    # Leemos el archivo de nonces y lo vamos introducciendo en el diccionario de nonces

    with open('./Data/dataNonces', 'r') as f:
        for line in f:
            clave = line.split(',')[0]
            value_nonce = line.split(',')[1]
            token = line.split(',')[2][:-1]
            dict_nonces[clave]=(value_nonce,token)

    # Leemos el archivo de claves y lo vamos introducciendo en el diccionario de claves

    with open('./Data/dataClaves', 'r') as f:
        for line in f:
            clave = line.split(',')[0]
            value_key = line.split(',')[1][:-1]
            dict_keys[clave]=value_key

    # Leemos el archivo de hashes para introduccirlo al diccionario de hashes

    with open('./Record/Hashes/hashes.txt','r') as f:
        for linea in f:
            # Dividimos la linea por comas y obtenermos cada valor
            lista_linea = str(linea).split(', ')
            name = lista_linea[0][2:-1]
            hash = lista_linea[1][1:-1]
            hmac = lista_linea[2][1:-1]
            type_enc = lista_linea[3][1:-3]

            # Guardamos en el dict global anterior
            dict_hashes[name] = (hash,hmac,type_enc)


    return 0

### Función para la creación del test

def test():

    # Preguntamos al usuario con cuantos ficheros quiere realizar la prueba

    print('¿Con cuantos ficheros quieres realizar la prueba?:')
    nFiles = int(input())

    # Eliminamos todos los datos de test anterirores si estos exsistieran

    remove_data_for_test()

    # Almacenamos los nombres de los archivos creados en una lista

    lista_docs = []

    # Creamos tantos ficheros con un texto por defecto como nos indique el usuario

    for i in range(nFiles):
        name = 'ArchivoPruebaHIDS_'+str(i)+'.txt'
        path = './Documents/'+name
        file = open(path,'w')
        file.write(str("HOLA MUNDO")+'\n')
        file.close()
        lista_docs.append(path)
    
        # Para la prueba elegiremos el tipo de encriptación en función de si un número aleatorio es par o no

        num = random.randint(0,10)
        if num%2==0:
            hash_file(path,random.randint(0,100),'SHA1',name)
        else:
            hash_file(path,random.randint(0,100),'SHA256',name)

    # Recorremos todos los archivos y con una probabilidad del 20% los corrompemos

    for doc in lista_docs:
        prob = random.random()
        if(prob<=0.2):
            file = open(doc,'a')
            file.write(str("Archivo modificado")+'\n')

            # Indicamos que archivos se ha modificado para poder comprobarlos correctamente

            print('Se ha modificado: '+doc.split('/')[-1])
            file.close()

    # Comprobamos la integridad de los archivos

    check_integrity()

    # Guardamos un log provisional con el test realizado hasta el momento para poder visualizarlo

    archiveLog()

    return 0 

### Función para eliminar todos los datos que ha creado la función test

def remove_data_for_test():

    # Listamos el directorio de documentos y eliminamos todos los documentos creados

    docs = os.listdir('./Documents')
    for doc in docs:
        if('ArchivoPruebaHIDS' in doc):
            os.remove('./Documents/'+doc)
            
            # Creamos una lista para almacenar las lineas del archivo que no queremos perder para 
            # luego poder reescribirlo

            lista = []

            ## Modificar dataClaves
            with open('./Data/dataClaves','r') as f:
                for line in f:
                    if('ArchivoPruebaHIDS' not in line):
                        lista.append(line)

            # Eliminamos el contenido del dataClaves
            
            file = open('./Data/dataClaves','w')
            file.write('')
            file.close()

            # Lo escribimos solo con la información que queremos mantener

            file = open('./Data/dataClaves','a')
            for line in lista:
                file.write(line)
            file.close()

            # Vaciamos lista anterior para poder reutiliazrla

            lista = []

            ## Modificar dataNonces
            with open('./Data/dataNonces','r') as f:
                for line in f:
                    if('ArchivoPruebaHIDS' not in line):
                        lista.append(line)

            # Eliminamos el contenido del dataNonces

            file = open('./Data/dataNonces','w')
            file.write('')
            file.close()

            # Lo escribimos solo con la información que queremos mantener
            
            file = open('./Data/dataNonces','a')
            for line in lista:
                file.write(line)
            file.close()

            # Vaciamos lista anterior para poder reutiliazrla

            lista = []

            ## Modificar hashes
            with open('./Record/Hashes/hashes.txt','r') as f:
                for line in f:
                    if('ArchivoPruebaHIDS' not in line):
                        lista.append(line)

            # Eliminamos el contenido del hashes

            file = open('./Record/Hashes/hashes.txt','w')
            file.write('')
            file.close()
    
            # Lo escribimos solo con la información que queremos mantener

            file = open('./Record/Hashes/hashes.txt','a')
            for line in lista:
                file.write(line)
            file.close()

    return 0

### Función para archivar log antiguo

def archiveLog():

    ## Contadores

    lineas_totales = 0
    correctos = 0

    ## Leemos el archivo para comprobar el porcentaje de fallos

    with open("./Record/Logs/log.txt", 'r') as f:
        for linea in f:
            if('correcto' in linea):
                correctos = correctos +1
            lineas_totales = lineas_totales+1

    ## Creamos el nuevo log

    file = open('./Record/Logs/log-'+str(datetime.now())[:10]+'.txt','w')
    file.write('##########################################################################\n\tEl porcentaje sin fallos de integridad es '+str(correctos*100/lineas_totales)[:5]+"%\n##########################################################################\n\n")
    file.close()

    ## Escribirmos el log antiguo en el nuevo para tener el registro
    file = open('./Record/Logs/log-'+str(datetime.now())[:10]+'.txt','a')
    with open("./Record/Logs/log.txt", 'r') as f:
        for linea in f:
            file.write(linea)
    file.close()

    ## Limpiamos el archivo log original para empezar a escribirlo de nuevo
    file = open('./Record/Logs/log.txt','w')
    file.write('')
    file.close()

    return 0

### Función para archivar log prueba

def archiveLogTest():

    ## Contadores

    lineas_totales = 0
    correctos = 0

    ## Leemos el archivo para comprobar el porcentaje de fallos

    with open("./Record/Logs/log.txt", 'r') as f:
        for linea in f:
            if('correcto' in linea):
                correctos = correctos +1
            lineas_totales = lineas_totales+1

    ## Creamos el nuevo log

    file = open('./Record/Logs/log-TEST-'+str(datetime.now())[:10]+'.txt','w')
    file.write('##########################################################################\n\tEl porcentaje sin fallos de integridad es '+str(correctos*100/lineas_totales)[:5]+"%\n##########################################################################\n\n")
    file.close()

    ## Escribirmos el log antiguo en el nuevo para tener el registro
    file = open('./Record/Logs/log-TEST-'+str(datetime.now())[:10]+'.txt','a')
    with open("./Record/Logs/log.txt", 'r') as f:
        for linea in f:
            file.write(linea)
    file.close()

    return 0


#########################################################################################################################
############################################# INTEGRIDAD ######################################################
#########################################################################################################################

#Función para comprobar integridad
def check_integrity():
      
    # Cargamos el dict de hashes, keys y nonces para poder utilizarlo

    check_dicts()

    # Empezamos intentando abrir el archivo log

    try:
        file = open('./Record/Logs/log.txt','a')
    
    except FileNotFoundError:
        print('El archivo de registro LOG no existe')
        return 0

    # Listamos el contenido de la carpeta Documentos

    docs = os.listdir('./Documents')

    # Recorremos listado de documentos

    for document in docs:

        # Creamos una variable local para ver si el archivo tiene fallo de integridad o no

        correct = True

        # Si el diccionario contiene el documento buscamos la encriptación
        if(document in dict_hashes):

            # Comprobamos valor de encrypt
            encrypt = dict_hashes[document][2]
            token = int(dict_nonces[document][1])
            key = generaClave(document)
            nonce = generatoken(document,token)

            if(encrypt == 'SHA1'):

                # Calculamos hash
                hash = hash_file_SHA1('./Documents/'+document,nonce) ##NONCE AQUII WARNING TOKEN? o NONCE?
                if(hash==dict_hashes[document][0]):
                    
                    # Comprobamos ahora si conincide con hmac
                    hmac = createHmacSha1('./Documents/'+document,key)

                    if(hmac!=dict_hashes[document][1]):
                        correct = False
                
                else:
                    correct = False

            # Caso de SHA256
            else:
                # Calculamos hash
                hash = hash_file_SHA256('./Documents/'+document,nonce)
                if(hash==dict_hashes[document][0]):
                    
                    # Comprobamos ahora si conincide con hmac
                    hmac = createHmacSHA256('./Documents/'+document,key)

                    if(hmac!=dict_hashes[document][1]):
                        correct = False
                
                else:
                    correct = False
            
            # Escribimos en el archivo log el resultado de la comprobación

            if(not correct):
                file.write("[FECHA] "+str(datetime.now())+" --- Archivo "+document+" de tipo "+encrypt+". Fallo de integridad\n")
            else:
                file.write("[FECHA] "+str(datetime.now())+" --- Archivo "+document+" de tipo "+encrypt+". Todo correcto\n")

        else:
            print('El documento '+document+" no tiene una entrada asociada")

    file.close()

    return 0

### Función para comprobar un único archivo

def check_file(path,token):

    # Comprobamos si todos los diccionarios están cargados correctamente

    check_dicts()

    # Obtenemos el nombre del archivo

    name = path.split('/')[-1]

    # Comprobamos primero si el archivo existe en el diccionario de hashes

    if name in dict_hashes:

        # Comprobamos si el token introducido por el cliente coincide con el que tenemos registrado

        if token == int(dict_nonces[name][1]):

            # Comprobamos tipo de encriptación

            if dict_hashes[name][2] =='SHA1':

                # Calculamos hash para SHA1 y comparamos con el que tenemos guardado

                hash = hash_file_SHA1(path,generatoken(name,token))

                if hash == dict_hashes[name][0] :

                    # Calculamos y comprobamos si la clave proporcionada genera el mismo hmac que tenemos registrado

                    key = generaClave(name)
                    chmac = createHmacSha1(path,key)
                    if chmac == dict_hashes[name][1] :
                        print(" El archivo No ha sido modificado")
                    else:
                        print("El archivo ha sido modificado")
                else:
                    print("El archivo ha sido modificado")
       
            elif dict_hashes[name][2] == 'SHA256':

                # Calculamos hash para SHA256 y comparamos con el que tenemos guardado

                hash = hash_file_SHA256(path,generatoken(name,token))
                
                if hash == dict_hashes[name][0] :

                    # Calculamos y comprobamos si la clave proporcionada genera el mismo hmac que tenemos registrado

                    key = generaClave(name)
                    chmac = createHmacSHA256(path,key)
                    if chmac == dict_hashes[name][1] :
                        print(" El archivo No ha sido modificado")
                    else:
                        print("El archivo ha sido modificado")
                else:
                 print("El archivo ha sido modificado")
        else :      
            print("El token dado no es valido")
    else:
        print("No existe el archivo")

    return 0

