class Param:
    buffer: list = list()
    option: list = list()
    keywrd: dict = dict()
    data: dict = dict()

    @classmethod
    def required(cls, nom_parametre: str, type_variable=object):
        """
        Decorateur permettant de declarer les parametres obligatoires ainsi que leur type 
        pour la definition de la fonction qu'il decore

        Parametres :
            @nom_parametre: str
                Nom du parametre en chaine de caracteres

            @type_variable: type = object
                Type du precedent parametre

        Resultat :
            decorateur de la fonction
        """
        if not isinstance(nom_parametre, str):
            raise TypeError("def required: Le premier parametre n'est pas de type str")

        def decorateur(fonction):
            def wrapper(*args, **kwargs):
                return fonction(*args, **kwargs)
            return wrapper
        cls.buffer.append((nom_parametre, type_variable))
        return decorateur

    @classmethod
    def optional(cls, nom_parametre: str, type_variable=object):
        """
        Decorateur permettant de declarer les parametres facultatifs ainsi que leur type 
        pour la definition de la fonction qu'il decore

        Parametres :
            @nom_parametre: str
                Nom du parametre en chaine de caracteres

            @type_variable: type = object
                Type du precedent parametre

        Resultat :
            decorateur de la fonction
        """
        if not isinstance(nom_parametre, str):
            raise TypeError("def optional: Le premier parametre n'est pas de type str")

        def decorateur(fonction):
            def wrapper(*args, **kwargs):
                return fonction(*args, **kwargs)
            return wrapper
        cls.option.append((nom_parametre, type_variable))
        return decorateur

    @classmethod
    def keyword(cls, nom_parametre: str, type_variable=object):
        if not isinstance(nom_parametre, str):
            raise TypeError("def keyword: Le premier parametre n'est pas de type str")

        def decorateur(fonction):
            def wrapper(*args, **kwargs):
                return fonction(*args, **kwargs)
            return wrapper
        cls.keywrd[nom_parametre] = type_variable
        return decorateur

    @classmethod
    def result(cls, type_resultat=object, **options):
        """
        Decorateur permettant de declarer le type du resultat 
        de la fonction qu'il decore

        Parametres :
            @type_resultat: type = object
                Type du resultat de la fonction qui est decoree

            @options :
                Permet de modifier le comportement lors de l'execution de la fonction :
                - result_if_error = valeur
                    permet de retourner la valeur lorsqu'il y a une erreur
                    lors de l'execution de la fonction decoree
                    la valeur doit etre du meme type que type_resultat


        Resultat :
            decorateur de la fonction
        """
        def check_args(nom_fonction, args):
            # Controle des parametres obligatoires et facultatifs (non keyword)
            nb_params = len(cls.data[nom_fonction]["params"])
            nb_option = len(cls.data[nom_fonction]["option"])
            nb_args = len(args)
            
            # Controle des options obligatoires et facultatives
            if nb_args < nb_params or nb_args > nb_params+nb_option:
                errmsg: str = f"{nom_fonction}"
                errmsg += f"{args}:"
                errmsg += f" {nb_params} parametres obligatoires "
                if nb_option > 0:
                    errmsg += f"(+{nb_option} facultatifs) "
                errmsg += f"attendus au lieu de {nb_args} donnes."
                raise Exception(errmsg)

            all_params = cls.data[nom_fonction]["params"] + cls.data[nom_fonction]["option"]
            for index, v in enumerate(args):
                if not isinstance(v, all_params[index][1]):
                    if "result_if_error" in options:
                        return True, options.get("result_if_error")

                    else:
                        errmsg: str = f"{nom_fonction}{args}: "
                        errmsg += f"Le {1+index}"
                        errmsg += "eme" if index else "er"
                        errmsg += f" parametre {all_params[index][0]}(="
                        errmsg += f"{v!r}) n'est pas de type {cls.nom_classe(all_params[index][1])}"
                        raise TypeError(errmsg)

        def check_kwargs(nom_fonction, args, kwargs):
            # Controle des parametres keywords
            for keyword in kwargs:
                if keyword not in cls.data[nom_fonction]["keywrd"]:
                    raise Exception(f"{nom_fonction}{args, kwargs}: Le parametre {keyword!r} est inconnu.")
                else:
                    if not isinstance(kwargs[keyword], cls.data[nom_fonction]["keywrd"][keyword]):
                        errmsg: str = f"{nom_fonction}{args}: "
                        errmsg += f"Le parametre {keyword!r} est de type "
                        errmsg += kwargs[keyword].__class__.__name__
                        errmsg += " au lieu de "
                        errmsg += cls.data[nom_fonction]["keywrd"][keyword].__name__
                        raise TypeError(errmsg)

        def check_result(nom_fonction, args, result):
            if cls.data[nom_fonction]["result"] is None:
                if result is None:
                    return None

                errmsg: str = f"{nom_fonction}{args}: "
                errmsg += f"a renvoye {result.__class__.__name__} au lieu de None."
                raise TypeError(errmsg)

            if isinstance(result, cls.data[nom_fonction]["result"]):
                return result

            if "result_if_error" in options:
                return options.get("result_if_error")

            errmsg: str = f"{nom_fonction}{args}: "
            errmsg += f"Le resultat obtenu est de type {cls.nom_classe(result.__class__)}, "
            errmsg += f"le type attendu est de type {cls.nom_classe(cls.data[nom_fonction]['result'])}"
            raise TypeError(errmsg)

        def save_parametres(nom_fonction):
            cls.data[nom_fonction] = dict()
            cls.data[nom_fonction]["params"] = cls.buffer.copy()
            cls.data[nom_fonction]["option"] = cls.option.copy()
            cls.data[nom_fonction]["keywrd"] = cls.keywrd.copy()
            cls.data[nom_fonction]["result"] = type_resultat
            cls.buffer.clear()
            cls.option.clear()
            cls.keywrd.clear()
            # print(cls.definition(nom_fonction))

        def decorateur(fonction):
            def wrapper(*args, **kwargs):
                result = check_args(nom_fonction, args)
                if result.__class__.__name__ == "tuple" and result[0] is True:
                    return result[1]
                check_kwargs(nom_fonction, args, kwargs)

                try:
                    result = fonction(*args, **kwargs)
                except Exception as error:
                    if "result_if_error" in options:
                        return options.get("result_if_error")
                    raise Exception(f"{nom_fonction}{args}: {error}") from error

                return check_result(nom_fonction, args, result)                    

            nom_fonction = fonction.__name__
            save_parametres(nom_fonction)

            return wrapper
        return decorateur

    @classmethod
    def nom_classe(cls, classe):
        if hasattr(classe, "__name__"):
            return classe.__name__

        return str(classe)

    @classmethod
    def definition(cls, nom_fonction):
        defstr: str = f"def {nom_fonction}("
        defstr += ", ".join([v + ": " + cls.nom_classe(t) for v, t in cls.data[nom_fonction]["params"]])
        if cls.data[nom_fonction]["option"]:
            defstr += ", ["
            defstr += ", ".join([v + ": " + cls.nom_classe(t) for v, t in cls.data[nom_fonction]["option"]])
            defstr += "]"
        defstr += ") -> "
        defstr += cls.nom_classe(cls.data[nom_fonction]["result"])

        return defstr


def datas():
    print()
    for fonction in Param.data:
        print(Param.definition(fonction))


class Test:

    @Param.required("self")
    @Param.required("texte", str)
    @Param.result(None)
    def __init__(self, texte):
        self.texte = texte

    @Param.required("self")
    @Param.result(str)
    def print(self):
        return self.texte


t = Test("classe Test")
print(t.print())


@Param.keyword("screen", bool)
@Param.keyword("kwargs", int)
@Param.result(result_if_error="#N/A")
def cls(**kwargs):
    # print(f"cls({kwargs})")
    return 1/1  # "clear screen"


@Param.required("texte", str | None)
@Param.keyword("flush", bool)
@Param.keyword("end", bool)
@Param.result(None)
def dprint(texte, **options):
    print("dprint:", texte, **options)
    # return 1


@Param.required("a", int)
@Param.required("b", int)
@Param.result(int, result_if_error=-1)
def division(a, b):
    if a == 0:
        return "Zero"
    return a//b


@Param.required("c1", str)
@Param.required("c2", str)
@Param.optional("repeat", str)
@Param.optional("nb", int)
@Param.result(str)
def concat(a, b, repeat="", nb=1):
    return f"{a}-{b}-{nb*repeat}"


def main():
    print("cls:", cls(screen=True, kwargs=0))
    dprint("Hello")
    print("div/'2'':", division(10, "2"))
    print("concat:", concat("20", "7"))
    print("concat:", concat("2024", "05", "1", 2))
    print("div0/x:", division(0, 4))
    print("div/0:", division(4, 0))
    print("div 3p:", division(1, 2, 3))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)

    datas()
