import flask


class Spel(flask.Flask):

    @property
    def kaart(self):
        return "Groene Geest Blauwe Muis"


spel = Spel(__name__)


@spel.route("/ik_weet/<wat>")
def ik_weet(wat):
    pass


@spel.route("/kaart")
def kaart():
    return spel.kaart


def main():
    spel.run()



if __name__ == "__main__":
    main()