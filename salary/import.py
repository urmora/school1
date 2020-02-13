import pandas
import sqlite3

cn = sqlite3.connect('salary.db')

# Puhastame baasi
cn.execute('drop table if exists job_position')
cn.execute('drop table if exists job_family')
cn.execute('drop table if exists dsa_job_family')

# Lisame tööpered
cn.execute("""
create table job_family (
  id integer primary key,
  name text not null,
  unique(name)
);
""")

# Lisame ametid
cn.execute("""
create table job_position (
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
""")

# Laadimisala
cn.execute("""
create table dsa_job_family (
  family_name text not null,
  job_name text not null,
  level integer(1) not null,
  level_suffix text(1),
  score text,
  month_base_salary text,
  annual_total_salary text
);
""")

df = pandas.read_csv(
    'palgad.csv',
    sep = ';',
    header = 0,
    names = ['family_name', 'job_name', 'level', 'level_suffix', 'score', 'month_base_salary', 'annual_total_salary']
)
df.to_sql('dsa_job_family', cn, if_exists='append', index=False)

# Lisame tööpered, unikaalselt
cn.execute("""
insert into job_family (name)
select
    distinct family_name
from
    dsa_job_family
""")

# Lisame ametid
cn.execute("""
insert into job_position (job_family_id, name, level, level_suffix, month_base_salary, annual_total_salary)
select
    id,
    job_name,
    level,
    coalesce(level_suffix, ''),
    cast(replace(month_base_salary, ' ', '') as integer),
    cast(replace(annual_total_salary, ' ', '') as integer)
from
    dsa_job_family dsa
    inner join job_family jf on jf.name = dsa.family_name
where
    cast(replace(month_base_salary, ' ', '') as integer) is not null
    and
    cast(replace(annual_total_salary, ' ', '') as integer) is not null
""")

cn.commit()
cn.close()