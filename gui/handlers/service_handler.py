from PyQt6.QtWidgets import QMessageBox, QPushButton, QInputDialog, QWidget, QHBoxLayout, QTableWidgetItem, QTableWidget, QAbstractItemView
from functools import partial
from utils.Formato import permitir_ingreso
from gui.table_manager import TableManager
from PyQt6.QtCore import  Qt
class ServiceHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion

        # Access service instances from the main screen
        self.servicio = self.main_window.servicio
        self.tipo_servi = self.main_window.tipo_servi
        
        # Load service types into the combobox and connect the signal
        if hasattr(self.navegacion, 'tipoBuscar'):
            self.cargar_tipos_servicios_for_recepcion()
            self.navegacion.tipoBuscar.currentIndexChanged.connect(self.listar_servicio_segun_tipo)

    def cargar_tipos_servicios_for_recepcion(self):
        self.navegacion.tipoBuscar.clear()
        self.navegacion.tipoBuscar.addItem("Seleccione un tipo de servicio:", None)

        tpos_servcios = self.tipo_servi.listar_tipos_servicios()

        for tipo in tpos_servcios:
            self.navegacion.tipoBuscar.addItem(
                tipo["descripcion"], tipo["codigoTiSer"]
            )

    # =========================================================================================
    # MÉTODOS PARA EXPERIMENTAR
    # =========================================================================================



    # =========================================================================================
    # MÉTODOS PARA SERVICIOS
    # =========================================================================================

    def cargar_tipos_servicios(self):
        self.navegacion.sTipoServicio.clear()
        self.navegacion.sTipoServicio.addItem("Seleccione un tipo de servicio:", None)

        tpos_servcios = self.tipo_servi.listar_tipos_servicios()

        for tipo in tpos_servcios:
            self.navegacion.sTipoServicio.addItem(
                tipo["descripcion"], tipo["codigoTiSer"]
            )

    def registrar_servicio(self, nombre, descripcion, costo_renta, tipo_servicio):
        try:
            resultado = self.servicio.registrar_servicio(
                nombre, descripcion, costo_renta, tipo_servicio
            )

            if not resultado:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Registro",
                    f"El servicio '{nombre}' no pudo ser registrado. Puede que ya exista o haya un error de base de datos.",
                )
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Registro Exitoso",
                    f"El servicio '{nombre}' ha sido registrado correctamente.",
                )

        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos durante el registro: {e}",
            )

    def actualizar_servicio(self, campo: str, id_busqueda: int, nuevo_valor: str):
        try:
            resultado = self.servicio.actualizar_campos(campo, id_busqueda, nuevo_valor)

            if not resultado:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Actualización",
                    f"No se pudo actualizar el campo '{campo}' del servicio {id_busqueda}. Verifique los datos, el número o el tipo de valor nuevo.",
                )
            return resultado

        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos: {e}",
            )
            return False

    def listar_servicio(self):
        # NOTE: Asegúrate de que 'sResultadoListar' sea un QTableWidget en el archivo .ui
        tabla = self.navegacion.sResultadoListar
        try:
            id_busqueda = self.navegacion.slIngresarBusqueda.text().strip()
            if not id_busqueda:
                TableManager.show_message(tabla, "Ingrese un ID para buscar")
                return

            resultado = self.servicio.listar_servicio_busqueda(int(id_busqueda))
            
            if not resultado:
                TableManager.show_message(tabla, f"No se encontró servicio con ID: {id_busqueda}")
                return

            headers = ['Número', 'Nombre', 'Costo Renta']
            # Convertir el diccionario a una lista de listas
            data = [[ser['numServicio'], ser['nombre'], TableManager.format_as_currency(ser['costoRenta'])] for ser in resultado]

            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)

        except ValueError:
            QMessageBox.warning(self.navegacion, "Error", "El ID de búsqueda debe ser un número.")
        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error", f"Error al listar servicio: {e}")


    def listar_servicio_act(self):
        # NOTE: Asegúrate de que 'sResultadoListar_3' sea un QTableWidget en el archivo .ui
        tabla = self.navegacion.sResultadoListar_3
        try:
            id_busqueda = self.navegacion.slIngresarBusqueda_3.text().strip()
            if not id_busqueda:
                TableManager.show_message(tabla, "Ingrese un ID para buscar")
                return
            
            resultado = self.servicio.listar_servicio_busqueda(int(id_busqueda))
            
            if not resultado:
                TableManager.show_message(tabla, f"No se encontró servicio con ID: {id_busqueda}")
                return

            headers = ['ID', 'Nombre', 'Costo', 'Estado']
            data = [[ser['numServicio'], ser['nombre'], TableManager.format_as_currency(ser['costoRenta']), ser.get('estado', 'Activo')] for ser in resultado]

            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)
            
        except ValueError:
            QMessageBox.warning(self.navegacion, "Error", "ID inválido. Debe ser un número.")
        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error", f"Ocurrió un error: {e}")

    def listar_servicio_del(self):
        # NOTE: Asegúrate de que 'sResultadoListar_2' sea un QTableWidget en el archivo .ui
        tabla = self.navegacion.sResultadoListar_2
        try:
            resultado = self.servicio.listar_servicio()
            
            if not resultado:
                TableManager.show_message(tabla, "No hay servicios registrados para mostrar")
                return

            headers = ['Número', 'Nombre', 'Costo Renta']
            data = [[ser['numServicio'], ser['nombre'], TableManager.format_as_currency(ser['costoRenta'])] for ser in resultado]

            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)

        except Exception as e:
            QMessageBox.warning(self.navegacion, "Error", f"Error al listar servicios: {e}")

    # def listar_servicio_segun_tipo(self):
    #     # NOTE: Asegúrate de que 'tResultadoS' sea un QTableWidget en el archivo .ui
    #     tabla = self.navegacion.tResultadoS
    #     try:
    #         tipo_buscado = self.navegacion.tipoBuscar.currentText()
    #
    #         if not tipo_buscado or self.navegacion.tipoBuscar.currentIndex() == 0:
    #             tabla.setRowCount(0)
    #             TableManager.show_message(tabla, "Seleccione un tipo de servicio para buscar.")
    #             return
    #
    #         resultado = self.servicio.listar_servicio_y_tipo(tipo_buscado)
    #
    #         if not resultado:
    #             TableManager.show_message(tabla, f"No se encontraron servicios para el tipo: '{tipo_buscado}'")
    #             return
    #         
    #         headers = ['Servicio', 'Descripción', 'Costo Renta']
    #         data = [[ts.get('servicio', 'N/D'), ts.get('descservicio', 'N/D'), TableManager.format_as_currency(ts.get('costo_renta', 'N/D'))] for ts in resultado]
    #         
    #         tabla.setColumnCount(len(headers))
    #         tabla.setHorizontalHeaderLabels(headers)
    #         TableManager.fill_table(tabla, data)
    #
    #     except Exception as e:
    #         QMessageBox.critical(
    #             self.navegacion,
    #             "Error Inesperado",
    #             f"Ocurrió un error al intentar listar los servicios: {e}",
    #         )


    def buscar_tipoS_eli(self):
        # NOTE: Asegúrate de que 'tipoResultado' sea un QTableWidget en el archivo .ui
        tabla = self.navegacion.tipoResultado
        try:
            tipo_busqueda = self.navegacion.tipoBusqueda.text()
            resultado = self.tipo_servi.listar_tipos_servicio(tipo_busqueda)
            
            if not resultado:
                TableManager.show_message(tabla, f"No se encontró un tipo de servicio con el nombre '{tipo_busqueda}'")
                return

            headers = ['Código', 'Descripción']
            data = [[row['codigoTiSer'], row['descripcion']] for row in resultado]
            
            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)

        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error", f"Ocurrió un error al buscar: {e}")


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
                f"¿Deseas registrar el servicio '{nombre}' con un costo de ${costo_renta}?",
            ):
                self.registrar_servicio(
                    nombre, descripcion, costo_renta, tipo_servicio_data
                )
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Registro Cancelado",
                    "La operación de registro de servicio ha sido cancelada.",
                )

        except ValueError as e:
            error_type = str(e)
            if "float" in error_type:
                QMessageBox.warning(
                    self.navegacion,
                    "Datos Inválidos",
                    "El costo de renta debe ser un valor numérico.",
                )
            elif "Nombre" in error_type:
                QMessageBox.warning(
                    self.navegacion,
                    "Validación de Datos",
                    "El nombre del servicio no es válido (mínimo 2 caracteres).",
                )
            elif "Descripción" in error_type:
                QMessageBox.warning(
                    self.navegacion,
                    "Validación de Datos",
                    "La descripción del servicio no es válida (mínimo 2 caracteres).",
                )
            elif "Costo Inválido" in error_type:
                QMessageBox.warning(
                    self.navegacion,
                    "Validación de Datos",
                    "El costo del servicio debe ser mayor o igual a 1.",
                )
            elif "Tipo de Servicio" in error_type:
                QMessageBox.warning(
                    self.navegacion,
                    "Validación de Datos",
                    "Debes seleccionar un tipo de servicio válido.",
                )
            else:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Validación",
                    f"Ocurrió un error inesperado en los datos: {e}",
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
                f"¿Estás seguro de actualizar el campo '{campo}' del servicio {id_busqueda} al nuevo valor '{nuevo_valor}'?",
            ):
                self.actualizar_servicio(campo, id_busqueda, nuevo_valor)
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Actualización Cancelada",
                    "La operación de actualización del servicio ha sido cancelada.",
                )

        except ValueError:
            QMessageBox.warning(
                self.navegacion,
                "Datos Inválidos",
                "Asegúrate de que el número de búsqueda sea un valor numérico válido y que los demás campos no estén vacíos.",
            )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Pre-Validación",
                f"Ocurrió un error al procesar los datos: {e}",
            )

    def intentar_eliminar_servicio(self):
        try:
            id_servicio_a_eliminar = int(self.navegacion.seEliminarInput.text())

            if self.main_window.mostrar_confirmacion(
                "Confirmar Eliminación",
                f"⚠️ **Advertencia:** ¿Estás seguro de ELIMINAR el servicio: {id_servicio_a_eliminar}? Esta acción es irreversible.",
            ):
                self.eliminar_servicio(id_servicio_a_eliminar)
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Operación Cancelada",
                    "La eliminación del servicio ha sido cancelada por el usuario.",
                )

        except ValueError:
            QMessageBox.warning(
                self.navegacion,
                "Datos Inválidos",
                "El ID de servicio a eliminar debe ser un número entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Pre-Validación",
                f"Ocurrió un error al intentar leer el ID: {e}",
            )


# ... dentro de tu clase principal ...
    # ... (Tu inicialización habitual)

    # def listar_servicio_segun_tipo(self):
    #     tabla = self.navegacion.tResultadoS
    #     
    #     # 1. Desconectar señal para evitar bucles al llenar la tabla
    #     try:
    #         tabla.itemChanged.disconnect()
    #     except (TypeError, RuntimeError):
    #         pass 
    #
    #     try:
    #         tipo_buscado = self.navegacion.tipoBuscar.currentText()
    #         if not tipo_buscado or self.navegacion.tipoBuscar.currentIndex() == 0:
    #             tabla.setRowCount(0)
    #             return
    #
    #         resultado = self.servicio.listar_servicio_y_tipo(tipo_buscado)
    #         
    #         headers = ['ID', 'Servicio', 'Descripción', 'Costo Renta']
    #         tabla.setColumnCount(len(headers))
    #         tabla.setHorizontalHeaderLabels(headers)
    #         tabla.setRowCount(0)
    #
    #         for row_number, ts in enumerate(resultado):
    #             tabla.insertRow(row_number)
    #             
    #             # Columna ID: No editable (Sintaxis PyQt6)
    #             id_item = QTableWidgetItem(str(ts.get('id_servicio', '0')))
    #             id_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #             tabla.setItem(row_number, 0, id_item)
    #             
    #             # Columnas editables: Al presionar Enter sobre estas, saltará la confirmación
    #             tabla.setItem(row_number, 1, QTableWidgetItem(str(ts.get('servicio', 'N/D'))))
    #             tabla.setItem(row_number, 2, QTableWidgetItem(str(ts.get('descservicio', 'N/D'))))
    #             tabla.setItem(row_number, 3, QTableWidgetItem(str(ts.get('costo_renta', '0'))))
    #
    #         # 2. Conectar la señal: Se activa cuando el usuario cambia algo y pulsa ENTER o cambia de celda
    #         tabla.itemChanged.connect(self.confirmar_edicion_en_tabla)
    #
    #     except Exception as e:
    #         QMessageBox.critical(self.navegacion, "Error", f"No se pudo cargar la tabla: {e}")
    #
    # def confirmar_edicion_en_tabla(self, item):
    #     """Manejador que pide confirmación antes de guardar en la BD."""
    #     tabla = self.navegacion.tResultadoS
    #     columna = item.column()
    #     fila = item.row()
    #     nuevo_valor = item.text()
    #
    #     # Mapeo de columnas
    #     columnas_map = {
    #         1: "servicio",
    #         2: "descservicio",
    #         3: "costo_renta"
    #     }
    #     
    #     campo = columnas_map.get(columna)
    #     if not campo:
    #         return
    #
    #     # Obtener el ID de la fila actual
    #     id_busqueda = int(tabla.item(fila, 0).text())
    #
    #     # Preguntar al usuario
    #     # NOTA: Usamos 'main_window' si tienes centralizada la confirmación, o QMessageBox directo
    #     confirmar = QMessageBox.question(
    #         self.navegacion,
    #         "Confirmar Cambio",
    #         f"¿Deseas actualizar el campo '{campo}' a '{nuevo_valor}'?",
    #         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    #     )
    #
    #     if confirmar == QMessageBox.StandardButton.Yes:
    #         self.ejecutar_actualizacion(campo, id_busqueda, nuevo_valor)
    #     else:
    #         # Si dice que NO, refrescamos la tabla para devolver el valor original
    #         # (Evitamos que la tabla muestre un dato que no se guardó)
    #         self.listar_servicio_segun_tipo()
    #
    # def ejecutar_actualizacion(self, campo, id_busqueda, nuevo_valor):
    #     """Lógica final de guardado."""
    #     try:
    #         exito = self.servicio.actualizar_campos(campo, id_busqueda, nuevo_valor)
    #         if exito:
    #             # Opcional: un mensaje temporal en la barra de estado
    #             print(f"ID {id_busqueda} actualizado correctamente.")
    #         else:
    #             QMessageBox.warning(self.navegacion, "Error", "La base de datos no aceptó el cambio.")
    #             self.listar_servicio_segun_tipo()
    #     except Exception as e:
    #         QMessageBox.critical(self.navegacion, "Error Crítico", f"Fallo de conexión: {e}")
    #         self.listar_servicio_segun_tipo()

    def listar_servicio_segun_tipo(self):
        # NOTE: Asegúrate de que 'tResultadoS' sea un QTableWidget en el archivo .ui
        tabla = self.navegacion.tResultadoS
        
        try:
            tipo_buscado = self.navegacion.tipoBuscar.currentText()
    
            if not tipo_buscado or self.navegacion.tipoBuscar.currentIndex() == 0:
                # IMPORTANTE: Bloquear señales antes de limpiar
                tabla.blockSignals(True)
                tabla.setRowCount(0)
                tabla.blockSignals(False)
                TableManager.show_message(tabla, "Seleccione un tipo de servicio para buscar.")
                return
    
            resultado = self.servicio.listar_servicio_y_tipo(tipo_buscado)
    
            if not resultado:
                # IMPORTANTE: Bloquear señales antes de limpiar
                tabla.blockSignals(True)
                tabla.setRowCount(0)
                tabla.blockSignals(False)
                TableManager.show_message(tabla, f"No se encontraron servicios para el tipo: '{tipo_buscado}'")
                return
            
            # NUEVO: Guardar los datos originales y los IDs para referencia
            self.datos_tabla_actual = resultado
            self.id_servicios = [ts.get('id_servicio') for ts in resultado]
            
            headers = ['Servicio', 'Descripción', 'Costo Renta']
            data = [
                [
                    ts.get('servicio', 'N/D'), 
                    ts.get('descservicio', 'N/D'), 
                    TableManager.format_as_currency(ts.get('costo_renta', 'N/D'))
                ] 
                for ts in resultado
            ]
            resultado = self.servicio.listar_servicio_y_tipo(tipo_buscado)
    
            # DEBUG: Verificar qué campos llegan
            if resultado:
                print("=== DEBUG ===")
                print("Primer registro:", resultado[0])
                print("Campos disponibles:", list(resultado[0].keys()))
            
            # CORRECCIÓN: Usar numServicio como ID
            self.id_servicios = [ts.get('numServicio') for ts in resultado]
            
            # DEBUG: Verificar los IDs obtenidos
            print("IDs obtenidos (numServicio):", self.id_servicios)
                    # CRÍTICO: Desconectar completamente la señal durante la recarga
            try:
                # Desconectar la señal si ya está conectada
                tabla.itemChanged.disconnect(self.on_table_item_changed)
            except Exception:
                pass  # Si no estaba conectada, no hay problema
            
            # Configurar tabla
            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            
            # BLOQUEAR SEÑALES antes de llenar la tabla
            tabla.blockSignals(True)
            
            # Limpiar tabla existente
            tabla.setRowCount(0)
            
            # Configurar filas
            tabla.setRowCount(len(data))
            
            # Llenar datos
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    
                    # Configurar propiedades para todas las columnas
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    if col_idx == 2:  # Alinear a la derecha la columna de costo
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    
                    tabla.setItem(row_idx, col_idx, item)
            
            # Restaurar bloqueo de señales
            tabla.blockSignals(False)
            
            # RECONECTAR la señal DESPUÉS de llenar la tabla
            tabla.itemChanged.connect(self.on_table_item_changed)
            
            # Ajustar columnas al contenido
            tabla.resizeColumnsToContents()
            
            # Asegurar que la tabla esté configurada como editable
            tabla.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed)
    
        except Exception as e:
            # Asegurar que las señales estén restauradas incluso en caso de error
            tabla.blockSignals(False)
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error al intentar listar los servicios: {e}",
            )
        
        
    # NUEVO: Función para manejar cambios en la tabla
    def on_table_item_changed(self, item):
        """
        Maneja los cambios en las celdas de la tabla.
        Se activa cada vez que el usuario modifica una celda.
        """
        try:
            # Obtener información de la celda modificada
            fila = item.row()
            columna = item.column()
            nuevo_valor = item.text()
            
            # Validar que tenemos los datos necesarios
            if not hasattr(self, 'id_servicios') or fila >= len(self.id_servicios):
                QMessageBox.warning(
                    self.navegacion,
                    "Error de Datos",
                    "No se encontró la información del servicio. Recargue la tabla."
                )
                return
            
            # Obtener el ID del servicio
            id_servicio = self.id_servicios[fila]
            
            # Mapear columnas a campos de la base de datos
            mapeo_campos = {
                0: 'nombre',      # Columna "Servicio"
                1: 'descripcion',  # Columna "Descripción"
                2: 'costoRenta'    # Columna "Costo Renta"
            }
            
            campo = mapeo_campos.get(columna)
            if not campo:
                QMessageBox.warning(
                    self.navegacion,
                    "Campo Inválido",
                    f"No se puede actualizar la columna {columna}"
                )
                return
            
            # NUEVO: Para la columna de costo, formatear/quitar formato de moneda
            if columna == 2:  # Columna de costo
                try:
                    # Si tu formato de moneda incluye símbolos como $, removerlos
                    nuevo_valor = nuevo_valor.replace('$', '').replace(',', '').strip()
                    # Validar que sea un número
                    float(nuevo_valor)
                except ValueError:
                    QMessageBox.warning(
                        self.navegacion,
                        "Valor Inválido",
                        "El costo debe ser un valor numérico válido."
                    )
                    # Restaurar valor anterior
                    self.restaurar_valor_celda(fila, columna)
                    return
            
            # Confirmar la actualización
            respuesta = QMessageBox.question(
                self.navegacion,
                "Confirmar Cambio",
                f"¿Desea actualizar el campo '{campo}' del servicio ID {id_servicio} a '{nuevo_valor}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # <-- CAMBIADO
                QMessageBox.StandardButton.No  # <-- CAMBIADO
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:  # <-- CAMBIADO
                # Usar la función existente de actualización y capturar el resultado
                exito = self.actualizar_servicio(campo, id_servicio, nuevo_valor)
                
                # Si la actualización fue exitosa, proceder
                if exito:
                    # Actualizar los datos en memoria
                    if hasattr(self, 'datos_tabla_actual'):
                        self.datos_tabla_actual[fila][campo] = nuevo_valor
                        
                    # Si es costo, reformatear con formato de moneda
                    if columna == 2:
                        item.setText(TableManager.format_as_currency(nuevo_valor))
                        
                    QMessageBox.information(
                        self.navegacion,
                        "Cambio Guardado",
                        "El cambio ha sido guardado exitosamente."
                    )
                else:
                    # Si la actualización falló, restaurar la celda
                    self.restaurar_valor_celda(fila, columna)
            else:
                # Restaurar el valor original si el usuario cancela
                self.restaurar_valor_celda(fila, columna)
                
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error",
                f"Error al procesar el cambio: {e}"
            )
            # Restaurar valor en caso de error
            if 'fila' in locals() and 'columna' in locals():
                self.restaurar_valor_celda(fila, columna)
    
    # NUEVO: Función auxiliar para restaurar valores de celdas
    def restaurar_valor_celda(self, fila, columna):
        """
        Restaura el valor original de una celda.
        """
        tabla = self.navegacion.tResultadoS
        if hasattr(self, 'datos_tabla_actual') and fila < len(self.datos_tabla_actual):
            datos = self.datos_tabla_actual[fila]
            
            # Mapeo inverso para obtener el valor original
            mapeo_valores = {
                0: datos.get('servicio', ''),
                1: datos.get('descservicio', ''),
                2: TableManager.format_as_currency(datos.get('costo_renta', ''))
            }
            
            valor_original = mapeo_valores.get(columna, '')
            
            # Desconectar señal para evitar recursión
            tabla.blockSignals(True)
            tabla.item(fila, columna).setText(str(valor_original))
            tabla.blockSignals(False)
    
    # NUEVO: Método para guardar todos los cambios manualmente (opcional)
    def guardar_cambios_tabla(self):
        """
        Guarda todos los cambios realizados en la tabla.
        Útil si prefieres que el usuario guarde explícitamente.
        """
        tabla = self.navegacion.tResultadoS
        cambios = []
        
        for fila in range(tabla.rowCount()):
            if fila >= len(self.id_servicios):
                continue
                
            id_servicio = self.id_servicios[fila]
            
            for columna in range(tabla.columnCount()):
                item = tabla.item(fila, columna)
                if item and hasattr(item, 'isModified') and item.isModified():  # Solo si fue modificado
                    mapeo_campos = {0: 'servicio', 1: 'descservicio', 2: 'costo_renta'}
                    campo = mapeo_campos.get(columna)
                    
                    if campo:
                        nuevo_valor = item.text()
                        if columna == 2:  # Formatear costo
                            nuevo_valor = nuevo_valor.replace('$', '').replace(',', '').strip()
                        
                        cambios.append({
                            'id': id_servicio,
                            'campo': campo,
                            'valor': nuevo_valor
                        })
        
        if cambios:
            respuesta = QMessageBox.question(
                self.navegacion,
                "Guardar Cambios",
                f"¿Desea guardar {len(cambios)} cambio(s)?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No  # <-- CAMBIADO
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:  # <-- CAMBIADO
                for cambio in cambios:
                    self.actualizar_servicio(cambio['campo'], cambio['id'], cambio['valor'])
                
                QMessageBox.information(
                    self.navegacion,
                    "Cambios Guardados",
                    f"Se guardaron {len(cambios)} cambio(s) exitosamente."
                )
        else:
            QMessageBox.information(
                self.navegacion,
                "Sin Cambios",
                "No hay cambios pendientes por guardar."
                )
