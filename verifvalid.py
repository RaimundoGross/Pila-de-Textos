import logging
#------------------------------------------------- CONFIGURACION DE LOGS ------------------------------------------

logging.basicConfig(filename='./logs/verifvalid.log', format='[%(asctime)s] %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)

#--------------------------------------------------- VARIABLES GLOBALES -------------------------------------------
allowed_symbols="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!\"#$%&/()=?¡¿}{[]+*'-_.:,;^~ \t\n"

index_larger = 0
index_shorter = 0

stack = []
size = 0

#-------------------------------------------------------- FUNCIONES -----------------------------------------------
def calc_largo(texto):
    total = 0
    for c in texto:
        if c in allowed_symbols:
            total += 1
        else:
            return -1
    return total

def ingresar_op(n_options):
    while True:
        try:
            op = input("> ")
            op = int(op)
            if op not in list(range(n_options + 1)):
                raise ValueError
        except ValueError:
            print("La opcion ingresada no es valida. Por favor intentelo nuevamente")
            logging.info('La entrada %s no es valida como opcion.', op)
        else:
            break

    return op

def print_texto(n_texto, *, log_label):
    texto = stack[n_texto][0]
    largo = stack[n_texto][1]
    print(texto)
    print("\ny tiene", largo, "caracteres.")
    logging.info('%s Se muestra el texto: %s (%d caracteres)', log_label,texto, largo)

def texto_largo():
    if size == 0:
        print("\nLa pila se encuentra vacia. Ingrese un texto primero")
        logging.info('[Texto Largo] No se puede mostrar texto mas largo. Pila vacia')
        #log se pide texto mas largo, rechazado por pila vacia
    else:
        print("\nEl texto mas largo de la pila es:")
        print_texto(index_larger, log_label='[Texto Largo]')
        #log se muestra el texto mas largo tanto

def texto_corto():
    if size == 0:
        print("\nLa pila se encuentra vacia. Ingrese un texto primero")
        logging.info('[Texto Corto] No se puede mostrar texto mas corto. Pila vacia')
        #log se pide texto mas corto, rechazado por pila vacia
    else:
        print("\nEl texto mas largo de la pila es:")
        print_texto(index_shorter, log_label='[Texto Corto]')
        #log se muestra el texto mas corto tanto

def cmp_textos():

    if size < 2:
        print("No existen suficientes textos en la pila para realizar esta operacion. Asegurese de tener al menos 2 textos y vuelva a intentarlo.")
        logging.info('[Comparar Textos] No se puede realizar la comparacion. Cantidad de textos insuficientes')
        #log se pide comparar dos texto, rechazado por textos insuficientes
    else:
        print("En la pila existen", size, "textos. Pogra ingresar dos numeros entre 1 y", size, "para poder comparar los textos (0 para cancelar).")
        op = ingresar_op(size)
        if op == 0:
            print("Operacion cancelada")
            logging.info('[Comparar Textos] Se cancela la operacion')
            #log se cancela comparacion de textos
        else:
            op2 = ingresar_op(size)
            if op2 == 0:
                print("Operacion cancelada")
                logging.info('[Comparar Textos] Se cancela la operacion')
                #log se cancela comparacion de textos
            else:
                largo1 = stack[op][1]
                largo2 = stack[op2][1]
                diff = abs(largo1 - largo2)
                if largo1 > largo2:
                    print("El texto", op, "es mas largo que el texto", op2, "por", diff, "caracteres.")
                    logging.info('[Comparar Textos] Textos %d y %d seleccionados. El texto %d es mas largo por %d caracteres', op, op2, op, diff)
                    #log se comparan texto op y op2, op es mas largo
                elif largo1 < largo2:
                    print("El texto", op2, "es mas largo que el texto", op, "por", diff, "caracteres.")
                    logging.info('[Comparar Textos] Textos %d y %d seleccionados. El texto %d es mas largo por %d caracteres', op, op2, op2, diff)
                    #log se comparan texto op y op2, op2 es mas largo
                else:
                    print("Ambos textos tienen el mismo largo ("+str(op)+" caracteres).")
                    logging.info('[Comparar Textos] Textos %d y %d seleccionados. Ambos textos son del mismo largo (%d caracteres)', op, op2, largo1)

def ingresar_texto():
    print("\nIngrese el texto que desee agregar a la pila:")
    while True:
        texto = input("> ")
        largo = calc_largo(texto)
        if largo == -1:
            print("El texto ingresado ha sido rechazado por contener caracteres no permitidos. Inténtelo nuevamente")
            logging.info('[Ingresar Texto] La entrada %s rechazada por contener caracteres no permitidos', texto)
            #log entrada texto no valida
        else:
            break
    stack.append((texto, largo))
    global size, index_larger, index_shorter
    if size != 0:
        if largo > stack[index_larger][1]:
            index_larger = size
        if largo < stack[index_shorter][1]:
            index_shorter = size
    size += 1 
    print("El texto ha sido agregado a la pila correctamente. Su largo es de", largo)
    logging.info('[Ingresar Texto] La entrada %s de largo %d ingresada correctamente a la pila', texto, largo)
    #log nuevo texto agregado en la pos tanto?

def mostrar_texto():
    if size == 0:
        print("\nLa pila se encuentra vacia. Ingrese un texto primero")
        logging.info('[Mostrar Texto] No se puede realizar. Pila vacia')
        #log se pide mostrar texto, se rechaza por pila vacia
    elif size == 1:
        print("\nEn la pila existe un unico texto: ")
        print_texto(0, log_label='[Mostrar Texto]')
        #log se muestra el texto 0
    else:
        print("\nEn la pila existen", size, "textos. Ingrese un numero entre 1 y", size, "para poder ver uno de los textos (0 para cancelar).")
        op = ingresar_op(size)
        if op == 0:
            print("Operacion cancelada.")
            logging.info('[Mostrar Texto] Operación cancelada')
        else:
            print_texto(op, log_label='[Mostrar Texto]')
            #log (se printeo el texto tanto)
        

def menu():
    logging.info('[Pila de Textos] Nueva sesion. Inicio del programa')
    while True:
        texto_menu = """
        
Seleccione una de las siguientes opciones ingresando su respectivo numero:
        
1) Ingresar un texto nuevo a la pila.
2) Mostrar el texto mas largo de la pila.
3) Mostrar el texto mas corto de la pila
4) Mostrar un texto es especifico de la pila
5) Comparar dos textos de la pila

0) Salir"""

        print(texto_menu)
        op = ingresar_op(5)
        if op == 1:
            ingresar_texto()
        elif op == 2:
            texto_largo()
        elif op == 3:
            texto_corto()
        elif op == 4:
            mostrar_texto()
        elif op == 5:
            cmp_textos()
        else:
            logging.info('[Pila de Textos] FInalizando sesion. Cierre del Programa')
            break

#--------------------------------------------------------- PROGRAMA -----------------------------------------------

print("*********************************************************************************************************")
print("                                                 PILA DE TEXTOS                                          ")
print("*********************************************************************************************************")
menu()


