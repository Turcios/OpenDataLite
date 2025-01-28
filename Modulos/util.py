import variable
import json
from pathlib import Path

# Obtén la ruta del archivo relativa al script actual
script_dir = Path(__file__).resolve().parent
file_path = script_dir / "../language/languages.json"

def cambiar_idioma(idioma):
   with open(file_path, "r", encoding="utf-8") as f:
        variable.idioma_actual=json.load(f).get(idioma, {})