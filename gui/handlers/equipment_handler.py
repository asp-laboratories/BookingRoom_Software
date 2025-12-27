from PyQt6.QtWidgets import QMessageBox, QLabel, QPushButton, QListWidgetItem
from PyQt6.QtCore import Qt


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

    def registrar_equipamiento(self, nombre, descripcion, costo, stock, tipo):
        try:
            resultado = self.equipamiento.registrar_equipamento(
                nombre, descripcion, costo, stock, tipo
            )

            if not resultado:
                QMessageBox.critical(
                    None,
                    "Error de Registro",
                    f"No se pudo registrar el equipo '{nombre}'. Verifique la conexión o si el equipo ya existe.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Registro Exitoso",
                    f"El equipamiento '{nombre}' ha sido registrado correctamente.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
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
                    None,
                    "Error de Actualización",
                    f"No se pudo actualizar el campo '{campo}' del equipo {id_busqueda}. Verifique los datos o si el ID existe.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Actualización Exitosa",
                    f"El equipamiento {id_busqueda} ha sido actualizado correctamente.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error de conexión/base de datos: {e}",
            )

    def desplegar_informacion_equipamiento(self):
        self.navegacion.sResultadoListar_5.clear()
        try:
            resultado = self.equipamiento.listar_equipamentos_informacion(
                int(self.navegacion.slIngresarBusqueda_5.text())
            )
            if resultado is None:
                pass
            else:
                mensaje = "INFORMACION DEL EQUIPAMIENTO\n"
                mensaje += f"\n -Nombre: {resultado['nombre']}"
                mensaje += f"\n -Descripcion: {resultado['descripcion']}"
                mensaje += f"\n -Costo de renta: {str(resultado['costoRenta'])}"
                mensaje += f"\n -Cantidad: {str(resultado['stock'])}"
                self.navegacion.sResultadoListar_5.setText(mensaje)
        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "El numero de equipamiento debe ser un número entero válido.",
            )
        except TypeError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "El numero de equipamiento debe ser un número entero válido.",
            )

    def listar_equipamentos_del(self):
        self.navegacion.sResultadoListar_7.clear()
        try:
            resultado = self.equipamiento.listar_equipamentos()

            if not resultado:
                self.navegacion.sResultadoListar_7.setText("No hay equipamientos registrados para mostrar.")
            else:
                mensaje_html = '<div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">'
                mensaje_html += '<h3 style="color: #9b582b;">LISTA DE EQUIPAMIENTOS</h3>'
                
                for e in resultado:
                    numEquipa = e.get('numEquipa', 'N/A')
                    nombre = e.get('nombre', 'N/A')
                    descripcion = e.get('descripcion', 'N/A')
                    
                    mensaje_html += f"""
                    <div style="border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 5px;">
                        <p><b>Número:</b> {numEquipa}</p>
                        <p><b>Nombre:</b> {nombre}</p>
                        <p><b>Descripción:</b> {descripcion}</p>
                    </div>
                    """
                
                mensaje_html += "</div>"
                self.navegacion.sResultadoListar_7.setHtml(mensaje_html)
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error inesperado",
                f"Ocurrió un error al listar los equipamientos: {e}",
            )

    def eliminar_equipamiento(self, id_equipamiento: int):
        try:
            resultado = self.equipamiento.eliminar_registro(id_equipamiento)
            if not resultado:
                QMessageBox.critical(
                    None,
                    "Error de Eliminación",
                    "No se pudo eliminar el equipamiento. Verifique que el numero.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Eliminación Exitosa",
                    f"El equipamiento {id_equipamiento} ha sido eliminado correctamente.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
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
        self.navegacion.tResultadoS_3.setText("")
        try:
            tipo_equipamiento_buscado = self.navegacion.sEquipamiento.currentData()
            if not tipo_equipamiento_buscado:
                self.navegacion.tResultadoS_3.setText("Por favor, seleccione un tipo de equipamiento válido.")
                return

            resultado = self.equipamiento.listar_equipamiento_tipo(tipo_equipamiento_buscado)

            if not resultado:
                self.navegacion.tResultadoS_3.setText(f"No se encontraron equipamientos para el tipo: '{tipo_equipamiento_buscado}'.")
            else:
                mensaje_html = '<div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">'
                mensaje_html += f'<h3 style="color: #9b582b;">EQUIPAMIENTOS DE TIPO: {tipo_equipamiento_buscado.upper()}</h3>'
                
                for bes in resultado:
                    numero = bes.get('numero', 'N/A')
                    equipamiento_nombre = bes.get('equipamiento', 'N/A')
                    
                    mensaje_html += f"""
                    <div style="border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 5px;">
                        <p><b>Número:</b> {numero}</p>
                        <p><b>Equipamiento:</b> {equipamiento_nombre}</p>
                    </div>
                    """
                
                mensaje_html += "</div>"
                self.navegacion.tResultadoS_3.setHtml(mensaje_html)
        except Exception as e:
            QMessageBox.critical(
                None,
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
                    None,
                    "Actualización Exitosa",
                    f"Se han movido {cantidad} unidades del equipo {num_equipo} al estado '{estado_nuevo}'.",
                )
            else:
                QMessageBox.critical(
                    None,
                    "Error de Actualización",
                    f"No se pudo actualizar el estado del equipo {num_equipo}. Verifique la existencia del numero, la cantidad disponible en el estado origen o si los estados son válidos.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
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

    def intentar_registrar_equipamiento(self):
        try:
            costo_renta = float(self.navegacion.eCostoRenta.text())
            stock = int(self.navegacion.eStock.text())
            nombre_equipo = self.navegacion.eNombreEqui.text()
            descripcion = self.navegacion.eDescripcion.text()
            tipo = self.navegacion.eTipoEquipamiento.text()
            if self.main_window.mostrar_confirmacion(
                "Confirmar Registro de Equipamiento",
                f"¿Deseas registrar el equipo '{nombre_equipo}' (Costo: ${costo_renta}, Stock: {stock})?",
            ):
                self.registrar_equipamiento(
                    nombre_equipo, descripcion, costo_renta, stock, tipo
                )
            else:
                QMessageBox.information(
                    None,
                    "Registro Cancelado",
                    "La operación de registro ha sido cancelada.",
                )
        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "Asegúrate de que 'Costo de Renta' y 'Stock' contengan valores numéricos válidos.",
            )
        except Exception as e:
            QMessageBox.critical(
                None,
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
                    None,
                    "Actualización Cancelada",
                    "La operación de actualización del equipamiento ha sido cancelada.",
                )
        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "Asegúrate de que la búsqueda contenga un valor numérico entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                None,
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
                    None,
                    "Operación Cancelada",
                    "La eliminación del equipamiento ha sido cancelada por el usuario.",
                )
        except ValueError:
            QMessageBox.warning(
                None,
                "Datos Inválidos",
                "El equipamiento a eliminar debe ser un número entero válido.",
            )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error de Pre-Validación",
                f"Ocurrió un error al intentar leer el ID: {e}",
            )

    def intentar_actualizar_estado_equipa(self):
        try:
            num_equipo = int(self.navegacion.numE.text())
            cantidad = int(self.navegacion.almCantidade.text())
            estado_nuevo = self.navegacion.almEstadoO.text().strip()
            estado_origen = self.navegacion.almEstadoE.text().strip()
            if not estado_nuevo or not estado_origen:
                raise ValueError("Campos de estado vacíos")
            if self.main_window.mostrar_confirmacion(
                "Confirmar Actualización de Estado",
                f"¿Deseas mover {cantidad} unidades del equipo {num_equipo} desde el estado '{estado_origen}' al nuevo estado '{estado_nuevo}'?",
            ):
                self.actualizar_estado_equipa(
                    num_equipo, estado_nuevo, estado_origen, cantidad
                )
            else:
                QMessageBox.information(
                    None,
                    "Actualización Cancelada",
                    "La operación de actualización del estado ha sido cancelada.",
                )
        except ValueError as e:
            error_msg = str(e)
            if "invalid literal for int()" in error_msg:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "Asegúrate de que los campos de numero y cantidad contengan valores numéricos enteros válidos.",
                )
            elif "Campos de estado vacíos" in error_msg:
                QMessageBox.warning(
                    None,
                    "Datos Faltantes",
                    "Los campos Estado Nuevo' y Estado Origen' no pueden estar vacíos.",
                )
            else:
                QMessageBox.critical(
                    None,
                    "Error de Pre-Validación",
                    f"Ocurrió un error inesperado al validar los datos: {e}",
                )
        except Exception as e:
            QMessageBox.critical(
                None, "Error Inesperado", f"Ocurrió un error al procesar los datos: {e}"
            )

    def buscar_estado_equipamiento(self):
        self.navegacion.almResulE.clear()  # Limpiar resultados anteriores

        try:
            estado_buscado = self.navegacion.almBuscadorE.text().strip()

            if not estado_buscado:
                QMessageBox.warning(
                    None,
                    "Búsqueda Inválida",
                    "Por favor, ingresa el **estado de equipamiento** que deseas buscar (ej. 'Operativo', 'En Reparación').",
                )
                return

            resultado = self.equipamiento.obtener_equipa_estado(estado_buscado)

            if not resultado: # If resultado is None or empty list
                QMessageBox.information(
                    None,
                    "Sin Resultados",
                    f"No se encontró equipamiento en el estado '{estado_buscado}' o el estado no es válido.",
                )
                # Removed redundant setText call here
                return
            else:
                mensaje_html = '<div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">'
                mensaje_html += f'<h3 style="color: #9b582b;">EQUIPAMIENTOS EN ESTADO: {estado_buscado.upper()}</h3>'

                for equi in resultado:
                    numero = equi.get('Numero', 'N/A')
                    nombre = equi.get('Nombre', 'N/A')
                    estado_actual = equi.get('Estado', 'N/A')
                    cantidad = equi.get('Cantidad', 'N/A')
                    
                    mensaje_html += f"""
                    <div style="border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 5px;">
                        <p><b>Número:</b> {numero}</p>
                        <p><b>Nombre:</b> {nombre}</p>
                        <p><b>Estado Actual:</b> {estado_actual}</p>
                        <p><b>Cantidad:</b> {cantidad}</p>
                    </div>
                    """
                
                mensaje_html += "</div>"
                self.navegacion.almResulE.setHtml(mensaje_html)

        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error al intentar buscar el equipamiento: {e}",
            )
