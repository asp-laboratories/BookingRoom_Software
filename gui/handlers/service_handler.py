from PyQt6.QtWidgets import QMessageBox
from utils.Formato import permitir_ingreso

class ServiceHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        
        # Access service instances from the main screen
        self.servicio = self.main_window.servicio
        self.tipo_servi = self.main_window.tipo_servi

    # =========================================================================================
    # MÉTODOS PARA SERVICIOS
    # =========================================================================================

    def cargar_tipos_servicios(self):
        self.navegacion.sTipoServicio.clear()
        self.navegacion.sTipoServicio.addItem("Seleccione un tipo de servicio:", None)

        tpos_servcios = self.tipo_servi.listar_tipos_servicios()

        for tipo in tpos_servcios:
            self.navegacion.sTipoServicio.addItem(tipo['descripcion'], tipo['codigoTiSer'])

    def registrar_servicio(self, nombre, descripcion, costo_renta, tipo_servicio):
        try:
            resultado = self.servicio.registrar_servicio(nombre, descripcion, costo_renta, tipo_servicio)
    
            if not resultado:
                QMessageBox.critical(
                    None, 
                    "Error de Registro", 
                    f"El servicio '{nombre}' no pudo ser registrado. Puede que ya exista o haya un error de base de datos."
                )
            else:
                QMessageBox.information(
                    None, 
                    "Registro Exitoso", 
                    f"El servicio '{nombre}' ha sido registrado correctamente."
                )
    
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error de conexión/base de datos durante el registro: {e}"
            )

    def actualizar_servicio(self, campo: str, id_busqueda: int, nuevo_valor: str):
        try:
            resultado = self.servicio.actualizar_campos(campo, id_busqueda, nuevo_valor)
            
            if not resultado:
                QMessageBox.critical(
                    None, 
                    "Error de Actualización", 
                    f"No se pudo actualizar el campo '{campo}' del serviciO{id_busqueda}. Verifique los datos, el numero o el tipo de valor nuevo."
                )
            else:
                QMessageBox.information(
                    None, 
                    "Actualización Exitosa", 
                    f"El servicio {id_busqueda} ha sido actualizado correctamente."
                )
                
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error de conexión/base de datos: {e}"
            )

    def listar_servicio(self): # No necesaria
        self.navegacion.sResultadoListar.clear()

        resultado = self.servicio.listar_servicio_busqueda(int(self.navegacion.slIngresarBusqueda.text()))
        if not resultado:
            pass
        else:
            mensaje = "\n---SERVICIOS---\n"
            for ser in resultado:
                mensaje += f"\nNumero: {ser["numServicio"]}.\nNombre: {ser["nombre"]}.\nCosto Renta: {ser["costoRenta"]}\n"
            self.navegacion.sResultadoListar.setText(mensaje)

    def listar_servicio_act(self):
        self.navegacion.sResultadoListar_3.clear()
        try:
            resultado = self.servicio.listar_servicio_busqueda(int(self.navegacion.slIngresarBusqueda_3.text()))
            if not resultado:
                pass
            else:
                mensaje = "\n---SERVICIOS---\n"
                for ser in resultado:
                    mensaje += f"\nNumero: {ser["numServicio"]}.\nNombre: {ser["nombre"]}.\nCosto Renta: {ser["costoRenta"]}\n"
                self.navegacion.sResultadoListar_3.setText(mensaje)
        except ValueError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "El numero de servicio a eliminar debe ser un número entero válido."
            )

    def listar_servicio_del(self):
        self.navegacion.sResultadoListar_2.clear()
        resultado = self.servicio.listar_servicio()
        if not resultado:
            pass
        else:
            mensaje = "\n---SERVICIOS---\n"
            for ser in resultado:
                mensaje += f"\nNumero: {ser["numServicio"]}.\nNombre: {ser["nombre"]}.\nCosto Renta: {ser["costoRenta"]}\n"
            self.navegacion.sResultadoListar_2.setText(mensaje)

    def listar_servicios_del_mismo_tipo(self):
        self.navegacion.sResultadoListar_2.clear()
        tposervicio = self.navegacion.slIngresarBusqueda_2.text()
        if not permitir_ingreso(tposervicio, 'onlytext'):
            QMessageBox.warning(self.navegacion, "Tipo de dato no valido", "Favor de ingresar el nombre del tipo de servicio")
            return

        resultado = self.servicio.servicios_tipo(tposervicio)
        if not resultado:
            pass
        else:
            mensaje = "\n---SERVICIOS---\n"
            for st in resultado:
                mensaje += f"\nTipo de servicio: {st["tipo_servicio"]}"
            self.navegacion.sResultadoListar_2.setText(mensaje)
    
    def eliminar_servicio(self, id_servicio: int):
        try:
            resultado = self.servicio.eliminar_fila(id_servicio)
            
            if not resultado:
                QMessageBox.critical(
                    None, 
                    "Error de Eliminación", 
                    f"No se pudo eliminar el servicio {id_servicio}. Verifique que el numero exista o haya un error en la base de datos."
                )
            else:
                QMessageBox.information(
                    None, 
                    "Eliminación Exitosa", 
                    f"El servicio {id_servicio} ha sido eliminado correctamente."
                )
                
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error grave de base de datos durante la eliminación: {e}"
            )

    def buscar_tipo_ser(self):
        resultado = self.tipo_servi.mostrar_servicios_de_tipo(self.navegacion.tipoBuscar.text())
        if resultado:
            mensaje = f"\n--- {resultado} ---\n Servicios:\n"
            if resultado.servicios:
                for servicios in resultado.servicios:
                    mensaje += f"- {servicios.nombre}\n"
            else:
                print(" No tiene servicios registrados")

            self.navegacion.tResultadoS.setText(mensaje)

    def listar_servicio_segun_tipo(self):
        self.navegacion.tResultadoS.clear() # Limpiar resultados anteriores
        try:
            tipo_buscado = self.navegacion.tipoBuscar.text().strip()
            
            if not tipo_buscado:
                QMessageBox.warning(
                    None,
                    "Búsqueda Inválida", 
                    "Por favor, ingresa el **nombre del tipo de servicio** para realizar la búsqueda."
                )
                return
    
            resultado = self.servicio.listar_servicio_y_tipo(tipo_buscado)
            
            if resultado and isinstance(resultado, list) and len(resultado) > 0:
                mensaje = f"\n--- SERVICIOS ENCONTRADOS PARA: {tipo_buscado.upper()} ---\n"
                
                for ts in resultado:
                    mensaje += f"\nServicio: {ts.get('servicio', 'N/D')}\n"
                    mensaje += f"Descripción: {ts.get('descservicio', 'N/D')}\n"
                    mensaje += f"Costo Renta: {ts.get('costo_renta', 'N/D')}\n"
                    mensaje += "--------------------------------------"
    
                self.navegacion.tResultadoS.setText(mensaje)
            
            else:
                QMessageBox.information(
                    None,
                    "Sin Resultados", 
                    f"No se encontraron servicios registrados para el tipo: **{tipo_buscado}**."
                )
                self.navegacion.tResultadoS.setText(f"Tipo '{tipo_buscado}' sin servicios.")
    
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado", 
                f"Ocurrió un error al intentar listar los servicios: {e}"
            )

    def buscar_tipoS_eli(self):
        resultado = self.tipo_servi.listar_tipos_servicio(self.navegacion.tipoBusqueda.text())
        if resultado:
            mensaje = "\nTipo de servicios\n"
            for row in resultado:
                mensaje += f"\nCodigo del tipo: {row['codigoTiSer']}\nDescripcion del tipo: {row['descripcion']}\n"
            self.navegacion.tipoResultado.setText(mensaje)

    # =========================================================================================
    # MÉTODOS DE CONFIRMACIÓN (UI Triggers)
    # =========================================================================================
    
    def intentar_registrar_servicio(self):
        try:
            nombre = self.navegacion.sNombreSer.text()
            if len(nombre) < 2:
                raise ValueError("Nombre")
    
            descripcion = self.navegacion.sDescripcion.text()
            if len(descripcion) < 2:
                raise ValueError("Descripción")
    
            resCostoRenta = self.navegacion.sCostoRenta.text()
            costo_renta = float(resCostoRenta)
    
            if costo_renta < 1:
                 raise ValueError("Costo Inválido")
    
            tipo_servicio_data = self.navegacion.sTipoServicio.currentData()
            if not tipo_servicio_data: 
                raise ValueError("Tipo de Servicio")
    
            if self.main_window.mostrar_confirmacion(
                "Confirmar Registro de Servicio", 
                f"¿Deseas registrar el servicio '{nombre}' con un costo de ${costo_renta}?"
            ):
                self.registrar_servicio(nombre, descripcion, costo_renta, tipo_servicio_data)
            else:
                QMessageBox.information(
                    None, 
                    "Registro Cancelado", 
                    "La operación de registro de servicio ha sido cancelada."
                )
    
        except ValueError as e:
            error_type = str(e)
            if "float" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El costo de renta debe ser un valor numérico."
                )
            elif "Nombre" in error_type:
                 QMessageBox.warning(
                    None, "Validación de Datos", "El nombre del servicio no es válido (mínimo 2 caracteres)."
                )
            elif "Descripción" in error_type:
                 QMessageBox.warning(
                    None, "Validación de Datos", "La descripción del servicio no es válida (mínimo 2 caracteres)."
                )
            elif "Costo Inválido" in error_type:
                QMessageBox.warning(
                    None, "Validación de Datos", "El costo del servicio debe ser mayor o igual a 1."
                )
            elif "Tipo de Servicio" in error_type:
                 QMessageBox.warning(
                    None, "Validación de Datos", "Debes seleccionar un tipo de servicio válido."
                )
            else:
                 QMessageBox.critical(
                    None, "Error de Validación", f"Ocurrió un error inesperado en los datos: {e}"
                )

    def intentar_actualizar_servicio(self):
        try:
            campo = self.navegacion.sCampo.text()
            id_busqueda = int(self.navegacion.slIngresarBusqueda_3.text())
            nuevo_valor = self.navegacion.sNuevoValor.text()
            
            if not campo or not nuevo_valor:
                raise ValueError("Campos Vacíos")
    
            if self.main_window.mostrar_confirmacion(
                "Confirmar Actualización de Servicio", 
                f"¿Estás seguro de actualizar el campo '{campo}' del servicio {id_busqueda} al nuevo valor '{nuevo_valor}'?"
            ):
                self.actualizar_servicio(campo, id_busqueda, nuevo_valor)
            else:
                QMessageBox.information(
                    None, 
                    "Actualización Cancelada", 
                    "La operación de actualización del servicio ha sido cancelada."
                )
    
        except ValueError as e:
            error_msg = str(e)
            if "invalid literal for int()" in error_msg:
                QMessageBox.warning(
                    None, 
                    "Datos Inválidos", 
                    "Asegúrate de que el numero de búsqueda contenga un valor numérico entero válido."
                )
            elif "Campos Vacíos" in error_msg:
                 QMessageBox.warning(
                    None, 
                    "Datos Inválidos", 
                    "Los campos 'Campo', 'busqueda' y 'Nuevo Valor' no pueden estar vacíos."
                )
            else:
                 QMessageBox.critical(
                    None, 
                    "Error de Pre-Validación", 
                    f"Ocurrió un error inesperado: {e}"
                )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error de Pre-Validación", 
                f"Ocurrió un error al procesar los datos: {e}"
            )

    def intentar_eliminar_servicio(self):
        try:
            id_servicio_a_eliminar = int(self.navegacion.seEliminarInput.text()) 
            
            if self.main_window.mostrar_confirmacion(
                "Confirmar Eliminación", 
                f"⚠️ **Advertencia:** ¿Estás seguro de ELIMINAR el servicio: {id_servicio_a_eliminar}? Esta acción es irreversible."
            ):
                self.eliminar_servicio(id_servicio_a_eliminar)
            else:
                QMessageBox.information(
                    None, 
                    "Operación Cancelada", 
                    "La eliminación del servicio ha sido cancelada por el usuario."
                )
    
        except ValueError:
            QMessageBox.warning(
                None, 
                "Datos Inválidos", 
                "El ID de servicio a eliminar debe ser un número entero válido."
            )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error de Pre-Validación", 
                f"Ocurrió un error al intentar leer el ID: {e}"
            )
