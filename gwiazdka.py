import numpy as np
import math


###############################
# Adrian Orzoł                #
# Algorytm A*                 #
###############################


# obliczanie heurystyki
def heu(poz, cel):
    x = poz[0]-cel[0]
    y = poz[1]-cel[1]
    wynik = math.sqrt(x**2+y**2)
    return wynik


# funkcje od kierunkow
def gora():
    return -1, 0


def dol():
    return 1, 0


def lewo():
    return 0, -1


def prawo():
    return 0, 1


# znajdywanie dzieci punktu
def dziecko(poz, dane, kol):
    odp = []
    for x in kol:
        odpx = poz[0] + x[0]
        odpy = poz[1] + x[1]
        if odpx < 0 or odpx > dane.__len__() - 1 or odpy < 0 or odpy > dane.__len__() - 1:
            continue
        if dane[odpx][odpy] != 0:
            continue
        odp.append((odpx, odpy))
    return odp


def gwiazdka(start, stop, dane, koszt):
    otwarta = []
    zamknieta = [[start, start, 0]]
    obecny = [start, koszt]
    droga = []
    ogranicznik = 0
    # maksymalna liczba prób
    maks = 1000
    while 1:
        dzieci = dziecko(obecny[0], dane, kolejnosc)
        wyniki = []
        # dodawanie dzieci do listy otwartej
        for x in dzieci:
            z = 0
            for y in zamknieta:
                if x == y[0]:
                    z = z+1
            if z == 0:
                zmienna = []
                k = 0
                zmienna.append(x)
                zmienna.append(obecny[0])
                zmienna.append(obecny[1])
                j = 0
                while j != otwarta.__len__():
                    if zmienna[0] == otwarta[j][0]:
                        if zmienna[2] < otwarta[j][2]:
                            otwarta[j] = zmienna
                        k = 1
                    j = j + 1
                if k != 1:
                    otwarta.append(zmienna)
        # obliczanie wartości pól
        for a in otwarta:
            wyniki.append(heu(a[0], stop)+a[2])
        # dodawanie pól do listy zamkniętej
        i = wyniki.__len__()-1
        while i != -1:
            if wyniki[i] == min(wyniki):
                zamknieta.append(otwarta[i])
                obecny = [otwarta[i][0], otwarta[i][2]+koszt]
                otwarta.remove(otwarta[i])
                break
            i = i-1
        # tworzenie drogi
        if zamknieta[-1][0] == stop:
            droga = [zamknieta[-1][1]]
            while droga[-1] != start:
                for b in zamknieta:
                    if b[0] == droga[-1]:
                        droga.append(b[1])
            break
        ogranicznik = ogranicznik + 1
        if ogranicznik == maks:
            break
        # droga pusta, jeśli nie znaleziono trasy
    return droga


kolejnosc = [gora(), dol(), lewo(), prawo()]
poczatek = (19, 0)
koniec = (0, 19)
koszt = 1
grid = np.loadtxt("grid.txt")
trasa = gwiazdka(poczatek, koniec, grid, koszt)
if trasa.__len__() == 0:
    print("Nie znaleziono drogi")
else:
    for x in trasa:
        grid[x[0]][x[1]] = 3
    grid[poczatek[0]][poczatek[1]] = 1
    grid[koniec[0]][koniec[1]] = 2
    print(grid)
