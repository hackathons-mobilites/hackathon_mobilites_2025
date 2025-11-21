from enum import Enum


class TransportsPossiblesColumns(str, Enum):
    serie_de_materiel = "Série de Materiel"
    numero_materiel = "Numéro matériel"
    equipe_de_porte_velo = "Equipé de porte vélo ou d'espace vélo (Oui/Non)"
    ligne = "Ligne"
    nombre_de_rames_equipees = "Nombre de rames équipées pour vélos"
    nombre_de_place_par_rame = "Nombre de place par rame en US"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value
