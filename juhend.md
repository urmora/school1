# Maod, pläskud ja veebirakendused

## Veebirakendusest üldisest

Veebirakendusest on kasulik aru saada väga üldisel tasemel, eristades kõigepealt:

* Client side - asjad, mis juhtuvad rakenduse kasutaja internetilehitsejas
* Server side - asjad, mis juhtuvad veebiserveris

Ja tähtis on aru saada ka kuidas client side ja server side omavahel läbi saavad.
Näiteks kui kasutaja sisestab lehitsejasse aadressi www.minurakendus.ee juhtub järgmine:

1. Lehitseja pöördub kohaliku nimeserveri poole (DNS) ja küsib, mis IP aadress vastab www.minurakendus.ee-le
2. Nimeserver lahendab nimest IP aadressi, kui ise ei tea, küsib teiste serverite käest ja annab selle lehitsejale tagasi
3. Lehitseja teeb saadud aadressile ühenduse, vaikimisi porti 80 ja saadab sinna HTTP päringu - standardformaadis andmete 
kogu millest peamine on millist aadressi ta serverist otsib, vaikimisi on see /
4. Veebiserver saab päringu, töötleb seda ja saadab tagasi kas siis aadressile vastava dokumendi, programmi vastuse või ka 
näiteks teate, et sellist asja selles serveris pole
5. Kui vastus on HTML dokument, vaatab lehitseja sinna sisse ja kui leiab sealt viited lehe kuvamiseks vajalikele teistele 
ressurssidele (pildid, CSS, välised JavaScripti) failid, siis kordub tegevus punktist 3 igale ressursile.

Näiteks küsides aadressi http://www.küps.ee/ saab tuleb veebiserverist kohale kõigepealt HTML dokument:

```
<html lang="et">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>Pagarid on ametis | Work in progress</title>
		<meta name="google-site-verification" content="iYclTs0d8nJX7483h5VnontMREmDPXyaLanc6Cx2heY" />
		<link href="css/app.css" rel="stylesheet" type="text/css"></link>
	</head>
	<body>
		<img class="centered" src="img/bread.png" title="Pagarid alles kergitavad / Bread is still in the making" />
	</body>
</html>
```

Kust on näha, et lisaks on vaja lehe kuvamiseks CSS faili http://www.küps.ee/css/app.css ning pilti aadressilt
http://www.küps.ee/img/bread.png

Antud veebileht on nn. staatiline, serveris pole peale veebiserveri muid programme. Staatiline võib ka olla
veebirakendus kui kogu töö tehakse ära client side, tüüpiliselt JavaScriptis. 

Kui serveris oleks vastanud isetehtud programm (kas siis otse või "läbi" veebiserveri), siis räägitakse server side
rakendusest, olgu ta siis tehtud Pythonis, Rubys, C#-is vms. Oluline vahe on, kus programm käib - kas serveris või kliendi lehitsejas.
Loomulikult on tänapäeval rakendused peaaegu alati segu client side ja server side rakendustest.


