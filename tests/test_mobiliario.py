import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.mobiliarioService import mobiliarioService
from config.db_settings import BaseDeDatos


if __name__ == "__main__":
    db = BaseDeDatos()
    db.conectar()
    prueba = mobiliarioService(db)
    # prueba.listar_tipo_carac()
    # prueba.actu_carac_mob(1,"hhh", 'mater')
    prueba.actu_esta_mob(
        numMob=3, cantidad=10, esta_mob_og="Disponible", new_esta_mob="No Disponible"
    )
    # print(prueba.obtener_tipo_carac('espec'))
    # print(prueba.caracteristicas_mob(1))
    # prueba.actu_esta_mob(numMob=1,cantidad=50,esta_mob_og='disponible',new_esta_mob='no disponible')
    # print(prueba.obtener_tipo_carac('espec'))
    # print(prueba.caracteristicas_mob(1))
    # print(prueba.obtener_mob_estado('Disponible'))
    db.desconectar()
