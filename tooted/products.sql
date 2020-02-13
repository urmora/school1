drop table if exists products;

create table products
(
    id integer primary key,
    name text not null
);

insert into products(name) values('Aabitsa');
insert into products(name) values('Praktiline');
insert into products(name) values('Teadus');
