from xlwt import Workbook
import sys

def kodneTabele(file_name):
    """
    Funkcija kot argument sprejme ime excel datoteke, kamor se izpisejo vse kodne zamenjave.
    """

    # Crke, za katere zelimo dobiti kodne zamenjave
    txt = "ČŠŽčšž" 
    # Datoteka excell kamor shranimo rezultate
    file_name = file_name+".xls"
    
    wb = Workbook()
    sheet1 = wb.add_sheet("Sheet 1")
    
    sheet1.write(1, 0, "ZNAK")  
    # Vnesi crke v prvi stolpec  
    for c in range(len(txt)):  
        sheet1.write(2+c, 0, txt[c])

    # Lista tabel
    tables_list = ["cp852", "iso8859_2", "cp1250", "mac_latin2", "utf_8", "utf_16_le", "utf_16_be"]

    # Vnesi vrednosti v celice v tabeli
    for i in range(len(tables_list)):
        # Vnesi ime kodirne tabele
        sheet1.write(0, 1+i*3, tables_list[i]) 
        sheet1.write(1, 1+i*3, "BIN")
        sheet1.write(1, 2+i*3, "DEC")
        sheet1.write(1, 3+i*3, "HEX")
        for k in range(len(txt)):
            # Lista binarnih vrednosti za en znak
            list = [format(b, '08b') for b in txt[k].encode(tables_list[i])]
            # Zdruzi binarne vrednosti za en znak v string 
            list_to_string = ''.join(map(str, list[:])) 
            sheet1.write(2+k, 1+i*3, list_to_string)
            

            # Lista decimalnih vrednosti za en znak 
            list = [str(b) for b in txt[k].encode(tables_list[i])]
            # Zdruzi decimalne vrednosti za en znak v string 
            list_to_string = ' '.join(map(str, list[:]))
            sheet1.write(2+k, 2+i*3, list_to_string)

            # Lista hexadecimalnih vrednosti za en znak 
            list = [format(b, '02x') for b in txt[k].encode(tables_list[i])]
            # Zdruzi hexadecimalne vrednosti za en znak v string
            list_to_string = ''.join(map(str, list[:])) 
            sheet1.write(2+k, 3+i*3, list_to_string)

    wb.save(file_name)

    
    print("Kodne zamenjave za črke: ", txt)
    print(20*"-")
    print("Kodne tabele so v datoteki: " , file_name)
    

def kodiranjeDekodiranje(file_in, file_out, file_name):
    """
    Funkcija kot argument sprejme vhodno .txt datoteko, ime izhodne .txt datoteke in ime .xls datoteke.
    """
    #file_in = "kodne to¦Źke.txt"
    #file_out = "dekodirano_besedilo.txt"

    f_in = open(file_in)
    txt_data = f_in.read()
    # Loci vrednosti - naredi seznam
    list_data = txt_data.split(", ") 
    f_in.close()

    tekst = ""
    vrednost = ""

    for i in range(len(list_data)):
        number = (int(list_data[i]))
        # Pretvori decimalno vrednost v string bitov npr. "01010011"
        strng = format(number, '08b') 
        if len(strng) == 8:
            # Zapis v enem bajtu 
            vrednost = strng

        if len(strng) > 8 and len(strng) < 12:
            # Zapis v dveh bajtih
            d=11-len(strng)
            vrednost = "110"
            vrednost += d*"0"
            vrednost += strng[:-6] 
            vrednost += "10"
            vrednost += strng[-6:]

        if len(strng) > 11 and len(strng) < 17:
            # Zapis v treh bajtih 
            d=16-len(strng)
            vrednost = "1110"
            vrednost += d*"0"
            vrednost += strng[:-12] 
            vrednost += "10"
            vrednost += strng[-12:-6]
            vrednost += "10"
            vrednost += strng[-6:]

        if len(strng) > 16:
            # Zapis v stirih bajtih 
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
        # Dvojiska base 
        bajti = int(vrednost,2).to_bytes(8,'big') 
        # Dekodiraj
        znak = bajti.decode("utf_8") 
        # Odrezi drugace v .txt file pred vsak znak zapisuje presledke... 
        znak=znak[-1:]
        tekst += znak

    # Zapisi rezultat v .txt datoteko
    f_out = open(file_out, "w", encoding="utf_8")
    f_out.write(tekst)
    f_out.close()

    # Dobi unikatne znake in jih soritraj po velikosti
    unikatni = ''.join(sorted(set(tekst))) 

    # Datoteka excell kamor shranimo rezultate
    file_name = file_name+".xls"
    
    wb = Workbook()
    sheet1 = wb.add_sheet("Sheet 1")
    
    # Vnesi crke v celice  
    for c in range(len(unikatni)):  
        sheet1.write(1+c, 0, unikatni[c])

    # Vnesi "glavo" tabele
    sheet1.write(0, 0, "ZNAK")
    sheet1.write(0, 1, "BIN")
    sheet1.write(0, 2, "DEC")
    sheet1.write(0, 3, "HEX")

    # Vnesi vrednosti v celice v tabeli
    for k in range(len(unikatni)):
        # Lista binarnih vrednosti za en znak
        list = [format(b, '08b') for b in unikatni[k].encode("utf_8")] 
        list_to_string = ''.join(map(str, list[:])) 
        # Zdruzi binarne vrednosti za en znak v string
        sheet1.write(1+k, 1, list_to_string)

        list = [str(b) for b in unikatni[k].encode("utf_8")] 
        # Lista decimalnih vrednosti za en znak
        list_to_string = ' '.join(map(str, list[:])) 
        # Zdruzi decimalne vrednosti za en znak v string
        sheet1.write(1+k, 2, list_to_string)

        list = [format(b, '02x') for b in unikatni[k].encode("utf_8")] 
        # Lista hexadecimalnih vrednosti za en znak
        list_to_string = ''.join(map(str, list[:])) 
        # Zdruzi hexadecimalne vrednosti za en znak v string
        sheet1.write(1+k, 3, list_to_string)

    wb.save(file_name)


    print("Dekodirano besedilo je v datoteki: " , file_out)
    print(20*"-")
    print("Unikatni znaki so v datoteki: " , file_name)



if __name__ == "__main__":
    try:
        filename_xls_1_out = sys.argv[1]
        filename_txt_in = sys.argv[2]
        filename_txt_out = sys.argv[3]
        filename_xls_2_out = sys.argv[4]


    except IndexError:
        print("Usage: python vaja2.py <output .xls file name without extension> <input .txt file name with extension> <output .txt file name with extension> <.xls output file name without extension>")
        print("Primer klica: python vaja2.py  kodne_zamenjave_1 kodne_tocke.txt besedilo.txt tabela_unikatnih")
        sys.exit(1)

    print(40*"-")
    print("Naloga 1: ")
    kodneTabele(filename_xls_1_out)
    print(40*"-")

    print(40*"-")
    print("Naloga 2: ")
    kodiranjeDekodiranje(filename_txt_in,filename_txt_out,filename_xls_2_out)
    print(40*"-")