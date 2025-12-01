
class InventarioEquipaRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def actualizar_estado_equipamiento(self, numEquipa, esta_og, new_esta, cantidad):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT *
                            FROM inventario_equipa
                            WHERE equipamiento = %s and esta_equipa = %s
                            """, (numEquipa, new_esta))
            
            resultados = cursor.fetchall()

            if not resultados:
                cursor.execute( """
                                INSERT INTO inventario_equipa 
                                """)