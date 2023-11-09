from typing import Self, Optional


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

        def traverse(emplacement):
            if place.get(emplacement.level):
                place[emplacement.level].append(emplacement.valeur)
            else:
                place[emplacement.level] = [emplacement.valeur]

            if emplacement.gauche:
                traverse(emplacement.gauche)
            if emplacement.droite:
                traverse(emplacement.droite)

        traverse(self)
        longueur: int = 3 * max([len(place[idx]) for idx in place])

        res: str = ""
        for level in place:
            res += f"\n| {str(place[level]):^{longueur}} |"
        return res[1:]


def reverse_tree(tree: Tree) -> Tree:
    copie: Tree = Tree(tree.valeur, tree.level)

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
        else:
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

    def main(pl_liste: list[int]) -> list[int]:

        root: Tree = list2tree(pl_liste)
        print("depth:", Tree.MAX)
        print(root, "\n")

        liste: list[int] = tree2list(root)

        root = reverse_tree(root)
        print(root, "\n")

        print(tree2list(root))

        return liste

    return main(pl_liste)


if __name__ == "__main__":
    liste: list[int] 

    liste = [4, 2, 7, 1, 3, 6, 9]
    init = liste.copy()
    # liste = [5, 7, 3, 4, 6, 8, 9]

    print(liste)
    liste = tri_binaire(liste)

    assert "-".join(str(liste)) == "-".join(str(init))
