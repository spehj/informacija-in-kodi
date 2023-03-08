
import numpy as np
import math
import sys

def calculate_h(znaki,n):
    """
    Funkcija kot argument sprejme znake prebrane datoteke in število možnih členov nizov (n). Kot izhod vrne seznam izračunanih etropij na kombinacijo oz. na znak.
    """
    # H/kombinacijo
    hs = []
    # H/znak
    hsZnak = []
    
    # Niz spremenimo v zaporedje kombinacij
    # Za vsako kombinacijo znakov od 1 do 5
    for i in range(1, n+1):
        diction = {}
        noviNiz = []

        # Pripravi nize znakov glede na kombinacijo
        for j in range(len(znaki)):
            comb = znaki[j:j+i]
            if len(comb) == i:
                noviNiz.append(comb)
                if comb in diction:
                    diction[comb]+=1
                else:
                    diction[comb] = 1

        # Izracunaj H
        h = 0
        for k in diction.values():
            h += (k/len(noviNiz))*math.log2((k/len(noviNiz)))
        h = -h

        print(f"H{i}: {h:.2f} bit/kombinacijo")
        print(f"H{i}: {(h/i):.2f} bit/znak")
        
        h_i = h/i
        h = '{:.4f}'.format(h)
        h_i = '{:.4f}'.format(h_i)
        hs.append(h)
        hsZnak.append(h_i)
        print()

    print(f"List of H/kombinacijo: {hs}")
    print(f"List of H/znak: {hsZnak}")
    return hs, hsZnak

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        n = int(sys.argv[2])

    except IndexError:
        print("Usage: python vaja1.py <filename> <number of combinations>")
        sys.exit(1)

    # Odpri datoteko
    if filename == "default":
        files = ['datoteke/slika.bmp', 'datoteke/slika.png', 'datoteke/slika.jpeg', 'datoteke/posnetek.wav','datoteke/posnetek.mp3','datoteke/posnetek.ogg', 'datoteke/posnetek.flac','datoteke/besedilo.txt','datoteke/besedilo.zip']
        for file in files:
            with open(file, "rb") as f:
                vsebina = f.read()

            print(f"Results for {file}:")
            title = "Rezulat za "+ file
            hCombs, hChars = calculate_h(vsebina,n)

            # Rezultate zapisemo v .txt datoteko
            with open('results1.txt', 'a') as fi:
                fi.write(title)
                fi.write('\n')
                fi.write('Rezultat: H/niz:\t')
                fi.write(str(hCombs))
                fi.write('\n')
                fi.write('Rezultat: H/znak:\t')
                fi.write(str(hChars))
                fi.write('\n')
                fi.write('\n')

            print()
            
    else: 
        with open(filename, "rb") as f:
            vsebina = f.read()
        print(f"Results for {filename}:")
        title = "Rezultat za "+ filename
        hCombs, hChars = calculate_h(vsebina,n)
        
        # Rezultate zapisemo v .txt datoteko
        with open('results1.txt', 'w') as fi:
            fi.write(title)
            fi.write('\n')
            fi.write('Rezultat: H/niz:\t')
            fi.write(str(hCombs))
            fi.write('\n')
            fi.write('Rezultat: H/znak:\t')
            fi.write(str(hChars))
            fi.write('\n')
            fi.write('\n')

    
    
    