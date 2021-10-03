create table students
(
    id serial primary key,
    name text not null,
    middle_name text not null,
    email text not null,
    password text not null,
    group_id text not null,
    is_sick boolean default false,
    is_vaccinated boolean default false,
    sick_expires date null,
    vaccinated_expires date null
);

create table teachers
(
    id serial primary key,
    name text not null,
    email text not null,
    password text not null
);

create table schedule
(
    teacher_id integer,
    class text not null,
    time text not null,
    subject text not null,
    group_id text not null
);