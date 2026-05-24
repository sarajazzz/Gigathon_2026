import random



# Słownik z nazwami ruchów
NAZWY_RUCHOW = {
    "polnoc": "północ",
    "poludnie": "południe",
    "wschod": "wschód",
    "zachod": "zachód",
    "odpoczynek": "odpoczynek"
}



# Główne wejście programu
def main():
    while True:
        uruchom_symulacje()

        print()
        decyzja = input("Czy chcesz ponownie uruchomić symulację? (t/n): ").strip().lower()

        if decyzja != "t":
            print("Koniec programu. Dziękujemy za udział w wyprawie!")
            break



# Uruchomienie symulacji
def uruchom_symulacje():
    parametry = pobierz_parametry()
    elementy = utworz_elementy_swiata(parametry)
    historia = []

    liczba_krokow = 0
    powod_zakonczenia = ""
    sukces = False

    pokaz_start(parametry)

    while True:
        liczba_krokow += 1

        print()
        linia()
        print(f"KROK {liczba_krokow}")
        linia()

        stara_pozycja = (parametry["x"], parametry["y"])
        energia_przed = parametry["energia"]

        akcja = wybierz_akcje()

        poprzednia_pozycja = wykonaj_akcje(
            parametry,
            akcja,
            historia,
            liczba_krokow
        )

        sprawdz_element_swiata(
            parametry,
            elementy,
            historia,
            liczba_krokow,
            poprzednia_pozycja
        )

        losuj_zdarzenie(
            parametry,
            historia,
            liczba_krokow
        )

        pokaz_status_po_kroku(
            parametry,
            akcja,
            stara_pozycja,
            energia_przed,
            liczba_krokow
        )
    
        input("Naciśnij Enter, aby przejść do następnego kroku...")  # Pauza przed kolejnym krokiem

        koniec, powod_zakonczenia, sukces = sprawdz_koniec(
            parametry,
            liczba_krokow
        )

        if koniec:
            break

    wynik = oblicz_wynik(parametry, liczba_krokow, sukces)

    pokaz_raport(
        parametry,
        liczba_krokow,
        powod_zakonczenia,
        sukces,
        wynik,
        historia
    )



# Pobranie parametrów od użytkownika
def pobierz_parametry():
    print("Witaj w symulatorze wyprawy 2D!")
    print("Motyw programu: Kurier 2D - dostawa przez miasto")
    print("Twoim zadaniem jest doprowadzić kuriera do celu, zanim zabraknie energii albo kroków.")
    linia()

    nazwa_wyprawy = pobierz_tekst(
        "Podaj nazwę wyprawy (np. Dostarczyć awizo): ",
        "Dostarczyć awizo"
    )

    kurier = pobierz_tekst(
        "Podaj imię kuriera (np. King Julian): ",
        "King Julian"
    )

    rozmiar_swiata = pobierz_liczbe(
        "Podaj rozmiar miasta (np. 20): ",
        20,
        5,
        100
    )

    print()
    print(f"Miasto ma granice od {-rozmiar_swiata} do {rozmiar_swiata} na osi X i Y.")

    start_x = pobierz_liczbe(
        "Podaj pozycję startową dla osi X (np. 0): ",
        0,
        -rozmiar_swiata,
        rozmiar_swiata
    )

    start_y = pobierz_liczbe(
        "Podaj pozycję startową dla osi Y (np. 0): ",
        0,
        -rozmiar_swiata,
        rozmiar_swiata
    )

    energia = pobierz_liczbe(
        "Podaj początkową energię kuriera (np. 30): ",
        30,
        1,
        200
    )

    print()
    print("Podaj cel dostawy (musi znajdować się w granicach miasta): ")

    cel_x = pobierz_liczbe(
        "Podaj pozycję celu dla osi X (np. 9): ",
        9,
        -rozmiar_swiata,
        rozmiar_swiata
    )

    cel_y = pobierz_liczbe(
        "Podaj pozycję celu dla osi Y (np. 4): ",
        4,
        -rozmiar_swiata,
        rozmiar_swiata
    )

    if cel_x == start_x and cel_y == start_y:
        print("Wskazano cel w lokalizacji startowej. Program przesuwa cel o 1 na osi X.")
        if cel_x < rozmiar_swiata:
            cel_x += 1
        else:
            cel_x -= 1

    limit_krokow = pobierz_liczbe(
        "Podaj limit kroków (np. 18): ",
        18,
        1,
        500
    )

    return {
        "nazwa_wyprawy": nazwa_wyprawy,
        "kurier": kurier,
        "start_x": start_x,
        "start_y": start_y,
        "x": start_x,
        "y": start_y,
        "cel_x": cel_x,
        "cel_y": cel_y,
        "energia": energia,
        "energia_startowa": energia,
        "rozmiar_swiata": rozmiar_swiata,
        "limit_krokow": limit_krokow,
        "pozytywne_zdarzenia": 0,
        "negatywne_zdarzenia": 0,
        "odwiedzone_elementy": []
    }



# Tworzenie elementów świata symulacji
def utworz_elementy_swiata(parametry):
    """
    Tworzy elementy świata w losowych miejscach.

    Elementy świata:
    - korki,
    - stacje odpoczynku,
    - skróty,
    - roboty drogowe.
    """

    rozmiar = parametry["rozmiar_swiata"]

    zajete = {
        (parametry["start_x"], parametry["start_y"]),
        (parametry["cel_x"], parametry["cel_y"])
    }

    elementy = {
        "korki": [],
        "stacje": [],
        "skroty": [],
        "roboty": []
    }

    for _ in range(4):
        elementy["korki"].append(losowa_pozycja(rozmiar, zajete))

    for _ in range(3):
        elementy["stacje"].append(losowa_pozycja(rozmiar, zajete))

    for _ in range(3):
        elementy["skroty"].append(losowa_pozycja(rozmiar, zajete))

    for _ in range(3):
        elementy["roboty"].append(losowa_pozycja(rozmiar, zajete))

    return elementy



# Wyświetlenie informacji o starcie wyprawy
def pokaz_start(parametry):
    linia()
    print("START WYPRAWY")
    linia()

    print(f"Nazwa wyprawy: {parametry['nazwa_wyprawy']}")
    print(f"Kurier: {parametry['kurier']}")
    print(f"Pozycja startowa: ({parametry['start_x']}, {parametry['start_y']})")
    print(f"Cel wyprawy: ({parametry['cel_x']}, {parametry['cel_y']})")
    print(f"Początkowa energia: {parametry['energia_startowa']}")
    print(f"Granice miasta: od {-parametry['rozmiar_swiata']} do {parametry['rozmiar_swiata']} na osi X i Y")
    print(f"Limit kroków: {parametry['limit_krokow']}")
    print(f"Odległość od celu: {odleglosc_od_celu(parametry['x'], parametry['y'], parametry['cel_x'], parametry['cel_y'])}")

    linia()



# Menu wyboru akcji dla użytkownika
def wybierz_akcje():
    
    RUCHY = {
        "1": "polnoc",
        "2": "poludnie",
        "3": "wschod",
        "4": "zachod",
        "5": "odpoczynek"
    }
    
    while True:
        print()
        print("Wybierz akcję:")
        print("1 - północ (Y + 1)")
        print("2 - południe (Y - 1)")
        print("3 - wschód (X + 1)")
        print("4 - zachód (X - 1)")
        print("5 - odpoczynek (odzyskanie części energii)")

        wybor = input("Twój wybór: ").strip()

        if wybor in RUCHY:
            return RUCHY[wybor]

        print("Niepoprawny wybór. Wpisz liczbę od 1 do 5.")



# Realizacja akcji wybranej przez użytkownika
def wykonaj_akcje(parametry, akcja, historia, krok):
    stara_pozycja = (parametry["x"], parametry["y"])

    if akcja == "odpoczynek":
        parametry["energia"] += 5

        opis = "Kurier odpoczywa i odzyskuje 5pkt energii."
        print(opis)
        dodaj_historie(historia, krok, opis)
        input("Naciśnij Enter, aby kontynuować...")  # Pauza po odpoczynku

        return stara_pozycja

    nowe_x, nowe_y = oblicz_nowa_pozycje(
        parametry["x"],
        parametry["y"],
        akcja
    )

    if not czy_w_granicach(nowe_x, nowe_y, parametry["rozmiar_swiata"]):
        parametry["energia"] -= 1

        opis = "Próba wyjścia poza granice miasta. Pozycja bez zmian, utrata 1pkt energii."
        print(opis)
        dodaj_historie(historia, krok, opis)
        input("Naciśnij Enter, aby kontynuować...")  # Pauza po próbie wyjścia poza granice

        return stara_pozycja

    parametry["x"] = nowe_x
    parametry["y"] = nowe_y
    parametry["energia"] -= 2

    opis = f"Ruch w kierunku: {NAZWY_RUCHOW[akcja]}. Utrata 2pkt energii."
    print(opis)
    dodaj_historie(historia, krok, opis)

    return stara_pozycja



# Obliczanie współrzędnych kuriera po wykonaniu ruchu
def oblicz_nowa_pozycje(x, y, akcja):
    if akcja == "polnoc":
        y += 1
    elif akcja == "poludnie":
        y -= 1
    elif akcja == "wschod":
        x += 1
    elif akcja == "zachod":
        x -= 1

    return x, y



# Sprawdzenie, czy w aktualnej pozycji kuriera znajduje się jakiś element świata
def sprawdz_element_swiata(parametry, elementy, historia, krok, poprzednia_pozycja):
    x = parametry["x"]
    y = parametry["y"]
    pozycja = (x, y)

    if pozycja in elementy["korki"]:
        parametry["energia"] -= 3
        parametry["negatywne_zdarzenia"] += 1
        parametry["odwiedzone_elementy"].append("korek uliczny")

        opis = "Element świata: korek uliczny. Kurier traci dodatkowe 3 punkty energii."
        print(opis)
        dodaj_historie(historia, krok, opis)
        input("Naciśnij Enter, aby kontynuować...")  # Pauza po zatorze

    elif pozycja in elementy["stacje"]:
        parametry["energia"] += 6
        parametry["pozytywne_zdarzenia"] += 1
        parametry["odwiedzone_elementy"].append("stacja odpoczynku")

        opis = "Element świata: stacja odpoczynku. Kurier odzyskuje 6 punktów energii."
        print(opis)
        dodaj_historie(historia, krok, opis)
        input("Naciśnij Enter, aby kontynuować...")  # Pauza po stacji odpoczynku

    elif pozycja in elementy["skroty"]:
        stare_x = parametry["x"]
        stare_y = parametry["y"]

        nowe_x, nowe_y = przesun_blizej_celu(
            parametry["x"],
            parametry["y"],
            parametry["cel_x"],
            parametry["cel_y"]
        )

        parametry["x"] = nowe_x
        parametry["y"] = nowe_y
        parametry["pozytywne_zdarzenia"] += 1
        parametry["odwiedzone_elementy"].append("skrót przez park")

        opis = f"Element świata: skrót przez park. Pozycja zmienia się z ({stare_x}, {stare_y}) na ({nowe_x}, {nowe_y})."
        print(opis)
        dodaj_historie(historia, krok, opis)
        input("Naciśnij Enter, aby kontynuować...")  # Pauza po skorzystaniu ze skrótu

    elif pozycja in elementy["roboty"]:
        parametry["x"] = poprzednia_pozycja[0]
        parametry["y"] = poprzednia_pozycja[1]
        parametry["energia"] -= 2
        parametry["negatywne_zdarzenia"] += 1
        parametry["odwiedzone_elementy"].append("roboty drogowe")

        opis = "Element świata: roboty drogowe. Kurier wraca na poprzednią pozycję i traci 2 energii."
        print(opis)
        dodaj_historie(historia, krok, opis)
        input("Naciśnij Enter, aby kontynuować...")  # Pauza po robotach drogowych

    else:
        print("Element świata: brak specjalnego pola na tej pozycji.")
        input("Naciśnij Enter, aby kontynuować...")  # Pauza po sprawdzeniu pozycji



# Losowanie zdarzenia w symulacji dla kuriera
def losuj_zdarzenie(parametry, historia, krok):
    los = random.randint(1, 100)

    if los > 30:
        print("Zdarzenie losowe: brak.")
        return

    zdarzenie = random.choice([
        "deszcz",
        "zielona_fala",
        "przebita_opona",
        "pomocny_mieszkaniec"
    ])

    if zdarzenie == "deszcz":
        parametry["energia"] -= 2
        parametry["negatywne_zdarzenia"] += 1

        opis = "Zdarzenie losowe: zaczął padać deszcz. Kurier traci 2 punkty energii."

    elif zdarzenie == "zielona_fala":
        parametry["energia"] += 3
        parametry["pozytywne_zdarzenia"] += 1

        opis = "Zdarzenie losowe: zielona fala na światłach. Kurier odzyskuje 3 punkty energii."

    elif zdarzenie == "przebita_opona":
        parametry["energia"] -= 4
        parametry["negatywne_zdarzenia"] += 1

        opis = "Zdarzenie losowe: przebita opona. Naprawa kosztuje 4 punkty energii."

    else: # pomocny mieszkaniec
        stare_x = parametry["x"]
        stare_y = parametry["y"]

        nowe_x, nowe_y = przesun_blizej_celu(
            parametry["x"],
            parametry["y"],
            parametry["cel_x"],
            parametry["cel_y"]
        )

        parametry["x"] = nowe_x
        parametry["y"] = nowe_y
        parametry["pozytywne_zdarzenia"] += 1

        opis = f"Zdarzenie losowe: pomocny mieszkaniec wskazał krótszą drogę. Pozycja zmienia się z ({stare_x}, {stare_y}) na ({nowe_x}, {nowe_y})."

    print(opis)
    dodaj_historie(historia, krok, opis)
    input("Naciśnij Enter, aby kontynuować...")  # Pauza po zdarzeniu losowym



# Wyświetlenie podsumowania statusu kuriera po wykonaniu akcji i zdarzeń w danym kroku
def pokaz_status_po_kroku(parametry, akcja, stara_pozycja, energia_przed, liczba_krokow):
    nowa_pozycja = (parametry["x"], parametry["y"])
    energia_po = parametry["energia"]

    dystans = odleglosc_od_celu(
        parametry["x"],
        parametry["y"],
        parametry["cel_x"],
        parametry["cel_y"]
    )

    print()
    print("Podsumowanie kroku:")
    print(f"- numer kroku: {liczba_krokow}")
    print(f"- wybrana akcja: {NAZWY_RUCHOW[akcja]}")
    print(f"- pozycja przed ruchem: {stara_pozycja}")
    print(f"- pozycja po ruchu i zdarzeniach: {nowa_pozycja}")
    print(f"- energia przed krokiem: {energia_przed}")
    print(f"- energia po kroku: {energia_po}")
    print(f"- odległość od celu: {dystans}")



# Weryfikacja, czy symulacja powinna się zakończyć
def sprawdz_koniec(parametry, liczba_krokow):
    if parametry["x"] == parametry["cel_x"] and parametry["y"] == parametry["cel_y"]:
        return True, "Kurier dotarł do celu dostawy.", True

    if parametry["energia"] <= 0:
        return True, "Kurierowi zabrakło energii.", False

    if liczba_krokow >= parametry["limit_krokow"]:
        return True, "Przekroczono limit kroków.", False

    return False, "", False



# Obliczenie wyniku końcowego przeprowadzonej symulacji
def oblicz_wynik(parametry, liczba_krokow, sukces):
    wynik = 0

    if sukces:
        wynik += 100

    wynik += parametry["energia"] * 2
    wynik -= liczba_krokow
    wynik += parametry["pozytywne_zdarzenia"] * 10
    wynik -= parametry["negatywne_zdarzenia"] * 5

    dystans = odleglosc_od_celu(
        parametry["x"],
        parametry["y"],
        parametry["cel_x"],
        parametry["cel_y"]
    )

    wynik -= dystans * 3

    return wynik



# Wyświetlenie raportu końcowego z przebiegu symulacji
def pokaz_raport(parametry, liczba_krokow, powod, sukces, wynik, historia):
    linia()
    print("RAPORT KOŃCOWY")
    linia()

    print(f"Nazwa wyprawy: {parametry['nazwa_wyprawy']}")
    print(f"Kurier: {parametry['kurier']}")

    print()
    print("Parametry początkowe:")
    print(f"- pozycja startowa: ({parametry['start_x']}, {parametry['start_y']})")
    print(f"- energia początkowa: {parametry['energia_startowa']}")
    print(f"- granice miasta: od {-parametry['rozmiar_swiata']} do {parametry['rozmiar_swiata']}")
    print(f"- cel wyprawy: ({parametry['cel_x']}, {parametry['cel_y']})")
    print(f"- limit kroków: {parametry['limit_krokow']}")

    print()
    print(f"Pozycja końcowa: ({parametry['x']}, {parametry['y']})")
    print(f"Liczba wykonanych kroków: {liczba_krokow}")
    print(f"Pozostała energia: {parametry['energia']}")
    print(f"Pozytywne zdarzenia lub elementy: {parametry['pozytywne_zdarzenia']}")
    print(f"Negatywne zdarzenia lub elementy: {parametry['negatywne_zdarzenia']}")
    print(f"Przyczyna zakończenia: {powod}")

    if sukces:
        print("Rezultat: SUKCES")
    else:
        print("Rezultat: PORAŻKA")

    print(f"Końcowy wynik: {wynik}")

    print()
    print("Odwiedzone elementy świata:")

    if len(parametry["odwiedzone_elementy"]) == 0:
        print("- brak")
    else:
        for element in parametry["odwiedzone_elementy"]:
            print(f"- {element}")

    print()
    print("Najważniejsze wydarzenia z przebiegu wyprawy:")

    if len(historia) == 0:
        print("- brak wydarzeń")
    else:
        for wpis in historia:
            print(f"- {wpis}")

    linia()



# Funkcja pomocnicza do rysowania linii
def linia():
    print("-" * 60)



# Funkcja pomocnicza do pobierania tekstu od użytkownika
def pobierz_tekst(komunikat, wartosc_domyslna):
    tekst = input(komunikat).strip()

    if tekst == "":
        print(f"Nie podano odpowiedzi. Przyjęto wartość domyślną: {wartosc_domyslna}")
        return wartosc_domyslna

    return tekst



# Funkcja pomocnicza do pobierania liczby od użytkownika
def pobierz_liczbe(komunikat, wartosc_domyslna, minimum=None, maksimum=None):
    while True:
        wartosc = input(komunikat).strip()

        if wartosc == "":
            print(f"Nie podano wartości. Przyjęto: {wartosc_domyslna}")
            return wartosc_domyslna

        try:
            liczba = int(wartosc)
        except ValueError:
            print("To nie jest poprawna liczba całkowita. Spróbuj ponownie.")
            continue

        if minimum is not None and liczba < minimum:
            print(f"Wartość nie może być mniejsza niż {minimum}.")
            continue

        if maksimum is not None and liczba > maksimum:
            print(f"Wartość nie może być większa niż {maksimum}.")
            continue

        return liczba



# Funkcja pomocnicza do generowania losowej pozycji dla zdarzenia w symulacji
def losowa_pozycja(rozmiar_swiata, zajete):
    while True:
        x = random.randint(-rozmiar_swiata, rozmiar_swiata)
        y = random.randint(-rozmiar_swiata, rozmiar_swiata)

        pozycja = (x, y)

        if pozycja not in zajete:
            zajete.add(pozycja)
            return pozycja



# Funkcja pomocnicza zwracająca odległość kuriera od celu wyprawy
def odleglosc_od_celu(x, y, cel_x, cel_y):
    return abs(cel_x - x) + abs(cel_y - y)



# Funkcja pomocnicza dodająca wpis do historii symulacji
def dodaj_historie(historia, krok, opis):
    historia.append(f"Krok {krok}: {opis}")



# Funkcja pomocnicza do weryfikacji, czy dana pozycja znajduje się w granicach świata symulacji
def czy_w_granicach(x, y, rozmiar_swiata):
    return -rozmiar_swiata <= x <= rozmiar_swiata and -rozmiar_swiata <= y <= rozmiar_swiata



# Funkcja pomocnicza przenosząca kuriera o jedno pole bliżej celu
def przesun_blizej_celu(x, y, cel_x, cel_y):
    """
    Przesuwa kuriera o jedno pole bliżej celu.
    Najpierw zmniejsza różnicę na osi X, potem na osi Y.
    """

    if x < cel_x:
        x += 1
    elif x > cel_x:
        x -= 1
    elif y < cel_y:
        y += 1
    elif y > cel_y:
        y -= 1

    return x, y



# Uruchomienie programu jako wykonywalnego skryptu, nie jako importowanego modułu
if __name__ == "__main__":
    main()