
import time
from datetime import datetime
import Encriptacion
import SendMail

revision = None
last_revision = None

### Función para la comprobación de si se ha modificado la configuración

def check_var():

    # Declaramos las variables globales para poder modificarlas

    global revision
    global last_revision

    # Leemos el archivo de configuración y establecemos variables

    with open('./Data/dataTimer', "r") as conf_file:
            lines = conf_file.readlines()
            revision = int(lines[0][:-1])
            last_revision= lines[1][:-1]

    return 0

### Función para actualizar el archivo de configuración

def update_conf_file(days,last_chek):

    # Abrimos el fichero y escribimos la nueva configuración

    file = open('./Data/dataTimer','w')
    file.write(str(days)+'\n'+str(last_chek)+'\n')
    file.close()

    return 0

### Función para establecer el número de días hasta revisión, por defecto 1

def setRevision():

    # Declaramos las variables globales para poder modificarlas

    global revision
    global last_revision

    # Comprobamos las variables por si se han modificado

    check_var()

    # Preguntamos al usuario por el cambio

    print('Revision actual cada '+str(revision)+' día(s).')
    print('¿Cada cuantos días quieres que se comprueben los archivos?:')
    days = input()

    # Establecemos las variables y actualizamos el archivo de configuración

    try:
        revision = int(days)
        update_conf_file(revision,last_revision)

    # En caso de error volvemos al inico de la función indicando el error

    except ValueError:
        print('Debe ser un valor numérico.')
        return setRevision()

    return 0

### Esta función se utiliza para comprobar si han pasado los días necesarios para la revisión

def check_revision():

    # Declaramos la variable global para poder modificarla

    global revision

    # Obtenemos el dia actual y comprobamos si han pasado los dias necesarios para una nueva revisión

    current_date = datetime.now()
    diff = current_date-datetime.strptime(last_revision, "%Y-%m-%d")
    if(diff.days>=revision):

        # Comprobamos integridad y actualizamos la última revisión en el archivo de configuración

        Encriptacion.check_integrity()
        update_conf_file(revision,str(current_date)[:10])

        #Miramos si ya ha pasado un mes y en ese caso enviamos un correo con el archivo correspondiente
        if(current_date.month!=datetime.strptime(last_revision, "%Y-%m-%d").month):
            Encriptacion.archiveLog()
            SendMail.send_mail()

    return 0

### Función principal del timer

def main_method():

    while(True):
        ## Comprobamos si se han modificado las variables globales
        check_var()
        ## Hacemos la comprobación de si ha pasado el tiempo necesario
        check_revision()
        ## Espera un minuto para la siguiente comprobación
        time.sleep(60) 

if __name__ == "__main__":
    main_method()
