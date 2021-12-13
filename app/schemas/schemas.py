"""Liste des schémas qui nous permettent de valider des données reçu via une
requête de type POST ou un PUT"""


update_playground_slide_schema = {
    "type": "object",
    "required": ["nom", "arrondissement_id", "ouvert", "deblaye", "condition"],
    "properties": {
        "nom": {"type": "string", "minLength": 1},
        "arrondissement_id": {
            "type": "number",
            "minimum": 0,
        },
        "ouvert": {"type": "number", "minimum": 0},
        "deblaye": {"type": "number", "minimum": 0},
        "condition": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False,
}

update_ice_rink_schema = {
    "type": "object",
    "required": [
        "nom",
        "arrondissement_id",
        "date_heure",
        "ouvert",
        "deblaye",
        "arrose",
        "resurface",
    ],
    "properties": {
        "nom": {"type": "string", "minLength": 1},
        "arrondissement_id": {
            "type": "number",
            "minimum": 0,
        },
        "date_heure": {
            "type": "string",
            "format": "full-date",
            "minLength": 10,
        },
        "ouvert": {"type": "number", "minimum": 0},
        "deblaye": {"type": "number", "minimum": 0},
        "arrose": {"type": "number", "minimum": 0},
        "resurface": {"type": "number", "minimum": 0},
    },
    "additionalProperties": False,
}

update_aquatic_installation_schema = {
    "type": "object",
    "required": [
        "nom",
        "arrondissement_id",
        "type",
        "adresse",
        "propriete",
        "gestion",
        "equipement",
    ],
    "properties": {
        "nom": {"type": "string", "minLength": 1},
        "arrondissement_id": {
            "type": "number",
            "minimum": 0,
        },
        "type": {"type": "string", "minLength": 1},
        "adresse": {"type": "string", "minLength": 1},
        "propriete": {"type": "string", "minLength": 1},
        "gestion": {"type": "string", "minLength": 1},
        "equipement": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False,
}
