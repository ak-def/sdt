create table if not exists skills (
    skill_id integer primary key,
    skill_name text not null  unique,
    skilled text not null default 0,
    skill_category text,
    skill_level text 
);