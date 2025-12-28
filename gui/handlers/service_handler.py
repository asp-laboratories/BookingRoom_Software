from PyQt6.QtWidgets import QMessageBox, QPushButton, QInputDialog, QWidget, QHBoxLayout, QTableWidgetItem
from functools import partial
from utils.Formato import permitir_ingreso
from gui.table_manager import TableManager

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

        if hasattr(self.navegacion, 'experimentarBoton'):
            self.setup_experimentar_tab()

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

    def setup_experimentar_tab(self):
        # Cargar tipos de servicio en el ComboBox
        self.cargar_tipos_servicios_experimentar()
        # Conectar el ComboBox a la función de listar
        self.navegacion.experimentarCombo.currentIndexChanged.connect(self.listar_servicios_para_experimentar)

    def cargar_tipos_servicios_experimentar(self):
        combo = self.navegacion.experimentarCombo
        combo.clear()
        combo.addItem("Seleccione un tipo de servicio", None)
        tipos = self.tipo_servi.listar_tipos_servicios()
        for tipo in tipos:
            combo.addItem(tipo['descripcion'], tipo['codigoTiSer'])

    def listar_servicios_para_experimentar(self):
        tabla = self.navegacion.experimentarTabla
        tipo_servicio_nombre = self.navegacion.experimentarCombo.currentText()

        if self.navegacion.experimentarCombo.currentIndex() == 0:
            TableManager.show_message(tabla, "Por favor, seleccione un tipo de servicio.")
            return

        try:
            resultado = self.servicio.servicios_tipo(tipo_servicio_nombre)
            if not resultado:
                TableManager.show_message(tabla, f"No se encontraron servicios del tipo '{tipo_servicio_nombre}'.")
                tabla.setRowCount(0) # Limpiar la tabla si no hay resultados
                return

            headers = ['ID', 'Nombre', 'Costo', 'Tipo Servicio', 'Acciones']
            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            tabla.setRowCount(len(resultado))

            for row, st in enumerate(resultado):
                service_id = st['numServicio']
                
                # Llenar la tabla con datos
                tabla.setItem(row, 0, QTableWidgetItem(str(st['numServicio'])))
                tabla.setItem(row, 1, QTableWidgetItem(st['nombre']))
                tabla.setItem(row, 2, QTableWidgetItem(TableManager.format_as_currency(st['costoRenta'])))
                tabla.setItem(row, 3, QTableWidgetItem(st['tipo_servicio']))

                # Crear y añadir botones de acción
                action_buttons_widget = self._crear_botones_accion(service_id)
                tabla.setCellWidget(row, len(headers) - 1, action_buttons_widget)

        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error", f"Ocurrió un error al listar los servicios: {e}")

    def _crear_botones_accion(self, service_id):
        # Contenedor para los botones
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Botón de Actualizar
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(partial(self._actualizar_servicio_desde_tabla, service_id))
        layout.addWidget(btn_actualizar)

        # Botón de Eliminar
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(partial(self._eliminar_servicio_desde_tabla, service_id))
        layout.addWidget(btn_eliminar)

        return widget

    def _actualizar_servicio_desde_tabla(self, service_id):
        # Aquí iría la lógica para la actualización.
        # Por simplicidad, usamos QInputDialog para obtener el nuevo valor de un campo.
        campo, ok = QInputDialog.getText(self.navegacion, 'Actualizar Servicio', 'Campo a actualizar (nombre, descripcion, costoRenta):')
        if ok and campo and campo in ['nombre', 'descripcion', 'costoRenta']:
            nuevo_valor, ok = QInputDialog.getText(self.navegacion, 'Actualizar Servicio', f'Nuevo valor para {campo}:')
            if ok and nuevo_valor:
                self.actualizar_servicio(campo, service_id, nuevo_valor)
                # Refrescar la tabla
                self.listar_servicios_para_experimentar()
        elif ok:
            QMessageBox.warning(self.navegacion, "Campo no válido", "El campo a actualizar no es válido.")

    def _eliminar_servicio_desde_tabla(self, service_id):
        confirmacion = self.main_window.mostrar_confirmacion(
            "Confirmar Eliminación",
            f"⚠️ ¿Estás seguro de ELIMINAR el servicio con ID: {service_id}? Esta acción es irreversible."
        )
        if confirmacion:
            self.eliminar_servicio(service_id)
            # Refrescar la tabla
            self.listar_servicios_para_experimentar()


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
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Actualización Exitosa",
                    f"El servicio {id_busqueda} ha sido actualizado correctamente.",
                )

        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos: {e}",
            )

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

    def listar_servicios_del_mismo_tipo(self):
        # NOTE: Asegúrate de que 'sResultadoListar_2' sea un QTableWidget en el archivo .ui
        tabla = self.navegacion.sResultadoListar_2
        try:
            tposervicio = self.navegacion.slIngresarBusqueda_2.text()
            if not permitir_ingreso(tposervicio, "onlytext"):
                QMessageBox.warning(
                    self.navegacion,
                    "Tipo de dato no valido",
                    "Favor de ingresar el nombre del tipo de servicio",
                )
                return

            resultado = self.servicio.servicios_tipo(tposervicio)

            if not resultado:
                TableManager.show_message(tabla, f"No se encontraron servicios del tipo '{tposervicio}'")
                return
            
            headers = ['ID', 'Nombre', 'Costo', 'Tipo Servicio']
            data = [[st['numServicio'], st['nombre'], TableManager.format_as_currency(st['costoRenta']), st['tipo_servicio']] for st in resultado]

            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)

        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error", f"Ocurrió un error al buscar servicios por tipo: {e}")


    def eliminar_servicio(self, id_servicio: int):
        try:
            resultado = self.servicio.eliminar_fila(id_servicio)

            if not resultado:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Eliminación",
                    f"No se pudo eliminar el servicio {id_servicio}. Verifique que el número exista o haya un error en la base de datos.",
                )
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Eliminación Exitosa",
                    f"El servicio {id_servicio} ha sido eliminado correctamente.",
                )

        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error grave de base de datos durante la eliminación: {e}",
            )

    def listar_servicio_segun_tipo(self):
        # NOTE: Asegúrate de que 'tResultadoS' sea un QTableWidget en el archivo .ui
        tabla = self.navegacion.tResultadoS
        try:
            tipo_buscado = self.navegacion.tipoBuscar.currentText()

            if not tipo_buscado or self.navegacion.tipoBuscar.currentIndex() == 0:
                tabla.setRowCount(0)
                TableManager.show_message(tabla, "Seleccione un tipo de servicio para buscar.")
                return

            resultado = self.servicio.listar_servicio_y_tipo(tipo_buscado)

            if not resultado:
                TableManager.show_message(tabla, f"No se encontraron servicios para el tipo: '{tipo_buscado}'")
                return
            
            headers = ['Servicio', 'Descripción', 'Costo Renta']
            data = [[ts.get('servicio', 'N/D'), ts.get('descservicio', 'N/D'), TableManager.format_as_currency(ts.get('costo_renta', 'N/D'))] for ts in resultado]
            
            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)

        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error al intentar listar los servicios: {e}",
            )

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
