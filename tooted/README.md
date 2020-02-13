# Andmebaasi kasutamise näide

## Baasi (taas)loomine

Kui Python 3 ja Flask on olemas juba arvutis, siis tuleb käivitada command promptis programmis flaski shellis init_db:

```
set FLASK_APP=products.py
set FLASK_ENV=development
flask shell

from init_products import init_db
init_db()
```

See loob andmebaasi tabeli ja lisab sinna mõned näidisread.

### Andmebaasi loomine Thonnys

Võta lahti init_products.py, käivita see. Seejärel vajuta Control+C.
Allolevas shelli aknas kirjuta:

```
init_db()
```

Sulle peab tekkima programmikataloogi fail products.db

## Rakenduse käivitamine

```
set FLASK_APP=products.py
set FLASK_ENV=development
flask shell

flask run
```

### Thonnys rakenduse käivitamine

Ava products.py ja käivita see

Mõlemal juhul käivitub rakendus aadressil http://localhost:5000
ja tagastab tootenimekirja aadressil http://localhost:5000/products


