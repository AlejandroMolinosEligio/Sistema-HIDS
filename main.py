import Encriptacion
import TimerHIDS
import SendMail

def main():
    while(True):
        print('¿Que quieres hacer?\n\t1. Creacion de fichero\n\t2. Comprobar Fichero\n\t3. Establecer días de comprobación')
        print('\t4. Establecer correo destino\n\t5. Comprobar integridad\n\t6. Test\n\t7. Borrar datos Test\n\t8. Enviar correo de prueba\n\t9. SALIR')
        option = input()
        
        if(option=='1'):
            Encriptacion.create_file()
        elif(option=='3'):
            TimerHIDS.setRevision()
        elif(option=='4'):
            SendMail.setToEmail()
        elif(option=='5'):
            Encriptacion.check_integrity()
        elif(option=='6'):
            Encriptacion.test()
        elif(option=='7'):
            Encriptacion.remove_data_for_test()
        elif(option=='8'):
            Encriptacion.archiveLogTest()
            SendMail.send_mail_TEST()
        elif(option=='9'):
            return 0
        elif(option=='2'):
            print('Nombre del Fichero:')
            name = input()
            print('token:')
            token = input()
            Encriptacion.check_file("./Documents/"+name,int(token))
        else:
            print('Eso no es una opción válida.\n')

if __name__ == "__main__":
    main()