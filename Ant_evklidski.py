from random import *
import time
start = time.time()
import math
# Ant Colony za iskanje najkrajše poti za problem TSP
# Za vsako iteracijo je dodana funkcija time
# Za vsako iteracijo zato vemo koliko casa porabi
# Izbiro problema dolocimo v 58. vrstici, kjer z ukazom open.file("ime datoteke",r) dolocimo, katero datotetko bomo prebrali
#
def izberi_pot(ant,vozlisce,neobiskana,pher,verjetnosti,razdalja,seznam,n,a,b,q0):
    # Vsaka mravlja se v vsakem vozliscu odloca, katero vozlisce bo naslednje obisakala.
    # Ta proces simulira funkcija izberi_pot
    # Najprej izracunamo verjetnosti obiska za vsako vozlisce, ki ga mravlja se ni obiskala
    # Nato pa s funkcijo choice nakljucno izberemo eno izmed vozlisc.
    vsota = 0
    for i in range(n):
        if neobiskana[ant][i] == 1:
            verjetnosti[i] = (pher[vozlisce][i]**a)*((1/razdalja[vozlisce][i])**b)
            vsota += (pher[vozlisce][i]**a)*(razdalja[vozlisce][i]**b)
        else:
            verjetnosti[i] = 0
    for i in range(n): # Če je verjetnost, da obiščemo neko vozlišče > 90%, se za to vozlišče nemudoma odločimo.
        if verjetnosti[i] > q0*vsota:
            return [i]
    # Ce izberemo slabe vhodne podatke lahko pride do podkoracitve, zaradi pomanjkanja feromona
    # To povzroci Error, saj "choices" opravlja z verjetnostmi, ki so vse enake 0.
    # To resimo tako, da uvedemo funkcijo "try", "except", ki v primeru, da pride do podkoracitve izbere naslednje vozlisce, ki je mravlja se ni obiskala
    # Ker pa velja, da v primeru podkoracitve program vec ne dela kot bi moral, so rezultati primerno slabsi
    # Zato program opozori, da je prislo do podkoracitve, kar je signal, da je treba spremeniti vhodne parametre.
    
    try:
            a = choices(seznam,verjetnosti)
    except:
            print("PODKORACITEV!")
            for i in range(n):
                    if neobiskana[ant][i] == 1:
                            return [i]
    return a
    
def spremeni_obliko(tabela,n):
    # Za planarne grafe navadno dobimo podatke v obliki koordinat (x,y).
    # Zato je treba izračunati razdalje (evklidske) med vozlisci, da dobimo matriko uteži.
    razdalja = [[0]*n for i in range(n)]
    for i in range(n):
        for j in range(n):
            razdalja[i][j] = round((abs(tabela[i][1]-tabela[j][1])**2 + abs(tabela[i][2] - tabela[j][2])**2)**(1/2))
    return razdalja
    
def main():
    
    a = 1 # pomen pher
    b = 5 # pomen razdalje
    c = 0.001 # zacetni pher
    s = 0.1 # zmanjsanje pheronoma po vsakem obhodu
    p = 0.1 # Povecanje pheronoma, k najvedcji poti
    q0 = 0.9 # pozresnost
    m = 10 # stevilo mravelj
    q = 0.01 # kolicina pher, ki ga izloci ena mravlja
    n = 52 #int(input()) #stevilo_mest
    razdalja = [[0]*n for i in range(n)]
    pher = [[c]*n for i in range(n)]
    verjetnosti = [0]*n
    seznam = [i for i in range(n)]
    lokacija = [0]*m # lokacija na kateri se nahaja i-ta mravlja
    dolzina_poti = [0]*m # razdalja, ki jo je na svoji poti opravila i-ta mravlja
    pher_dodan = [[0]*n for i in range(n)]
    min_dolzina = 999999
    opt_pot = []

    file = open('52.txt', 'r')
    for i in range(n):
        razdalja[i] = file.readline().split()
        for j in range(3):
            razdalja[i][j] = float(razdalja[i][j])
    razdalja = spremeni_obliko(razdalja,n)
    korak = 0
    global inp
    inp = time.time()
    while korak < 1000:
        # Sedaj imamo vse podatke in lahko zacnemo z resevanjem problema
        # Po vsakem obhodu bomo spremenili stanje pheronom in si shranili novo najkrajso pot, ce jo uspemo doseci.
        korak += 1
        pot = [[] for i in range(m)] # pot za vsako mravljo
        neobiskana = [[1]*n for i in range(m)] # mnozica neobiskanih vozlisc za vsako mravljo (morda bolj smiselno sete za boljso casovno zahtebnost)
        pher_dodan = [[0]*n for i in range(n)] # kolicina pheranoma dodanega zaradi mravljine poti
        dolzina_poti = [0]*m
        for i in range(m):
            lokacija[i] = randint(0,n-1) # Izberemo zacetno vozlisce za vsako mravljo
            neobiskana[i][lokacija[i]] = 2 # Damo mu poseben indeks, saj se bomo v vozlisce kasneje tudi vrnili
        
        for i in range(n):      # tukaj simuliramo pot
            for j in range(m):
                if i == n-1: 
                    for k in range(n): 
                     if neobiskana[j][k] == 2: #Na predzadnjem vozliscu najdemo zacetno vozlisce in se vanj vrnemo
                        naslednje_vozlisce = k
                        dolzina_poti[j] +=  razdalja[lokacija[j]][naslednje_vozlisce]
                        pot[j].append((lokacija[j],naslednje_vozlisce))
                else:   
                    naslednje_vozlisce = izberi_pot(j,lokacija[j],neobiskana,pher,verjetnosti,razdalja,seznam,n,a,b,q0)[0] # na vseh ostalih nakljucno izberemo naslednje vozlisce na podlagi
                    dolzina_poti[j] +=  razdalja[lokacija[j]][naslednje_vozlisce]
                    pot[j].append((lokacija[j],naslednje_vozlisce))
                    lokacija[j] = naslednje_vozlisce
                    neobiskana[j][naslednje_vozlisce] = 0
                pher[pot[j][i][0]][pot[j][i][1]] = (1-s)*pher[pot[j][i][0]][pot[j][i][1]] + s*c #sprememba feronoma, namenjena temu, da mravlje ne bi uporabljale istih poti v istem vrstnem redu
                # Dodatno pojasnilo:
                # Brez tega dodatka, bi hitro verjetnosti da ponavljamo prvo najkrajso pot, ki smo jo nasli postajale vedno vecje in ostali bi v lokalnem minimumu
                # S pomocjo te funkcije imajo mravlje dodatno "motivacijo" spreminjati svojo pot in s tem lahko najdejo se kaksen lok min.
                pher[pot[j][i][1]][pot[j][i][0]] = pher[pot[j][i][0]][pot[j][i][1]] #Za simetricne grafe sta utezi za obe smeri seveda enaki


        for  i in range(m): # Po vsaki iteraciji preverimo, ce smo nasli novi lokalni minimum in ga v tem primeru tudi shranimo. 
            if dolzina_poti[i] == min(dolzina_poti):
                if (dolzina_poti[i] < min_dolzina):
                    min_dolzina = dolzina_poti[i]
                    opt_pot = pot[i]

        for i in range(n-1):
            pher_dodan[opt_pot[i][0]][opt_pot[i][1]] = p*(q/min_dolzina) # Pheronom dodamo najboljši poti
            pher_dodan[opt_pot[i][1]][opt_pot[i][0]] = pher[opt_pot[i][0]][opt_pot[i][1]]
        for i in range(n):
            for j in range(n):
                pher[i][j] = (1-p)*pher[i][j] + pher_dodan[i][j] # Po vsaki iteraiciji nekaj pheronoma izhlapi.
        for i in range(n-1):
            pher_dodan[opt_pot[i][0]][opt_pot[i][1]] = 0
            pher_dodan[opt_pot[i][1]][opt_pot[i][0]] = 0
    #print(dolzina_poti) # dolzina poti v zadnji iteraciji, (samo informativno)
    #print(opt_pot) # optimalna pot (to nas zanima!)
    #print(min_dolzina) # dolzina opt poti (to nas zanima!)
    #print(pher) # kolicina pher ob koncu hitro opazis da so ene popolnoma polne druge prazne (samo informativno)
    global tj
    tj= time.time()
    print("Ant Colony " + str(tj-inp))
    return min_dolzina, opt_pot
#for i in range(10):
#    main()
#t = time.time()
#print("skupni " + str(t - start))

def average(stevilo): # izračun povprečnega "najboljšega " obhoda ob želenm številu ponovitev algoritma, vrne tudi najkrajsi obhod in njegovo dolzino
    vsota = 0
    najkrajsa_pot = []
    najkrajsa_dolzina = math.inf
    for i in range(stevilo):
        print(i)
        dolzina, pot = main()
        print(dolzina)
        vsota += dolzina
        if dolzina < najkrajsa_dolzina:
            najkrajsa_dolzina = dolzina
            najkrajsa_pot = pot
    t = time.time()
    print("skupni " + str(t - start))
    print("Povprečna dolžina " + str(vsota/stevilo))
    print("Dolžina najboljše poti " + str(najkrajsa_dolzina))
    print("Najboljša pot ")
    print(najkrajsa_pot)
    return(vsota/stevilo, najkrajsa_dolzina, najkrajsa_pot)
print("Določite število iteracij algoritma")
print("Ena iteracija traja približno 35 sekund (Problem 52Berlin)")
A = int(input())
average(A)
