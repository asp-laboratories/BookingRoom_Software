from PyQt6.QtWidgets import QMessageBox

class SalonHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.salon = self.main_window.salon

    # =========================================================================================
    # MÉTODOS PARA SALONES
    # =========================================================================================

    def registrar_salon(self):
        try:
            largo = float(self.navegacion.saLargo.text())
            ancho = float(self.navegacion.saAncho.text())
            altura = float(self.navegacion.saAltura.text())
            m2 = largo * ancho
            self.navegacion.saResultadoM2.setText(str(m2))
            
            resultado = self.salon.registrar_salones(
                self.navegacion.saNombre.text(), 
                float(self.navegacion.saCostoRenta.text()), 
                self.navegacion.saNombrePasillo.text(), 
                self.navegacion.saNumeroPasillo.text(), 
                largo, ancho, altura, m2
            )
            
            if not resultado:
                QMessageBox.critical(
                    None, 
                    "Error de Registro", 
                    "No se pudo registrar el salón. Verifica los datos."
                )
            else:
                QMessageBox.information(
                    None, 
                    "Registro Exitoso", 
                    f"El salón '{self.navegacion.saNombre.text()}' ha sido registrado correctamente."
                )
                
        except ValueError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "Asegúrate de que los campos numéricos (Largo, Ancho, Altura, Costo) contengan valores válidos."
            )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error inesperado: {e}"
            ) 

    def actualizar_salon(self):
        try:
            campo = self.navegacion.sCampo_2.text()
            id_busqueda = int(self.navegacion.slIngresarBusqueda_4.text()) 
            nuevo_valor = self.navegacion.sNuevoValor_2.text()
            
            resultado = self.salon.actualizar_campos(campo, id_busqueda, nuevo_valor)
            
            if not resultado:
                QMessageBox.critical(
                    None,
                    "Error de Actualización", 
                    f"No se pudo actualizar el campo '{campo}' del salón {id_busqueda}. Verifica el campo."
                )
            else:
                QMessageBox.information(
                    None, 
                    "Actualización Exitosa", 
                    f"El salón con ID {id_busqueda} ha sido actualizado correctamente."
                )
                
        except ValueError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "Asegúrate de que el campo de búsqueda contenga un valor numérico entero válido."
            )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error inesperado durante la actualización: {e}"
            )

    def listar_salones_del(self):
        resultado = self.salon.listar_salones()
        if not resultado:
            pass
        else:
            mensaje = "\n---SALONES---\n"
            for sali in resultado:
                mensaje += f"\nNumero: {sali["numSalon"]}.\nNombre: {sali["nombre"]}.\n"
            self.navegacion.sResultadoListar_6.setText(mensaje)

    def eliminar_salon(self, id_salon: int):
        try:
            resultado = self.salon.eliminar_salones(id_salon)
            
            if not resultado:
                QMessageBox.critical(
                    None, 
                    "Error de Eliminación", 
                    f"No se pudo eliminar el salon {id_salon}. Es posible que no exista o haya un error en la base de datos."
                )
            else:
                QMessageBox.information(
                    None, 
                    "Eliminación Exitosa", 
                    f"El salon {id_salon} ha sido eliminado correctamente."
                )
                
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error grave durante la operación de eliminación: {e}"
            )

    def desplegar_informacion_salon(self):
        self.navegacion.sResultadoListar_4.clear()
        try: 
            sali = self.salon.listar_salones_informacion(self.navegacion.slIngresarBusqueda_4.text())
            if not sali:
                pass
            else:
                mensaje = "INFORMACION DEL SALON\n"
                mensaje += f"\n -Nombre: {sali["nombre"]}"
                mensaje += f"\n -Costo de renta: {str(sali["costoRenta"])}"
                mensaje += "\n -Dimensiones:"
                mensaje += f"\n -Largo del salon: {str(sali["dimenLargo"])}"
                mensaje += f"\n -Ancho del salon: {str(sali['dimenAncho'])}"
                mensaje += f"\n -Altura del salon: {str(sali['dimenAltura'])}"
                mensaje += f"\n -Metros cuadrados: {str(sali["mCuadrados"])}"
                mensaje += f"\n -Ubicado en:{sali["ubiNombrePas"]} y numero {sali['ubiNumeroPas']}"
                mensaje += f"\n -Nombre del pasillo: {sali["ubiNombrePas"]}"
                mensaje += f"\n -Numero del pasillo: {sali['ubiNumeroPas']}"
                self.navegacion.sResultadoListar_4.setText(mensaje)
        except ValueError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "El numero de salon debe ser un número entero válido."
            )
        except TypeError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "El numero de salon debe ser un número entero válido."
            )

    def cargar_seleccion_estado_salon(self):
        self.navegacion.reSalonSelecc_2.clear()
        self.navegacion.reSalonSelecc_2.addItem("Seleccione un estado:", None)
        self.navegacion.reSalonSelecc_3.addItem("Seleccione un estado:", None)
        estado = self.salon.listar_estados()

        for es in estado:
            self.navegacion.reSalonSelecc_2.addItem(es['descripcion'], es['codigoSal'])
            self.navegacion.reSalonSelecc_3.addItem(es['descripcion'], es['codigoSal'])

    def buscar_estado_salon(self):
        self.navegacion.almResulE_6.setText("")
        estado = self.navegacion.reSalonSelecc_2.currentText()
        resultado = self.salon.salon_en_estado(estado)
        if resultado:
            mensaje = ""
            for bes in resultado:
                mensaje += f"\n{bes["numero"]}. {bes["salon"]}\n"
            self.navegacion.almResulE_6.setText(mensaje)
            
    def cambiar_estado_salon_ejecutar(self, numSalon: int, estado: str):
        try:
            resultado = self.salon.actualizar_salon(numSalon, estado)
            if resultado:
                QMessageBox.information(
                    None, 
                    "Actualización Exitosa", 
                    f"El estado del Salón #{numSalon} ha sido actualizado a **{estado}** correctamente."
                )
            else:
                QMessageBox.critical(
                    None, 
                    "Error de Actualización", 
                    f"No se pudo actualizar el estado del Salón #{numSalon}. Verifique si el salón existe o hay un problema de conexión a la base de datos."
                )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error de Ejecución", 
                f"Ocurrió un error de base de datos durante la actualización: {e}"
            )

    def cargar_seleccion_salon(self):
        self.navegacion.reSalonSelecc.clear()
        self.navegacion.reSalonSelecc.addItem("Selecciona un salon", None)
        obtener = self.salon.listar_salones()
        for sln in obtener:
            self.navegacion.reSalonSelecc.addItem(sln["nombre"], sln["numSalon"])

    def mostrar_info_salon(self):
        salNumero = self.navegacion.reSalonSelecc.currentData()
        if salNumero:
            sali = self.buscar_salon_por_id(salNumero)
            mensaje = "INFORMACION DEL SALON\n"
            mensaje += f"\n -Nombre: {sali["nombre"]}"
            mensaje += f"\n -Costo de renta: {str(sali["costoRenta"])}"
            mensaje += f"\n -Dimensiones: {str(sali["dimenLargo"])}x{str(sali['dimenAncho'])}x{str(sali['dimenAltura'])}"
            mensaje += f"\n -Ubicado en el pasillo {sali["ubiNombrePas"]} y numero {sali['ubiNumeroPas']}"
            
            self.main_window.subtotal_salon = sali["costoRenta"]
            if sali:
                self.navegacion.resultadoSalon.setText(mensaje)
        else:
            self.navegacion.resultadoSalon.setText("Seleccione un salon")

    def buscar_salon_por_id(self, salNumero):
        for s in self.salon.listar_salones():
            if s["numSalon"] == salNumero:
                return s
        return None

    def limpiar_salon(self):
        self.navegacion.saNombre.clear()
        self.navegacion.saCostoRenta.clear()
        self.navegacion.saNombrePasillo.clear()
        self.navegacion.saNumeroPasillo.clear()
        self.navegacion.saLargo.clear()
        self.navegacion.saAncho.clear()
        self.navegacion.saAltura.clear()
        self.navegacion.saResultadoM2.clear()

    # Confirmation methods
    def intentar_registrar_salon(self):
        nombre_salon = self.navegacion.saNombre.text()
        if self.main_window.mostrar_confirmacion(
            "Confirmar Registro de Salón", 
            f"¿Deseas registrar el salón '{nombre_salon}'?"
        ):
            self.registrar_salon() 
        else:
            print("Registro de salón cancelado.")

    def intentar_actualizar_salon(self):
        try:
            campo = self.navegacion.sCampo_2.text()
            id_busqueda = int(self.navegacion.slIngresarBusqueda_4.text()) 
            nuevo_valor = self.navegacion.sNuevoValor_2.text()
            
            if self.main_window.mostrar_confirmacion(
                "Confirmar Actualización", 
                f"¿Estás seguro de actualizar el campo '{campo}' del salón {id_busqueda} al nuevo valor '{nuevo_valor}'?"
            ):
                self.actualizar_salon()
            else:
                QMessageBox.information(
                    None, 
                    "Actualización Cancelada", 
                    "La operación de actualización ha sido cancelada."
                )
        except ValueError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "Asegúrate de que el campo de ID contenga un valor numérico entero válido."
            )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error de Pre-Validación", 
                f"Ocurrió un error al procesar los datos: {e}"
            )

    def intentar_eliminar_salon(self):
        try:
            salon_a_eliminar = int(self.navegacion.seEliminarInput_2.text())
            if self.main_window.mostrar_confirmacion(
                "Confirmar Eliminación", 
                f"Advertencia: ¿Estás seguro de que deseas ELIMINAR el salon: {salon_a_eliminar}? Esta acción es irreversible."
            ):
                self.eliminar_salon(salon_a_eliminar)
            else:
                QMessageBox.information(
                    None, 
                    "Operación Cancelada", 
                    "La eliminación del salon ha sido cancelada por el usuario."
                )
        except ValueError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "El numero de salon a eliminar debe ser un número entero válido."
            )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error de Pre-Validación", 
                f"Ocurrió un error al intentar leer el ID: {e}"
            )

    def intentar_cambiar_estado_salon(self):
        try:
            estado = self.navegacion.reSalonSelecc_3.currentData()
            numSalon_txt = self.navegacion.sCampo_4.text().strip()
            numSalon = int(numSalon_txt)
            
            if estado is None or not estado:
                raise ValueError("Estado Faltante")
            if numSalon <= 0:
                raise ValueError("Número Salón Inválido")
    
            if self.main_window.mostrar_confirmacion(
                "Confirmar Cambio de Estado",
                f"¿Estás seguro de que deseas cambiar el estado del Salón #{numSalon} a '{estado}'?"
            ):
                self.cambiar_estado_salon_ejecutar(numSalon, estado)
            else:
                QMessageBox.information(
                    None, 
                    "Operación Cancelada", 
                    "El cambio de estado del salón ha sido cancelado."
                )
        except ValueError as e:
            error_type = str(e)
            if "invalid literal for int()" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El Número de Salón debe ser un valor numérico entero válido."
                )
            elif "Número Salón Inválido" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El Número de Salón debe ser mayor que cero."
                )
            elif "Estado Faltante" in error_type:
                 QMessageBox.warning(
                    None, "Datos Faltantes", "Debe seleccionar un nuevo estado para el salón."
                )
            else:
                 QMessageBox.critical(
                    None, "Error de Validación", f"Ocurrió un error inesperado al validar: {e}"
                )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error grave durante el proceso: {e}"
            )
