import flask


class Kaart:
    def __init__(self, beeld, antwoord):
        self.antwoord = antwoord
        self.beeld = beeld


class Speler:
    def __init__(self, naam):
        self.naam = naam
        self.gewonnen = []

    def juist_geraden(self, kaart):
        self.gewonnen.append(kaart)

    def fout_geraden_geef_kaart_terug(self):
        try:
            return self.gewonnen.pop(-1)
        except IndexError:
            return None


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
    spulletjes = ["Wit Spook"]

    ik, jij, hij = map(Speler, ["ik", "jij", "hij"])
    spel = Spel([ik, jij, hij], [spook, zetel], spulletjes)

    spel.probeer(ik, "Geel Spook")
    assert ik.gewonnen == []
    spel.probeer(jij, "Wit Spook")
    assert jij.gewonnen == [spook]
    assert spel.kaart == zetel


def test_speler():
    ik = Speler("Ik")
    kaart1 = Kaart("X", "x")
    kaart2 = Kaart("Y", "y")

    assert ik.fout_geraden_geef_kaart_terug() == None

    ik.juist_geraden(kaart1)
    assert ik.gewonnen == [kaart1]

    ik.juist_geraden(kaart2)
    assert ik.gewonnen == [kaart1, kaart2]

    assert kaart2 == ik.fout_geraden_geef_kaart_terug()
    assert ik.gewonnen == [kaart1]


spel = Spel(map(Speler, ["xtofl", "jona", "isaak"]),
            kaarten=[
                Kaart("Blauw Geest Groen Boek", "Grijze Muis"),
                Kaart("Rood Boek Groen Geest", "Grijze Muis")
            ],
            spulletjes=["Wit Spook", "Blauw Boek", "Rode Zetel", "Grijze Muis", "Groene Fles"])


@spel.route("/grijp/<wie>/<wat>", methods=["POST"])
def grijp(wie, wat):
    if spel.probeer(wie, wat):
        return "Juist!"
    else:
        return "fout..."


@spel.route("/kaart")
def kaart():
    return flask.render_template('speeltafel.html', kaart=spel.kaart.beeld, spulletjes=spel.spulletjes)


def main():
    spel.run()

if __name__ == "__main__":
    main()

