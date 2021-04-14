create table students
(
    id serial primary key,
    name text not null,
    email text not null,
    password text not null,
    group_id text not null,
    is_sick boolean default false
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