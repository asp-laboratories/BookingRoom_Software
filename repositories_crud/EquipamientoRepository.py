from models.Equipamiento import Equipamiento

class EquipamentoRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_equipamiento(self, equipamiento):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO equipamiento (numEquipa, nombre, descripcion, costoRenta, stock, esta_equipa, tipo_equipa)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (equipamiento.numEquipa, equipamiento.nombre, equipamiento.descripcion, equipamiento.costoRenta, equipamiento.stock, equipamiento.esta_equipa, equipamiento.tipo_equipa))
    
            self.db.connection.commit()
            print("Se añadio un equipamento")
        except Exception as error:
            print(f"Error al crear un equipamento: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()    
        return True

    def listar_equipamiento(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM equipamiento")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los equipamentos: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados

