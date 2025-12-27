from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from services.DatosClienteService import DatosClienteService
from services.TelefonoServices import TelefonoServices
from utils.Formato import permitir_ingreso

ruta_ui = Path(__file__).parent / "registro_cliente.ui"


cliente = DatosClienteService()
telefono = TelefonoServices()


class RegistroCliente:
    def __init__(self):
        self.registro_cliente = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.registro_cliente.show()
        self.registro_cliente.clienteConfirmar.clicked.connect(
            self.intentar_registrar_cliente_completo
        )
        self.deshabilitar_telefonos()
        self.registro_cliente.cbTelefono2.toggled.connect(self.ingresar_segundoTel)
        self.registro_cliente.cbTelefono3.toggled.connect(self.ingresar_tercerTel)

        self.registro_cliente.cbTipoFisica.toggled.connect(self.seleccionar_fisica)
        self.registro_cliente.cbTipoMoral.toggled.connect(self.seleccionar_moral)
        self.registro_cliente.reNombreFiscal.setEnabled(False)

    def registrar_cliente_ejecutar(
        self,
        rfc,
        nombre,
        priApellido,
        priAmater,
        nombreFiscal,
        correo,
        colonia,
        calle,
        numero,
        tipo_cliente,
        telefono1,
        telefono2,
        telefono3,
    ):
        try:
            # 1. Registro del Cliente
            resultado = cliente.registrar_clientes(
                rfc,
                nombre,
                priApellido,
                priAmater,
                nombreFiscal,
                correo,
                colonia,
                calle,
                numero,
                tipo_cliente,
            )

            # 2. Registro de Teléfonos (solo si tienen contenido)
            if telefono1:
                telefono.registrar_telefono(telefono1, rfc, None)
            if (
                telefono2 and self.registro_cliente.reTelefono2.isEnabled()
            ):  # Verifica si el campo está habilitado
                telefono.registrar_telefono(telefono2, rfc, None)
            if (
                telefono3 and self.registro_cliente.reTelefono3.isEnabled()
            ):  # Verifica si el campo está habilitado
                telefono.registrar_telefono(telefono3, rfc, None)

            # 3. Retroalimentación Final
            if resultado is None:
                # Aquí se asume que si el resultado es None, es un error de la capa de datos.
                QMessageBox.critical(
                    None,
                    "Error de Registro",
                    f"No se pudo registrar el cliente (RFC: {rfc}). Verifique si el RFC ya está registrado.",
                )
            else:
                QMessageBox.information(
                    None,
                    "Cliente Registrado",
                    f"Cliente registrado con éxito: {nombre} {priApellido} {priAmater}",
                )

        except Exception as e:
            QMessageBox.critical(
                None,
                "Error de Ejecución",
                f"Ocurrió un error grave durante el registro (Cliente y/o Teléfonos): {e}",
            )

    def intentar_registrar_cliente_completo(self):
        try:
            # --- 1. DETERMINAR TIPO DE CLIENTE ---
            tipo_cliente = ""
            if self.registro_cliente.cbTipoFisica.isChecked():
                tipo_cliente = "TCLPF"
            if self.registro_cliente.cbTipoMoral.isChecked():
                tipo_cliente = "TCLPM"

            if not tipo_cliente:
                raise ValueError("Tipo Cliente Faltante")

            # --- 2. OBTENCIÓN Y VALIDACIÓN DE CAMPOS PRIMARIOS ---

            rfc = self.registro_cliente.reRfc.text().strip()
            nombre = self.registro_cliente.reNombre.text().strip()
            priApellido = self.registro_cliente.reApellPat.text().strip()
            priAmater = self.registro_cliente.reApellMa.text().strip()
            correo = self.registro_cliente.reCorreo.text().strip()

            # Validaciones específicas respetando 'permitir_ingreso' y longitud
            if (not permitir_ingreso(rfc, "rfc")) or len(rfc) < 2:
                raise ValueError("RFC Inválido")
            if (not permitir_ingreso(nombre, "onlytext")) or len(nombre) < 2:
                raise ValueError("Nombre Inválido")
            if not permitir_ingreso(priApellido, "onlytext"):
                raise ValueError("Apellido Paterno Inválido")
            if (not permitir_ingreso(priAmater, "onlytext")) or len(priAmater) < 2:
                raise ValueError("Apellido Materno Inválido")

            nombre_fiscal = self.registro_cliente.reNombreFiscal.text().strip()

            if (len(correo) < 2) or (not permitir_ingreso(correo, "correo")):
                raise ValueError("Email Inválido")

            colonia = self.registro_cliente.reColonia.text().strip()
            if (len(colonia) < 2) or (not permitir_ingreso(colonia, "onlytext")):
                raise ValueError("Colonia Inválida")

            calle = self.registro_cliente.reCalle.text().strip()
            if (len(calle) < 2) or (not permitir_ingreso(calle, "onlytext")):
                raise ValueError("Calle Inválida")

            numero_txt = self.registro_cliente.reNumero.text().strip()
            numero = int(numero_txt)

            telefono1 = self.registro_cliente.reTelefono1.text().strip()
            telefono2 = self.registro_cliente.reTelefono2.text().strip()
            telefono3 = self.registro_cliente.reTelefono3.text().strip()

            if not telefono1:
                raise ValueError("Teléfono Principal Faltante")

            if tipo_cliente == "TCLPM" and not nombre_fiscal:
                raise ValueError("Nombre Fiscal Faltante")

            nombre_completo = f"{nombre} {priApellido} {priAmater}"
            if self.mostrar_confirmacion(
                "Confirmar Registro de Cliente",
                f"¿Deseas registrar al cliente {nombre_completo} (RFC: {rfc}, Tipo: {tipo_cliente})?",
            ):
                self.registrar_cliente_ejecutar(
                    rfc,
                    nombre,
                    priApellido,
                    priAmater,
                    nombre_fiscal,
                    correo,
                    colonia,
                    calle,
                    numero,
                    tipo_cliente,
                    telefono1,
                    telefono2,
                    telefono3,
                )
            else:
                QMessageBox.information(
                    None,
                    "Registro Cancelado",
                    "La operación de registro de cliente ha sido cancelada.",
                )

        except ValueError as e:
            error_type = str(e)

            if "Tipo Cliente Faltante" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Faltantes",
                    "Debes seleccionar si es Persona Física o Moral.",
                )
            elif "RFC Inválido" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El RFC no es válido o es demasiado corto."
                )
            elif "Nombre Inválido" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El Nombre solo debe contener texto y debe tener al menos 2 caracteres.",
                )
            elif "Apellido Paterno Inválido" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El Apellido Paterno es inválido (solo texto, min. 2 caracteres).",
                )
            elif "Apellido Materno Inválido" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El Apellido Materno es inválido."
                )
            elif "Email Inválido" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El Correo Electrónico no es válido o es demasiado corto.",
                )
            elif "Colonia Inválida" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "La Colonia no es válida (solo texto, min. 2 caracteres).",
                )
            elif "Calle Inválida" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "La Calle no es válida (solo texto, min. 2 caracteres).",
                )
            elif "Teléfono Principal Faltante" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Faltantes",
                    "Debes ingresar el número de teléfono principal.",
                )
            elif "Nombre Fiscal Faltante" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Faltantes",
                    "El Nombre Fiscal es obligatorio para Personas Morales.",
                )
            elif "invalid literal for int()" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El campo 'Número' (de la calle) debe ser un número entero válido.",
                )
            else:
                QMessageBox.critical(
                    None,
                    "Error de Validación",
                    f"Ocurrió un error inesperado al validar datos: {e}",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error grave durante el pre-registro: {e}",
            )

    def deshabilitar_telefonos(self):
        self.registro_cliente.reTelefono2.setEnabled(False)
        self.registro_cliente.reTelefono3.setEnabled(False)

    def ingresar_segundoTel(self, estado):
        self.registro_cliente.reTelefono2.setEnabled(estado)

    def ingresar_tercerTel(self, estado):
        self.registro_cliente.reTelefono3.setEnabled(estado)

    def seleccionar_fisica(self, estado):
        if estado:
            self.registro_cliente.cbTipoMoral.setChecked(False)
            self.registro_cliente.reNombreFiscal.setEnabled(False)
            nombre_fiscal = f"{self.registro_cliente.reNombre.text()} {self.registro_cliente.reApellPat.text()} {self.registro_cliente.reApellMa.text()}"
            self.registro_cliente.reNombreFiscal.setText(nombre_fiscal)
            self.registro_cliente.clNombre.setText("Nombre")
            self.registro_cliente.clAp.setText("Apellido paterno")
            self.registro_cliente.clAm.setText("Apellido materno")

    def seleccionar_moral(self, estado):
        if estado:
            self.registro_cliente.cbTipoFisica.setChecked(False)
            self.registro_cliente.reNombreFiscal.setEnabled(True)
            self.registro_cliente.clNombre.setText("Nombre del contacto")
            self.registro_cliente.clAp.setText("Apellido paterno del contacto")
            self.registro_cliente.clAm.setText("Apellido materno del contacto")

    def mostrar_confirmacion(self, titulo: str, mensaje: str) -> bool:
        reply = QMessageBox.question(
            None,
            titulo,
            mensaje,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        return reply == QMessageBox.StandardButton.Yes

    # def initGUI(self):
    #   self.registro_cliente.btnRegistrar.clicked.connect(self.registrar)
