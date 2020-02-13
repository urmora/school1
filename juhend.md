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

## Server side rakendused ja andmebaasid

Server side rakendused kasutavad tihti ka relatsioonilist andmebaasi - seal on mugav andmeid hoida, sealt saab SQL keele abil (võrdlemisi) standardselt andmeid pärida. Tüüpiliselt on andmebaasi tarvara serverlahendus, analoogselt veebiserverile. Aga arenduseks ja väga väikesteks lahendusteks võib sobida ka näiteks SQLite, mille puhul andmebaasimootor käivitatakse otse rakenduses.

Tüüpiline sündmuste ahel andmebaasi kasutavas server side rakenduses on:

1. Lehitsejast saabub päring, näiteks aadressile http://www.rakendus.ee/api/products
2. Serveri vaatenurgast küsitakse /products, server side rakenduses on keegi programmeerinud sellele vastama toodete nimekirja väljastamise, see käivitatakse
3. Väljastamiseks koostab server side rakendus SQL päringu ja edastab selle andmebaasiserverile/-mootorile
4. Andmebaasiserver/-mootor muretseb omal, optimeeritud moel, soovitud andmed ja tagastab need server side rakendusele
5. Server side rakendus, sõltuvalt kas ta on realiseeritud tavarakendusena või API-na vastavalt kas liidab andmed HTML malliga või siis konverteerib need JSON kujule ning tagastab tulemuse mõlemal juhul lehitsejale.

Näiteks oletades, et igal tootel on ainult identifikaator ja nimi ning kasutades API rakenduses Flaski ja SQLite, võiks lahendus välja näha (näite alus võetud https://test-flask.readthedocs.io/en/latest/patterns/sqlite3.html)

```
import sqlite3
import json
from flask import ( Flask, g )

app = Flask(__name__)

# Kus asub SQLite andmebaasi fail, täpsemalt edaspidi sellest
DATABASE = 'products.db'

# avab andmebaasi faili
def get_db():
    cn = getattr(g, '_database', None)
    if cn is None:
        cn = g._database = sqlite3.connect(DATABASE)
        cn.row_factory = sqlite3.Row
    return cn.cursor()

# See on tegelik API "entry point" ehk koht millele veebirakendus vastab tagastades toodete nimekirja JSON formaadis
@app.route('/products')
def product_list():
    db = get_db()
    data = db.execute('select id, name from products order by name').fetchall()
    return json.dumps( [dict(ix) for ix in data] )
   
# Rakenduse töö lõppedes on vajalik andmebaasi fail sulgeda
@app.teardown_appcontext
def close_connection(exception):
    cn = getattr(g, '_database', None)
    if cn is not None:
        cn.close()
```

