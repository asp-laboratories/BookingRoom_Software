from PyQt6.QtWidgets import QMessageBox, QLabel, QPushButton, QListWidgetItem,  QTableWidgetItem, QTableWidget 
from PyQt6.QtCore import Qt
from gui.table_manager import TableManager


class EquipmentHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.equipamiento = self.main_window.equipamiento
        self.tipo_equipamiento = self.main_window.tipo_equipamiento

        # UI-related state for equipment
        self.cantidades = {}
        self.controles_equipos = {}
        self.datos_finales = {}

        if hasattr(self.navegacion, 'sEquipamiento'):
            self.cargar_tipos_equipamiento()
            self.navegacion.sEquipamiento.currentIndexChanged.connect(self.buscar_tipo_equipo)

    def registrar_equipamiento(self, nombre, descripcion, costo, stock, tipo):
        try:
            resultado = self.equipamiento.registrar_equipamento(
                nombre, descripcion, costo, stock, tipo
            )

            if not resultado:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Registro",
                    f"No se pudo registrar el equipo '{nombre}'. Verifique la conexión o si el equipo ya existe.",
                )
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Registro Exitoso",
                    f"El equipamiento '{nombre}' ha sido registrado correctamente.",
                )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos durante el registro: {e}",
            )

    def actualizar_equipamiento(self, campo: str, id_busqueda: int, nuevo_valor: str):
        try:
            resultado = self.equipamiento.actualizar_equipamento(
                campo, id_busqueda, nuevo_valor
            )
            if not resultado:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Actualización",
                    f"No se pudo actualizar el campo '{campo}' del equipo {id_busqueda}. Verifique los datos o si el ID existe.",
                )
            return resultado
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos: {e}",
            )
            return False





    def eliminar_equipamiento(self, id_equipamiento: int):
        try:
            resultado = self.equipamiento.eliminar_registro(id_equipamiento)
            if not resultado:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Eliminación",
                    "No se pudo eliminar el equipamiento. Verifique que el numero.",
                )
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Eliminación Exitosa",
                    f"El equipamiento {id_equipamiento} ha sido eliminado correctamente.",
                )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error grave de base de datos durante la eliminación: {e}",
            )

    def cargar_tipos_equipamiento(self):
        self.navegacion.sEquipamiento.clear()
        self.navegacion.sEquipamiento.addItem("Seleccione un tipo de servicio:", None)
        tpos_equipa = self.tipo_equipamiento.listar_tipos_equipamentos()
        for tipo in tpos_equipa:
            self.navegacion.sEquipamiento.addItem(
                tipo["descripcion"], tipo["codigoTiEquipa"]
            )

    def buscar_tipo_equipo(self):
        tabla = self.navegacion.tResultadoS_3
        
        try:
            tipo_equipamiento_buscado = self.navegacion.sEquipamiento.currentData()
            if not tipo_equipamiento_buscado:
                TableManager.show_message(tabla, "Por favor, seleccione un tipo de equipamiento válido.")
                return

            resultado = self.equipamiento.listar_equipamiento_tipo(tipo_equipamiento_buscado)

            if not resultado:
                TableManager.show_message(tabla, f"No se encontraron equipamientos para el tipo seleccionado.")
                return

            self.datos_tabla_actual_equipo = resultado
            self.id_equipos = [eq.get('numero') for eq in resultado]

            headers = ['Nombre', 'Descripción', 'Costo', 'Stock']
            data = [
                [
                    eq.get('equipamiento', 'N/A'),
                    eq.get('descripcion', 'N/A'),
                    TableManager.format_as_currency(eq.get('costo', 0)),
                    eq.get('stock', 0)
                ]
                for eq in resultado
            ]
            
            try:
                tabla.itemChanged.disconnect(self.on_equipo_table_item_changed)
            except Exception:
                pass

            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            
            tabla.blockSignals(True)
            tabla.setRowCount(0)
            tabla.setRowCount(len(data))
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    if col_idx == 2:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    tabla.setItem(row_idx, col_idx, item)
            
            tabla.blockSignals(False)
            tabla.itemChanged.connect(self.on_equipo_table_item_changed)
            tabla.resizeColumnsToContents()
            tabla.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed)

        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error inesperado",
                f"Ocurrió un error al buscar equipamientos por tipo: {e}",
            )

    def actualizar_estado_equipa(
        self, num_equipo: int, estado_nuevo: str, estado_origen: str, cantidad: int
    ):
        try:
            resultado = self.equipamiento.actualizar_estado_equipamiento(
                num_equipo, estado_nuevo, estado_origen, cantidad
            )
            if resultado:
                QMessageBox.information(
                    self.navegacion,
                    "Actualización Exitosa",
                    f"Se han movido {cantidad} unidades del equipo {num_equipo} al estado '{estado_nuevo}'.",
                )
                # Refresh the table to show the change
                self.buscar_estado_equipamiento()
            else:
                QMessageBox.critical(
                    self.navegacion,
                    "Error de Actualización",
                    f"No se pudo actualizar el estado del equipo {num_equipo}. Verifique la existencia del numero, la cantidad disponible en el estado origen o si los estados son válidos.",
                )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos: {e}",
            )

    def cargar_lista_equipamiento(self):
        self.navegacion.listaEquipamiento.clear()
        for equipa in self.equipamiento.listar_equipamentos():
            texto = f"{equipa['nombre']} - ${equipa['costoRenta']:.2f}"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, equipa)
            self.navegacion.listaEquipamiento.addItem(item)

    def mostrar_controles_cantidad(self):
        self.limpiar_todos_controles()
        equipamientos_seleccionados = self.navegacion.listaEquipamiento.selectedItems()
        for equipamiento_item in equipamientos_seleccionados:
            equipa_data = equipamiento_item.data(Qt.ItemDataRole.UserRole)
            if equipa_data is None:
                continue
            nombre = equipa_data["nombre"]
            costoRenta = equipa_data["costoRenta"]
            numEquipa = equipa_data["numEquipa"]
            if nombre not in self.cantidades:
                self.cantidades[nombre] = 1
            self.crear_control_cantidad(nombre, costoRenta, numEquipa)

    def crear_control_cantidad(self, nombre, costoRenta, numEquipa):
        layEqui = self.navegacion.equipamientoW.layout()
        lbl_producto = QLabel(f"{nombre} (${costoRenta} c/u)")
        lbl_producto.setMinimumWidth(150)
        lbl_producto.setStyleSheet("color: #000000;")
        btn_menos = QPushButton("-")
        btn_menos.setFixedSize(30, 30)
        btn_menos.clicked.connect(lambda: self.cambiar_cantidad(nombre, -1, numEquipa))
        btn_menos.setStyleSheet("color: #ffffff; background-color: #000000;")
        lbl_cantidad = QLabel(str(self.cantidades[nombre]))
        lbl_cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_cantidad.setMinimumWidth(30)
        lbl_cantidad.setStyleSheet("font-weight: bold; color: #000000;")
        btn_mas = QPushButton("+")
        btn_mas.setFixedSize(30, 30)
        btn_mas.clicked.connect(lambda: self.cambiar_cantidad(nombre, 1, numEquipa))
        btn_mas.setStyleSheet("color: #ffffff; background-color: #000000;")
        subtotal = self.cantidades[nombre] * costoRenta
        lbl_subtotal = QLabel(f"${subtotal:.2f}")
        lbl_subtotal.setMinimumWidth(60)
        lbl_subtotal.setStyleSheet("font-weight: bold; color: blue;")
        if nombre not in self.controles_equipos:
            self.controles_equipos[nombre] = {
                "label_cantidad": lbl_cantidad,
                "label_subtotal": lbl_subtotal,
                "costo": costoRenta,
            }
        sub = QLabel("Subtotal: ")
        sub.setStyleSheet("color: #000000;")
        layEqui.addWidget(lbl_producto)
        layEqui.addWidget(btn_menos)
        layEqui.addWidget(lbl_cantidad)
        layEqui.addWidget(btn_mas)
        layEqui.addWidget(sub)
        layEqui.addWidget(lbl_subtotal)

    def cambiar_cantidad(self, nombre, cambio, numEquipa):
        nueva_cantidad = self.cantidades.get(nombre, 0) + cambio
        if nueva_cantidad < 0:
            return
        self.cantidades[nombre] = nueva_cantidad
        if nombre in self.controles_equipos:
            controles = self.controles_equipos[nombre]
            controles["label_cantidad"].setText(str(nueva_cantidad))
            self.datos_finales[numEquipa] = nueva_cantidad
            nuevo_subtotal = nueva_cantidad * controles["costo"]
            controles["label_subtotal"].setText(f"${nuevo_subtotal:.2f}")
        self.main_window.reservacion_handler.calcular_total_general()

    def limpiar_todos_controles(self):
        layEqui = self.navegacion.equipamientoW.layout()
        while layEqui.count():
            child = layEqui.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.controles_equipos.clear()

    def cargar_tipos_equipamiento_registro(self):
        """
        Carga los tipos de equipamiento en el ComboBox de la pantalla de registro.
        """
        # NOTE: Asegúrate de que 'eTipoEquipamiento' sea un QComboBox en tu archivo .ui
        combo = self.navegacion.eTipoEquipamiento
        combo.clear()
        combo.addItem("Seleccione un tipo...", None)
        try:
            tipos = self.tipo_equipamiento.listar_tipos_equipamentos()
            if tipos:
                for tipo in tipos:
                    combo.addItem(tipo["descripcion"], tipo["codigoTiEquipa"])
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Carga",
                f"No se pudieron cargar los tipos de equipamiento: {e}",
            )

    def cargar_estados_equipamiento(self):
        """
        Carga todos los estados de equipamiento disponibles en el QComboBox.
        """
        # NOTE: Asegúrate de que 'almBuscadorE' sea un QComboBox en tu archivo .ui
        combo = self.navegacion.almBuscadorE
        combo.clear()
        combo.addItem("Seleccione un estado...", None)

        try:
            estados = self.equipamiento.listar_estados()
            if estados:
                for estado in estados:
                    combo.addItem(estado["descripcion"], estado["codigoEquipa"])
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Carga",
                f"No se pudieron cargar los estados de equipamiento: {e}",
            )

    def intentar_registrar_equipamiento(self):
        try:
            costo_renta = float(self.navegacion.eCostoRenta.text())
            stock = int(self.navegacion.eStock.text())
            nombre_equipo = self.navegacion.eNombreEqui.text()
            descripcion = self.navegacion.eDescripcion.text()
            
            # Obtener el código del tipo de equipamiento desde el ComboBox
            codigo_tipo = self.navegacion.eTipoEquipamiento.currentData()

            if not codigo_tipo:
                QMessageBox.warning(self.navegacion, "Dato Requerido", "Debe seleccionar un tipo de equipamiento.")
                return

            if self.main_window.mostrar_confirmacion(
                "Confirmar Registro de Equipamiento",
                f"¿Deseas registrar el equipo '{nombre_equipo}' (Costo: ${costo_renta}, Stock: {stock})?",
            ):
                # Se pasa el código directamente al servicio refactorizado
                self.registrar_equipamiento(
                    nombre_equipo, descripcion, costo_renta, stock, codigo_tipo
                )
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Registro Cancelado",
                    "La operación de registro ha sido cancelada.",
                )
        except ValueError:
            QMessageBox.warning(
                self.navegacion,
                "Datos Inválidos",
                "Asegúrate de que 'Costo de Renta' y 'Stock' contengan valores numéricos válidos.",
            )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Pre-Validación",
                f"Ocurrió un error al procesar los datos: {e}",
            )

    def intentar_actualizar_equipamiento(self):
        try:
            campo = self.navegacion.sCampo_3.text()
            id_busqueda = int(self.navegacion.slIngresarBusqueda_5.text())
            nuevo_valor = self.navegacion.sNuevoValor_3.text()
            if self.main_window.mostrar_confirmacion(
                "Confirmar Actualización de Equipamiento",
                f"¿Deseas cambiar el campo '{campo}' del equipo con ID {id_busqueda} al valor '{nuevo_valor}'?",
            ):
                self.actualizar_equipamiento(campo, id_busqueda, nuevo_valor)
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Actualización Cancelada",
                    "La operación de actualización del equipamiento ha sido cancelada.",
                )
        except ValueError:
            QMessageBox.warning(
                self.navegacion,
                "Datos Inválidos",
                "Asegúrate de que la búsqueda contenga un valor numérico entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Pre-Validación",
                f"Ocurrió un error al procesar los datos: {e}",
            )

    def intentar_eliminar_equipamiento(self):
        try:
            id_equipo_a_eliminar = int(self.navegacion.seEliminarInput_3.text())
            if self.main_window.mostrar_confirmacion(
                "Confirmar Eliminación de Equipamiento",
                f"⚠️ **Advertencia:** ¿Estás seguro de ELIMINAR el equipo: {id_equipo_a_eliminar}? Esta acción es irreversible.",
            ):
                self.eliminar_equipamiento(id_equipo_a_eliminar)
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Operación Cancelada",
                    "La eliminación del equipamiento ha sido cancelada por el usuario.",
                )
        except ValueError:
            QMessageBox.warning(
                self.navegacion,
                "Datos Inválidos",
                "El equipamiento a eliminar debe ser un número entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Pre-Validación",
                f"Ocurrió un error al intentar leer el ID: {e}",
            )

    def intentar_actualizar_estado_desde_tabla(self):
        """
        Intenta actualizar el estado de un equipo seleccionado desde la tabla.
        Lee la fila seleccionada para obtener el estado de origen y el ID.
        Toma el nuevo estado y la cantidad de los campos de entrada de la UI.
        """
        # NOTE: Asegúrate de que los widgets 'almNuevoEstado', 'almCantidadMover' 
        # y 'tablaEstadosEqui' existan en tu archivo .ui
        tabla = self.navegacion.tablaEstadosEqui
        selected_items = tabla.selectedItems()

        if not selected_items:
            QMessageBox.warning(self.navegacion, "Selección Requerida", "Por favor, selecciona un equipo de la tabla para actualizar.")
            return

        try:
            selected_row = selected_items[0].row()
            num_equipo = int(tabla.item(selected_row, 0).text())
            estado_origen = tabla.item(selected_row, 2).text()
            cantidad_disponible = int(tabla.item(selected_row, 3).text())

            estado_nuevo = self.navegacion.almNuevoEstado.text().strip()
            cantidad_a_mover_str = self.navegacion.almCantidadMover.text().strip()

            if not estado_nuevo or not cantidad_a_mover_str:
                raise ValueError("Campos de entrada vacíos")

            cantidad_a_mover = int(cantidad_a_mover_str)

            if cantidad_a_mover <= 0:
                QMessageBox.warning(self.navegacion, "Cantidad Inválida", "La cantidad a mover debe ser mayor que cero.")
                return
            
            if cantidad_a_mover > cantidad_disponible:
                QMessageBox.warning(self.navegacion, "Cantidad Excedida", f"No puedes mover más de {cantidad_disponible} unidades.")
                return

            if self.main_window.mostrar_confirmacion(
                "Confirmar Actualización de Estado",
                f"¿Mover {cantidad_a_mover} unidad(es) del equipo #{num_equipo}\n"
                f"Desde '{estado_origen}' hacia '{estado_nuevo}'?",
            ):
                self.actualizar_estado_equipa(
                    num_equipo, estado_nuevo, estado_origen, cantidad_a_mover
                )
            else:
                QMessageBox.information(
                    self.navegacion,
                    "Actualización Cancelada",
                    "La operación ha sido cancelada.",
                )

        except ValueError:
            QMessageBox.warning(
                self.navegacion,
                "Datos Inválidos",
                "Asegúrate de que la 'Cantidad a Mover' sea un número válido y que el 'Nuevo Estado' no esté vacío.",
            )
        except Exception as e:
            QMessageBox.critical(
                self.navegacion, "Error Inesperado", f"Ocurrió un error al procesar la actualización: {e}"
            )

    def buscar_estado_equipamiento(self):
        # NOTE: Asegúrate de que 'tablaEstadosEqui' sea un QTableWidget y 'almBuscadorE' un QComboBox en el archivo .ui
        tabla = self.navegacion.tablaEstadosEqui
        combo = self.navegacion.almBuscadorE
        
        try:
            # No realizar la búsqueda si el placeholder está seleccionado
            if combo.currentIndex() == 0:
                TableManager.show_message(tabla, "Seleccione un estado para buscar")
                return
            
            estado_buscado = combo.currentText()
            resultado = self.equipamiento.obtener_equipa_estado(estado_buscado)

            if not resultado:
                TableManager.show_message(tabla, f"No se encontró equipamiento en estado '{estado_buscado}'")
                return
            
            headers = ['Número', 'Nombre', 'Estado Actual', 'Cantidad']
            data = [[
                equi.get('Numero', 'N/A'),
                equi.get('Nombre', 'N/A'),
                equi.get('Estado', 'N/A'),
                equi.get('Cantidad', 'N/A')
            ] for equi in resultado]
            
            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)

        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error Inesperado",
                                f"Ocurrió un error al buscar el equipamiento: {e}",
                            )
                
    def on_equipo_table_item_changed(self, item):
        """
        Maneja los cambios en las celdas de la tabla de equipamiento.
        """
        try:
            fila = item.row()
            columna = item.column()
            nuevo_valor = item.text()
            
            if not hasattr(self, 'id_equipos') or fila >= len(self.id_equipos):
                QMessageBox.warning(self.navegacion, "Error de Datos", "No se encontró la información del equipo. Recargue la tabla.")
                return
            
            id_equipo = self.id_equipos[fila]
            
            mapeo_campos = {
                0: 'nombre',
                1: 'descripcion',
                2: 'costoRenta',
                3: 'stock'
            }
            
            campo = mapeo_campos.get(columna)
            if not campo:
                return

            if columna in [2, 3]:  # Validar costo y stock como números
                try:
                    float(nuevo_valor)
                except ValueError:
                    QMessageBox.warning(self.navegacion, "Valor Inválido", f"El campo '{campo}' debe ser un valor numérico.")
                    self.restaurar_valor_celda_equipo(fila, columna)
                    return

            respuesta = QMessageBox.question(
                self.navegacion,
                "Confirmar Cambio",
                f"¿Desea actualizar el campo '{campo}' del equipo ID {id_equipo} a '{nuevo_valor}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:
                exito = self.actualizar_equipamiento(campo, id_equipo, nuevo_valor)
                
                if exito:
                    if hasattr(self, 'datos_tabla_actual_equipo'):
                        self.datos_tabla_actual_equipo[fila][campo] = nuevo_valor
                    
                    if columna == 2: # Formato de moneda para costo
                        item.setText(TableManager.format_as_currency(nuevo_valor))

                    QMessageBox.information(self.navegacion, "Cambio Guardado", "El cambio ha sido guardado exitosamente.")
                else:
                    self.restaurar_valor_celda_equipo(fila, columna)
            else:
                self.restaurar_valor_celda_equipo(fila, columna)
                
        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error", f"Error al procesar el cambio: {e}")
            if 'fila' in locals() and 'columna' in locals():
                self.restaurar_valor_celda_equipo(fila, columna)

    def restaurar_valor_celda_equipo(self, fila, columna):
        """
        Restaura el valor original de una celda en la tabla de equipamiento.
        """
        tabla = self.navegacion.tResultadoS_3
        if hasattr(self, 'datos_tabla_actual_equipo') and fila < len(self.datos_tabla_actual_equipo):
            datos = self.datos_tabla_actual_equipo[fila]
            
            mapeo_valores = {
                0: datos.get('nombre', ''),
                1: datos.get('descripcion', ''),
                2: TableManager.format_as_currency(datos.get('costoRenta', '')),
                3: datos.get('stock', '')
            }
            
            valor_original = mapeo_valores.get(columna, '')
            
            tabla.blockSignals(True)
            tabla.item(fila, columna).setText(str(valor_original))
            tabla.blockSignals(False)

