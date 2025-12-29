from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QSize, Qt


class WorkerHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.trabajador = self.main_window.trabajador
        self.rol_service = self.main_window.TrabajadorRol
        self.telefono_service = self.main_window.telefono
        self.reservacion_service = self.main_window.reservacion

        # Conectar la señal del buscador
        if hasattr(self.navegacion, 'atBuscador'):
            # self.navegacion.atBotonBuscador.clicked.connect(self.buscar_trabajadores_y_mostrar) # Reemplaza 'atBotonBuscador' con el nombre de tu botón
            self.navegacion.atBuscador.returnPressed.connect(self.buscar_trabajadores_y_mostrar)

    # def buscar(self):
    #     rfc = self.navegacion.atBuscador.text()
    #     resultado = self.trabajador.buscar_trabajador(rfc)
    #     resul_telefono = self.telefono_service.listar_telefonos_info(rfc)
    #
    #     if not resultado:
    #         self.navegacion.atOutput.setText("No se encontraron resultados")
    #         return
    #
    #     mensaje = "INFORMACION DEL TRABAJADOR\n"
    #     mensaje += f"\nNombre: {resultado['nombre']} {resultado['priApe']} {resultado['segApe']}\n"
    #     mensaje += f"\nRFC: {resultado['RFC']}\n"
    #     mensaje += f"\nNumero de trabajador: {resultado['numTraba']}\n"
    #     mensaje += f"\nRol: {resultado['rol']}\n"
    #     mensaje += f"\nCorreo: {resultado['email']}\n"
    #     mensaje += "\nTelefonos:\n"
    #
    #     contador = 0
    #     for cel in resul_telefono:
    #         contador += 1
    #         if not cel["telefono"] == "":
    #             mensaje += f"{contador}: {cel['telefono']}\n"
    #
    #     self.navegacion.atOutput.setText(mensaje)
    def buscar_trabajadores_y_mostrar(self):
        
        tabla = self.navegacion.atResultadoText
        try:
            termino_busqueda = self.navegacion.atBuscador.text()
            resultado = self.trabajador.buscar_al_trabajador(termino_busqueda)

            if not resultado:
                QMessageBox.information(None, "Sin Resultados", "No se encontraron trabajadores con ese término de búsqueda.")
                tabla.setRowCount(0)
                return

            self.datos_tabla_trabajador = resultado
            self.rfc_trabajadores = [t.get('RFC') for t in resultado]

            headers = ['RFC', 'Num Trab', 'Nombre', '1er Apellido', '2do Apellido', 'Email', 'Rol']
            
            try:
                tabla.itemChanged.disconnect(self.on_trabajador_table_item_changed)
            except TypeError:
                pass

            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            
            tabla.blockSignals(True)
            tabla.setRowCount(len(resultado))

            for row_idx, traba in enumerate(resultado):
                # Columnas no editables
                rfc_item = QTableWidgetItem(traba.get('RFC', ''))
                rfc_item.setFlags(rfc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                tabla.setItem(row_idx, 0, rfc_item)

                num_item = QTableWidgetItem(str(traba.get('numTrabajador', '')))
                num_item.setFlags(num_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                tabla.setItem(row_idx, 1, num_item)
                
                rol_item = QTableWidgetItem(traba.get('rol', ''))
                rol_item.setFlags(rol_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                tabla.setItem(row_idx, 6, rol_item)

                # Columnas editables
                editable_data = {
                    2: traba.get('nombre', 'N/A'),
                    3: traba.get('priApellido', 'N/A'),
                    4: traba.get('segApellido', 'N/A'),
                    5: traba.get('email', 'N/A'),
                }

                for col_idx, cell_data in editable_data.items():
                    item = QTableWidgetItem(cell_data)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row_idx, col_idx, item)

            tabla.blockSignals(False)
            tabla.itemChanged.connect(self.on_trabajador_table_item_changed)
            tabla.resizeColumnsToContents()
            tabla.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed)

        except AttributeError:
             QMessageBox.critical(None, "Error de UI", "El elemento 'atResultadoText' no es una tabla (QTableWidget).\n\nPor favor, en Qt Designer, cambie el tipo de este widget.")
        except Exception as e:
            QMessageBox.critical(None, "Error Inesperado", f"Ocurrió un error al buscar trabajadores: {e}")


    def buscar_sus_reservaciones(self):
        rfc = self.navegacion.atRFC_2.text()
        resultado = self.reservacion_service.reservaciones_trabajador(rfc)

        if not resultado:
            self.navegacion.atOutput_2.setText("No se encontraron resultados")
            return

        mensaje = ""
        for reser in resultado:
            mensaje += f"Numero de reservacion: {reser['numReser']}\n"
            mensaje += f"Fecha de la reservacion: {reser['fechaReser']}\n"
            mensaje += f"Fecha del evento: {reser['fecha']}\n"
            mensaje += "--------------------------------------------------------\n"

        self.navegacion.atOutput_2.setText(mensaje)

    def establecer_rol(self):
        rol = self.navegacion.atRol.text()
        rfc = self.navegacion.atRFC_3.text()
        resultado = self.trabajador.establecer_rol(rol, rfc)

        if not resultado:
            self.navegacion.atOutput_3.setText("No se encontraron resultados")
            return

        self.navegacion.atOutput_3.setText("Rol establecido con éxito")

    def intentar_establecer_rol(self):
        if self.main_window.mostrar_confirmacion(
            "Confirmar rol", "¿Desea confirmar rol?"
        ):
            self.establecer_rol()
        else:
            self.navegacion.atOutput_3.setText("Rol no establecido")

    def llenar_combox_roles(self):
        self.navegacion.rolBuscadorTrabajadores.clear()
        self.navegacion.rolBuscadorTrabajadores.addItem("Selecciona un rol", None)
        roles = self.rol_service.listar_rol()
        for rol in roles:
            self.navegacion.rolBuscadorTrabajadores.addItem(
                rol["descripcion"], rol["descripcion"]
            )

    def llenar_lista_trabajadores(self):
        self.navegacion.rolTrabajadores.clear()
        self.navegacion.rolDetalleTrabajador.clear()
        rol_obtenido = self.navegacion.rolBuscadorTrabajadores.currentText()
        if not rol_obtenido:
            QMessageBox.warning(
                self.navegacion,
                "Rol no seleccionado",
                "Favor de seleccionar un rol para buscar",
            )
            return
        trabajadores = self.rol_service.obtener_trabajadores_rol(rol_obtenido)
        for traba in trabajadores:
            item = QListWidgetItem(self.navegacion.rolTrabajadores)
            item.setSizeHint(QSize(0, 60))
            item.setData(Qt.ItemDataRole.UserRole, traba)
            tarjeta = self.tarjeta_trabajador(traba)
            self.navegacion.rolTrabajadores.setItemWidget(item, tarjeta)

    def detalles_trabajador(self, item):
        self.navegacion.rolDetalleTrabajador.clear()
        traba = item.data(Qt.ItemDataRole.UserRole)
        infoTrabajador = f"\n---{traba['nombre']}---\n"
        infoTrabajador += f"Numero de trabajador: {traba['numTraba']}\n"
        infoTrabajador += f"RFC: {traba['RFC']}\n"
        infoTrabajador += "\n---CONTACTO---\n"
        infoTrabajador += f"Correo Electronico: {traba['email']}\n"
        infoTrabajador += "--Telefonos:\n"
        contador = 0
        for telef in traba["telefonos"]:
            contador += 1
            infoTrabajador += f"{contador}. {telef}\n"
        self.navegacion.rolDetalleTrabajador.setText(infoTrabajador)

    def tarjeta_trabajador(self, trabajador):
        widget = QWidget()
        layoutTar = QVBoxLayout()
        widget.setLayout(layoutTar)

        widget.setStyleSheet("""
        QWidget {
            background-color: transparent;
        }
        QLabel {
            background-color: transparent;
        }
        """)

        label_nombre = QLabel(trabajador["nombre"])
        label_nombre.setStyleSheet(
            """
                color: rgb(0, 0, 0);
                border-radius: 5px;
                border-bottom: 3px solid rgba(155, 88, 43, 1.0);
                border-right: 3px solid  rgba(155, 88, 43, 1.0);
                """,
        )

        label_id = QLabel(f"ID: {trabajador['numTraba']}")
        label_id.setStyleSheet(
            """
                color: rgb(0, 0, 0);
                border-radius: 5px;
                border-bottom: 3px solid rgba(155, 88, 43, 1.0);
                border-right: 3px solid  rgba(155, 88, 43, 1.0);
                """,
        )

        layoutTar.addWidget(label_nombre)
        layoutTar.addWidget(label_id)

        return widget

    def on_trabajador_table_item_changed(self, item):
        """
        Maneja los cambios en las celdas de la tabla de trabajadores.
        """
        try:
            fila = item.row()
            columna = item.column()
            nuevo_valor = item.text()

            if not hasattr(self, 'rfc_trabajadores') or fila >= len(self.rfc_trabajadores):
                return

            rfc = self.rfc_trabajadores[fila]

            mapeo_campos = {
                2: 'nombre', 3: 'priApellido', 4: 'segApellido', 5: 'email'
            }
            
            campo_bd = mapeo_campos.get(columna)
            if not campo_bd:
                return # Columna no editable

            # Validacion simple de email
            if campo_bd == 'email' and '@' not in nuevo_valor:
                QMessageBox.warning(self.navegacion, "Valor Inválido", "Por favor, ingrese un correo electrónico válido.")
                self.restaurar_valor_celda_trabajador(fila, columna)
                return

            respuesta = QMessageBox.question(
                self.navegacion, "Confirmar Cambio",
                f"¿Desea actualizar el campo '{campo_bd}' del trabajador con RFC {rfc} a '{nuevo_valor}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:
                exito = self.trabajador.actualizar_trabajador(campo_bd, rfc, nuevo_valor)
                
                if exito:
                    self.datos_tabla_trabajador[fila][campo_bd] = nuevo_valor
                    QMessageBox.information(self.navegacion, "Cambio Guardado", "El cambio ha sido guardado exitosamente.")
                else:
                    QMessageBox.critical(self.navegacion, "Error de Actualización", f"No se pudo actualizar el campo '{campo_bd}'.")
                    self.restaurar_valor_celda_trabajador(fila, columna)
            else:
                self.restaurar_valor_celda_trabajador(fila, columna)
                
        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error", f"Error al procesar el cambio: {e}")
            if 'fila' in locals() and 'columna' in locals():
                self.restaurar_valor_celda_trabajador(fila, columna)

    def restaurar_valor_celda_trabajador(self, fila, columna):
        """
        Restaura el valor original de una celda en la tabla de trabajadores.
        """
        tabla = self.navegacion.atResultadoText
        if hasattr(self, 'datos_tabla_trabajador') and fila < len(self.datos_tabla_trabajador):
            datos_originales = self.datos_tabla_trabajador[fila]
            
            mapeo_campos = {
                2: 'nombre', 3: 'priApellido', 4: 'segApellido', 5: 'email'
            }
            campo_bd = mapeo_campos.get(columna)

            if not campo_bd: return

            valor_original = datos_originales.get(campo_bd, '')
            
            tabla.blockSignals(True)
            tabla.item(fila, columna).setText(str(valor_original))
            tabla.blockSignals(False)
