def obt_int(mensaje, intento=1):
    print(mensaje)
    try:
        return int(input())
    except ValueError:
        print("Valor invalido, favor de ingresar un valor numerico")
        intento += 1
        return obt_int(mensaje, intento)


def obt_float(mensaje, intento=1):
    print(mensaje)
    try:
        return float(input())
    except ValueError:
        print("Valor invalido, favor de ingresar un valor numerico")
        intento += 1
        return obt_float(mensaje, intento)
