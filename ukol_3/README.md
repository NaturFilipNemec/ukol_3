Vzdálenost ke kontejnerům

Zadání:
Pro zvolenou množínu adresních bodů a množinu kontejnerů na tříděný odpad zjistěte průměrnou a maximální vzdálenost k nejbližšímu veřejnému kontejneru na tříděný odpad. Pro každý adresní bod tedy určete nejbližší veřejný kontejner na tříděný odpad a následně z těchto vzdáleností spočtěte průměr a maximum. Průměr a maximum vypište, pro maximum vypište i adresu, která má nejbližší veřejný kontejner nejdále.

Uživatelská dokumentace:
Do programu vstupují dva GEOJSON soubory, jeden s adresa a druhy s kontejnerama. Oba vstupy jsou ošetřeny pomoci try a expect aby uzivateli nahlasilo pripadnou chybu v souborech. Program postupne prochazi kazdou adresu a kontejnery. Pomoci Pythagorovy veta pocita vzdalenosti mezi nima a uklada nejmensi vzdalenost kazde adresy ke verejnemu kontejneru a ulozi i ID do seznamu nejblizsich kontejneru. Pokud je nejmensi vzdalenost ke kontejneru vetsi jak 10 km, program na to upozorni. Nasledne vypise median a prumer nejblizsich kontejneru a take jaka adresa to má nejdale. Jako vystup jeste program vytvori GEOJSON soubor adresy_kontejnery.geojson, kde jsou zapsany vsechny adresy a k nim prislusnej nejblizsi kontejner a jeho vzdalenost k nemu.

chtěl bych se omluvit ale nejakym zpusobem na zacatku se mi odpojil repositář na githubu od slozky a vsiml jsem si toho az po dokonceni celeho ukolu. Tedy postupny vyvoj aplikace nelze nalezt
