#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

# Camille Massimi et Fanny Courant
# lien github : https://github.com/fanny-crt/Projet_final.git

import gzip
from collections import defaultdict
import csv
import re
from pylatexenc.latex2text import LatexNodes2Text
import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import Counter



class Tri:

    def creation_fichier(self, nom_fichier, nom_en_tete):
        with open(nom_fichier, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(nom_en_tete)
            for key, value in self.dico.items():
                writer.writerow([key, value])

    def lecture_fichier(self, nom_fichier):
        with open(nom_fichier, "r", encoding="utf-8") as f:
            for line in f:
                print(line)


class Fichier_extrait(Tri):

    def __init__(self, fichier_extrait):
        self.dico = defaultdict(list)
        ## V7  Nettoyage des cas particulier (Jr/Jr. / pages / & / ) temps 25-30sec
        # ne corrige pas les (S.J.Gates / S.J.Gates Jr / S.James Gates Jr...)
        with gzip.open(fichier_extrait, 'rt', encoding="utf-8") as f:
            Ref = []  # liste contenant toutes les references des articles donnés
            Auteur = []  # liste contenant les auteurs
            i = 0
            for line in f:
                if "Paper: hep-th/" in line:
                    l = line.split("hep-th/")  # recupere la valeur apres le separateur "hep-th/"
                    # print(l)
                    reference = l[1].strip('\n')  # l[0]="Paper :" et l[1]=ref de l'article
                    if reference == '':  # si la valeur est manquante
                        Ref.append("NR")  # non renseigné
                    else:
                        Ref.append(reference)
                if "Authors:" in line or "Author:" in line:
                    ensembleauteurs = []
                    i = 1
                    l = line.split(":")
                    auteur_s = l[1].lstrip().strip('\n')  # supprime espace avant le nom et le \n
                    ensembleauteurs.append(auteur_s)
                if line.startswith("Comments:") or line.startswith("Comment:") or line.startswith(
                        "\\") and i == 1:  # pour ne pas recuperer les lignes qui ne sont pas dans authors
                    i = 0
                    if len(ensembleauteurs) != 0:
                        pourconv = " ".join(ensembleauteurs)
                        ## en LaTex "~" c'est pour forcer un espace
                        ## il faut les enlever avant la convertion text sinon pb quand on recupere dans liste à la fin
                        n0 = pourconv.replace(".~", "")
                        n0bis = n0.replace(" & ", ",")  # cas des " & " (ex:9504076,9512106...environ 20)
                        combiner = LatexNodes2Text().latex_to_text(n0bis)
                        n1 = combiner.replace(", and ", ',')
                        n2 = n1.replace(" and ", ',')
                        n3 = n2.replace("., ", "")
                        # n3bis= cas particulier article 9401052
                        n3bis = re.sub(r'\(\([^)]*\)[^)]*\([^)]*\)[^)]*\([^)]*\)[^)]*\([^)]*\)[^)]*\)', '', n3)
                        # n3ter = cas particulier artible 9604145
                        n3ter = re.sub(r'\(\([^)]*\)[^)]*\([^)]*\)[^)]*\([^)]*\)[^)]*\)', '', n3bis)
                        # n3quater = cas article 9612243
                        n3quater = re.sub(r'\(\([^)]*\)[^)]*\([^)]*\)[^)]*\)', '', n3ter)
                        # n3six = cas article 9501108
                        n3six = re.sub(r' \([^)]*\) ', ',', n3quater)
                        n4 = re.sub(r'\([^)]*\)', '', n3six)  # supprime les données entre parenthèse (bla)
                        # n4 = re.sub(r'\([^)]*\)', '', n3)  # supprime les données entre parenthèse
                        n5 = n4.strip()
                        n6 = n5.replace(". ", ".")  # evite d'avoir des "M. T." différent "M.T."
                        n7 = n6.replace(", ", ",")
                        n8 = n7.replace(" ,", ",")
                        n9 = n8.title()  # majuscule debut mot
                        grp_auteurs = n9.split(",")
                    Auteur.append(grp_auteurs)
                if line.startswith(" ") and i == 1:  # recupere uniquement les lignes apres authors
                    l = line.splitlines()
                    auteur_s = l[0].lstrip()
                    ensembleauteurs.append(auteur_s)
        # print(len(Ref))
        # print(len(Auteur))
        # print(f"L'auteur de l'article {Ref[13971]} est {Auteur[13971]}")
        for i in range(len(Ref)):
            lA = len(Auteur[i])
            for j in range(0, lA):
                self.dico[Auteur[i][j]].append(Ref[i])
        # print(len(self.dico.items()))  # len(self.dico.items())=13167
        # print(self.dico.items())  # len(self.dico.items())=apres avoir modifier avec tableau !


class Fichier_reference(Tri):

    def __init__(self, fichier_reference):
        self.dico = defaultdict(list)

        with gzip.open(fichier_reference, 'rt', encoding='utf-8') as f:
            for line in f:
                l = line.split()
                if len(l) == 2:
                    self.dico[l[0]].append(l[
                                               1])  # dictionnaire avec un numéro d'article en clé et tous les numéros d'articles qu'il référence
        # print(self.dico.items())


class Fichier_reference2(Tri):

    def __init__(self, fichier_reference):
        self.dico = defaultdict(list)
        with gzip.open(fichier_reference, 'rt', encoding="utf-8") as f:
            for line in f:
                l = line.split()
                if len(l) == 2:
                    self.dico[l[1]].append(l[
                                               0])  # dictionnaire avec un numéro d'article en clé et tous les numéros d'articles qui référencent cet article
        # print(self.dico.items())


class Auteur():
    def __init__(self, nom, fichier_ref, fichier_qui_ref, profondeur=1):
        self.nom = nom
        self.fichier_ref = fichier_ref
        self.fichier_qui_ref = fichier_qui_ref
        self.profondeur = profondeur  # par défaut 1 si non renseigné
        self.article = []  # references des  articles ecrit par l'auteur
        self.cite = []  # liste des auteurs cité par l'auteur
        self.article_qui_reference = []  # articles qui reference l'auteur
        self.article_reference = []  # article referencé par l'auteur
        self.intensite_qui_ref = defaultdict(float)
        self.intensite_ref = defaultdict(float)
        self.influence_par = defaultdict(float)  # les auteurs qui influencent l'auteur
        self.influence = defaultdict(float)  # auteurs influencé par l'auteur
        self.communaute = []

    def recherche_article(self, nom_fichier):
        """
        But : cherche les references des articles ecrit par l'auteur
        Parametre : fichier csv
        Fichier utilise : "reference_auteur.csv"
        "Sort" : self.article
        """
        with open(nom_fichier, "r", newline='', encoding="utf-8") as f:
            r = csv.reader(f, delimiter=",")  # permet de lire un fichier csv
            next(r)  # passer l'en-tête
            i = 0
            self.article = []
            for ligne in r:
                if self.nom == ligne[0]:
                    i = 1
                    # print(ligne[1])
                    l = ligne[1].rstrip("]").lstrip("[")  # pour supprimer les crochets
                    l = l.split(",")  # séparer la ligne où il y a les virgules
                    for article in l:
                        # print(article)
                        article = article.rstrip().lstrip()  # enleve les espaces avant et après les données
                        article = article.rstrip("'").lstrip("'")
                        self.article.append(article)
                    break  # permet de sortir de la boucle for une fois les références de ces articles trouvés
            if i == 0:  # l'article n'est pas référencé dans les archives donc on génère une exception
                raise PasReference()

    def recherche_reference(self, nom_fichier):
        """
        But : cherche les articles qui influence l'auteur ou les articles influencés par l'auteur
        Paramtre : fichier csv
        Fichier utilise : "articles_references.csv" pour avoir les articles qui influence l'auteur
                          "articles_qui_le_referencent.csv" pour avoir les articles influencé par l'auteur
        "Sort" : self.article_reference ou self.article_qui_reference
        """
        with open(nom_fichier, "r", newline='', encoding='utf-8') as f:
            r = csv.reader(f, delimiter=',')
            next(r)  # permet de passer l'en-tête
            self.article_qui_reference = []
            self.article_reference = []
            for ligne in r:
                for article in self.article:
                    if ligne[0] in article:
                        l = ligne[1].rstrip("]").lstrip("[")  # pour supprimer les crochets
                        l = l.split(",")
                        articles_cites = []
                        for ref in l:
                            ref = ref.rstrip().lstrip()
                            ref = ref.rstrip("'").lstrip("'")
                            articles_cites.append(ref)
                        for article in articles_cites:
                            if nom_fichier == self.fichier_ref:
                                if article not in self.article_reference:
                                    self.article_reference.append(article)
                            else:
                                if article not in self.article_qui_reference:
                                    self.article_qui_reference.append(article)
                        break  # sort de la boucle for, une fois la ligne avec l'article trouvé dans le fichier csv
        if nom_fichier == self.fichier_ref:
            if len(self.article_reference) == 0:  # liste vide : aucun article référencé
                raise ListeVide()
        else:
            if len(self.article_qui_reference) == 0:  # liste vide : aucun article référencé
                raise ListeVide()

    def affiche_auteur(self, nom_fichier, sens):
        """
        But : afficher les auteurs en fonction des references de leurs articles
        Parametre : fichier cvs
                    sens :  1 = c'est l'auteur qui influence / 2 = il est influence par
        Fichier utilisé : "reference_auteur.cvs"
        "Sort" : self.ref_auteur (liste qui sort les auteurs des articles référencés par l'auteur)
                ou self.qui_ref_auteur (liste qui sort les auteurs des articles qui réferencent l'auteur)
        """
        self.ref_auteur = []
        self.qui_ref_auteur = []
        with open(nom_fichier, "r", newline='', encoding='utf-8') as f:
            r = csv.reader(f, delimiter=",")
            next(r)  # passer l'en-tête
            if sens == 2:
                for ligne in r:
                    for a in self.article_reference:
                        if a in ligne[1]:
                            if ligne[0] not in self.ref_auteur and ligne[0] != self.nom:
                                self.ref_auteur.append(ligne[0])
            else:
                for ligne in r:
                    for a in self.article_qui_reference:
                        if a in ligne[1]:
                            if ligne[0] not in self.qui_ref_auteur and ligne[0] != self.nom:
                                self.qui_ref_auteur.append(ligne[0])

    def article_intensite(self, nom_fichier2, fichier1):
        """
        But : cherche les articles avec profondeur et leurs intensités
        Parametre : fichier csv
        Fichier utilisé : nom_fichier : "articles_references.csv" pour avoir les articles qui influence l'auteur
                                        "articles_qui_le_referencent.csv" pour avoir les articles influencé par l'auteur
                          fichier1 : "reference_auteur.csv"
        "Sort" : self.intensite_ref ou self.intensite_qui_ref
        Commentaires : commentaire 1 : pour pouvoir enchainer a la suite cette fonction sur les 2 fichiers differents
                                       sans avoir de probleme (pour communautes)
        """
        self.recherche_article(fichier1)  # voir commentaire 1
        articles_auteur = self.article
        if nom_fichier2 == self.fichier_ref:
            for i in range(self.profondeur):
                self.recherche_reference(nom_fichier2)
                self.article = self.article_reference
                for a in self.article_reference:
                    if a not in articles_auteur:
                        self.intensite_ref[a] += 1 / (i + 1)
        else:
            for i in range(self.profondeur):
                self.recherche_reference(nom_fichier2)
                self.article = self.article_qui_reference
                for a in self.article_qui_reference:
                    if a not in articles_auteur:
                        self.intensite_qui_ref[a] += 1 / (i + 1)

    def affiche_dico_intensite(self, nom_fichier, sens):
        """
        But : afficher les influences de l'auteur ou les auteurs qu'il influence AVEC profondeur
        Parametre : fichier csv
                    sens :  1 = c'est l'auteur qui influence / 2 = il est influence par
        Fichier utilise : "articles_references.csv" pour avoir les articles qui influence l'auteur
                          "articles_qui_le_referencent.csv" pour avoir les articles influencé par l'auteur
        "Sort" : self.influence ou self.influence_par
        """
        with open(nom_fichier, "r", newline='', encoding="utf-8") as f:
            r = csv.reader(f, delimiter=",")
            next(r)  # passer l'en-tête
            if sens == 1:
                for ligne in r:
                    for article in self.intensite_qui_ref.keys():
                        if article in ligne[1]:
                            self.influence[ligne[0]] += self.intensite_qui_ref[article]
            else:
                for ligne in r:
                    for article in self.intensite_ref.keys():
                        if article in ligne[1]:
                            self.influence_par[ligne[0]] += self.intensite_ref[article]

    def communautes(self):
        """
        But : Cherche la communaute de l'auteur de profondeur N
        Remarque : nécessite d'avoir self.influence et self.influence_par
        "Sort" : self.communaute
        """
        for c in self.influence:
            for k in self.influence_par:
                if c == k:
                    self.communaute.append(c)
                else:
                    pass

    def occurence(self,fichier):
        """
        But : sort un diagramme circulaire proportionnel au nb de fois où sont cité les auteurs
        Parametres : fichier = "reference_auteur.cvs"
        """
        self.ref2_auteur = [] #sort la liste des auteurs autant de fois que cite (si A est cité 4 fois il apparait 4 fois)
        with open(fichier, "r", newline='', encoding='utf-8') as f:
            r = csv.reader(f, delimiter=",")
            next(r)  # passer l'en-tête
            for ligne in r:
                for a in self.article_reference:
                    if a in ligne[1]:
                        if ligne[0] != self.nom:
                            self.ref2_auteur.append(ligne[0])
        occu = Counter(self.ref2_auteur).most_common() #compte les occurences des auteurs cité
        noms=[]
        nb=[]
        for i in range(len(occu)):
            noms.append(occu[i][0])
            nb.append(occu[i][1])
        plt.pie(nb, labels=noms, autopct='%1.f%%', startangle=90)
        plt.axis('equal')
        plt.title(f"Influence des auteurs sur : {self.nom}")
        plt.show()

    def proportion_ref(self,fichier):
        """
        But : montrer le pourcentage d'articles référencés par d'autres auteurs
        fichier : utiliser "articles_qui_le_referencent.csv" pour avoir les articles influencé par l'auteur
        """
        ref=0
        taille=[]
        with open(fichier, "r", newline='', encoding='utf-8') as f:
            r = csv.reader(f, delimiter=',')
            next(r)  # permet de passer l'en-tête
            for ligne in r:
                for article in self.article:
                    if ligne[0] in article:
                        ref+=1
                    else :
                        pass
        total = len(self.article)
        non_ref = total - ref
        etat = "Référencé", "Non référencé"
        taille.append(ref)
        taille.append(non_ref)
        plt.pie(taille, labels=etat, autopct='%1.f%%')
        my_circle = plt.Circle((0, 0), 0.7, color="white")
        p = plt.gcf()
        p.gca().add_artist(my_circle)
        plt.title(f"Proportion des articles de {self.nom} référencés par d'autres auteurs")
        plt.show()


class Graphe(Auteur):
    """
    But: représenter un graphe orienté de la communauté d'un auteur, et également de ces influences et des auteurs qu'il influence
    Remarque : le sens de la flèche auteur 1 -> auteur 2 signifique que l'auteur 1 influence l'auteur 2
    """

    def __init__(self, nom, fichier_ref, fichier_qui_ref, nom_fichier_auteur, profondeur=1):
        super().__init__(nom, fichier_ref, fichier_qui_ref, profondeur)
        self.nom_fichier_auteur = nom_fichier_auteur
        self.G = nx.MultiDiGraph()

    def add_influence_communaute(self, nom_fichier, fichier_auteur_reference):
        """
        But : ajouter des arretes dans self.G.edges afin d'afficher un graph orienté avec les auteurs influencés ou qui influencent un auteur donné
        Parametre : fichier csv nom_fichier = fichier_qui_ref(pour avoir les influences) ou fichier_ref(pour avoir les auteurs qu'ils influencent) en fonction de l'objectif
                                fichier_auteur_reference
        "Sort" : self.G.edges
        Remarque : le sens de la flèche auteur 1 -> auteur 2 signifique que l'auteur 1 influence l'auteur 2
                   Ce graph est intéressant seulement pour la profondeur 1, car pour les profondeurs>1, le graph devient illisible
        """
        nom = self.nom
        if nom_fichier == self.fichier_ref:  # cas où l'on cherche les influences de l'auteur donné
            liste_auteurs = []
            i = 1
            # profondeur 1
            super().recherche_article(fichier_auteur_reference)  # recherche des articles de l'auteur donné
            super().recherche_reference(nom_fichier)  # recherche des articles qu'il référence
            self.article = self.article_reference  # pour super().recherche_reference (on utilise self.article)
            super().affiche_auteur(self.nom_fichier_auteur,
                                   2)  # on détermine les auteurs cités par l'auteur donné de profondeur 1 : self.ref_auteur
            for auteur in self.ref_auteur:
                if self.nom != auteur:
                    self.G.add_edge(auteur, self.nom)  # on ajoute les arrêtes
                    liste_auteurs.append(auteur)  # liste des auteurs qui influencent l'auteur donné
            # profondeur >1
            while i < self.profondeur:
                super().recherche_reference(nom_fichier)
                self.article = self.article_reference
                liste = []
                for auteur in liste_auteurs:  # on regarde pour auteur, les auteurs qu'il cite
                    self.nom = auteur
                    self.ref_auteur = []
                    super().affiche_auteur(self.nom_fichier_auteur, 2)
                    for a in self.ref_auteur:
                        if auteur != a:
                            self.G.add_edge(a, auteur)  # on ajoute les arrêtes
                            if a not in liste and a != nom:
                                liste.append(a)
                liste_auteurs = liste
                i += 1
        self.nom = nom
        if nom_fichier == self.fichier_qui_ref:  # cas où l'on cherche les auteurs qui sont influencés par l'auteur donné
            liste_auteurs = []
            i = 1
            super().recherche_article(fichier_auteur_reference)
            super().recherche_reference(nom_fichier)
            self.article = self.article_qui_reference
            super().affiche_auteur(self.nom_fichier_auteur,
                                   1)  # on détermine les auteurs qui citent l'auteur donné de profondeur 1 : self.qui_ref_auteur
            for auteur in self.qui_ref_auteur:
                if self.nom != auteur:
                    self.G.add_edge(self.nom, auteur)
                    liste_auteurs.append(auteur)
            while i < self.profondeur:
                super().recherche_reference(nom_fichier)
                self.article = self.article_qui_reference
                liste = []
                for auteur in liste_auteurs:
                    self.nom = auteur
                    self.qui_ref_auteur = []
                    super().affiche_auteur(self.nom_fichier_auteur, 1)
                    for a in self.qui_ref_auteur:
                        if auteur != a:
                            self.G.add_edge(auteur, a)
                            if a not in liste and a != nom:
                                liste.append(a)
                liste_auteurs = liste
                i += 1

    def add_communautes(self):
        """
        But : ajouter des arretes dans self.G.edges afin d'afficher la communauté d'un auteur donné et de la profondeur donné
        "Sort" : self.G.edges
        """
        super().article_intensite(self.fichier_ref, self.nom_fichier_auteur)
        super().affiche_dico_intensite(self.nom_fichier_auteur, 2)
        super().article_intensite(self.fichier_qui_ref, self.nom_fichier_auteur)
        super().affiche_dico_intensite(self.nom_fichier_auteur, 1)
        super().communautes()
        for auteur in self.communaute:
            self.G.add_edges_from([(auteur, self.nom), (self.nom, auteur)])

    def trace(self):  # affiche le graph
        nx.draw(self.G, pos=nx.circular_layout(self.G), with_labels=True)
        plt.show()


class PasReference(Exception):
    pass


class ListeVide(Exception):
    pass


class Time:

    def __enter__(self):
        self.debut = time.time()

    def __exit__(self, type, value, traceback):
        self.fin = time.time() - self.debut
        print(f"Le temps d'exécution est {self.fin}.")