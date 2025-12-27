from datetime import date
from PyQt6.QtWidgets import (
    QMessageBox,
    QListWidgetItem,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt
from models.ReserEquipa import ReserEquipamiento
from utils.Formato import permitir_ingreso


class ReservacionHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.reservacion = self.main_window.reservacion
        self.trabajador = self.main_window.trabajador
        self.salon = self.main_window.salon
        self.tipo_montaje = self.main_window.tipo_montaje
        self.mobiliario = self.main_window.mobiliario
        self.datosMontaje = self.main_window.datosMontaje
        self.servicio = self.main_window.servicio
        self.equipamiento = self.main_window.equipamiento

    def obtener_fecha_reser(self):
        fecha_seleccion = self.navegacion.refecha_2.date()
        formato = fecha_seleccion.toString("yyyy-MM-dd")
        resultado = self.reservacion.fecha(formato)

        self.navegacion.tResultadoS_4.clear()

        if not resultado:
            self.navegacion.tResultadoS_4.setText(f"No se encontraron reservaciones para la fecha {formato}.")
            return

        mensaje_html = f"""
        <div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">
            <h3 style="color: #9b582b;">RESERVACIONES PARA EL {formato}</h3>
        """

        for f in resultado:
            cliente = f.get('cliente', 'N/A')
            evento = f.get('evento', 'N/A')
            hra_ini = f.get('hra_ini', 'N/A')
            hra_fin = f.get('hra_fin', 'N/A')
            asistentes = f.get('asistentes', 'N/A')
            salon = f.get('salon', 'N/A')

            mensaje_html += f"""
            <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <p><b>Cliente:</b> {cliente}</p>
                <p><b>Evento:</b> {evento}</p>
                <p><b>Horario:</b> {hra_ini} a {hra_fin}</p>
                <p><b>Asistentes:</b> {asistentes}</p>
                <p><b>Salón:</b> {salon}</p>
            </div>
            """
        
        mensaje_html += "</div>"
        self.navegacion.tResultadoS_4.setHtml(mensaje_html)
    def registrar_reservacion(self):
        from gui.login import resultadoEmail

        fecha = self.navegacion.refecha.date().toPyDate()
        fechaReserE = date.today()
        hora_inicio = self.navegacion.reHoraInicio.time().toString("HH:mm")
        hora_fin = self.navegacion.reHoraFin.time().toString("HH:mm")
        resultado = self.trabajador.obtener_nombre(resultadoEmail[0])
        rfcTrabajador = resultado["nombre"]

        descripEvento = self.navegacion.reDescripcion.text()
        if len(descripEvento) < 5:
            QMessageBox.warning(
                self.navegacion,
                "Error en Descripcion",
                "Ingrese una descripcion verdadera",
            )
            return

        estimaAsistentes = self.navegacion.reEstimadoAsistentes.text()
        if not permitir_ingreso(estimaAsistentes, "numint"):
            QMessageBox.warning(
                self.navegacion,
                "Error en Asistentes",
                "Ingrese un valor valido para el estimado de asistentes",
            )
            return

        salNumero = self.navegacion.reSalonSelecc.currentData()
        if not salNumero:
            QMessageBox.warning(
                self.navegacion,
                "Error Salon Seleccionado",
                "No se ha seleccionado un salon",
            )
            return

        sali = self.main_window.salon_handler.buscar_salon_por_id(salNumero)

        tipo_montaje = self.navegacion.reTipoMontaje.currentText()
        if not tipo_montaje:
            QMessageBox.warning(
                self.navegacion,
                "Error Tipo de Montaje",
                "No se ha seleccionado un tipo de montaje",
            )
            return

        lista_servicios = []
        servicios = self.navegacion.listaServicios.selectedItems()

        for item in servicios:
            data_servicio = item.data(Qt.ItemDataRole.UserRole)
            lista_servicios.append(data_servicio["nombre"])

        equipas = self.generar_lista_equipamiento_reservado()
        for equipa in equipas:
            equipa.equipamiento = self.equipamiento.obtener_codigo_equipamiento(
                equipa.equipamiento
            )
            if self.equipamiento.comprobar_stock(equipa.equipamiento, equipa.cantidad):
                QMessageBox.warning(
                    self.navegacion,
                    "Stock insuficiente",
                    f"No existe suficiente disponibilidad del equipamiento {equipa.equipamiento}",
                )
                return

        disponibilidad = self.salon.salon_disponible()
        for salon_disponible in disponibilidad:
            if (sali["numSalon"]) == (salon_disponible["numSalon"]) and str(
                fecha
            ) == str(salon_disponible["fecha"]):
                QMessageBox.warning(
                    self.navegacion,
                    "Salon ocupado en dia seleccionado",
                    "El salon seleccionado ya tiene una reservacion el dia seleccionado",
                )
                return

        try:
            clienteReservacion = self.main_window.clienteNombre
        except AttributeError:
            QMessageBox.warning(
                self.navegacion,
                "Error Cliente",
                "No se ha seleccionado un cliente para la reservacion",
            )
            return

        respuesta = self.main_window.mostrar_confirmacion(
            "Confirmacion de Reservacion", "¿Seguro de continuar con la resevacion?"
        )
        if respuesta:
            self.reservacion.crear_reservacion(
                fechaReserE,
                fecha,
                hora_inicio,
                hora_fin,
                descripEvento,
                estimaAsistentes,
                tipo_montaje,
                rfcTrabajador,
                clienteReservacion,
                sali["nombre"],
                equipas,
                lista_servicios,
            )

        def total_reservacion(self):
            self.intentar_registrar_reservacion()
            subtotalServicios = self.calcular_subtotal_serv()
            subtotalEquipamiento = self.calcular_total_general()
    
            total = (
                subtotalServicios + subtotalEquipamiento + self.main_window.subtotal_salon
            )
            iva = total * 0.16
            gran_total = total + iva
    
            # Using rich text for better visual presentation
            self.navegacion.reSubtotal.setText(f'Subtotal: <b style="color: #555;">${total:,.2f}</b>')
            self.navegacion.reIVA.setText(f'IVA (16%): <b style="color: #555;">${iva:,.2f}</b>')
            self.navegacion.reTotal.setText(f'<b style="font-size: 18pt; color: #c0392b;">Total: ${gran_total:,.2f}</b>')
    
            return gran_total
    def intentar_registrar_reservacion(self):
        try:
            from gui.login import resultadoEmail

            fecha = self.navegacion.refecha.date().toPyDate()
            fechaReserE = date.today()
            hora_inicio = self.navegacion.reHoraInicio.time().toString("HH:mm")
            hora_fin = self.navegacion.reHoraFin.time().toString("HH:mm")

            email_trabajador = resultadoEmail[0]
            resultado_trabajador = self.trabajador.obtener_nombre(email_trabajador)
            rfcTrabajador = resultado_trabajador.get("nombre")

            descripEvento = self.navegacion.reDescripcion.text().strip()
            if len(descripEvento) < 5:
                raise ValueError("Descripcion Corta")

            estimaAsistentes_txt = self.navegacion.reEstimadoAsistentes.text().strip()
            estimaAsistentes = int(estimaAsistentes_txt)
            if estimaAsistentes <= 0:
                raise ValueError("Asistentes Inválidos")

            tipo_montaje = self.navegacion.reTipoMontaje.currentText()
            if not tipo_montaje:
                raise ValueError("Tipo Montaje Faltante")

            salNumero = self.navegacion.reSalonSelecc.currentData()
            if salNumero is None:
                raise ValueError("Salon No Seleccionado")

            sali = self.main_window.salon_handler.buscar_salon_por_id(salNumero)
            if not sali:
                raise ValueError("Salon No Encontrado")

            equipas = self.generar_lista_equipamiento_reservado()
            for equipa in equipas:
                codigo_equipo = self.equipamiento.obtener_codigo_equipamiento(
                    equipa.equipamiento
                )

                if self.equipamiento.comprobar_stock(codigo_equipo, equipa.cantidad):
                    raise ValueError(f"Stock insuficiente: {equipa.equipamiento}")

            salon_reservado = False
            disponibilidad = self.salon.salon_disponible()

            num_salon_seleccionado = sali["numSalon"]
            fecha_seleccionada = str(fecha)

            for salon_disponible in disponibilidad:
                if (salon_disponible["numSalon"] == num_salon_seleccionado) and (
                    str(salon_disponible["fecha"]) == fecha_seleccionada
                ):
                    salon_reservado = True
                    break

            if salon_reservado:
                raise ValueError("Salon Ocupado")

            lista_servicios = []
            servicios = self.navegacion.listaServicios.selectedItems()
            for item in servicios:
                data_servicio = item.data(Qt.ItemDataRole.UserRole)
                lista_servicios.append(data_servicio["nombre"])

            nombre_salon = sali["nombre"]
            if self.main_window.mostrar_confirmacion(
                "Confirmar Reservación",
                f"¿Desea confirmar la reservación para el salón '{nombre_salon}' el día {fecha}? Esta acción afectará el stock de equipamiento.",
            ):
                self.reservacion.crear_reservacion(
                    fechaReserE,
                    fecha,
                    hora_inicio,
                    hora_fin,
                    descripEvento,
                    estimaAsistentes,
                    tipo_montaje,
                    rfcTrabajador,
                    self.main_window.clienteNombre,
                    sali["nombre"],
                    equipas,
                    lista_servicios,
                )
            else:
                QMessageBox.information(
                    None,
                    "Reservación Cancelada",
                    "La operación de registro de reservación ha sido cancelada por el usuario.",
                )

        except ValueError as e:
            error_type = str(e)

            if "Descripcion Corta" in error_type:
                QMessageBox.warning(
                    None,
                    "Error en Descripción",
                    "La descripción del evento es demasiado corta. Ingrese una descripción de 5 caracteres o más.",
                )
            elif (
                "Asistentes Inválidos" in error_type
                or "invalid literal for int()" in error_type
            ):
                QMessageBox.warning(
                    None,
                    "Error en Asistentes",
                    "Ingrese un valor numérico entero válido y positivo para el estimado de asistentes.",
                )
            elif "Tipo Montaje Faltante" in error_type:
                QMessageBox.warning(
                    None,
                    "Error en Montaje",
                    "Debe seleccionar un tipo de montaje para la reservación.",
                )
            elif (
                "Salon No Seleccionado" in error_type
                or "Salon No Encontrado" in error_type
            ):
                QMessageBox.warning(
                    None,
                    "Error en Salón",
                    "Debe seleccionar un salón válido para la reservación.",
                )
            elif "Stock insuficiente" in error_type:
                QMessageBox.critical(
                    None,
                    "Stock Insuficiente",
                    f"No existe suficiente disponibilidad del equipamiento: {error_type.split(': ')[1]}",
                )
            elif "Salon Ocupado" in error_type:
                QMessageBox.warning(
                    None,
                    "Salón Ocupado",
                    "El salón seleccionado ya tiene una reservación para la fecha indicada.",
                )
            else:
                QMessageBox.critical(
                    None,
                    "Error de Validación",
                    f"Ocurrió un error inesperado al validar los datos: {e}",
                )

        except Exception as e:
            # Manejo de cualquier otro error inesperado
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error grave durante el pre-registro: {e}",
            )

    def cargar_listas(self):
        self.navegacion.listaServicios.clear()
        for servi in self.servicio.listar_servicio():
            texto = f"{servi['nombre']} - ${servi['costoRenta']:.2f}"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, servi)
            self.navegacion.listaServicios.addItem(item)

    def calcular_subtotal_serv(self):
        servicios_seleccionados = self.navegacion.listaServicios.selectedItems()
        self.main_window.subtotal_servicios = 0.0

        for servicios in servicios_seleccionados:
            servicio = servicios.data(Qt.ItemDataRole.UserRole)
            self.main_window.subtotal_servicios += servicio["costoRenta"]
        return self.main_window.subtotal_servicios

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

            if nombre not in self.main_window.cantidades:
                self.main_window.cantidades[nombre] = 1

            self.crear_control_cantidad(nombre, costoRenta, numEquipa)

    def crear_control_cantidad(self, nombre, costoRenta, numEquipa):
        layEqui = self.navegacion.equipamientoW.layout()
        lbl_producto = QLabel(f"{nombre} (${costoRenta} c/u)")
        lbl_producto.setMinimumWidth(150)
        lbl_producto.setStyleSheet("QLabel{color: #000000}")
        btn_menos = QPushButton("-")
        btn_menos.setFixedSize(30, 30)
        btn_menos.clicked.connect(lambda: self.cambiar_cantidad(nombre, -1, numEquipa))
        btn_menos.setStyleSheet(
            "QPushButton{color: #ffffff; background-color: #000000;}"
        )
        lbl_cantidad = QLabel(str(self.main_window.cantidades[nombre]))
        lbl_cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_cantidad.setMinimumWidth(30)
        lbl_cantidad.setStyleSheet("font-weight: bold; color: #000000;")
        btn_mas = QPushButton("+")
        btn_mas.setFixedSize(30, 30)
        btn_mas.clicked.connect(lambda: self.cambiar_cantidad(nombre, 1, numEquipa))
        btn_mas.setStyleSheet("QPushButton{color: #ffffff; background-color: #000000;}")
        subtotal = self.main_window.cantidades[nombre] * costoRenta
        lbl_subtotal = QLabel(f"${subtotal:.2f}")
        lbl_subtotal.setMinimumWidth(60)
        lbl_subtotal.setStyleSheet("font-weight: bold; color: blue;")

        if nombre not in self.main_window.controles_equipos:
            self.main_window.controles_equipos[nombre] = {
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
        nueva_cantidad = self.main_window.cantidades[nombre] + cambio

        if nueva_cantidad < 0:
            return

        self.main_window.cantidades[nombre] = nueva_cantidad

        if nombre in self.main_window.controles_equipos:
            controles = self.main_window.controles_equipos[nombre]
            controles["label_cantidad"].setText(str(nueva_cantidad))
            self.main_window.datos_finales[numEquipa] = nueva_cantidad
            nuevo_subtotal = nueva_cantidad * controles["costo"]
            controles["label_subtotal"].setText(f"${nuevo_subtotal:.2f}")

        self.calcular_total_general()

    def generar_lista_equipamiento_reservado(self):
        lista_objetos_reservados = []
        equipamientos_seleccionados = self.navegacion.listaEquipamiento.selectedItems()

        for item in equipamientos_seleccionados:
            equipa_data = item.data(Qt.ItemDataRole.UserRole)
            nombre = equipa_data.get("nombre")
            cantidad_final = self.main_window.cantidades.get(nombre, 0)
            if cantidad_final > 0:
                nuevo_objeto = ReserEquipamiento(nombre, cantidad_final)
                lista_objetos_reservados.append(nuevo_objeto)
        return lista_objetos_reservados

    def limpiar_todos_controles(self):
        layEqui = self.navegacion.equipamientoW.layout()
        while layEqui.count():
            child = layEqui.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.main_window.controles_equipos.clear()

    def cargar_seleccion_tipoMontaje(self):
        self.navegacion.reTipoMontaje.clear()
        self.navegacion.reTipoMontaje.addItem("Selecciona un montaje", None)
        slon_especifico = self.navegacion.reSalonSelecc.currentText()
        if not slon_especifico == "Selecciona un salon":
            montajes = self.tipo_montaje.listar_mobiliarios_salon(slon_especifico)
            for datoSalon in montajes:
                bol = True
                for datosMobiliario in datoSalon["mobiliarios"]:
                    if not self.mobiliario.stock_disponible(
                        datosMobiliario.mobiliario, datosMobiliario.cantidad
                    ):
                        bol = False
                if bol:
                    self.navegacion.reTipoMontaje.addItem(datoSalon["nombre"], None)

            if self.navegacion.reTipoMontaje.count() <= 1:
                self.navegacion.resultadoMontaje.setText(
                    "No es posible usar el salon seleccionado"
                )
        else:
            self.navegacion.resultadoMontaje.setText("Seleccione un salon")

    def mostrar_info_montaje(self):
        tipoM = self.navegacion.reTipoMontaje.currentText()
        tip = self.buscar_por_id(tipoM)
        if tip:
            mensaje = "INFORMACION DEL MONTAJE\n"
            mensaje += f"\n -Nombre: {tip['nombre']}"
            mensaje += f"\n -Descripcion: {tip['descripcion']}"
            self.navegacion.resultadoMontaje.setText(mensaje)
        else:
            self.navegacion.resultadoMontaje.setText("Seleccione un tipo de montaje")
            return
        self.mostrar_mobiliarios_reservacion()

    def mostrar_mobiliarios_reservacion(self):
        salon = self.navegacion.reSalonSelecc.currentText()
        montaje = self.navegacion.reTipoMontaje.currentText()
        mobiliarios = self.datosMontaje.mobiliarios_montaje(montaje, salon)
        mensaje = "\n----Mobiliarios Necesarios-----\n"
        for mobi in mobiliarios:
            mensaje += f"\nMobiliario: {mobi['nombre']}\tCantidad: {mobi['cantidad']}"
        self.navegacion.reMobiliarioDatosMontaje.setText(mensaje)

    def buscar_por_id(self, tipoM):
        for t in self.tipo_montaje.listar_tipos_montajes():
            if t["nombre"] == tipoM:
                return t
        return None

    def calcular_total_general(self):
        total = 0
        for nombre, cantidad in self.main_window.cantidades.items():
            if nombre in self.main_window.controles_equipos:
                costo = self.main_window.controles_equipos[nombre]["costo"]
                subtotal = cantidad * costo
                total += subtotal
        if hasattr(self.navegacion, "lblTotalGeneral"):
            self.navegacion.lblTotalGeneral.setText(f"Total: ${total:.2f}")
        return total
