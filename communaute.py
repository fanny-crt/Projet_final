#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

# Camille Massimi et Fanny Courant
# lien github : https://github.com/fanny-crt/Projet_final.git

from projet_communaute import *
import sys
import time
import os

if __name__ == "__main__":

    if len(sys.argv) == 1:  # sys.argv: il faut mettre le nom du fichier
        print(f"Lors de vos recherches dans les archives, vous devez initialiser vos fichiers. Pour cela, il faut renseigner dans la ligne de commande : {sys.argv[0]} init nom_fichier_archive nom_fichier_citations")
        print(f"Si vous voulez déterminer la liste des auteurs cités par un auteur, il faut renseigner dans la ligne de commande : {sys.argv[0]} cite nom_auteur")
        print(f"Si vous souhaitez déterminer la liste pondérée des auteurs Bi influencés avec une profondeur d’au plus N par un auteur, il faut renseigner dans la ligne de commande : {sys.argv[0]} sont_influences nom_auteur profondeur")
        print(f"Pour déterminer la liste pondérée des auteurs Bi qui influencent l'auteur saisi avec une profondeur au plus N, il faut renseigner dans la ligne de commande : {sys.argv[0]} influence nom_auteur profondeur")
        print(f"Si vous préférez déterminer la communauté de l'auteur en fonction de la profondeur, il faut renseigner dans la ligne de commande : {sys.argv[0]} communautes nom_auteur profondeur")
        print(f"Pour tracer le graph d'un auteur avec ses influences et les auteurs qu'il influence en fonction de la profondeur, il faut renseigner dans la ligne de commande : {sys.argv[0]} graph nom_auteur profondeur.")
        print(f"Pour afficher un diagramme avec la proportion des occurences des auteurs cités par un auteur, il faut renseigner dans la ligne de commande : {sys.argv[0]} occurence nom_auteur.")
        print(f"pour montrer le pourcentage d'articles référencés d'un auteur donné par d'autres auteurs, il faut renseigner dans la ligne de commande : {sys.argv[0]} proportion nom_auteur")
        print("Les auteurs doivent être écris avec une majuscules pour les initiales du nom et prénom, et le reste en minuscules, et entre guillemets.")

    nom_fichier_auteur = "reference_auteur.csv"  # fichier avec l'auteur et ses articles
    fichier_ref = "articles_references.csv"  # article referencé par l'auteur
    fichier_qui_ref = "articles_qui_le_referencent.csv"  # articles qui reference l'auteur

    """
    1)
    Commande à saisir dans le terminal :  .\main.py init chemin\hep-th-abs.tar.gz chemin\hep-th-citations.tar.gz

    But : "Nettoyage" des données
    """
    if len(sys.argv) > 1:

        if sys.argv[1] == "init":  # sys.argv récupère ce qui est saisi dans la commande du terminal

            with Time() as t:  # context manager qui permet d'afficher le temps

                if len(sys.argv) == 4:

                    nom_fichier1 = sys.argv[2]
                    nom_fichier2 = sys.argv[3]

                    try:
                        # mouline les fichiers
                        F1 = Fichier_extrait(nom_fichier1)
                        try:
                            F1.creation_fichier(nom_fichier_auteur, ["Auteurs", "References articles"])
                        except OSError:
                            print(f"Le fichier {nom_fichier_auteur} existe déja et est ouvert.")
                    except OSError:
                        print(f"{sys.argv[2]} n'existe pas.")

                    try:
                        F2 = Fichier_reference(nom_fichier2)

                        try:
                            F2.creation_fichier(fichier_ref, ["Article", "Articles référencés"])
                            # articles_references: liste de tous les articles cités pour un article
                        except OSError:
                            print(f"Le fichier {fichier_ref} existe déjà et est ouvert.")

                        F3 = Fichier_reference2(nom_fichier2)

                        try:
                            F3.creation_fichier(fichier_qui_ref, ["Article", "Articles qui le référencent"])
                            # articles_qui_le_referencent : liste des articles qui référencent/citent l'article
                        except OSError:
                            print(f"Le fichier {fichier_qui_ref} existe déjà et est ouvert.")

                    except OSError:
                        print(f"{sys.argv[3]} n'existe pas.")

                else:
                    print(
                        f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 4 arguments : {sys.argv[0]} init nom_fichier_extrait nom_fichier_citations.")

                """
                2)
                Commande à saisir dans le terminal (exemple) : .\main.py cite "Michael Mueger"
                But : donner les auteurs cité par l'auteur
                """

        elif sys.argv[1] == "cite":

            with Time() as t:

                if len(sys.argv) == 3:

                    nom_auteur = sys.argv[2]

                    try:
                        a1 = Auteur(nom_auteur, fichier_ref, fichier_qui_ref)
                        a1.recherche_article(nom_fichier_auteur)

                        try:
                            a1.recherche_reference(fichier_ref)
                            a1.affiche_auteur(nom_fichier_auteur, 2)
                            print(f"{a1.nom} cite les auteurs : {a1.ref_auteur}")
                        except ListeVide:
                            print(f"{nom_auteur} ne cite aucun auteur.")
                    except PasReference:
                        print(f"{nom_auteur} n'est pas référencé dans les archives.")
                        print(f"Vérifiez l'orthographe et que la casse est bien respectée : majuscule au début des noms/prénoms/initiales et le reste en minuscule, et que le tout est entre guillemets. ")

                else:
                    print(
                        f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 3 arguments : {sys.argv[0]} cite nom_auteur.")

                """    
                3) 
                Commande à saisir dans le terminal (exemple): .\main.py sont_influences "Michael Mueger" 3
                But : Donner les auteurs qui sont influencés par l'auteur (avec profondeur)
                """

        elif sys.argv[1] == "sont_influences":

            with Time() as t:

                if len(sys.argv) == 4:
                    nom_auteur = sys.argv[2]

                    try:
                        profondeur = int(sys.argv[3])

                        a2 = Auteur(nom_auteur, fichier_ref, fichier_qui_ref, profondeur)
                        try:
                            a2.article_intensite(fichier_qui_ref, nom_fichier_auteur)
                            a2.affiche_dico_intensite(nom_fichier_auteur, 1)
                            print(f"Les influences de {a2.nom}, de profondeur {a2.profondeur}, sont : {a2.influence}")
                        except PasReference:
                            print(f"{a2.nom} n'est pas référencé dans les archives.")
                            print(
                                f"Vérifiez l'orthographe et que la casse est bien respectée : majuscule au début des noms/prénoms/initiales et le reste en minuscule, et que le tout est entre guillemets. ")
                        except ListeVide:
                            print(f"{a2.nom} n'influence aucun auteur.")
                    except ValueError:
                        print(f"{sys.argv[3]} n'est pas un entier. Veuillez saisir un entier.")

                else:
                    print(
                        f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 4 arguments : {sys.argv[0]} sont_influences nom_auteur profondeur.")

                """
                4) 
                Commande à saisir dans le terminal (exemple) : .\main.py influence "Michael Mueger" 3
                But : Donner les auteurs qui ont influencés l'auteur (avec profondeur)
                """

        elif sys.argv[1] == "influence":  # cite = influence de profondeur 1

            with Time() as t:

                if len(sys.argv) == 4:

                    nom_auteur = sys.argv[2]

                    try:
                        profondeur = int(sys.argv[3])

                        a3 = Auteur(nom_auteur, fichier_ref, fichier_qui_ref, profondeur)

                        try:
                            a3.article_intensite(fichier_ref, nom_fichier_auteur)
                            a3.affiche_dico_intensite(nom_fichier_auteur, 2)
                            print(
                                f"Les autheurs influencés par {a3.nom}, de profondeur {a3.profondeur}, sont : {a3.influence_par}")
                        except PasReference:
                            print(f"{a3.nom} n'est pas référencé dans les archives.")
                            print(
                                f"Vérifiez l'orthographe et que la casse est bien respectée : majuscule au début des noms/prénoms/initiales et le reste en minuscule, et que le tout est entre guillements. ")
                        except ListeVide:
                            print(f"{a3.nom} n'est influencé par aucun auteur.")
                    except ValueError:
                        print(f"{sys.argv[3]} n'est pas un entier. Veuillez saisir un entier.")

                else:
                    print(
                        f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 4 arguments : {sys.argv[0]} influence nom_auteur profondeur.")

                """
                5) 
                Commande à saisir dans le terminal (exemple) : .\main.py communautes "Michael Mueger" 3
                But : Donner la communaute de profondeur N de l'auteur
                """

        elif sys.argv[1] == "communautes":

            with Time() as t:

                if len(sys.argv) == 4:

                    nom_auteur = sys.argv[2]

                    try:
                        profondeur = int(sys.argv[3])

                        a4 = Auteur(nom_auteur, fichier_ref, fichier_qui_ref, profondeur)
                        try:
                            a4.article_intensite(fichier_ref, nom_fichier_auteur)
                            a4.affiche_dico_intensite(nom_fichier_auteur, 2)
                            a4.article_intensite(fichier_qui_ref, nom_fichier_auteur)
                            a4.affiche_dico_intensite(nom_fichier_auteur, 1)
                            a4.communautes()
                            print(
                                f"La communauté scientifique de {a4.nom}, de profondeur {a4.profondeur}, est : {a4.communaute}")
                        except PasReference:
                            print(f"{a4.nom} n'est pas référencé dans les archives.")
                            print(
                                f"Vérifiez l'orthographe et que la casse est bien respectée : majuscule au début des noms/prénoms/initiales et le reste en minuscule. ")
                        except ListeVide:
                            print(f"{a4.nom} n'a pas de communauté scientifique.")
                    except ValueError:
                        print(f"{sys.argv[3]} n'est pas un entier. Veuillez saisir un entier.")

                else:
                    print(f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 4 arguments : {sys.argv[0]} communautes nom_auteur profondeur. ")

                """
                6) 
                Commande à saisir dans le terminal (exemple) : ./main.py graph "Michael Mueger" 1 
                But: représenter un graphe orienté de la communauté d'un auteur, et également de ces influences et des auteurs qu'il influence
                """

        elif sys.argv[1] == "graph":

            with Time() as t:

                if len(sys.argv) == 4:

                    nom_auteur = sys.argv[2]

                    try:
                        profondeur = int(sys.argv[3])

                        g1 = Graphe(nom_auteur, fichier_ref, fichier_qui_ref, nom_fichier_auteur, profondeur)
                        g1.add_influence_communaute(fichier_ref, nom_fichier_auteur)
                        g1.add_influence_communaute(fichier_qui_ref, nom_fichier_auteur)
                        # g1.add_communautes()
                        g1.trace()
                    except ValueError:
                        print(f"{sys.argv[3]} n'est pas un entier. Veuillez saisir un entier.")

                else:
                    print(f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 4 arguments : {sys.argv[0]} graph nom_auteur profondeur.")

                """
                7) 
                Commande à saisir dans le terminal : ./main.py occurence "Michael Mueger"
                But : afficher visuellement des auteurs qui sont le plus cité
                """

        elif sys.argv[1] == "occurence":

            with Time() as t:

                if len(sys.argv) == 3:

                    nom_auteur = sys.argv[2]
                    try :
                       a6= Auteur(nom_auteur, fichier_ref, fichier_qui_ref)
                       a6.recherche_article(nom_fichier_auteur)
                       a6.recherche_reference(fichier_ref)
                       a6.occurence(nom_fichier_auteur)
                    except ListeVide:
                        print(f"{nom_auteur} n'est pas référencé dans les archives.")
                        print(f"Vérifiez l'orthographe et que la casse est bien respectée : majuscule au début des noms/prénoms/initiales et le reste en minuscule, et que le tout est entre guillemets. ")
                else:
                    print(f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 3 arguments : {sys.argv[0]} occurence nom_auteur.")

                """
                8)
                Commande à saisir dans le terminal : ./main.py proportion "Michael Mueger" 
                But : affiche visuellement la propotion d'articles qui sont référencés, par d'autres auteurs, de l'auteur
                """
        elif sys.argv[1] == "proportion":

            with Time() as t:
                if len(sys.argv) == 3:
                    nom_auteur = sys.argv[2]
                    try:
                        a7 = Auteur(nom_auteur, fichier_ref, fichier_qui_ref)
                        a7.recherche_article(nom_fichier_auteur)
                        a7.proportion_ref(fichier_qui_ref)
                    except ListeVide:
                        print(f"{nom_auteur} n'est pas référencé dans les archives.")
                        print(f"Vérifiez l'orthographe et que la casse est bien respectée : majuscule au début des noms/prénoms/initiales et le reste en minuscule, et que le tout est entre guillemets. ")
                else:
                    print(f"Le nombre d'arguments saisi sur la ligne de commande est incorrecte. Il faut saisir 3 arguments : {sys.argv[0]} proportion nom_auteur.")

        else:
            print(f"{sys.argv[1]} saisi n'est pas une option de l'application. Vérifiez l'orthographe.")
            print(f"Les applications possibles sont :")
            print("- init: pour initialiser vos fichiers, il faut également saisir dans la ligne de commande le nom du fichier des archives en 3ème argument et le nom du fichier des citations en 4ème argument.")
            print("- cite : pour déterminer la liste des auteurs cités par un auteur, il faut également saisir dans la ligne de commande le nom de l'auteur en 3ème argument")
            print("- sont_influences : pour déterminer la liste pondérée des auteurs Bi influencés avec une profondeur d’au plus N par un auteur, il faut également saisir dans la ligne de commande le nom de l'auteur en 3ème argument et la profondeur en 4ème argument")
            print("- influence : pour déterminer la liste pondérée des auteurs Bi qui influencent l'auteur saisi avec une profondeur au plus N, il faut également saisir dans la ligne de commande le nom de l'auteur en 3ème argument et la profondeur en 4ème argument")
            print("- communautes : pour déterminer la communauté de l'auteur en fonction de la profondeur, il faut également saisir dans la ligne de commande le nom de l'auteur en 3ème argument et la profondeur en 4ème argument")
            print("- graph : pour tracer le graph d'un auteur avec ses influences et les auteurs qu'il influence en fonction de la profondeur, il faut également saisir dans la ligne de commande le nom de l'auteur en 3ème argument et la profondeur en 4ème argument")
            print("- occurence : pour afficher un diagramme avec la proportion des occurences des auteurs cités par un auteur, il faut également renseigner dans la ligne de commande le nom de l'auteur en 4ème argument")
            print("- proportion : pour montrer le pourcentage d'articles référencés d'un auteur donné par d'autres auteurs, il faut également renseigner dans la ligne de commande le nom de l'auteur en 4ème argument")