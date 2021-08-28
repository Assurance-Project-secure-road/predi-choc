import pandas as pd
import numpy as np
from datetime import datetime
from joblib import load, dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, classification_report

model_collision = load("data/Collision_Acc.joblib")
model_gravite = load("data/Gravblessure_Usager.joblib")


def format_data_caracteristiques(caracteristiques: pd.DataFrame):

    caracteristiques["atm"] = caracteristiques["atm"].apply(
        lambda x: pd.NA if x == -1 else x
    )
    caracteristiques["col"] = caracteristiques["col"].apply(
        lambda x: pd.NA if x == -1 else x
    )
    caracteristiques["date"] = caracteristiques.apply(
        lambda line: datetime(
            line["an"],
            line["mois"],
            line["jour"],
            int(line["hrmn"].split(":")[0]),
            int(line["hrmn"].split(":")[1]),
        ),
        axis=1,
    )

    caracteristiques = caracteristiques.rename(
        columns={
            "Num_Acc": "Num_Acc_id",
            "date": "Date_Acc",
            "lum": "Lumiere_Acc",
            "dep": "Departement_Acc",
            "com": "Commune_Acc",
            "agg": "Agglomeration_Acc",
            "int": "Intersection_Acc",
            "atm": "Meteo_Acc",
            "col": "Collision_Acc",
            "adr": "Addresse_Acc",
            "lat": "Latitude_Acc",
            "long": "Longitude_Acc",
        }
    )

    caracteristiques = caracteristiques.drop(columns={"jour", "mois", "an", "hrmn"})

    return caracteristiques


def format_data_lieux(lieux: pd.DataFrame):

    lieux["catr"].replace(9, np.nan, inplace=True)
    lieux["circ"].replace(-1, np.nan, inplace=True)
    lieux["vosp"].replace(-1, np.nan, inplace=True)
    lieux["prof"].replace(-1, np.nan, inplace=True)
    lieux["vma"].replace(-1, np.nan, inplace=True)
    lieux["prof"].replace(-1, np.nan, inplace=True)
    lieux["surf"].replace([-1, 9], np.nan, inplace=True)
    lieux["infra"].replace([-1, 9], np.nan, inplace=True)
    lieux["situ"].replace([-1, 8], np.nan, inplace=True)

    lieux["pr"].replace("(1)", 1, inplace=True)
    lieux["pr1"].replace("(1)", 1, inplace=True)
    lieux["larrout"] = lieux["larrout"].apply(
        lambda x: np.ceil(float(x)) if not pd.isna(x) else x
    )
    lieux["lartpc"] = lieux["lartpc"].apply(
        lambda x: np.ceil(float(x)) if not pd.isna(x) else x
    )
    lieux["pr"] = lieux["pr"].apply(
        lambda x: np.ceil(float(x)) if not pd.isna(x) else x
    )
    lieux["pr1"] = lieux["pr1"].apply(
        lambda x: np.ceil(float(x)) if not pd.isna(x) else x
    )

    lieux.loc[lieux["vma"] > 130, "vma"] = lieux.loc[lieux["vma"] > 130, "vma"].apply(
        lambda x: x / 10
    )
    lieux.loc[lieux["vma"] < 10, "vma"] = lieux["vma"][lieux["vma"] < 10] * 10

    lieux = lieux.rename(
        columns={
            "Num_Acc": "Num_Acc_id",
            "catr": "Categorie_Route",
            "voie": "Numero_Route",
            "v1": "Indice_num_Route",
            "v2": "Indice_alphanum_Route",
            "circ": "Circulation_Route",
            "nbv": "Nb_voie_Route",
            "vosp": "Type_voie_Route",
            "prof": "Declivite_Route",
            "pr": "Num_borne_Route",
            "pr1": "Distance_Borne_Route",
            "plan": "Tracer_plan_Route",
            "lartpc": "Largeur_TPC_Route",
            "larrout": "Largeur_Route",
            "surf": "Surface_Route",
            "infra": "Infrastructure_Route",
            "situ": "Situation_Acc_Route",
            "vma": "Vitesse_max_Route",
        }
    )

    lieux = lieux.reset_index()
    lieux = lieux.rename(columns={"index": "id_Route"})
    lieux.id_Route = lieux.id_Route + 1

    col_name = "Num_Acc_id"
    fk_col = lieux.pop(col_name)
    lieux.insert(18, col_name, fk_col)

    return lieux


def format_data_usagers(usagers: pd.DataFrame):

    usagers.replace(-1, np.nan, inplace=True)
    usagers = usagers.replace(" -1", np.NAN)
    usagers = usagers.replace("0", np.NAN)
    usagers["trajet"] = usagers["trajet"].replace(0, np.NAN)
    usagers = usagers.rename(
        columns={
            "Num_Acc": "Num_Acc_id",
            "id_vehicule": "id_Vehicule",
            "place": "Place_Usager",
            "catu": "Categorie_Usager",
            "grav": "Gravblessure_Usager",
            "sexe": "Sexe_Usager",
            "an_nais": "Anne_Naissance_Usager",
            "trajet": "Motif_Deplacer_Usager",
            "secu1": "Equipement_Secu_Usager",
            "locp": "Localisation_pieton_Usager",
            "actp": "Action_pieton_Usager",
            "etatp": "Nb_pieton_Usager",
        }
    )

    usagers = usagers.reset_index()
    usagers = usagers.rename(columns={"index": "id_Usager"})
    usagers.id_Usager = usagers.id_Usager + 1

    usagers = usagers.drop(["num_veh", "secu2", "secu3"], axis=1)
    return usagers


def format_data_vehicules(vehicules: pd.DataFrame):

    col_replace_null = vehicules.columns[3:-1]

    for col in col_replace_null:
        vehicules[col].replace(-1, np.nan, inplace=True)
        vehicules[col] = vehicules[col].astype("Int64")

    vehicules = vehicules.rename(
        columns={
            "Num_Acc": "Num_Acc_id",
            "id_vehicule": "id_Vehicule",
            "num_veh": "Num_Vehicule",
            "senc": "Sens_circulation_Vehicule",
            "catv": "Categorie_Vehicule",
            "obs": "Obstacle_fixe_heurte_Vehicule",
            "obsm": "Obstacle_mobile_heurte_Vehicule",
            "choc": "Point_choc_Vehicule",
            "manv": "Manoeuvre_avant_accident_Vehicule",
            "motor": "Type_motorisation_Vehicule",
            "occutc": "Nb_occupant_Vehicule",
        }
    )

    return vehicules


def getTypeModel():
    return model_collision


def getGraviteModel():
    return model_gravite


def train_model(data, y, num_attribs, cat_attribs):
    data_x = data[num_attribs + cat_attribs]
    num_pipeline = Pipeline(
        [
            ("std_scaler", StandardScaler()),
        ]
    )
    col_transform = ColumnTransformer(
        [
            ("num", num_pipeline, num_attribs),
            ("cat", OneHotEncoder(), cat_attribs),
        ]
    )
    classifier = RandomForestClassifier(n_estimators=200, n_jobs=-1)
    full_pipeline = Pipeline([("data_tr", col_transform), ("classifier", classifier)])
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
    for train_index, test_index in split.split(data_x, data[y]):
        X_train, y_train = (
            data_x.loc[train_index],
            data.loc[train_index][y],
        )
        X_test, y_test = (
            data_x.loc[test_index],
            data.loc[test_index][y],
        )

    full_pipeline.fit(X_train, np.ravel(y_train))
    y_pred = full_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy RFST (train) for '{y}': {(accuracy * 100): 0.1f} ")
    print(classification_report(y_test, y_pred))
    dump(full_pipeline, f"data/{y}.joblib")

    return accuracy
