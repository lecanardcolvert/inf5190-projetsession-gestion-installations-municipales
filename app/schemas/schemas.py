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
