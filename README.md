# Réalisation d'une modélisation des communautés et des influences des scientifiques

L'objectif de ce projet est de concevoir une application qui indique les influences ou les communautés d'un auteur, et également de les représenter graphiqumement.
Tout d'abord, l'auteur A est une influence de l'auteur B, si l'auteur B cite un article de l'auteur A et l'auteur B est influencé par l'auteur A.
De plus, l'auteur C est une influence de l'auteur B de profondeur 2, si l'auteur C cite un article de l'auteur A. On dit alors que l'auteur C a une influence d'intensité 1/2 sur l'auteur B. 
En effet, l'intensité est égale à la somme des inverses des profondeurs.
Cette application objet détermine également les communautés d'un auteur. L'auteur D appartient à la communauté de l'auteur A de profondeur 1, si l'auteur A influence l'auteur D avec une profondeur 1,
et l'auteur D influence l'auteur A avec une profondeur 1.

Pour réaliser ce projet, on disposait d'une archive recensant les extraits d'articles de 29 000 auteurs (hep-th-abs.tar.gz) où chaque article possède un numéro de référence et un fichier
qui indiquait quelle article citait quelle article (hep-th-citations.tar.gz). 

Nous avons tout d'abord trier les données de ces fichiers pour en ressortir 3 fichiers CSV:
- le premier indiquait le nom de l'auteur et ses références d'articles, 
- le deuxièmre indiquait les références d'articles avec les articles qu'ils citaient,
- le troisième indiquait les références d'articles avec les articles qui les citaient

Puis, nous avons créer une classe Auteur qui permet de déterminer les influences et les communautés d'un auteur donné, en fonction de sa profondeur. On obtient 
un dictionnaire qui contient les influences de l'auteur donné avec leur intensité, et une liste contenant la communauté de l'auteur. 

Pour illustrer ces résultats, nous avons réaliser un graph orienté qui indique la communauté de l'auteur, et un diagramme circulaire indiquant en proportion le nombre de fois où les auteurs sont cités. 
