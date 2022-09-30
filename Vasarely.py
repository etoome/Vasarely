import os
import turtle
from math import cos, pi, sin

from PIL import Image

from deformation import deformation


def hexagone(point, longueur, col, centre, rayon):
    """
    Trace un hexagone déformé à une position donnée

    Entrées :
        point [(int, int, int)] : la valeur des trois coordonnées du point avant déformation où l’hexagone doit être peint
        longueur [int] : la distance (avant déformation) entre le centre et n’importe quel coin de l’hexagone
        col [(str, str, str)] : les trois couleurs qui vont être utilisées pour dessiner les hexagones
        centre [(int, int, int)] : le point qui donne le centre de la sphère de déformation
        rayon [int] : le rayon de la sphère de déformation

    Sorties :
        Affichage d'un hexagone déformé

    Variables :

          ++++++++++++++++++       |
         +  +             | +      |
        +    +            |  +     | hauteur_relative
       +      +           |   +    |
      +        +          |    +   |
     +          +++++++++++++++++  |
      +        +               +
       +      +               +
        +    +               +
         +  +               +
          ++++++++++++++++++

                          -------
                      largeur_relative
    """

    hauteur_relative = (sin(pi/3)*longueur)
    largeur_relative = (cos(pi/3)*longueur)

    turtle.hideturtle()
    turtle.tracer(0, 0)

    turtle.up()
    turtle.goto(deformation((point[0], point[1], 0), centre, rayon)[:2])
    turtle.down()

    # Pavé Nord-Est (en haut à droite)

    turtle.fillcolor(col[0])
    turtle.begin_fill()
    turtle.goto(deformation(
        (point[0] + longueur, point[1], 0), centre, rayon)[:2])
    turtle.goto(deformation((point[0] + (longueur - largeur_relative),
                point[1] + hauteur_relative, 0), centre, rayon)[:2])
    turtle.goto(deformation(
        (point[0] - largeur_relative, point[1] + hauteur_relative, 0), centre, rayon)[:2])
    turtle.end_fill()

    # Pavé Ouest (à gauche)

    turtle.fillcolor(col[1])
    turtle.begin_fill()
    turtle.goto(deformation(
        (point[0] - longueur, point[1], 0), centre, rayon)[:2])
    turtle.goto(deformation(
        (point[0] - largeur_relative, point[1] - hauteur_relative, 0), centre, rayon)[:2])
    turtle.goto(deformation((point[0], point[1], 0), centre, rayon)[:2])
    turtle.end_fill()

    # Pavé Sud-Est (en bas à droite)

    turtle.fillcolor(col[2])
    turtle.begin_fill()
    turtle.goto(deformation(
        (point[0] + longueur, point[1], 0), centre, rayon)[:2])
    turtle.goto(deformation((point[0] + (longueur - largeur_relative),
                point[1] - hauteur_relative, 0), centre, rayon)[:2])
    turtle.goto(deformation(
        (point[0] - largeur_relative, point[1] - hauteur_relative, 0), centre, rayon)[:2])
    turtle.end_fill()


def pavage(inf_gauche, sup_droit, longueur, col, centre, rayon):
    """
    La fonction pavage peint les hexagones déformés dont les centres, avant déformation,
    se trouvent dans la fenêtre (les bords inclus) avec l’hexagone en bas à gauche,
    avant déformation, centré sur le point (inf_gauche, inf_gauche).
    Pour cela, elle utilise la fonction hexagone.

    Entrées :
        inf_gauche [(int, int)] : coordonnées du bord inférieur gauche
        sup_droit [(int, int)] : coordonnées du bord supérieur droit
        longueur [int] : la distance (avant déformation) entre le centre et n’importe quel coin de l’hexagone
        col [(str, str, str)] : les trois couleurs qui vont être utilisées pour dessiner les hexagones
        centre [(int, int, int)] : le point qui donne le centre de la sphère de déformation
        rayon [int] : le rayon de la sphère de déformation

    Sorties :
        Affichage et sauvegarde de la génération dans un fichier 'pavage.eps'
    """

    WIDTH = HEIGHT = sup_droit-inf_gauche+(longueur*3)
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)

    decale = False
    for ligne in range(inf_gauche, sup_droit, int((sin(pi/3)*longueur))):
        if not decale:
            for colonne in range(inf_gauche, sup_droit, int(longueur*3)):
                hexagone((colonne, ligne), longueur, col, centre, rayon)

            decale = True
        else:
            for colonne in range(inf_gauche, sup_droit - longueur, int(longueur*3)):
                hexagone((colonne + (longueur*1.5), ligne),
                         longueur, col, centre, rayon)

            decale = False


def save():
    if not os.path.exists('exports'):
        os.makedirs('exports')

    file_name = f'exports/Vasarely_{inf_gauche}x{sup_droit}_l{longueur}_{col0}-{col1}-{col2}_r{rayon}'

    turtle.getcanvas().postscript(
        file=f'{file_name}.eps')
    turtle.done()

    pic = Image.open(f'{file_name}.eps')
    pic.load(scale=10)
    if pic.mode in ('P', '1'):
        pic = pic.convert("RGBA")
    ratio = min(1024 / pic.size[0],
                1024 / pic.size[1])
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

    pic = pic.resize(new_size, Image.ANTIALIAS)
    pic.save(f'{file_name}.png')

    os.remove(f'{file_name}.eps')


inf_gauche = int(input("Coordonnée du bord inférieur gauche : "))
sup_droit = int(input("Coordonnée du bord supérieur droit : "))
longueur = int(input("Longueur de l'hexagone : "))
col0 = input("Couleur 1 : ")
col1 = input("Couleur 2 : ")
col2 = input("Couleur 3 : ")
c_x = int(input("Coordonnée en x du centre de la sphère de déformation : "))
c_y = int(input("Coordonnée en y du centre de la sphère de déformation : "))
c_z = int(input("Coordonnée en z du centre de la sphère de déformation : "))
rayon = int(input("Rayon de la sphère de déformation : "))

pavage(inf_gauche, sup_droit, longueur,
       (col0, col1, col2), (c_x, c_y, c_z), rayon)
save()
