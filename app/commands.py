import click
import pandas as pd
from flask.cli import with_appcontext
from getpass import getpass
from werkzeug.security import generate_password_hash
from consolemenu import SelectionMenu
from app.db import db
from app.models import Caracteristique, Lieux, Usager, Vehicule, User, UserRole
from app.helpers import (
    format_data_caracteristiques,
    format_data_lieux,
    format_data_usagers,
    format_data_vehicules,
)


@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application"""
    # On récupère les données du fichier CSV dans un dataframe
    caracteristiques = pd.read_csv(
        "data/caracteristiques.csv", delimiter=";", decimal=","
    )
    lieux = pd.read_csv("data/lieux.csv", delimiter=";", decimal=",")
    usagers = pd.read_csv("data/usagers.csv", delimiter=";", decimal=",")
    vehicules = pd.read_csv("data/vehicules.csv", delimiter=";", decimal=",")
    # On format les données (int64 pour les champs) afin de les préparer à l'insertion
    caracteristiques = format_data_caracteristiques(caracteristiques)
    lieux = format_data_lieux(lieux)
    vehicules = format_data_vehicules(vehicules)
    usagers = format_data_usagers(usagers)
    # On insère les données dans la table
    Caracteristique.insert_from_pd(caracteristiques)
    Lieux.insert_from_pd(lieux)
    Vehicule.insert_from_pd(vehicules)
    Usager.insert_from_pd(usagers)
    print("Données dans la BDD insérées")

    # On crée les roles Admin et Membre avec des permissions différentes
    roles = [
        UserRole(
            name="Admin",
            permissions=[
                "admin.read",
                "admin.write",
                "admin.update",
                "user.read",
                "user.write",
                "user.update",
            ],
        ),
        UserRole(name="Membre", permissions=["user.read"]),
    ]
    # On ajoute chaque rôle à la BDD
    for role in roles:
        db.session.add(role)
    print("Roles ajoutées")

    # On confirme tous les changements pour la transaction
    db.session.commit()
    print("Tout a été inséré dans la base de données !")


@click.command("create-user")
@with_appcontext
def create_user():
    """Insert un utilisateur la base de données de l'application"""
    # On récupère tous les roles utilisateurs possibles présents de la BDD
    roles = UserRole.query.all()

    # On affiche un menu de sélection du rôle pour le nouvel utilisateur et on récupère la sélection
    index = SelectionMenu.get_selection(
        [role.name for role in roles],
        title="Sélectionner un rôle d'utilisateur",
        show_exit_option=False,
    )

    print(f"Ajout d'un utilisateur appartenant au groupe {roles[index].name}")
    # On demande l'adresse e-mail
    email = input("Entrez votre addresse mail : ")
    # On demande le mot de passe
    password = getpass("Entrer le mot de passe utilisateur : ")
    confirm_password = getpass("Veuillez confirmer votre mot de passe : ")

    # On vérifie que les mots de passes tapées soient les mêmes
    if confirm_password == password:
        # On crée un nouvel utilisateur avec les champs renseignés et le role_id
        insert_user = User(
            email=email,
            password=generate_password_hash(password),
            role_id=roles[index].id,
        )
        # On l'ajoute à la BDD
        db.session.add(insert_user)
        # On confirme les changements de la transaction
        db.session.commit()
        print("Utilisateur ajouté !")
    else:
        print("Mot de passe non identique")
