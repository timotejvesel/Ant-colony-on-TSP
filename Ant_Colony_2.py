from random import *
import time
start = time.time()


def izberi_pot(ant,vozlisce,neobiskana,pher,verjetnosti,razdalja,seznam,n,a,b,q0):
    vsota = 0
    for i in range(n):
        if neobiskana[ant][i] == 1:
            verjetnosti[i] = (pher[vozlisce][i]**a)*(razdalja[vozlisce][i]**b)
            vsota += (pher[vozlisce][i]**a)*(razdalja[vozlisce][i]**b)
        else:
            verjetnosti[i] = 0
    for i in range(n):
        if verjetnosti[i]/vsota > q0:
            return [i]

    return choices(seznam,verjetnosti)

def main():
    
    a = 1 # pomen razdalje
    b = 2.5 # pomen pher
    c = 1 # zacetni pher
    s = 0.1 # odstranitev slabih poti
    p = 0.1 # dodatek k opt poti
    q0 = 0.9 # pozresnost
    m = 10 # stevilo mravelj
    q = 100 # kolicina pher, ki ga izloci ena mravlja
    n = 10 #int(input()) #stevilo_mest
    razdalja = [[0]*n for i in range(n)]
    pher = [[c]*n for i in range(n)]
    verjetnosti = [0]*n
    seznam = [i for i in range(n)]
    lokacija = [0]*m # lokacija na kateri se nahaja i-ta mravlja
    dolzina_poti = [0]*m # razdalja, ki jo je na svoji poti opravila i-ta mravlja
    pher_dodan = [[0]*n for i in range(n)]
    min_dolzina = 999999
    opt_pot = []
    for i in range(n):
        for j in range(n):
            razdalja[i][j] = i*j+1
    korak = 0
    global inp
    inp = time.time()
    while korak < 750:
        korak += 1
        pot = [[] for i in range(m)] # pot za vsako mravljo
        neobiskana = [[1]*n for i in range(m)] # mnozica neobiskanih vozlisc za vsako mravljo (morda bolj smiselno sete za boljso casovno zahtebnost)
        pher_dodan = [[0]*n for i in range(n)] # kolicina pheranoma dodanega zaradi mravljine poti
        dolzina_poti = [0]*m
        for i in range(m):
            lokacija[i] = randint(0,n-1)
            neobiskana[i][lokacija[i]] = 2
        
        for i in range(n):      # tukaj simuliramo pot
            for j in range(m):
                if i == n-1:
                    for k in range(n):
                     if neobiskana[j][k] == 2:
                        f = k
                        dolzina_poti[j] +=  razdalja[lokacija[j]][f]
                        pot[j].append((lokacija[j],f))
                else:   
                    f = izberi_pot(j,lokacija[j],neobiskana,pher,verjetnosti,razdalja,seznam,n,a,b,q0)[0]
                    dolzina_poti[j] +=  razdalja[lokacija[j]][f]
                    pot[j].append((lokacija[j],f))
                    lokacija[j] = f
                    neobiskana[j][f] = 0
                pher[pot[j][i][0]][pot[j][i][1]] = (1-s)*pher[pot[j][i][0]][pot[j][i][1]] + s*c
                pher[pot[j][i][1]][pot[j][i][0]] = pher[pot[j][i][0]][pot[j][i][1]] 


        for  i in range(m):
            if dolzina_poti[i] == min(dolzina_poti):
                if (dolzina_poti[i] < min_dolzina):
                    min_dolzina = dolzina_poti[i]
                    opt_pot = pot[i]

        for i in range(n-1):
            pher_dodan[opt_pot[i][0]][opt_pot[i][1]] = p*(q/min_dolzina)
            pher_dodan[opt_pot[i][1]][opt_pot[i][0]] = pher[opt_pot[i][0]][opt_pot[i][1]]
        for i in range(n):
            for j in range(n):
                pher[i][j] = (1-p)*pher[i][j] + pher_dodan[i][j]
        for i in range(n-1):
            pher_dodan[opt_pot[i][0]][opt_pot[i][1]] = 0
            pher_dodan[opt_pot[i][1]][opt_pot[i][0]] = 0
    #print(dolzina_poti) # dolzina poti v zadnji iteraciji, (samo informativno)
    #print(opt_pot) # optimalna pot (to nas zanima!)
    print(min_dolzina) # dolzina opt poti (to nas zanima!)
    #print(pher) # kolicina pher ob koncu hitro opazis da so ene popolnoma polne druge prazne (samo informativno)
    global tj
    tj= time.time()
    print("Ant Colony " + str(tj-inp))
for i in range(10):
    main()
t = time.time()
print("skupni " + str(t - start))
