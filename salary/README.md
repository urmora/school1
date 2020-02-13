# Palgauuringu näide

## Võlad

Hetkel ei tea, kuidas flaski väljundis utf-8 unicode JSON-it saata. Seetõttu täpitähed on imelikud.

## Andmebaas

Algandmed on esitatud exceli kujul:

```
| Tööpere | Ametinimetus(ed) | Tase | Tase eristus | Punktid | Kuu põhipalk | Aasta kogupalk |
```

Originaalis polnud antud tase eristust (see oli taseme osa), näidet oli lihtsam korrigeerida lisades ühe täiendava tulba.

Ühele tööperele võib vastata mitu ametinimetust, seetõttu andmebaasi disainil võib kasutada kahte erinevat tabelit - ühte
tööperede ning ühte ametinimetuste ja vastavate palgaandmete jaoks. Teist tabelit esimesega seob välisvõti (foreign key).

Ametipositsiooni tase on valdavalt numbriline väärtus dimensioonis 1..7 ühe tööpere lõikes, kuid kahel sama tööpere ametil on täiendav suffix A ja B.
Seetõttu võib eeldada, et tööpere, tase ja suffix moodustavad unikaalse piirangu.

Palgaandmed on antud täisarvudena, kasutame integer(4), kuna integer(2) maksimaalne väärtus, ~32000 jääb väikeseks.

Punkte pole andmebaasis vaja, neid ei kajasta.


### Tabelite loomine

Vaata: https://www.sqlitetutorial.net/sqlite-create-table/

```
create table if not exists job_family (
  id integer primary key,
  name text not null,
  unique(name)
);

create table if not exists job_position (
  id integer primary key,
  job_family_id integer not null,
  name text not null,
  level integer(1) not null,
  level_suffix text(1) not null default '',
  month_base_salary integer(4) not null,
  annual_total_salary integer(4) not null,
  unique(job_family_id, level, level_suffix),
  foreign key (job_family_id) references job_family(id)
);
```

Lisaks loome andmete laadimiseks ajutise tabeli, mis vastab 1:1 exceli formaadile. Kuna algandmetes on osadel ridadel
palgaandmetega propleeme, expordime nad alguses tekstina.

```
create table if not exists dsa_job_family (
  family_name text not null,
  job_name text not null,
  level integer(1) not null,
  level_suffix text(1) not null default '',
  score text,
  month_base_salary text,
  annual_total_salary text
);
```


### Andmete import

Andmeid saab andmebaasi importida erineval moel, väiksemaid andmekogusid on lihtne importida
näiteks otse excelist SQL-i genereerides või kasutades CSV-d.

Antud juhul teeme CSV vahendusel, Selleks on vaja pandas nimelist pythoni teeki, mida saab installida
käsurealt

```
pip install pandas
```

või Thonny-s valides menüüst Tools > Manage packages, otsides pandas ning pannes install.

1) expordime excelist tabeli CSV formaadis faili (repositooriumis juba tehtud, salary/database.csv)
2) impordime csv faili andmebaasi käivitades salary/import.py

Ülalolev programm loeb andmed csv-st vahealasse (staging), seejärel sisestab sealt andmed kahte põhitabelisse.
Lihtsuse mõttes programm loob tabelid otse, ilma SQL failita.

https://www.sqlitetutorial.net/
https://www.sqlitetutorial.net/sqlite-inner-join/
