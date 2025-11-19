
# Ingreso de datos dentro del registro
def permitir_ingreso(texto, formato): 
    permitidoLe = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    permitidoNu = "0123456789"
    PermitidoCaEs = "-_."

    match formato:
        case 1: # Nombre
            texto = texto.replace(" ", "")
            for c in texto:
                if (c not in permitidoLe):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
                else:
                    print("Todo correcto")
            return True # Salida True

        case 2: # Correo
            contador_arrobas = 0
            for c in texto:
                if c == "@":
                    contador_arrobas += 1
                if contador_arrobas > 1:
                    print("Muchso arrobas")
                    return 
            
            if contador_arrobas == 0:
                print("Error no arrobas")
                return
        
            texto = texto.replace("@", '')

            for c in texto:
                if (c not in permitidoLe) and (c not in permitidoNu) and (c not in PermitidoCaEs):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
                else:
                    print("Todo correcto")
            return True

        case 3: # Matricula
            for c in texto:
                if (c not in permitidoNu):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
                else:
                    print("Todo correcto")
            return True

        case 4: # RFC
            for c in texto:
                if (c not in permitidoLe) and (c not in permitidoNu):
                    print("Hay un caracter especial:", c)
                    return False # Salida False
                else:
                    print("Todo correcto")
            return True
