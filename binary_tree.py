from typing import Self, Optional
from random import randint


class Tree:
    MAX: int = 0

    level: int
    valeur: int
    gauche: Optional[Self]
    droite: Optional[Self]

    def __init__(self, valeur: int, level: int):

        self.level = level + 1
        if self.level > Tree.MAX:
            Tree.MAX = self.level

        self.valeur = valeur
        self.gauche = None
        self.droite = None

    def __str__(self) -> str:
        place: dict = {}
        nombre: list[int] = [1]

        def traverse(emplacement, nombre):
            fils: str = ""
            valeur: str

            if emplacement.gauche:
                nombre[0] += 1
                fils += f"{emplacement.gauche.valeur} "
            if emplacement.droite:
                nombre[0] += 1
                fils += f"{emplacement.droite.valeur}"
            fils = fils.strip()
            valeur = f"{emplacement.valeur}({fils})"

            if place.get(emplacement.level):
                place[emplacement.level].append(valeur)
            else:
                place[emplacement.level] = [valeur]

            if emplacement.gauche:
                traverse(emplacement.gauche, nombre)
            if emplacement.droite:
                traverse(emplacement.droite, nombre)

        traverse(self, nombre)

        ligne: list[str] = []
        res: str = f"Profondeur de {Tree.MAX}"
        res += f" pour {nombre[0]} valeurs"
        for level in place:
            ligne.append(str(place[level]))

        largeur: int = max([len(contenu) for contenu in ligne])

        def ligne_horizontale(largeur) -> str:
            res: str = "\n+--"
            res += largeur * "-"
            res += "+"

            return res

        res += ligne_horizontale(largeur)
        for level in place:
            res += f"\n| {str(place[level]):^{largeur}} |"
        res += ligne_horizontale(largeur)

        return res


def reverse_tree(tree: Tree) -> Tree:
    copie: Tree = Tree(tree.valeur, tree.level-1)

    if tree.gauche:
        copie.droite = reverse_tree(tree.gauche)
    if tree.droite:
        copie.gauche = reverse_tree(tree.droite)

    return copie


def tri_binaire(pl_liste: list[int]) -> list[int]:

    def add_tree(valeur: int, emplacement: Tree) -> Tree:
        copie: Tree = emplacement

        if valeur > copie.valeur:
            if copie.droite is None:
                # print("Ajout a droite")
                copie.droite = Tree(valeur, copie.level)
            else:
                # print("Descendre a droite")
                copie.droite = add_tree(valeur, copie.droite)
        elif valeur < copie.valeur:
            if copie.gauche is None:
                # print("Ajout a gauche")
                copie.gauche = Tree(valeur, copie.level)
            else:
                # print("Descendre a gauche")
                copie.gauche = add_tree(valeur, copie.gauche)

        return emplacement

    def tree2list(tree: Tree, add_first: bool = True) -> list[int]:
        liste: list[int] = []

        if tree.gauche:
            liste.append(tree.gauche.valeur)
        if tree.droite:
            liste.append(tree.droite.valeur)

        if tree.gauche:
            liste.extend(tree2list(tree.gauche, False))
        if tree.droite:
            liste.extend(tree2list(tree.droite, False))

        return ([tree.valeur] if add_first else []) + liste

    def list2tree(pl_liste: list[int]) -> Tree:
        liste: list[int] = pl_liste[1:]

        valeur = pl_liste[0]
        root: Tree = Tree(valeur, 0)

        for valeur in liste:
            root = add_tree(valeur, root)

        return root

    def is_value_in_tree_rec(valeur: int, tree: Tree) -> bool:
        search: Tree = tree
        trouve: bool

        if valeur > search.valeur:
            if search.droite:
                trouve = is_value_in_tree(valeur, search.droite)
            else:
                trouve = False
        elif valeur < search.valeur:
            if search.gauche:
                trouve = is_value_in_tree(valeur, search.gauche)
            else:
                trouve = False
        else:
            trouve = True

        return trouve

    def is_value_in_tree(valeur: int, tree: Tree) -> bool:
        search: Tree = tree
        trouve: bool = False

        while not trouve:
            # print(f"check {valeur} with {search.valeur}")
            if valeur > search.valeur:
                if search.droite:
                    # print(f"(>{search.valeur})", end="")
                    search = search.droite
                else:
                    # print(f"#{valeur}# ", end="")
                    return False
            elif valeur < search.valeur:
                if search.gauche:
                    # print(f"(<{search.valeur})", end="")
                    search = search.gauche
                else:
                    # print(f"#{valeur}# ", end="")
                    return False
            else:
                # print(":", end="")
                trouve = True
        # print("return", trouve, " tree.valeur", tree.valeur)
        return trouve

    def main(pl_liste: list[int]) -> list[int]:

        root: Tree = list2tree(pl_liste)
        print(root, "\n")

        print("Valeurs in root: ", end="")
        for valeur in range(100):
            if is_value_in_tree(valeur, root):
                print(valeur, end=" ")
        print()

        liste: list[int] = tree2list(root)

        root = reverse_tree(root)
        print(root, "\n")

        print(tree2list(root))

        return liste

    return main(pl_liste)


if __name__ == "__main__":
    liste: list[int] 

    liste = [4, 2, 7, 1, 3, 6, 9]
    # liste = [randint(0, 99) for _ in range(40)]

    print(liste)
    liste = tri_binaire(liste)
