from typing import Self


class FunctionCallException(Exception):
    pass


class Vars:
    data: dict = dict()
    result: object
    fonction: str = ""

    @classmethod
    def nom_classe(cls, classe):
        if classe.__class__.__name__ == "UnionType":
            return f"{'|'.join([c.__name__ for c in classe.__args__])}"

        return classe.__name__

    @classmethod
    def definition(cls, nom_fonction):
        defstr: str = f"def {nom_fonction}("
        defstr += ", ".join([f"{p}: {cls.nom_classe(t)}" for p, t in reversed(cls.data[nom_fonction]["liste"])])
        defstr += ")"
        return defstr


# Decorateur de recuperation des parametres
def def_param(*params):

    def get_params(fonction):
        if fonction.__name__ != "wrapper":
            Vars.fonction = fonction.__name__

        if params[0] == "=":
            Vars.data[Vars.fonction] = {}
            Vars.data[Vars.fonction]["liste"] = list()
            Vars.data[Vars.fonction]["result"] = params[1]
        else:
            Vars.data[Vars.fonction]["liste"].append(params)

        def wrapper(*args, **kwargs):
            try:
                return fonction(*args, **kwargs)

            except Exception as error:
                print(f"Def {Vars.fonction}():", error)

        return wrapper
    return get_params


# decorateur de test des parametres utilises
def check_error(nom_fonction):
    def decorateur(fonction):
        def wrapper(*args, **kwargs):
            try:
                nb_params = len(args)
                nb_defs = len(Vars.data[nom_fonction]["liste"])
                if nb_params != nb_defs:
                    raise Exception(f"Le nombre de parametres ({nb_params}) n'est pas correct ({nb_defs} attendu).")

                for index, param in enumerate(reversed(Vars.data[nom_fonction]["liste"])):
                    if param[1].__class__.__name__ == "type" and not isinstance(args[index], param[1]):
                        raise TypeError(f"Le parametre {param[0]!r} n'est pas de type {param[1].__name__} ({args[index].__class__.__name__}: {args[index]!r}).")
                    elif param[1].__class__.__name__ == "UnionType" and not isinstance(args[index], param[1]):
                        raise TypeError(f"Le parametre {param[0]!r} n'est pas de type {'|'.join([c.__name__ for c in param[1].__args__])} ({args[index].__class__.__name__}: {args[index]!r}).")

                result = fonction(*args, **kwargs)
                if not isinstance(result, Vars.data[nom_fonction]["result"]):
                    raise TypeError(f"Le resultat {result.__class__.__name__}:{result!r} n'est pas de type {Vars.nom_classe(Vars.data[nom_fonction]['result'])}.")

                return result

            except Exception as error:
                return f"{Vars.definition(nom_fonction)}: {error}"
                raise FunctionCallException(f"{Vars.definition(nom_fonction)}: {error}") from error

        return wrapper
    return decorateur


class Chaine:
    valeur: str

    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return self.valeur


class Nombre:
    def __init__(self, valeur):
        self.valeur = valeur

    @check_error("addition")
    @def_param("self", Self)
    @def_param("nombre", int)
    @def_param("=", int)
    def addition(self, valeur):
        return self.valeur + valeur


n = Nombre(3)
print(n.addition())
print(n.addition("4"))
print(n.addition(4))
exit()


@check_error("concat")
@def_param("c1", Chaine | None)
@def_param("c2", Chaine)
@def_param("=", Chaine)
def concat(a: Chaine, b: Chaine):
    if not a:
        return f"{b}"
    return Chaine(f"{a} {b}")


@check_error("multipli")
@def_param("n1", int)
@def_param("n2", int)
@def_param("=", int)
def multipli(a, b):
    if a == 0:
        return "Zero"
    return (a * b)


@check_error("somme")
@def_param("i1", int)
@def_param("i2", int)
@def_param("=", int)
def somme(a, b):
    if a == 0:
        return "Zero"
    return (a + b)


def main():
    print(somme(1, 2, 3))
    print(somme(3, "4"))
    print(somme(0, 8))
    print(somme(6, 8))

    print(multipli(1, 2, 3))
    print(multipli(3))
    print(multipli(3, "4"))
    print(multipli(0, 8))
    print(multipli(4, 8))

    print(concat(1, Chaine('suite')))
    print(concat(Chaine("Une"), 'suite'))
    print(concat(None, Chaine('suite')))
    print(concat(Chaine("Une"), None))
    print(concat(Chaine("Une"), Chaine('suite')))


if __name__ == '__main__':
    main()
