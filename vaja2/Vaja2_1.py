from xlwt import Workbook

txt = "ČŠŽčšž" # Crke katere zelimo dobiti kodne zamenjave
txt_len = len(txt)
file_name = "tabela_kodnih_zamenjav.xls" # Datoteka excell kamor shranimo rezultate
  
wb = Workbook()
sheet1 = wb.add_sheet("Sheet 1")
  
sheet1.write(1, 0, "ZNAK")  
# Vnesi crke v celice  
for c in range(txt_len):  
    sheet1.write(2+c, 0, txt[c])

# Lista tabel
tables_list = ["cp852", "iso8859_2", "cp1250", "mac_latin2", "utf_8", "utf_16_le", "utf_16_be"]

# Vnesi vrednosti v celice v tabeli
for i in range(len(tables_list)):
    sheet1.write(0, 1+i*3, tables_list[i]) # Vnesi ime kodirne tabele
    sheet1.write(1, 1+i*3, "BIN")
    sheet1.write(1, 2+i*3, "DEC")
    sheet1.write(1, 3+i*3, "HEX")
    for k in range(txt_len):
        list = [format(b, '08b') for b in txt[k].encode(tables_list[i])] # Lista binarnih vrednosti za en znak
        list_to_string = ''.join(map(str, list[:])) # Zdruzi binarne vrednosti za en znak v string
        sheet1.write(2+k, 1+i*3, list_to_string)

        list = [str(b) for b in txt[k].encode(tables_list[i])] # Lista decimalnih vrednosti za en znak
        list_to_string = ' '.join(map(str, list[:])) # Zdruzi decimalne vrednosti za en znak v string
        sheet1.write(2+k, 2+i*3, list_to_string)

        list = [format(b, '02x') for b in txt[k].encode(tables_list[i])] # Lista hexadecimalnih vrednosti za en znak
        list_to_string = ''.join(map(str, list[:])) # Zdruzi hexadecimalne vrednosti za en znak v string
        sheet1.write(2+k, 3+i*3, list_to_string)

wb.save(file_name)

print(20*"-")
print("Kodne zamenjave za črke: ", txt)
print(20*"-")
print("Kodne tabele so v datoteki: " , file_name)
print(20*"-")
