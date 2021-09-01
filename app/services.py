import os
from flask import Flask
from joblib import load, dump
from sklearn.pipeline import Pipeline
import click


class ModelService:
    def __init__(self):
        self.__gravite = None
        self.__collision = None

    def init_app(self, app: Flask):
        self.gravite_path = app.config.get(
            "GRAVITE_PATH", "data/Gravblessure_Usager.joblib"
        )
        self.collision_path = app.config.get(
            "COLLISION_PATH", "data/Collision_Acc.joblib"
        )

        if os.path.isfile(self.gravite_path):
            self.__gravite: Pipeline = load(self.gravite_path)
        else:
            app.logger.warning(
                f"Le fichier '{self.gravite_path}' pour le modèle de prédiction n'a pas été généré correctement, merci de lancer flask generate-model."
            )

        if os.path.isfile(self.collision_path):
            self.__collision: Pipeline = load(self.collision_path)
        else:
            app.logger.warning(
                f"Le fichier '{self.collision_path}' pour le modèle de prédiction n'a pas été généré correctement, merci de lancer flask generate-model."
            )

    @property
    def gravite(self):
        return self.__gravite

    @property
    def collision(self):
        return self.__collision

    def save_gravite(self, model: Pipeline):
        dump(model, self.gravite_path)

    def save_collision(self, model: Pipeline):
        dump(model, self.collision_path)


model_service = ModelService()
