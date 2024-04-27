class MesVariables:
    valeurs: dict = {}

    @classmethod
    def getvalue(cls, *args):
        if type(args[0]) is tuple:
            result: tuple = tuple()
            for arg in args[0]:
                if arg not in cls.valeurs:
                    raise KeyError(f"Variable: {arg!r} inexistante.")
                result += (cls.valeurs.get(arg), )
            return result

        if args[0] not in cls.valeurs:
            raise KeyError(f"Variable: {args[0]!r} inexistante.")

        return cls.valeurs.get(args[0])

    @classmethod
    def __call__(cls, *args):
        if len(args) == 0:
            return cls.valeurs
        else:
            return cls.getvalue(args)

    @classmethod
    def __getitem__(cls, *args):
        # print("^", args)
        return cls.getvalue(*args)

    @classmethod
    def __setitem__(cls, *args):
        # print("v", args)
        if type(args[0]) in (list, tuple):
            nb_params = len(args[0])
            nb_valeurs = len(args[1])
            if nb_params != nb_valeurs:
                msg: str = f"Le nombre de valeurs affectees ({nb_valeurs}) ne correspond pas "
                msg += f"au nombre de variables ({nb_params})."
                raise IndexError(msg)

            for index, arg in enumerate(args[0]):
                if type(args[1]) in (list, tuple):
                    cls.valeurs[arg] = args[1][index]
                else:
                    cls.valeurs[arg] = args[1]
        else:
            cls.valeurs[args[0]] = args[1]


# Decorateur de recuperation des erreurs
def print_error(fonction):

    def wrapper(*args, **kwargs):
        try:
            return fonction(*args, **kwargs)
        except Exception as error:
            print(f"def {fonction.__name__}():", error)

    return wrapper


@print_error
def write():
    var = MesVariables()

    var["user"] = "Mcj"
    var["pass", "dblauth"] = "mdp", "1234"
    var["index"] = 1
    var["index"] += 10


@print_error
def read():
    res = MesVariables()

    print(1, res["user"])
    print(2, res["pass"])
    print(3, res["user", "pass"])
    print(4, res("user"))
    print(5, res("pass"))
    print(6, res("user", "pass"))
    print(7, res())
    print(res["inconnu"])


@print_error
def write_read():
    var = MesVariables()

    var["connect"] = {}
    var["connect"]["user"] = "Mcj"
    var["connect"]["pass"] = "mdpdict"
    print(var())

    var["pass", "dblauth", "trois"] = "mdp", "1234"


@print_error
def calcul():
    return 5 / 0


def main():
    write()
    read()
    write_read()
    calcul()


if __name__ == '__main__':
    main()
