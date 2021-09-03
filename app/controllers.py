from flask import Blueprint, request, jsonify, render_template
import pandas as pd
from app.helpers import getTypeModel, getGraviteModel

main_controllers = Blueprint("main", __name__, url_prefix="/")


@main_controllers.route("/")
def index():
    return render_template("index.html")


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
    gravite_model = getGraviteModel()
    type_model = getTypeModel()
    resp_list = []

    if request.is_json:
        form_json = request.json
        if not isinstance(form_json, list):
            form_json = [form_json]
        for form in form_json:
            f_dict = {name: value for (name, value) in form.items()}
            data = pd.DataFrame.from_dict({attr: [f_dict.get(attr)] for attr in attrs})
            gravite = gravite_model.predict_proba(data)
            type = type_model.predict_proba(data)
            resp_list.append(
                {
                    "gravite": {
                        str(cls): proba
                        for (cls, proba) in zip(
                            gravite_model.classes_, gravite.tolist()[0]
                        )
                    },
                    "type": {
                        str(int(cls)): proba
                        for (cls, proba) in zip(type_model.classes_, type.tolist()[0])
                    },
                }
            )
    else:
        form = pd.DataFrame.from_dict(
            {attr: [request.form.get(attr)] for attr in attrs}
        )
        gravite = gravite_model.predict_proba(form)
        type = type_model.predict_proba(form)
        resp_list.append({"gravite": gravite, "type": type})

    return jsonify(data=resp_list, ok=True)
