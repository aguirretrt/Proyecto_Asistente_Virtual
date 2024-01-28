#Sube el cursor la cantidad de lineas nL en la terminal
def cursor_arriba(nL = 1):
    print(f'\33[{nL}A', end = '')

