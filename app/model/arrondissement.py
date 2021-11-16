from dataclasses import dataclass


@dataclass
class Arrondissement:
    id: int
    nom: str
    cle: str
    dateMaj: str
