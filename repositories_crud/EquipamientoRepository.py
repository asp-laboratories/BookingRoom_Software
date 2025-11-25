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
                INSERT INTO equipamiento (nombre, descripcion, costoRenta, stock, esta_equipa, tipo_equipa)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, ( equipamiento.nombre, equipamiento.descripcion, equipamiento.costoRenta, equipamiento.stock, equipamiento.esta_equipa, equipamiento.tipo_equipa))
    
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
    
    def listar_equipamiento(self):
        if not self.db.conectar(): 
            return None
        try:

            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM equipamiento")
            valores_equipamiento = cursor.fetchall()

        except Exception as error:
            print(f"Error al actualizar salon: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()

        return valores_equipamiento
    
    def actualizar_equipamiento(self, numEquipa, nombre, cambiodato):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute(f"""
                UPDATE equipamiento SET
                nombre = {cambiodato}
                WHERE numEquipa = %s
                    """,(nombre, numEquipa))
            self.db.connection.commit()
            print(f"Se actualizo el equipamiento: {nombre} = {numEquipa}")

        except Exception as error:
            print(f"Ocurrio un error actualizar: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()
        return True
    
    def eliminar_equipamiento(self, esta_equipa):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute(f"""
                DELETE FROM equipamiento
                WHERE esta_equipa = %s
                    """,(esta_equipa))
            self.db.connection.commit()
            print(f"Se elimino el esta_equipa: {esta_equipa}")

        except Exception as error:
            print(f"Ocurrio un error al eliminar: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()
        return True