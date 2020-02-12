# Maod, pläskud ja veebirakendused

## Veebist üldisest

Veebirakendusest on kasulik aru saada väga üldisel tasemel, eristades kõigepealt:

* Client side - asjad, mis juhtuvad rakenduse kasutaja internetilehitsejas. Tihti nimetatakse seda ka frontend
* Server side - asjad, mis juhtuvad veebiserveris. Tihti nimetatakse seda osa backend.

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

## Server side rakenduse siseelu

Server side rakendus on tüüpiliselt nagu väike omaette veebiserver - talle edastatakse päringu aadress ja sellega kaasa antud andmed,
rakendus vaatab aadressi pealt, millist tegevust ta peaks sooritama, näiteks baasist küsima andmeid ja need väljastama.

Server side rakendused võib jaga kahte liiki:

* Tavarakendused võtavad päringu, hangivad vajalikud andmed ja väljastavad vastuse HTML lehena. Lehitseja vaatest oleks tavarakenduse vastus nagu tavaline veebileht, lihtsalt see pannakse serveris dünaamiliselt kokku. Reaalses elus tavarakendused on tihti hübriidid - osa andmest hangitakse üle API-de.
* HTTP API-d suhtlevad reeglina ainult "puhaste" andmetega, kokkulepitud andmeformaatides. Nende vastustel pole HTML-i ja veebilehe kujundusega mingit pistmist. Enamasti on andmevahetuse formaadiks JSON. Näiteks kui client side programmil (lehitsejas töötav JavaScript) on vaja toodete nimekirja, küsib ta üle API andmed serverist, paigutab andmed HTML malli ja seejärel lisab saadud (renderdatud) HTML-i veebilehele.

Kumba lähenemist süsteemis kasutada on üsna oluline esimene arhitektuurne otsus. Erinevate ülesannete jaoks sobivad erinevad asjad, alati loeb ka arendustiimi senine kogemus.



