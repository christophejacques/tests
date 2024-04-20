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
        return cls.getvalue(*args)

    @classmethod
    def __setitem__(cls, *args):
        if type(args[0]) in (list, tuple):
            for index, arg in enumerate(args[0]):
                if type(args[1]) in (list, tuple):
                    cls.valeurs[arg] = args[1][index]
                else:
                    cls.valeurs[arg] = args[1]
        else:
            cls.valeurs[args[0]] = args[1]



def write():
    var = MesVariables()
    var["user"] = "Mcj"
    var["pass", "dblauth"] = "mdp", "1234"
    var["index"] = 1
    var["index"] += 10

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


if __name__ == '__main__':
    write()
    try:
        read()
    except Exception as error:
        print(error)
