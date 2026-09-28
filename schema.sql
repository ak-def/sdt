create table if not exists skills (
    skill_id integer primary key,
    skill_name text not null  unique,
    skilled text not null default 0,
    skill_category text,
    skill_level text 
);

create table if not exists certifications (
    cert_id integer primary key,
    cert_name text not null unique,
    cert_organization text not null,
    status text not null,
    cert_category text
);

create table if not exists applied_jobs(
    job_id integer primary key, 
    company_name text not null,
    job_title text not null,
    job_location text
)