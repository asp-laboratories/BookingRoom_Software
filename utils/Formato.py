
# Ingreso de datos dentro del registro
def permitir_ingreso(texto, formato : str): 
    permitidoLe = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóúÁÉÍÓÚ"
    permitidoNF = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóúÁÉÍÓÚ."
    permitidoNu = "0123456789"
    PermitidoCaEs = "-_."
    
    formato = (formato.lower())

    match formato:
        case 'onlytext': # Solo letras
            texto = texto.replace(" ", "")
            for c in texto:
                if (c not in permitidoLe):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
            print(f"Todo correcto: {texto}")
            return True # Salida True

        case 'correo': # Letras, numeros, puntos, guiones bajos y altos, y un solo arroba
            contador_arrobas = 0
            for c in texto:
                if c == "@":
                    contador_arrobas += 1
                if contador_arrobas > 1:
                    print("Muchso arrobas")
                    return False
            
            if contador_arrobas == 0:
                print("Error no arrobas")
                return False
        
            texto = texto.replace("@", '')

            for c in texto:
                if (c not in permitidoLe) and (c not in permitidoNu) and (c not in PermitidoCaEs):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
            print(f"Todo correcto: {texto}")
            return True

        case 'nombreFiscal': # Letras, numeros, puntos, guiones bajos y altos, y un solo arroba
            texto = texto.replace(" ", "")
            for c in texto:
                if (c not in permitidoNF):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
            print(f"Todo correcto: {texto}")
            return True # Salida True
        

        case 'numtraba': # Numeros de trabajador -> una letra, un guion y solo numeros
            contador_guiones = 0
            for c in texto:
                if c == "-":
                    contador_guiones += 1
                if contador_guiones > 1:
                    print("Muchso guiones")
                    return False
            if contador_guiones == 0:
                print("Error no guiones")
                return False
            texto = texto.replace("-", '')

            contador_Letras = 0
            for c in texto:
                if c in permitidoLe:
                    contador_Letras += 1
                if contador_Letras > 1:
                    print("Muchso letras")
                    return False
            
            if contador_Letras == 0:
                print("Error no letras")
                return False
        
            for c in permitidoLe:
                texto = texto.replace(c, '')
            
            for c in texto:
                if (c not in permitidoNu):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
            print(f"Todo correcto: {texto}")
            return True

        case 'rfc': # RFC -> Letras y numeros
            for c in texto:
                if (c not in permitidoLe) and (c not in permitidoNu):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
            print(f"Todo correcto: {texto}")
            return True
        
        case 'numint': # Numeros -> Enteros
            try:
                numero = int(texto)
                print(f"Todo correcto: {numero}")
                return True
            except:
                print("Error al ingresar un numero entero")
                return False

        case 'numfloat': # Numeros -> Flotantes
            try:
                numero = float(texto)
                print(f"Todo correcto: {numero}")
                return True
            except:
                print("Error al ingresar un numero de punto flotante")
                return False


if __name__ == "__main__":
    nombre = "h h h h"
    correo = 'hjk@s.bb'
    matricula ='j-56757'
    rfc ='ggg777'
    integer ='77'
    flotante ='6-77.7'
    print(f"Nombre: {permitir_ingreso(nombre, 'onlytext')}")
    print(f"Correo: {permitir_ingreso(correo, 'correo')}")
    print(f"Matricula: {permitir_ingreso(matricula, 'numtraba')}")
    print(f"RFC: {permitir_ingreso(rfc, 'rfc')}")
    print(f"Integer: {permitir_ingreso(integer, 'numint')}")
    print(f"Flotante: {permitir_ingreso(flotante, 'numfloat')}")
    flot = None
    if permitir_ingreso(flotante, 'numfloat'):
        flot = flotante
    print(flot)
