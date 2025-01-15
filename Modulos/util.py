import variable
import json

def cambiar_idioma(idioma):
   with open("C:/Users/keren/Desktop/Python/OpenDataLite/language/languages.json", "r", encoding="utf-8") as f:
        variable.idioma_actual=json.load(f).get(idioma, {})