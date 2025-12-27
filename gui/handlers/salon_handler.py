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
                largo,
                ancho,
                altura,
                m2,
            )

            if not resultado:
                QMessageBox.critical(
                    None,
                    "Error de Registro",
                    "No se pudo registrar el salón. Verifica los datos.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Registro Exitoso",
                    f"El salón '{self.navegacion.saNombre.text()}' ha sido registrado correctamente.",
                )

        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "Asegúrate de que los campos numéricos (Largo, Ancho, Altura, Costo) contengan valores válidos.",
            )
        except Exception as e:
            QMessageBox.critical(
                None, "Error Inesperado", f"Ocurrió un error inesperado: {e}"
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
                    f"No se pudo actualizar el campo '{campo}' del salón {id_busqueda}. Verifica el campo.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Actualización Exitosa",
                    f"El salón con ID {id_busqueda} ha sido actualizado correctamente.",
                )

        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "Asegúrate de que el campo de búsqueda contenga un valor numérico entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error inesperado durante la actualización: {e}",
            )

    def listar_salones_del(self):
        self.navegacion.sResultadoListar_6.clear()
        try:
            resultado = self.salon.listar_salones()

            if not resultado:
                self.navegacion.sResultadoListar_6.setText("No hay salones registrados para mostrar.")
            else:
                mensaje_html = '<div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">'
                mensaje_html += '<h3 style="color: #9b582b;">LISTA DE SALONES</h3>'
                
                for sali in resultado:
                    numSalon = sali.get('numSalon', 'N/A')
                    nombre = sali.get('nombre', 'N/A')
                    
                    mensaje_html += f"""
                    <div style="border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 5px;">
                        <p><b>Número:</b> {numSalon}</p>
                        <p><b>Nombre:</b> {nombre}</p>
                    </div>
                    """
                
                mensaje_html += "</div>"
                self.navegacion.sResultadoListar_6.setHtml(mensaje_html)
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error inesperado",
                f"Ocurrió un error al listar los salones: {e}",
            )

    def eliminar_salon(self, id_salon: int):
        try:
            resultado = self.salon.eliminar_salones(id_salon)

            if not resultado:
                QMessageBox.critical(
                    None,
                    "Error de Eliminación",
                    f"No se pudo eliminar el salon {id_salon}. Es posible que no exista o haya un error en la base de datos.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Eliminación Exitosa",
                    f"El salon {id_salon} ha sido eliminado correctamente.",
                )

        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error grave durante la operación de eliminación: {e}",
            )

    def desplegar_informacion_salon(self):
        self.navegacion.sResultadoListar_4.clear()
        try:
            termino_busqueda = self.navegacion.slIngresarBusqueda_4.text()
            sali = self.salon.listar_salones_informacion(termino_busqueda)

            if not sali:
                self.navegacion.sResultadoListar_4.setText(f"No se encontró información para el salón: {termino_busqueda}")
            else:
                nombre = sali.get('nombre', 'N/A')
                costoRenta = float(sali.get('costoRenta', 0.0))
                dimenLargo = sali.get('dimenLargo', 'N/A')
                dimenAncho = sali.get('dimenAncho', 'N/A')
                dimenAltura = sali.get('dimenAltura', 'N/A')
                mCuadrados = sali.get('mCuadrados', 'N/A')
                ubiNombrePas = sali.get('ubiNombrePas', 'N/A')
                ubiNumeroPas = sali.get('ubiNumeroPas', 'N/A')

                mensaje_html = f"""
                <div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">
                    <h3 style="color: #9b582b;">INFORMACIÓN DETALLADA DEL SALÓN</h3>
                    <p><b>Nombre:</b> {nombre}</p>
                    <p><b>Costo de Renta:</b> ${costoRenta:,.2f}</p>
                    <p><b>Dimensiones:</b></p>
                    <ul>
                        <li>Largo: {dimenLargo} m</li>
                        <li>Ancho: {dimenAncho} m</li>
                        <li>Altura: {dimenAltura} m</li>
                        <li>Metros Cuadrados: {mCuadrados} m²</li>
                    </ul>
                    <p><b>Ubicación:</b></p>
                    <ul>
                        <li>Pasillo: {ubiNombrePas}</li>
                        <li>Número de Pasillo: {ubiNumeroPas}</li>
                    </ul>
                </div>
                """
                self.navegacion.sResultadoListar_4.setHtml(mensaje_html)
        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "El número de salón debe ser un número entero válido para la búsqueda.",
            )
        except TypeError: # This might occur if list_salones_informacion returns unexpected data
            QMessageBox.warning(
                None,
                "Error de datos",
                "No se pudieron procesar los datos del salón. Verifique el formato.",
            )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error inesperado",
                f"Ocurrió un error al desplegar la información del salón: {e}",
            )

    def cargar_seleccion_estado_salon(self):
        self.navegacion.reSalonSelecc_2.clear()
        self.navegacion.reSalonSelecc_2.addItem("Seleccione un estado:", None)
        self.navegacion.reSalonSelecc_3.addItem("Seleccione un estado:", None)
        estado = self.salon.listar_estados()

        for es in estado:
            self.navegacion.reSalonSelecc_2.addItem(es["descripcion"], es["codigoSal"])
            self.navegacion.reSalonSelecc_3.addItem(es["descripcion"], es["codigoSal"])

    def buscar_estado_salon(self):
        self.navegacion.almResulE_6.setText("")
        try:
            estado_seleccionado = self.navegacion.reSalonSelecc_2.currentText()
            if not estado_seleccionado or estado_seleccionado == "Seleccione un estado:":
                self.navegacion.almResulE_6.setText("Por favor, seleccione un estado válido para buscar.")
                return

            resultado = self.salon.salon_en_estado(estado_seleccionado)

            if not resultado:
                self.navegacion.almResulE_6.setText(f"No hay salones en estado: '{estado_seleccionado}'.")
            else:
                mensaje_html = '<div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">'
                mensaje_html += f'<h3 style="color: #9b582b;">SALONES EN ESTADO: {estado_seleccionado.upper()}</h3>'
                
                for bes in resultado:
                    numero = bes.get('numero', 'N/A')
                    salon_nombre = bes.get('salon', 'N/A')
                    
                    mensaje_html += f"""
                    <div style="border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 5px;">
                        <p><b>Número:</b> {numero}</p>
                        <p><b>Salón:</b> {salon_nombre}</p>
                    </div>
                    """
                
                mensaje_html += "</div>"
                self.navegacion.almResulE_6.setHtml(mensaje_html)
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error inesperado",
                f"Ocurrió un error al buscar salones por estado: {e}",
            )

    def cambiar_estado_salon_ejecutar(self, numSalon: int, estado: str):
        try:
            resultado = self.salon.actualizar_salon(numSalon, estado)
            if resultado:
                QMessageBox.information(
                    None,
                    "Actualización Exitosa",
                    f"El estado del Salón #{numSalon} ha sido actualizado a **{estado}** correctamente.",
                )
            else:
                QMessageBox.critical(
                    None,
                    "Error de Actualización",
                    f"No se pudo actualizar el estado del Salón #{numSalon}. Verifique si el salón existe o hay un problema de conexión a la base de datos.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error de Ejecución",
                f"Ocurrió un error de base de datos durante la actualización: {e}",
            )

    def cargar_seleccion_salon(self):
        self.navegacion.reSalonSelecc.clear()
        self.navegacion.reSalonSelecc.addItem("Selecciona un salon", None)
        obtener = self.salon.listar_salones()
        for sln in obtener:
            self.navegacion.reSalonSelecc.addItem(sln["nombre"], sln["numSalon"])

    def mostrar_info_salon(self):
        salNumero = self.navegacion.reSalonSelecc.currentData()
        self.navegacion.resultadoSalon.clear() # Clear previous content
        if salNumero is None:
            self.navegacion.resultadoSalon.setText("Seleccione un salón para ver su información.")
            return

        sali = self.buscar_salon_por_id(salNumero)
        if sali:
            # Prepare data for display
            nombre = sali.get('nombre', 'N/A')
            costoRenta = float(sali.get('costoRenta', 0.0))
            dimenLargo = sali.get('dimenLargo', 'N/A')
            dimenAncho = sali.get('dimenAncho', 'N/A')
            dimenAltura = sali.get('dimenAltura', 'N/A')
            mCuadrados = sali.get('mCuadrados', 'N/A')
            ubiNombrePas = sali.get('ubiNombrePas', 'N/A')
            ubiNumeroPas = sali.get('ubiNumeroPas', 'N/A')

            mensaje_html = f"""
            <div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">
                <h3 style="color: #9b582b;">INFORMACIÓN DEL SALÓN</h3>
                <p><b>Nombre:</b> {nombre}</p>
                <p><b>Costo de Renta:</b> ${costoRenta:,.2f}</p>
                <p><b>Dimensiones:</b></p>
                <ul>
                    <li>Largo: {dimenLargo} m</li>
                    <li>Ancho: {dimenAncho} m</li>
                    <li>Altura: {dimenAltura} m</li>
                    <li>Metros Cuadrados: {mCuadrados} m²</li>
                </ul>
                <p><b>Ubicación:</b></p>
                <ul>
                    <li>Pasillo: {ubiNombrePas}</li>
                    <li>Número de Pasillo: {ubiNumeroPas}</li>
                </ul>
            </div>
            """
            # Ensure subtotal_salon is a float for calculations
            self.main_window.subtotal_salon = float(costoRenta) 
            self.navegacion.resultadoSalon.setHtml(mensaje_html)
        else:
            self.navegacion.resultadoSalon.setText("No se encontró información para el salón seleccionado.")

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
            f"¿Deseas registrar el salón '{nombre_salon}'?",
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
                f"¿Estás seguro de actualizar el campo '{campo}' del salón {id_busqueda} al nuevo valor '{nuevo_valor}'?",
            ):
                self.actualizar_salon()
            else:
                QMessageBox.information(
                    None,
                    "Actualización Cancelada",
                    "La operación de actualización ha sido cancelada.",
                )
        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "Asegúrate de que el campo de ID contenga un valor numérico entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error de Pre-Validación",
                f"Ocurrió un error al procesar los datos: {e}",
            )

    def intentar_eliminar_salon(self):
        try:
            salon_a_eliminar = int(self.navegacion.seEliminarInput_2.text())
            if self.main_window.mostrar_confirmacion(
                "Confirmar Eliminación",
                f"Advertencia: ¿Estás seguro de que deseas ELIMINAR el salon: {salon_a_eliminar}? Esta acción es irreversible.",
            ):
                self.eliminar_salon(salon_a_eliminar)
            else:
                QMessageBox.information(
                    None,
                    "Operación Cancelada",
                    "La eliminación del salon ha sido cancelada por el usuario.",
                )
        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "El numero de salon a eliminar debe ser un número entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error de Pre-Validación",
                f"Ocurrió un error al intentar leer el ID: {e}",
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
                f"¿Estás seguro de que deseas cambiar el estado del Salón #{numSalon} a '{estado}'?",
            ):
                self.cambiar_estado_salon_ejecutar(numSalon, estado)
            else:
                QMessageBox.information(
                    None,
                    "Operación Cancelada",
                    "El cambio de estado del salón ha sido cancelado.",
                )
        except ValueError as e:
            error_type = str(e)
            if "invalid literal for int()" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El Número de Salón debe ser un valor numérico entero válido.",
                )
            elif "Número Salón Inválido" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El Número de Salón debe ser mayor que cero.",
                )
            elif "Estado Faltante" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Faltantes",
                    "Debe seleccionar un nuevo estado para el salón.",
                )
            else:
                QMessageBox.critical(
                    None,
                    "Error de Validación",
                    f"Ocurrió un error inesperado al validar: {e}",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error grave durante el proceso: {e}",
            )
