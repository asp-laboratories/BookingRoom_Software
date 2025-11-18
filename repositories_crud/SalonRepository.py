class SalonRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_salon(self, salon):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO datos_salon (numSalon, nombre, ubiNombrePas, ubiNumeroPas, dimenLargo, dimenAncho, dimenAltura, mCuadrados, esta_salon)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (salon.numSalon, salon.nombre, salon.ubiNombrePas, salon.ubiNumeroPas, salon.dimenLargo, salon.dimenAncho, salon.dimenAltura, salon.mCuadrados, salon.esta_salon))
    
            self.db.connection.commit()
            print("Se añadio un salon")
            return True
        except Exception as error:
            print(f"Error al crear un salon: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_salones(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM datos_salon")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados

    def listar_estados(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM esta_salon")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados


    def actualizar(self, numSalon, esta_salon):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                UPDATE datos_salon 
                SET esta_salon = %s 
                WHERE numSalon = %s
            """, (esta_salon, numSalon))
            self.db.connection.commit()
            print("Salon actualizado exitosamente.")
            
        except Exception as e:
            print(f"Error al actualizar salon: {e}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
