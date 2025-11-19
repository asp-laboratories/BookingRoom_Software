
def obt_int(mensaje, intento = 1):
    print(mensaje)
    try:
        return int(input())
    except:
        print("Valor invalido, favor de ingresar un valor numerico")
        intento += 1
        return obt_int(mensaje, intento)