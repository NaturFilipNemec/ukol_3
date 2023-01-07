from pyproj  import Transformer
import json
import requests
from json.decoder import JSONDecodeError
from math import sqrt
from statistics import mean, median 
import sys

#promeny
wgs2jtsk = Transformer.from_crs(4326,5514,always_xy=True)   # Transformacia na S-JTSK
vzdalenost = None                                                  
pomocna_vzdalenost = None
nejblizsi_kontejner = None                                          
do_geojsonu = []   #seznam, ktery slouzi na ulozeni adres do noveho souboru GEOJSON

 
try: # nacteni souboru s adresama
    with open ("adresy.geojson", encoding="utf-8") as adresy:
        data_adresy  =json.load(adresy)                             
except FileNotFoundError:
    sys.exit("Vstupni soubor adries neexistuje. zkontroluj, zda se soubor nachazi ve stejnem adresari jako tento skript a je pojmenovany spravne.")
except IOError:
    sys.exit("Soubor adres se neda nacist. Prosim opravte ho a spuste skript znova.")   
except PermissionError:
    sys.exit("Skript nema opravneni otevrit soubor s adresami.")
except JSONDecodeError:
    sys.exit("Vstupny soubor s adresami neni  validny. Prosim zkontrolujte ho a opravte ho.")
except:
    sys.exit("Neco sa nepodarilo, program se tedka ukonci.")
try: #nacteni kontejneru ze souboru
    with open("kontejnery_adresy.geojson", encoding="utf-8") as kontejnery:  
        data_kontejnery = json.load(kontejnery)                            
except FileNotFoundError:
    sys.exit("Vstupn soubor s kontejnery neexistuje. Zkontrolujte, zda se soubor nachazi ve stejnem adresari jako tento skript a je pojmenovany spravne.")
except IOError:
    sys.exit("Soubor s kontejnery se neda nacist. Prosim opravte ho a spuste skript znova.")
except PermissionError:
    sys.exit("Skript nema opravneni otevrit soubor s kontejnery.")
except JSONDecodeError:
    sys.exit("Vstupny soubor s kontejnery neni validny. Prosim zkontrolujte ho a opravte ho.")
except:
    sys.exit("Neco se nepodarilo, program se tedka ukonci.")

print("Nactenych je {pocet_adres} adresnych bodu.".format(pocet_adres = len(data_adresy["features"])))
print("Nactenych je {pocet_kotejneru} kontejneru na trideny odpad.".format(pocet_kotejneru = len(data_kontejnery["features"])))
print("Program tedka vypocitava vzdalenosti adres od kontejneru . . .")

try:       
    for adresa in data_adresy["features"]:  # Nacteni adres a jejich souradnic. Prevod na krovaka
        krovak_x = adresa["geometry"]["coordinates"][0]
        krovak_y = adresa["geometry"]["coordinates"][1]       
        krovak = wgs2jtsk.transform(krovak_x,krovak_y)
        aktualni_adresa = "{ulice} {cislo}".format(ulice = adresa["properties"]["addr:street"], cislo = adresa["properties"]["addr:housenumber"])
                
        for kontejner in data_kontejnery["features"]:  # Cyklus pro prochazani kazdym kontejnerem
            aktualny_kontejner = kontejner["properties"]["ID"]    # Nacita se ID aktualneho kontejneru
                    
            if kontejner["properties"]["PRISTUP"] == "volně":   # Rozdeleni na verejny a soukromy kontejnery
                dlz_x = kontejner["geometry"]["coordinates"][0]
                dlz_y = kontejner["geometry"]["coordinates"][1]
                vzdalenost = float(sqrt((krovak[0]-dlz_x)**2+(krovak[1]-dlz_y)**2))  # Vypocet vzdalenosti pres Pytagorovu vetu

                if pomocna_vzdalenost == None or pomocna_vzdalenost > vzdalenost:
                    pomocna_vzdalenost = vzdalenost   # Zachovani nejmensi vzdalenosti
                    nejblizsi_kontejner = aktualny_kontejner   # Zachova se ID kontejneru, kde byla nejmensi vzdalenost od domu

            elif kontejner["properties"]["PRISTUP"] == "obyvatelům domu":
                if aktualni_adresa == kontejner['properties']['STATIONNAME']: # Porovna se sformatovana adresa s polohou kontejneru, jak je stejna, vzdalenosti se priradi 0
                    pomocna_vzdalenost = 0
                else:
                    pass
        
        if pomocna_vzdalenost > 10000:
            raise Exception("Nejblizsi kontejner je dale nez 10 km. Zkuste nahrat vice kontejneru do vstupu. Program se tedka ukonci.")

        adresa["properties"]["ku_kontejneru_m"] = round(pomocna_vzdalenost) # Do slovniku se k dany adrese pripise novy klic s nejmensi vzdalenosti
        adresa["properties"]["kontejner"] = nejblizsi_kontejner # Podobne se k atribute adresy pripise novy klic s ID nejblizsiho kontejneru
        pomocna_vzdalenost = None  # Pomocna vzdalenost se vynuluje pro praci s dalsi adresou
        do_geojsonu.append(adresa)  # Do seznamu se prida zpracovana adresa

except KeyError:
    sys.exit("Soubor nema vsechny pozadovane atributy, prosim opravte ho a nactete skript znova.")

with open("adresy_kontejnery.geojson","w", encoding="utf-8") as out: # seznam s adresama se hodi do novevytvoreneho souboru
    json.dump(do_geojsonu, out, ensure_ascii = False, indent = 2)
        
vzdalenosti = [adresa["properties"]["ku_kontejneru_m"] for adresa in data_adresy["features"]]  # Promenna, do ktory se nacita seznam vypocitanych nejmensich vzdalenosti
najdi_index = (vzdalenosti.index(max(vzdalenosti)))  # Najde sa index hodnoty s nejvetsi vzdalenosti od kontejneru, aby se tak nasla i adresa mista

print("Hotovo.")
print(f"Prumerna vzdalenost ke kontejnerum je: {round(mean(vzdalenosti),1)} m")            
print(f"Median vzdalenosti ke kontejnerum je: {round(median(vzdalenosti),1)}")  # Pouziti z knihovny statistics prumer a median
print("Nejdale od kontejneru ve vzdalenosti {max_vzdalenost} m je vchod na adrese {adresa} {cd}".format(max_vzdalenost = max(vzdalenosti),adresa = data_adresy["features"][najdi_index]["properties"]["addr:street"],cd = data_adresy["features"][najdi_index]["properties"]["addr:housenumber"]))