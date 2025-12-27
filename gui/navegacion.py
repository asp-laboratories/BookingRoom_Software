from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from services.SalonServices import SalonServices
from services.ServicioServices import ServicioService
from services.EquipamentoService import EquipamentoService
from services.TrabajadorServices import TrabajadorServices
from utils.Formato import permitir_ingreso

ruta_ui = Path(__file__).parent / "navegacion.ui"
servicio = ServicioService()
salon = SalonServices()
equipamiento = EquipamentoService()
trabajador = TrabajadorServices()


class Navegacion:
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.sMensaje.setText("")
        self.navegacion.saMensaje.setText("")
        self.navegacion.eMensaje.setText("")
        self.navegacion.atMensaR.setText("")
        self.navegacion.atMensaje.setText("")

        self.navegacion.subMenuAdministracion.setVisible(False)
        self.navegacion.subMenuAlmacen.setVisible(False)
        self.navegacion.subMenuRecepcion.setVisible(False)
        self.navegacion.widget.layout()
        self.navegacion.btnAdministracion.clicked.connect(self.abrir_opciones_admin)
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)
        self.navegacion.btnRecepcion.clicked.connect(self.abrir_opciones_recep)

        self.navegacion.atConfirmar.clicked.connect(self.establecer_rol)

        self.navegacion.servicios.clicked.connect(lambda: self.mostrar_pagina(1))
        self.navegacion.equipamiento.clicked.connect(lambda: self.mostrar_pagina(2))
        self.navegacion.salon.clicked.connect(lambda: self.mostrar_pagina(3))
        self.navegacion.reservacion.clicked.connect(lambda: self.mostrar_pagina(4))
        self.navegacion.subTrabajador.clicked.connect(lambda: self.mostrar_pagina(5))

        self.navegacion.sConfirmar.clicked.connect(self.registar_servicio)

        self.navegacion.sConfirmarAct.clicked.connect(self.actualizar_servicio)

        self.navegacion.saConfirmar.clicked.connect(self.registrar_salon)
        self.navegacion.saCancelar.clicked.connect(self.limpiar_salon)
        self.navegacion.atBuscar.clicked.connect(self.buscar)

        self.cargar_seleccion_salon()
        self.navegacion.reSalonInfo.clicked.connect(self.mostrar_info_salon)

        self.navegacion.eConfirmar.clicked.connect(self.registrar_equipamiento)

    def abrir_opciones_admin(self):
        self.navegacion.subMenuAdministracion.setVisible(
            not self.navegacion.subMenuAdministracion.isVisible()
        )

    def abrir_opciones_almac(self):
        self.navegacion.subMenuAlmacen.setVisible(
            not self.navegacion.subMenuAlmacen.isVisible()
        )

    def abrir_opciones_recep(self):
        self.navegacion.subMenuRecepcion.setVisible(
            not self.navegacion.subMenuRecepcion.isVisible()
        )

    def registar_servicio(self):
        nombre = self.navegacion.sNombreSer.text()
        if len(nombre) < 2:  # unica validacion?
            self.navegacion.sMensaje.setText("Ingresar un nombre valido")

        descripcion = self.navegacion.sDescripcion.text()
        if len(descripcion) < 2:
            self.navegacion.sMensaje.setText("Ingresar una descripcion valida")

        resCostoRenta = self.navegacion.sCostoRenta.text()
        if not (permitir_ingreso(resCostoRenta, "numfloat")):
            self.navegacion.sMensaje.setText(
                "Ingrese un valor valido como costo de renta"
            )
        else:
            costo_renta = float(resCostoRenta)

        tipo_servicio = self.navegacion.sTipoServicio.text()  # Combo box?

        resultado = servicio.registrar_servicio(
            nombre, descripcion, costo_renta, tipo_servicio
        )

        if not resultado:
            self.navegacion.sMensaje.setText("Registro fallido")
        else:
            self.navegacion.sMensaje.setText("Registro concretado")

    def registrar_salon(self):
        resLargo = self.navegacion.saLargo.text()
        if not permitir_ingreso(resLargo, "numfloat"):
            self.navegacion.saMensaje.setText("Ingrese valor numerico en largo")
        else:
            largo = float(resLargo)

        resAncho = self.navegacion.saAncho.text()
        if not permitir_ingreso(resAncho, "numfloat"):
            self.navegacion.saMensaje.setText("Ingrese valor numerico en ancho")
        else:
            ancho = float(resAncho)

        resAltura = float(self.navegacion.saAltura.text())
        if not permitir_ingreso(resAltura, "numfloat"):
            self.navegacion.saMensaje.setText("Ingrese valor numerico en altura")
        else:
            altura = float(resAltura)

        m2 = 2 * (largo + ancho) * altura
        self.navegacion.saResultadoM2.setText(str(m2))

        nombre = self.navegacion.saNombre.text()
        if len(nombre) < 2:
            self.navegacion.saMensaje.setText("Ingrese un nombre valido (solo letras)")
        # elif not permitir_ingreso(nombre, 'correo'): # Las lineas comentadas estan en caso de ser realmente requerido el ingreso de un formato en este tipo de campos
        #    self.navegacion.saMensaje.setText("Ingrese un nombre valido (solo letras)")

        costoRenta = self.navegacion.saCostoRenta.text()
        if not permitir_ingreso(costoRenta, "numfloat"):
            self.navegacion.saMensaje.setText(
                "Ingrese valor numerico en el costo de renta"
            )
        else:
            costoRenta = float(costoRenta)

        nombrePasillo = self.navegacion.saNombrePasillo.text()
        if len(nombrePasillo) < 2:
            self.navegacion.saMensaje.setText("Ingrese un nombre valido (solo letras)")
        # if not permitir_ingreso(nombrePasillo, 'correo'):
        #    self.navegacion.saMensaje.setText("Ingrese un nombre de pasillo valido")

        numPasillo = self.navegacion.saNumeroPasillo.text()
        if not permitir_ingreso(numPasillo, "numtraba"):
            self.navegacion.saMensaje.setText("Ingrese un nombre de pasillo valido")

        resultado = salon.registrar_salones(
            nombre, costoRenta, nombrePasillo, numPasillo, largo, ancho, altura, m2
        )
        if not resultado:
            self.navegacion.saMensaje.setText("Registro fallido")
        else:
            self.navegacion.saMensaje.setText("Registro concretado")

    def registrar_equipamiento(self):
        nombreEquipa = self.navegacion.eNombreEqui.text()
        if len(nombreEquipa) < 2:
            self.navegacion.saMensaje.setText("Ingrese un nombre valido")
        # if not permitir_ingreso(nombreEquipa, 'onlytext'):
        #    self.navegacion.eMensaje.setText("Nombre no valido (no caracteres especiales)")

        descripcion = self.navegacion.eDescripcion.text()
        if len(descripcion) < 2:
            self.navegacion.saMensaje.setText("Ingrese una descripcion valida")
        # if not permitir_ingreso(descripcion, 'correo'):
        #    self.navegacion.eMensaje.setText("Descripcion no valida (utilizar una descripcion mas simple)")

        resCostoRenta = self.navegacion.eCostoRenta.text()
        if not permitir_ingreso(resCostoRenta, "numfloat"):
            self.navegacion.eMensaje.setText(
                "Ingrese valor numerico en el costo de renta"
            )
        else:
            costoRenta = float(resCostoRenta)

        resStock = self.navegacion.eStock.text()
        if not permitir_ingreso(resStock, "numint"):
            self.navegacion.eMensaje.setText(
                "Ingrese valor numerico como cantidad de stock"
            )
        else:
            stock = int(resStock)

        tipoEquipa = self.navegacion.eTipoEquipamiento.text()
        # if not permitir_ingreso(tipoEquipa, 'onlytext'):
        #    self.navegacion.eMensaje.setText("Tipo de equipamiento no valido") # Segun yo esto se iba a cambiar para hacerse con combobox ¿¿

        # resultado = equipamiento.registrar_equipamento(nombreEquipa, descripcion, costoRenta, stock, tipoEquipa)

        if not equipamiento.registrar_equipamento(
            nombreEquipa, descripcion, costoRenta, stock, tipoEquipa
        ):
            self.navegacion.eMensaje.setText("Registro fallido")
        else:
            self.navegacion.eMensaje.setText("Registro concretado")

    def limpiar_salon(self):
        self.navegacion.saNombre.clear()
        self.navegacion.saCostoRenta.clear()
        self.navegacion.saNombrePasillo.clear()
        self.navegacion.saNumeroPasillo.clear()
        self.navegacion.saLargo.clear()
        self.navegacion.saAncho.clear()
        self.navegacion.saAltura.clear()
        self.navegacion.saResultadoM2.clear()

    def mostrar_pagina(self, indice):
        self.navegacion.stackedWidget.setCurrentIndex(indice)

    def cargar_seleccion_salon(self):
        self.navegacion.reSalonSelecc.clear()
        self.navegacion.reSalonSelecc.addItem("Selecciona un salon", None)
        obtener = salon.listar_salones()
        for sln in obtener:
            self.navegacion.reSalonSelecc.addItem(sln["nombre"], sln["numSalon"])

    def mostrar_info_salon(self):
        salNumero = self.navegacion.reSalonSelecc.currentData()
        sali = self.buscar_usuario_por_id(salNumero)
        mensaje = "INFORMACION DEL SALON"
        mensaje += f"\n NOMBRE: {sali['nombre']}"
        mensaje += f"\n COSTO: {str(sali['costoRenta'])}"
        if sali:
            self.navegacion.resultadoSalon.setText(mensaje)

    def buscar_usuario_por_id(self, salNumero):
        for s in salon.listar_salones():
            if s["numSalon"] == salNumero:
                return s
        return None

    def buscar(self):
        termino_busqueda = self.navegacion.atBuscador.text()
        if not termino_busqueda:
            self.navegacion.atResultadoText.setText("Por favor, ingrese un término de búsqueda.")
            self.navegacion.atMensaje.setText("")
            return

        resultado = trabajador.buscar_al_trabajador(termino_busqueda)

        if not resultado:
            self.navegacion.atResultadoText.setText(f"No se encontraron trabajadores con el RFC: {termino_busqueda}")
            self.navegacion.atMensaje.setText("Sin resultados")
        else:
            mensaje_html = '<div style="font-family: Adwaita Sans; font-size: 14px; color: #333;">'
            mensaje_html += '<h3 style="color: #9b582b;">RESULTADOS DE BÚSQUEDA</h3>'
            
            for traba in resultado:
                rfc = traba.get('RFC', 'N/A')
                nombre = traba.get('nombre', 'N/A')
                rol = traba.get('rol', 'N/A')
                
                mensaje_html += f"""
                <div style="border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
                    <p><b>RFC:</b> {rfc}</p>
                    <p><b>Nombre:</b> {nombre}</p>
                    <p><b>Rol:</b> {rol}</p>
                </div>
                """
            
            mensaje_html += "</div>"
            self.navegacion.atResultadoText.setHtml(mensaje_html)
            self.navegacion.atMensaje.setText(f"{len(resultado)} resultado(s)")

    def establecer_rol(self):
        resultado = trabajador.actualizar_roles(
            self.navegacion.atRfc.text(), self.navegacion.atNombreR.text()
        )
        if resultado is None:
            QMessageBox.information(self.navegacion, "Éxito", "Rol establecido correctamente.")
        else:
            QMessageBox.warning(self.navegacion, "Error", "No se pudo establecer el rol.")

    def actualizar_servicio(self):
        resultado = servicio.actualizar_campos(
            self.navegacion.sCampo.text(),
            int(self.navegacion.sNumeroServicio.text()),
            self.navegacion.sNuevoValor.text(),
        )
        if not resultado:
            QMessageBox.warning(self.navegacion, "Error de actualización", "La actualización del servicio fue incorrecta.")
        else:
            QMessageBox.information(self.navegacion, "Éxito", "Servicio actualizado correctamente.")

    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
