from math import ceil
import sys
from hashlib import md5
import os
from xlwt import Workbook

def kompresiraj(ST):
    """Kompresira zaporedje bajtov ST v kompresijsko kodo KT."""

    # inicializacija slovarja PT - vsi veljavni 8-bitni znaki
    dict_size = 256
    PT = {bytes([i]): i for i in range(dict_size)}

    KT = []

    # 1. korak:
    # Preberemo prvi znak iz tabele s sporocilom
    s = bytes([ST[0]])

    # 2. korak:
    # Gremo skozi celotno tabelo s sporocilom, do zadnjega znaka
    for i in range(1, len(ST)):
        # Preberemo i-ti znak iz tabele s sporocilom
        t = bytes([ST[i]])
        # Spnemo prejsnji znak s in trenutni znak t
        u = s + t
        # Ce je u v PT
        if u in PT:
            s = u
        # Ce ni u v PT
        else:
            # Pripnemo vrednost znaka iz PT s kljucem s v KT
            KT.append(PT[s])
            # V PT dodamo nov kljuc u (v bajtih) z vrednostjo dict_size
            PT[u] = dict_size
            # dic_size je na zacetku 256, nato ga v vsaki iteraciji povecamo za 1
            dict_size += 1
            # s postane zadnji prebrani znak 
            s = t

    # 3. korak:
    # Pripnemo vrednost iz slovarja PT s kljucem s (zadnji znak) v tabelo KT
    KT.append(PT[s])
    #print(PT)
 
    return KT
 
def dekompresiraj(KT): 
    """Dekompresira kompresijsko kodo KT v zaporedje bajtov ST."""
    # gradimo inverzni slovar PT - vsi veljavni 8-bitni znaki
    dict_size = 256
    PT = {i: bytes([i]) for i in range(dict_size)}

    ST = []
    

    # TODO: implementiraj dekompresijo po postopku LZW

    # Preberi prvi kod c iz vhodne tabele KT
    c = KT[0]
    # Preberi vrednost niza iz slovarja PT
    s = PT[c]
    # Shranimo prejsnji niz v spremenljivko
    s_pr = s
    # V izhodno tabelo ST vpisi niz znakov s iz PT s kljucem c
    ST.append(s)
    #for i in range(0, len(KT)):
    for i in range(1, len(KT)):
        # Iz kodne tabele vzamemo kljuc
        c = KT[i]
        # Ce je kljuc v PT
        if c in PT:
            # Poiscemo vrednost za kljuc c
            s = PT[c]
            # Dodamo vrednost v tabelo ST
            ST.append(s)
            # Sestavimo prejsnjo vrednost s_pr in prvi znak nove        
            nova = s_pr + bytes([s[0]])
            # Zapisemo nov niz v PT
            PT[dict_size]=bytes(nova)
            dict_size+=1

            # Shranimo prejsnjo vrednost s
            s_pr = s
            
        else:
            # Prvi znak niza (t||z||t)
            t = bytes([s[0]])
            # Poljubni niz znakov z
            z  = bytes(s[1:])
            # Na konec zadnjega dekodiranega niza pripnemo prvi znak niza t
            s = t + z + t
            # Pripnemo niz v seznam ST
            ST.append(s)
            # Shrani zadnji niz
            s_pr = s
            # Vpisi nov niz na prazno mesto v slovar PT
            PT[dict_size]= s
            dict_size+=1
    
    
    rezultat = bytes()
    for element in ST:
        rezultat += element
    return rezultat

def izracunaj_velikost(KT):
    # TODO: implementiraj funkcijo, ki izračuna velikost kompresiranega
    #       sporočila (KT), če bi ga zakodirali v bajtih

    vrednost = 0
    for index, i in enumerate(KT):
        # Pridobimo string binarne vrednosti za vsako stevilko v KT
        binary = bin(i)
        # Odstranimo prefix 0b
        binary = binary[2:]
        # Sestejemo stevilo bajtov za zapis binarne vrednosti
        vrednost += int(ceil(len(binary)/8))
    
    return vrednost

if __name__ == "__main__":

    try:
        file_name_in = sys.argv[1]
        file_name_out = sys.argv[2]
        if file_name_in == "test":
            bajti = b"TRALALALALA"
        else:
            with open(file_name_in, "rb") as f:
                    bajti = f.read()


    except IndexError:
        print("Usage: python vaja3.py <input file> <output file> ")
        print("Primer klica: python vaja3.py  besedilo.txt results.txt")
        sys.exit(1)


    KT = kompresiraj(bajti)
    ST = dekompresiraj(KT)

    vsebina = ST

    with open(file_name_out, 'wb') as fo:
                fo.write(vsebina)
                fo.close()

    print(f"Rezultat dekodirnika za vhodno datoteko: {file_name_in}")
    try:
        # Preveri ce se HASH vrednosti ujemata
        hash_res_input = md5(open(file_name_in, 'rb').read()).hexdigest()
        hash_res_output = md5(open(file_name_out, 'rb').read()).hexdigest()
        print(f"MD5 vhodna datoteka:\t{hash_res_input}\nMD5 izhodna datoteka:\t{hash_res_output}")
        print(f"Isti MD5 izvlecek:\t{hash_res_input==hash_res_output}")
    except:
        print("Ne morem izracunati MD5 izvlecka.")
    print(80*'-')
    print(f"1. Preizkus gospodarnosti kodiranja na različnih vrstah datotek: {file_name_in}")
    velikost_kompresiran = izracunaj_velikost(KT)
    print(f"Velikost kodiranega sporocila:\t\t{velikost_kompresiran} bajtov")
    velikost_original = os.stat(file_name_in).st_size
    print(f"Velikost originalnega sporocila:\t{velikost_original} bajtov")
    razmerje = velikost_original/velikost_kompresiran
    razmerje_2 = velikost_kompresiran/velikost_original
    print(f"Razmerje izvorna/kompresirana datoteka:\t{razmerje:.4f}")
    print(f"Razmerje kompresirana/izvorna datoteka:\t{razmerje_2:.4f}")
    print(80*'-')

    # Ce je vhodna datoteka besedilo.txt izvedemo preizkus delnega kodiranja nekompresirane datoteke
    if file_name_in == 'besedilo.txt':
        print(f"2. Preizkus gospodarnosti kodiranja pri delnem kodiranju nekompresirane datoteke: besedilo.txt")
        print()
        wb = Workbook()
        sheet1 = wb.add_sheet("Sheet 1")
        sheet1.write(0,0, 'besedilo.txt')
        sheet1.write(1,0, 'datoteka [MB]')
        sheet1.write(1,1, 'sporocilo [MB]')
        sheet1.write(1,2, 'izvorna/kompresirana')
        sheet1.write(1,3, 'kompresirana/izvorna')

        st = 1
        # Izvorno datoteko razdelimo na vec sekvenc po 50 000 bajtov
        for i in range(50000,len(bajti),50000):
            # Vzamemo dolzino datoteke od zacetka do konca neke sekvence
            bajti_original = bajti[0:i]
            # Za vsako dolzino izvorne datoteke izdelamo kompresirano tabelo
            KT = kompresiraj(bajti_original)
            # Izracunamo velikost kompresiranega sporocila
            velikost_kompresiran = izracunaj_velikost(KT)
            print(f"Rezultat za velikost datoteke:\t\t{(i/1000000):.2f} MB")
            print(f"Velikost kodiranega sporocila:\t\t{(velikost_kompresiran/1000000):.2f} MB")
            # Izracunamo razmerje kompresirane in izvorne datoteke 
            razmerje = len(bajti_original)/velikost_kompresiran
            razmerje_2 = velikost_kompresiran/len(bajti_original)
            print(f"Razmerje izvorna/kompresirana datoteka:\t{(razmerje):.4f}")
            print(f"Razmerje kompresirana/izvorna datoteka:\t{(razmerje_2):.4f}")
            sheet1.write(1+st,0, (i/1000000))
            sheet1.write(1+st,1, (velikost_kompresiran/1000000))
            sheet1.write(1+st,2, razmerje)
            sheet1.write(1+st,3, razmerje_2)
            st+=1
            print(40*'-')
        wb.save('delno_kodiranje.xls')
        print('Rezultat delnega kodiranja zapisan v datoteki delno_kodiranje.xls')

            


    



        