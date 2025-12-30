from PyQt6.QtWidgets import QMessageBox, QLabel, QLineEdit, QTableWidget 
from models.MobCarac import MobCarac
from PyQt6.QtCore import Qt
from gui.table_manager import TableManager

class MobiliarioHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.mobiliario = self.main_window.mobiliario
        self.tipo_mobiliario = self.main_window.tipo_mobiliario
        self.inputs = []
        self.inputs_tipo = []

        if hasattr(self.navegacion, 'almBuscadorM'):
            self.cargar_estados_mobiliario()
            self.navegacion.almBuscadorM.currentIndexChanged.connect(self.buscar_estado_mobiliario)
        
        if hasattr(self.navegacion, 'almConfirmarMobi_3'):
            self.navegacion.almConfirmarMobi_3.clicked.connect(self.intentar_actualizar_estado_manual_mob)


    def registrar_mobiliario_ejecutar(
        self, nombre, costoRenta, stock, tipo, caracteristicas
    ):
        try:
            resultado = self.mobiliario.registrar_mobiliario(
                nombre, costoRenta, stock, tipo, caracteristicas
            )

            if not resultado:
                QMessageBox.critical(
                    None,
                    "Error de Registro",
                    f"No se pudo registrar el mobiliario '{nombre}'. Verifique si ya existe o hay un problema en la base de datos.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Registro Exitoso",
                    f"El mobiliario '{nombre}' ha sido registrado correctamente.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error de Ejecución",
                f"Ocurrió un error de base de datos durante el registro: {e}",
            )

    def limpiar_caracteristicas(self):
        lay = self.navegacion.mobcont2.layout()
        while lay.count():
            child = lay.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.inputs.clear()
        self.inputs_tipo.clear()

    def generar_caracteristicas(self):
        self.limpiar_caracteristicas()
        lay = self.navegacion.mobcont2.layout()
        cantidad = self.navegacion.seleccionCaracteristicas.value()
        for i in range(cantidad):
            label1 = QLabel(f"Característica {i + 1}")
            label1.setStyleSheet("color: #000000;")
            lay.addWidget(label1)
            input_caracteristica = QLineEdit()
            input_caracteristica.setPlaceholderText(
                f"Ingrese el nombre de la caracteristica {i + 1}:"
            )
            input_caracteristica.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ecf0f1;
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
            QLineEdit:hover {
                border-color: #3498db;
            }
            """)
            lay.addWidget(input_caracteristica)
            label2 = QLabel(f"Tipo de caracteristica {i + 1}")
            label2.setStyleSheet("color: #000000;")
            lay.addWidget(label2)
            input_tipo_carac = QLineEdit()
            input_tipo_carac.setPlaceholderText(
                f"Ingrese el tipo de caracteristica {i + 1}: "
            )
            input_tipo_carac.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ecf0f1;
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
            QLineEdit:hover {
                border-color: #3498db;
            }
            """)
            lay.addWidget(input_tipo_carac)
            self.inputs.append(input_caracteristica)
            self.inputs_tipo.append(input_tipo_carac)

    def cargar_seleccion_tipoMobiliario(self):
        self.navegacion.combo_tipos_simple.clear()
        self.navegacion.combo_tipos_simple.addItem(
            "Selecciona un tipo de mobiliario", None
        )
        self.navegacion.combo_mobiliarios.currentTextChanged.connect(
            self.mostrar_detalles_mobiliario
        )
        obtener = self.tipo_mobiliario.listar_tipos_mobiliarios()
        for tmob in obtener:
            self.navegacion.combo_tipos_simple.addItem(
                tmob["descripcion"], tmob["codigoTiMob"]
            )
        self.navegacion.combo_tipos_simple.currentTextChanged.connect(
            self.cargar_mobiliarios_por_tipo
        )

    def cargar_mobiliarios_por_tipo(self, tipo_seleccionado):
        self.navegacion.combo_mobiliarios.clear()
        self.navegacion.combo_mobiliarios.addItem("Selecciona un mobiliario", None)
        if (
            tipo_seleccionado == "Selecciona un tipo de mobiliario"
            or not tipo_seleccionado
        ):
            return
        index = self.navegacion.combo_tipos_simple.currentIndex()
        codigo_tipo = self.navegacion.combo_tipos_simple.itemData(index)
        mobiliarios = self.mobiliario.mob_por_tipo(codigo_tipo)
        if mobiliarios:
            for mob in mobiliarios:
                texto = f"{mob['mobiliario']} - ${mob['costoRenta']}"
                self.navegacion.combo_mobiliarios.addItem(texto, mob["numero"])
        else:
            self.navegacion.combo_mobiliarios.addItem(
                "No hay mobiliarios de este tipo", None
            )

    def mostrar_detalles_mobiliario(self, mob_seleccionado):
        self.navegacion.texto_detalles_simple.clear()
        if mob_seleccionado == "Selecciona un mobiliario" or not mob_seleccionado:
            self.navegacion.texto_detalles_simple.setText(
                "Seleccione un mobiliario para ver detalles"
            )
            return
        index = self.navegacion.combo_mobiliarios.currentIndex()
        mob_numero = self.navegacion.combo_mobiliarios.itemData(index)
        if mob_numero:
            detalles = self.mobiliario.datos_mob(str(mob_numero))
            if detalles:
                mensaje_html = '<div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">'
                mensaje_html += '<h3 style="color: #9b582b;">DATOS DEL MOBILIARIO</h3>'

                mensaje_html += f"<p><b>Número:</b> {detalles.get('numMob', 'N/A')}</p>"
                mensaje_html += f"<p><b>Nombre:</b> {detalles.get('nombre', 'N/A')}</p>"
                mensaje_html += f"<p><b>Cantidad total:</b> {detalles.get('stockTotal', 0)}</p>"

                mensaje_html += '<h3 style="color: #9b582b;">CARACTERÍSTICAS</h3><ul>'
                for caracteristica in detalles.get("caracteristicas", []):
                    tipo_carac = caracteristica.get('tipo_carac', 'N/A')
                    nombre_carac = caracteristica.get('caracteristica', 'N/A')
                    mensaje_html += f"<li><b>{tipo_carac}:</b> {nombre_carac}</li>"
                mensaje_html += "</ul>"

                mensaje_html += '<h3 style="color: #9b582b;">DISTRIBUCIÓN DE ESTADOS</h3><ul>'
                for estado in detalles.get("estados", []):
                    cantidad = estado.get('cantidad', 0)
                    estado_nombre = estado.get('estado', 'N/A')
                    stock_total = detalles.get('stockTotal', 0)
                    porcentaje = (cantidad / stock_total) * 100 if stock_total > 0 else 0
                    mensaje_html += f"<li><b>{estado_nombre}:</b> {cantidad} unidades ({porcentaje:.1f}%)</li>"
                mensaje_html += "</ul>"
                
                mensaje_html += "</div>"
                self.navegacion.texto_detalles_simple.setHtml(mensaje_html)
            else:
                self.navegacion.texto_detalles_simple.setText(
                    "No se encontraron detalles para este mobiliario"
                )

    def actualizar_estado_mob(
        self, num_mob: int, cantidad: int, buscador: str, nuevo_estado: str
    ):
        try:
            resultado = self.mobiliario.actu_esta_mob(
                num_mob, cantidad, buscador, nuevo_estado
            )
            if not resultado:
                QMessageBox.critical(
                    None,
                    "Error de Actualización",
                    f"No se pudo actualizar el estado del mobiliario '{buscador}'. Verifique que el ID o el nombre de búsqueda existan.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Actualización Exitosa",
                    f"El estado de **{cantidad}** unidades de '{buscador}' ha sido actualizado a '{nuevo_estado}'.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos: {e}",
            )

    def cargar_estados_mobiliario(self):
        """
        Carga todos los estados de mobiliario en los ComboBoxes almBuscadorM y almNuevoEstadoMobi.
        """
        try:
            estados = self.mobiliario.listar_estados()
            
            # Asumiendo que ambos son QComboBox
            combo_buscador = self.navegacion.almBuscadorM
            combo_nuevo = self.navegacion.almNuevoEstadoMobi
            
            combo_buscador.clear()
            combo_buscador.addItem("Seleccione un estado...", None)
            
            combo_nuevo.clear()
            combo_nuevo.addItem("Seleccione nuevo estado...", None)

            if estados:
                for estado in estados:
                    combo_buscador.addItem(estado["descripcion"], estado["codigoMob"])
                    combo_nuevo.addItem(estado["descripcion"], estado["codigoMob"])
        
        except Exception as e:
            QMessageBox.critical(
                self.navegacion,
                "Error de Carga",
                f"No se pudieron cargar los estados de mobiliario: {e}",
            )

    def buscar_estado_mobiliario(self):
        # Asumiendo que 'tablaEstadosMobi' es un QTableWidget en el .ui
        tabla = self.navegacion.tablaEstadosMobi
        combo = self.navegacion.almBuscadorM # Asumiendo que ahora es un QComboBox
        
        try:
            if combo.currentIndex() == 0:
                TableManager.show_message(tabla, "Seleccione un estado para buscar")
                return
            
            estado_buscado = combo.currentText()
            resultado = self.mobiliario.obtener_mob_estado(estado_buscado)

            if not resultado:
                TableManager.show_message(tabla, f"No se encontró mobiliario en estado '{estado_buscado}'")
                return
            
            headers = ['Número', 'Nombre', 'Estado Actual', 'Cantidad']
            data = [[
                mob.get('Numero', 'N/A'),
                mob.get('Nombre', 'N/A'),
                mob.get('Estado', 'N/A'),
                mob.get('Cantidad', 'N/A')
            ] for mob in resultado]
            
            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            TableManager.fill_table(tabla, data)
            tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Hacer la tabla de solo lectura

        except Exception as e:
            QMessageBox.critical(
                self.navegacion, "Error Inesperado", f"Ocurrió un error al buscar el mobiliario: {e}"
            )

    def intentar_actualizar_estado_manual_mob(self):
        """
        Intenta actualizar el estado de un mobiliario usando los campos de entrada manuales.
        """
        try:
            # Asumiendo nuevos widgets en el .ui
            num_mob_str = self.navegacion.almNumeroMobi.text().strip()
            cantidad_a_mover_str = self.navegacion.almCantidadMoverMobi.text().strip()
            estado_nuevo = self.navegacion.almNuevoEstadoMobi.currentText()
            estado_origen = self.navegacion.almBuscadorM.currentText()

            if not num_mob_str or not cantidad_a_mover_str:
                QMessageBox.warning(self.navegacion, "Campos Vacíos", "Complete los campos de Número y Cantidad.")
                return

            if estado_origen == "Seleccione un estado..." or not estado_origen:
                QMessageBox.warning(self.navegacion, "Estado Origen Inválido", "Seleccione un Estado Origen válido.")
                return
            
            if estado_nuevo == "Seleccione nuevo estado..." or not estado_nuevo:
                QMessageBox.warning(self.navegacion, "Estado Destino Inválido", "Seleccione un Estado de Destino válido.")
                return

            num_mob = int(num_mob_str)
            cantidad_a_mover = int(cantidad_a_mover_str)

            if cantidad_a_mover <= 0:
                QMessageBox.warning(self.navegacion, "Cantidad Inválida", "La cantidad debe ser mayor a cero.")
                return

            cantidad_disponible = self.mobiliario.obtener_cantidad_en_estado(num_mob, estado_origen)

            if cantidad_disponible < cantidad_a_mover:
                QMessageBox.warning(self.navegacion, "Cantidad Excedida", f"Solo hay {cantidad_disponible} unidades del mobiliario {num_mob} en '{estado_origen}'.")
                return

            if estado_nuevo == estado_origen:
                QMessageBox.information(self.navegacion, "Mismo Estado", "El mobiliario ya se encuentra en ese estado.")
                return

            if self.main_window.mostrar_confirmacion(
                "Confirmar Actualización",
                f"¿Mover {cantidad_a_mover} unidad(es) del mobiliario #{num_mob}\n"
                f"Desde '{estado_origen}' hacia '{estado_nuevo}'?",
            ):
                self.actualizar_estado_mob(num_mob, cantidad_a_mover, estado_origen, estado_nuevo)
                self.navegacion.almNumeroMobi.clear()
                self.navegacion.almCantidadMoverMobi.clear()
            else:
                QMessageBox.information(self.navegacion, "Actualización Cancelada", "La operación ha sido cancelada.")

        except ValueError:
            QMessageBox.warning(self.navegacion, "Datos Inválidos", "El Número y la Cantidad deben ser números válidos.")
        except Exception as e:
            QMessageBox.critical(self.navegacion, "Error Inesperado", f"Ocurrió un error al procesar la actualización: {e}")


    def intentar_registrar_mobiliario(self):
        try:
            nombre = self.navegacion.mobNombre.text().strip()
            tipo = self.navegacion.mobTipo.text().strip()
            
            if not nombre:
                raise ValueError("Nombre del Mobiliario")
            if not tipo:
                raise ValueError("Tipo de Mobiliario")
    
            costoRenta = float(self.navegacion.mobCostoRenta.text())
            stock = int(self.navegacion.mobStock.text())
            
            if costoRenta <= 0 or stock <= 0:
                raise ValueError("Valores Numéricos")
                
            caracteristicas = []
            num_caracteristicas = len(self.inputs)
            
            for i in range(num_caracteristicas):
                nombre_carac = self.inputs[i].text().strip()
                tipo_carac = self.inputs_tipo[i].text().strip()
    
                if nombre_carac and tipo_carac:
                    caracteristica = MobCarac(nombre_carac, tipo_carac)
                    caracteristicas.append(caracteristica)
                elif nombre_carac or tipo_carac:
                    raise ValueError(f"Característica Incompleta: Faltó el Nombre o el Tipo de la Característica {i+1}")
            
            if self.navegacion.seleccionCaracteristicas.value() > 0 and len(caracteristicas) == 0:
                 if QMessageBox.question(
                    None, 
                    "Advertencia de Característica",
                    "Ha indicado que desea características, pero no ingresó ninguna. ¿Desea continuar con el registro sin características?"
                ) == QMessageBox.StandardButton.No:
                     return 
    
            if self.mostrar_confirmacion(
                "Confirmar Registro de Mobiliario", 
                f"¿Deseas registrar el mobiliario '{nombre}' (Stock: {stock}, Costo: ${costoRenta})?"
            ):
                self.registrar_mobiliario_ejecutar(nombre, costoRenta, stock, tipo, caracteristicas)
            else:
                QMessageBox.information(
                    None, 
                    "Registro Cancelado", 
                    "La operación de registro de mobiliario ha sido cancelada."
                )
    
        except ValueError as e:
            error_type = str(e)
            
            if "float" in error_type or "int" in error_type:
                 QMessageBox.warning(
                    None, "Datos Inválidos", "El Costo de Renta y el Stock deben ser números enteros o decimales válidos."
                )
            elif "Valores Numéricos" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El Costo de Renta y el Stock deben ser mayores que cero."
                )
            elif "Nombre del Mobiliario" in error_type:
                 QMessageBox.warning(
                    None, "Datos Faltantes", "Debes ingresar el Nombre del mobiliario."
                )
            elif "Tipo de Mobiliario" in error_type:
                 QMessageBox.warning(
                    None, "Datos Faltantes", "Debes ingresar el Tipo de mobiliario."
                )
            elif "Característica Incompleta" in error_type:
                 QMessageBox.warning(
                    None, "Datos Incompletos", f"Corrija la entrada: {error_type}."
                )
            else:
                 QMessageBox.critical(
                    None, "Error de Validación", f"Ocurrió un error inesperado al validar: {e}"
                )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error grave durante el pre-registro: {e}"
            )
