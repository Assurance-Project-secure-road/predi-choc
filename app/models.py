import urllib, hashlib
from pandas import DataFrame
from flask_login import UserMixin
from app.db import db

class Caracteristique(db.Model):
    __tablename__ = 'Caracteristique'
    Num_Acc_id = db.Column('Num_Acc_id', db.Integer, primary_key=True)
    Date_Acc = db.Column('Date_Acc', db.DateTime)
    Lumiere_Acc = db.Column('Lumiere_Acc', db.Integer)
    Departement_Acc = db.Column("Departement_Acc", db.String)
    Commune_Acc = db.Column("Commune_Acc", db.String)
    Agglomeration_Acc = db.Column("Agglomeration_Acc", db.Integer)
    Intersection_Acc = db.Column("Intersection_Acc", db.Integer)
    Meteo_Acc = db.Column("Meteo", db.Integer)
    Collision_Acc = db.Column("Collision_Acc", db.Integer)
    Addresse_Acc = db.Column("Addresse_Acc", db.String)
    Latitude_Acc = db.Column("Latitude_Acc", db.Numeric(10,7))
    Longitude_Acc = db.Column("Longitude_Acc", db.Numeric(10,7))

    def insert_from_pd(caracteristiques: DataFrame):
        caracteristiques.to_sql("Caracteristique")
    

class Vehicule(db.Model):
    __tablename__ = 'Vehicule'
    id_Vehicule = db.Column('id_vehicule', db.Integer, primary_key=True)
    Num_Vehicule = db.Column('Num_Vehicule', db.Integer)
    Sens_circulation_Vehicule = db.Column("Sens_circulation_Vehicule", db.Integer)
    Categorie_Vehicule = db.Column("Categorie_Vehicule", db.Integer)
    Obstacle_fixe_heurete_Vehicule = db.Column("Obstacle_fixe_heurete_Vehicule", db.Integer)
    Obstacle_mobile_heurete_Vehicule = db.Column("Obstacle_mobile_heurete_Vehicule", db.Integer)
    Point_choc_Vehicule = db.Column("Point_choc_Vehicule", db.Integer)
    Manoeuvre_avant_accident_Vehicule = db.Column("Manoeuvre_avant_accident_Vehicule", db.Integer)
    Type_motorisation_Vehicule = db.Column("Type_motorisation_Vehicule", db.Integer)
    Nb_occupant_Vehicule = db.Column("Nb_occupant_Vehicule", db.Integer)
    Num_Acc_id = db.Column("Num_Acc_id", db.ForeignKey("Caracteristique.Num_Acc_id"))

    def insert_from_pd(vehicules: DataFrame):
        vehicules.to_sql("Vehicule")


class Usager(db.Model):
    __tablename__ = 'Usager'
    id_Usager = db.Column('id_Usager', db.Integer, primary_key=True)
    Place_Usager = db.Column('Place_Usager', db.Integer)
    Categorie_Usager = db.Column("Categorie_Usager", db.Integer)
    Gravblessure_Usager = db.Column("Gravblessure_Usager", db.Integer)
    Sexe_Usager = db.Column("Sexe_Usager", db.Integer)
    Anne_Naissance_Usager = db.Column("Anne_Naissance_Usager", db.Integer)
    Motif_Deplacer_Usager = db.Column("Motif_Deplacer_Usager", db.Integer)
    Equipement_Secu_Usager = db.Column("Equipement_Secu_Usager", db.Integer)
    Localisation_pieton_Usager = db.Column("Localisation_pieton_Usager", db.Integer)
    Action_pieton_Usager = db.Column("Action_pieton_Usager", db.String)
    Nb_pieton_Usager = db.Column("Nb_pieton_Usager", db.Integer)
    Num_Acc_id = db.Column("Num_Acc_id", db.ForeignKey("Caracteristique.Num_Acc_id"))
    id_Vehicule = db.Column("id_Vehicule", db.ForeignKey("Vehicule.id_vehicule"))

    def insert_from_pd(usagers: DataFrame):
        usagers.to_sql("Usager")


class Lieux(db.Model):
    __tablename__ = 'Lieux'
    ID_Route = db.Column("ID_Route", db.Integer, primary_key=True)
    Categorie_Route = db.Column('Categorie_Route', db.Integer)
    Numero_Route = db.Column('Numero_Route', db.Integer)
    Indice_num_Route = db.Column('Indice_num_Route', db.Integer)
    Indice_alphanum_Route = db.Column("Indice_alphanum_Route", db.String(5))
    Circulation_Route = db.Column("Circulation_Route", db.Integer)
    Nb_voie_Route = db.Column("Nb_voie_Route", db.Integer)
    Type_voie_Route = db.Column("Type_voie_Route", db.Integer)
    Declivite_Route = db.Column("Declivite_Route", db.Integer)
    Num_borne_Route = db.Column("Num_borne_Route", db.Integer)
    Distance_borne_Route = db.Column("Distance_borne_Route", db.Integer)
    Tracer_plan_Route = db.Column("Tracer_plan_Route", db.Integer)
    Largeur_TPC_Route = db.Column("Largeur_TPC_Route", db.Integer)
    Largeur_Route = db.Column("Largeur_Route", db.Integer)
    Surface_Route = db.Column("Surface_Route", db.Integer)    
    Infrastruture_Route = db.Column("Infrastruture_Route", db.Integer)
    Situation_Acc_Route = db.Column("Situation_Acc_Route", db.Integer)
    Vitesse_max_Route = db.Column("Vitesse_max_Route", db.Integer)
    Num_Acc_id = db.Column("Num_Acc_id", db.ForeignKey("Caracteristique.Num_Acc_id"))

    def insert_from_pd(lieux: DataFrame):
        lieux.to_sql("Lieux")

class User(UserMixin, db.Model):
    """Table User de la BDD, il est possible de faire des requetes sql
    avec User.query (voir la doc de flask-sqlalchemy)
    """
    __tablename__ = "user"
    id = db.Column("u_id", db.Integer, primary_key=True)
    email = db.Column("u_email", db.String(60), nullable=False)
    password = db.Column("u_password", db.String(128), nullable=False)
    role_id = db.Column("u_role_id", db.ForeignKey("user_role.role_id"))

    def get_avatar(self):
        gravatar_url = (
            "https://www.gravatar.com/avatar/"
            + hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()
            + "?"
        )
        gravatar_url += urllib.parse.urlencode({"s": "40"})
        return gravatar_url
    
    def has_permissions(self, perms: list[str]):
        return all([perm in self.role.permissions for perm in perms])

class UserRole(db.Model):
    """Table UserRole de la BDD, il est possible de faire des requetes sql
    avec UserRole.query (voir la doc de flask-sqlalchemy)
    """
    __tablename__ = "user_role"
    id = db.Column("role_id", db.Integer, primary_key=True)
    name = db.Column("role_name", db.String(64), nullable=False)
    permissions = db.Column("role_permissions", db.PickleType, nullable=False)
    users = db.relationship("User", backref="role")