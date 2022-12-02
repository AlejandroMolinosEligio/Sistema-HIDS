### Imports para correo

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

emailTo = None

### Función para comprobar email en archivo configuración

def check_mail():

    # Declaramos la variable global para poder modificarla

    global emailTo

    # Obtenemos el correo destino
    try:
        with open('./Data/dataEmail', "r") as conf_file:
                lines = conf_file.readlines()
                emailTo = str(lines[0][:-1])

    except FileNotFoundError:
        print('Fichero de configuración no encontrado.')
        return 0


### Función para cambiar el correo destino

def setToEmail():

    # Comprobamos el correo destino por si se ha actualizado y preguntamos al usuario

    check_mail()
    print('Correo destino actual '+emailTo+'.')
    print('¿Quiere modificarlo?:[y/n]')
    response = input()

    ## Si rechazamos cerramos la operación
    if(response == 'n'):
        return print('No se modificó el email destino.')

    ## Si la respuesta no es correcta volvemos a formular la pregunta
    elif(response != 'y' and response=='n'):
        print('Respuesta no válida.')
        return setToEmail()

    ## Indicamos el nuevo correo si indicamos que queremos modificarlo
    else:
        print('Indique el nuevo correo destino:')
        newEmail = input()
        file = open('./Data/dataEmail','w')
        file.write('{NewEmail}\n'.format(NewEmail=newEmail))
        print('Correo actualizado, muchas gracias.')

    return 0

### Función para enviar correo

def send_mail():    

    ## Comprobamos el email destino
    check_mail()

    ## Iniciamos los parámetros del script
    remitente = 'grupo1SSII@gmail.com'
    destinatarios = [emailTo]
    asunto = 'Informe mensual sistema HIDS'
    cuerpo = 'Le adjuntamos el informe mensual en el que se indican todas las incidencias que ha habido.\nUn saludo.'
    ruta_adjunto = './Record/Logs/log-'+str(datetime.now())[:10]+'.txt'
    nombre_adjunto = 'log-'+str(datetime.now())[:10]+'.txt'

    ## Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    ## Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    ## Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    ## Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
    
    ## Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')

    ## Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())

    ## Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)

    ## Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    
    ## Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    ## Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    ## Ciframos la conexión
    sesion_smtp.starttls()

    ## Iniciamos sesión en el servidor
    sesion_smtp.login('grupo1SSII@gmail.com','fjckuvtdfsezjmab')

    ## Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    ## Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    ## Cerramos la conexión
    sesion_smtp.quit()

### Función para enviar correo

def send_mail_TEST():    

    ## Comprobamos el email destino
    check_mail()

    ## Iniciamos los parámetros del script
    remitente = 'grupo1SSII@gmail.com'
    destinatarios = [emailTo]
    asunto = 'Informe mensual sistema HIDS'
    cuerpo = 'Le adjuntamos el informe mensual en el que se indican todas las incidencias que ha habido.\nUn saludo.'
    ruta_adjunto = './Record/Logs/log-TEST-'+str(datetime.now())[:10]+'.txt'
    nombre_adjunto = 'log-'+str(datetime.now())[:10]+'.txt'

    ## Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    ## Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    ## Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    ## Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
    
    ## Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')

    ## Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())

    ## Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)

    ## Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    
    ## Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    ## Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    ## Ciframos la conexión
    sesion_smtp.starttls()

    ## Iniciamos sesión en el servidor
    sesion_smtp.login('grupo1SSII@gmail.com','fjckuvtdfsezjmab')

    ## Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    ## Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    ## Cerramos la conexión
    sesion_smtp.quit()
