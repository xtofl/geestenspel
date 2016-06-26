import flask


class Kaart:
    def __init__(self, beeld, antwoord):
        self.antwoord = antwoord
        self.beeld = beeld


class Speler:
    def __init__(self, naam):
        self.naam = naam
        self.gewonnen = []


class Spel(flask.Flask):

    def __init__(self, spelers, kaarten, spulletjes, naam="Geesten"):
        super(Spel, self).__init__(naam)
        self.spelers = spelers
        self.kaarten = iter(kaarten)
        self.kaart = next(self.kaarten)
        self.spulletjes = spulletjes

    def probeer(self, speler, wat):
        if self.kaart.antwoord == wat:
            speler.gewonnen.append(self.kaart)
            self.kaart = next(self.kaarten)
        else:
            return False


def test_spel_kan_starten():
    spook = Kaart("Groen Boek Blauw Zetel", "Wit Spook")
    zetel = Kaart("Blauw Muis Groen Spook", "Rood Zetel")

    ik, jij, hij = map(Speler, ["ik", "jij", "hij"])
    spel = Spel([ik, jij, hij], [spook, zetel])

    spel.probeer(ik, "Geel Spook")
    assert ik.gewonnen == []
    spel.probeer(jij, "Wit Spook")
    assert jij.gewonnen == [spook]
    assert spel.kaart == zetel


spel = Spel(map(Speler, ["xtofl", "jona", "isaak"]),
            kaarten=[
                Kaart("Blauw Geest Groen Boek", "Grijs Muis"),
                Kaart("Rood Boek Groen Geest", "Grijs Muis")
            ],
            spulletjes=["Wit Spook", "Blauw Boek", "Rode Zetel", "Grijze Muis", "Groene Fles"])


@spel.route("/ik_weet/<wie>/<wat>", methods=["POST"])
def ik_weet(wie, wat):
    if spel.probeer(wie, wat):
        pass


@spel.route("/kaart")
def kaart():
    return flask.render_template('speeltafel.html', kaart=spel.kaart.beeld, spulletjes=spel.spulletjes)


def main():
    spel.run()

if __name__ == "__main__":
    main()

