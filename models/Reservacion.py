class Reservacion:
    def __init__(
        self,
        fechaReser,
        fechaEvento,
        horaInicio,
        horaFin,
        descripEvento,
        estimaAsistentes,
        trabajador,
        datos_cliente,
        datos_montaje,
        servicios=[],
        equipamientos=[],
        subtotal=None,
        IVA=None,
        total=None,
        numReser=None,
        esta_reser="PENDI",
    ):
        self.__numReser = numReser
        self.__fechaReser = fechaReser
        self.__fechaEvento = fechaEvento
        self.__horaInicio = horaInicio
        self.__horaFin = horaFin
        self.__descripEvento = descripEvento
        self.__estimaAsistentes = estimaAsistentes
        self.__subtotal = subtotal
        self.__IVA = IVA
        self.__total = total
        self.__datos_montaje = datos_montaje
        self.__trabajador = trabajador
        self.__datos_cliente = datos_cliente
        self.__esta_reser = esta_reser
        self.__servicios = servicios
        self.__equipamientos = equipamientos

    @property
    def numReser(self):
        return self.__numReser

    @numReser.setter
    def numReser(self, numReser):
        self.__numReser = numReser

    @property
    def fechaReser(self):
        return self.__fechaReser

    @fechaReser.setter
    def fechaReser(self, fechaReser):
        self.__fechaReser = fechaReser

    @property
    def fechaEvento(self):
        return self.__fechaEvento

    @fechaEvento.setter
    def fechaEvento(self, fechaEvento):
        self.__fechaEvento = fechaEvento

    @property
    def horaInicio(self):
        return self.__horaInicio

    @horaInicio.setter
    def horaInicio(self, horaInicio):
        self.__horaInicio = horaInicio

    @property
    def horaFin(self):
        return self.__horaFin

    @horaFin.setter
    def horaFin(self, horaFin):
        self.__horaFin = horaFin

    @property
    def descripEvento(self):
        return self.__descripEvento

    @descripEvento.setter
    def descripEvento(self, descripEvento):
        self.__descripEvento = descripEvento

    @property
    def estimaAsistentes(self):
        return self.__estimaAsistentes

    @estimaAsistentes.setter
    def estimaAsistentes(self, estimaAsistentes):
        self.__estimaAsistentes = estimaAsistentes

    @property
    def subtotal(self):
        return self.__subtotal

    @subtotal.setter
    def subtotal(self, subtotal):
        self.__subtotal = subtotal

    @property
    def IVA(self):
        return self.__IVA

    @IVA.setter
    def IVA(self, IVA):
        self.__IVA = IVA

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, total):
        self.__total = total

    @property
    def trabajador(self):
        return self.__trabajador

    @trabajador.setter
    def trabajador(self, trabajador):
        self.__trabajador = trabajador

    @property
    def datos_cliente(self):
        return self.__datos_cliente

    @datos_cliente.setter
    def datos_cliente(self, datos_cliente):
        self.__datos_cliente = datos_cliente

    @property
    def esta_reser(self):
        return self.__esta_reser

    @esta_reser.setter
    def esta_reser(self, esta_reser):
        self.__esta_reser = esta_reser

    @property
    def datos_montaje(self):
        return self.__datos_montaje

    @datos_montaje.setter
    def datos_montaje(self, datos_montaje):
        self.__datos_montaje = datos_montaje

    @property
    def equipamientos(self):
        return self.__equipamientos

    @equipamientos.setter
    def equipamientos(self, equipamientos):
        self.__equipamientos = equipamientos

    @property
    def servicios(self):
        return self.__servicios

    @servicios.setter
    def servicios(self, servicios):
        self.__servicios = servicios


class Reservacion2:
    def __init__(
        self,
        fechaReser,
        fechaEvento,
        horaInicio,
        horaFin,
        descripEvento,
        estimaAsistentes,
        trabajador,
        datos_cliente,
        datos_montaje,
        subtotal=None,
        IVA=None,
        total=None,
        numReser=None,
        esta_reser="PENDI",
    ):
        self.__numReser = numReser
        self.__fechaReser = fechaReser
        self.__fechaEvento = fechaEvento
        self.__horaInicio = horaInicio
        self.__horaFin = horaFin
        self.__descripEvento = descripEvento
        self.__estimaAsistentes = estimaAsistentes
        self.__subtotal = subtotal
        self.__IVA = IVA
        self.__total = total
        self.__datos_montaje = datos_montaje
        self.__trabajador = trabajador
        self.__datos_cliente = datos_cliente
        self.__esta_reser = esta_reser

    @property
    def numReser(self):
        return self.__numReser

    @numReser.setter
    def numReser(self, numReser):
        self.__numReser = numReser

    @property
    def fechaReser(self):
        return self.__fechaReser

    @fechaReser.setter
    def fechaReser(self, fechaReser):
        self.__fechaReser = fechaReser

    @property
    def fechaEvento(self):
        return self.__fechaEvento

    @fechaEvento.setter
    def fechaEvento(self, fechaEvento):
        self.__fechaEvento = fechaEvento

    @property
    def horaInicio(self):
        return self.__horaInicio

    @horaInicio.setter
    def horaInicio(self, horaInicio):
        self.__horaInicio = horaInicio

    @property
    def horaFin(self):
        return self.__horaFin

    @horaFin.setter
    def horaFin(self, horaFin):
        self.__horaFin = horaFin

    @property
    def descripEvento(self):
        return self.__descripEvento

    @descripEvento.setter
    def descripEvento(self, descripEvento):
        self.__descripEvento = descripEvento

    @property
    def estimaAsistentes(self):
        return self.__estimaAsistentes

    @estimaAsistentes.setter
    def estimaAsistentes(self, estimaAsistentes):
        self.__estimaAsistentes = estimaAsistentes

    @property
    def subtotal(self):
        return self.__subtotal

    @subtotal.setter
    def subtotal(self, subtotal):
        self.__subtotal = subtotal

    @property
    def IVA(self):
        return self.__IVA

    @IVA.setter
    def IVA(self, IVA):
        self.__IVA = IVA

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, total):
        self.__total = total

    @property
    def trabajador(self):
        return self.__trabajador

    @trabajador.setter
    def trabajador(self, trabajador):
        self.__trabajador = trabajador

    @property
    def datos_cliente(self):
        return self.__datos_cliente

    @datos_cliente.setter
    def datos_cliente(self, datos_cliente):
        self.__datos_cliente = datos_cliente

    @property
    def esta_reser(self):
        return self.__esta_reser

    @esta_reser.setter
    def esta_reser(self, esta_reser):
        self.__esta_reser = esta_reser

    @property
    def datos_montaje(self):
        return self.__datos_montaje

    @datos_montaje.setter
    def datos_montaje(self, datos_montaje):
        self.__datos_montaje = datos_montaje
