from enum import Enum


class ParkingVeloColumns(str, Enum):
    osm_id = 'osm_id'
    couvert = 'couvert'
    capacite = 'capacite'
    nom = 'nom'
    acces = 'acces'
    payant = 'payant'
    surveille = 'surveille'
    type = 'type'
    insee_com = 'insee_com'
    nom_com = 'nom_com'
    date_modif = 'date_modif'
    notes = 'notes'
    geometry = 'geometry'

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value
