from flask import Blueprint, request, jsonify
import pandas as pd
from app.helpers import getTypeModel, getGraviteModel

main_controllers = Blueprint("main", __name__, url_prefix="/")


@main_controllers.route("/")
def index():
    return "Hello World!"


@main_controllers.route("/api/sondage", methods=["POST"])
def sondage():
    attrs = [
        "Age",
        "Nb_voie_Route",
        "Vitesse_max_Route",
        "Sexe_Usager",
        "Equipement_Secu_Usager",
        "Departement_Acc",
        "Categorie_Vehicule",
        "Month",
        "Type_motorisation_Vehicule",
        "Categorie_Route",
        "Circulation_Route",
        "Surface_Route",
        "Lumiere_Acc",
        "Meteo_Acc",
        "Motif_Deplacer_Usager",
    ]
    if request.is_json:
        form = pd.DataFrame.from_dict(
            {name: [value] for (name, value) in request.json.items()}
        )
    else:
        form = pd.DataFrame.from_dict(
            {attr: [request.form.get(attr)] for attr in attrs}
        )
    gravite_model = getGraviteModel()
    type_model = getTypeModel()
    gravite = gravite_model.predict(form)
    type = type_model.predict(form)
    return jsonify(gravite=int(gravite[0]), type=int(type[0]))
