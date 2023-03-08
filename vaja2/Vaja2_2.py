from xlwt import Workbook

file_in = "kodne to¦Źke.txt"
file_out = "dekodirano_besedilo.txt"

f_in = open(file_in)
txt_data = f_in.read()
#txt_data = "85, 269, 80, 1805" # Testni znaki UČP*
list_data = txt_data.split(", ") # Loci vrednosti - naredi listo
f_in.close()

tekst = ""
vrednost = ""

for i in range(len(list_data)):
    number = (int(list_data[i]))
    strng = format(number, '08b') # Pretvori decimalno vrednost v string bitov npr. "01010011"
    if len(strng) == 8: # Zapis v enem bajtu
        vrednost = strng

    if len(strng) > 8 and len(strng) < 12: # Zapis v dveh bajtih
        d=11-len(strng)
        vrednost = "110"
        vrednost += d*"0"
        vrednost += strng[:-6] 
        vrednost += "10"
        vrednost += strng[-6:]

    if len(strng) > 11 and len(strng) < 17: # Zapis v treh bajtih
        d=16-len(strng)
        vrednost = "1110"
        vrednost += d*"0"
        vrednost += strng[:-12] 
        vrednost += "10"
        vrednost += strng[-12:-6]
        vrednost += "10"
        vrednost += strng[-6:]

    if len(strng) > 16: # Zapis v stirih bajtih
        d=21-len(strng)
        vrednost = "11110"
        vrednost += d*"0"
        vrednost += strng[:-18] 
        vrednost += "10"
        vrednost += strng[-18:-12]
        vrednost += "10"
        vrednost += strng[-12:-6]
        vrednost += "10"
        vrednost += strng[-6:]
    
    bajti = int(vrednost,2).to_bytes(8,'big') # Dvojiska base 
    znak = bajti.decode("utf_8") # Dekodiraj
    znak=znak[-1:] # Odrezi drugace v .txt file pred vsak znak zapisuje presledke...
    tekst += znak

f_out = open(file_out, "w", encoding="utf_8")
f_out.write(tekst)
f_out.close()

unikatni = ''.join(sorted(set(tekst))) # Dobi unikatne znake in jih soritraj po velikosti

unikatni_len = len(unikatni)
file_name = "tabela_unikatnih_znakov.xls" # Datoteka excell kamor shranimo rezultate
  
wb = Workbook()
sheet1 = wb.add_sheet("Sheet 1")
  
# Vnesi crke v celice  
for c in range(unikatni_len):  
    sheet1.write(1+c, 0, unikatni[c])

# Vnesi "glavo" tabele
sheet1.write(0, 0, "ZNAK")
sheet1.write(0, 1, "BIN")
sheet1.write(0, 2, "DEC")
sheet1.write(0, 3, "HEX")

# Vnesi vrednosti v celice v tabeli
for k in range(unikatni_len):
    list = [format(b, '08b') for b in unikatni[k].encode("utf_8")] # Lista binarnih vrednosti za en znak
    list_to_string = ''.join(map(str, list[:])) # Zdruzi binarne vrednosti za en znak v string
    sheet1.write(1+k, 1, list_to_string)

    list = [str(b) for b in unikatni[k].encode("utf_8")] # Lista decimalnih vrednosti za en znak
    list_to_string = ' '.join(map(str, list[:])) # Zdruzi decimalne vrednosti za en znak v string
    sheet1.write(1+k, 2, list_to_string)

    list = [format(b, '02x') for b in unikatni[k].encode("utf_8")] # Lista hexadecimalnih vrednosti za en znak
    list_to_string = ''.join(map(str, list[:])) # Zdruzi hexadecimalne vrednosti za en znak v string
    sheet1.write(1+k, 3, list_to_string)

wb.save(file_name)

print(20*"-")
print("Dekodirano besedilo je v datoteki: " , file_out)
print(20*"-")
print("Unikatni znaki so v datoteki: " , file_name)
print(20*"-")

'''
file_in = "kodne to¦Źke.txt" #input("Ime vhodne datoteke: ") 
file_out = "test.txt" #output("Ime izhodne datoteke: ") 

f_in = open(file_in)
txt_data = f_in.read()
txt_data = "85, 196, 141, 80" #znaki UČP
list_data = txt_data.split(", ") # Loci vrednosti - naredi listo
f_in.close()

tekst = ""

for i in range(len(list_data)):
    number = (int(list_data[i]))
    strng = format(number, '08b') #Pretvori dec v string bitov npr. "010111"
    if strng[0] == '0': #Znak je dolg en bajt
        vrednost = strng
        j=0
        n=1
    if strng[0:3] == '110': #Znak je dolg 2 bajta
        vrednost = strng
        j=1
        n=2
    if strng[0:4] == '1110': #Znak je dolg 3 bajte
        vrednost = strng
        j=2
        n=3
    if strng[0:5] == '11110': #Znak je dolg 4 bajte
        vrednost = strng
        j=3
        n=4
    if strng[0:2] == '10': #Naslednji bajt od znaka ki je dolg vec kot en bajt
        vrednost += strng
        j=j-1

    if j == 0:
        bajti = int(vrednost,2).to_bytes(8,'big') #Dvojiska base 
        znak = bajti.decode("utf_8") #Dekodiraj
        print(znak)
        print(vrednost)
        tekst += znak
        #print("----")

f_out = open(file_out, "w", encoding="utf_8")
f_out.write(tekst)
f_out.close()
'''