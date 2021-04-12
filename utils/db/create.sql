create table if not exists students
(
    chat_id   bigint            not null
        constraint students_pk
            primary key,
    name      text,
    surname   text,
    email     text,
    password  text,
    group     text,
    is_sick   boolean,
);

alter table students
    owner to postgres;

create unique index if not exists students_id_uindex
    on students (id);


create table if not exists teachers
(
    chat_id   bigint            not null
        constraint teachers_pk
            primary key,
    name      text,
    surname   text,
    email     text,
    password  text,
);

alter table teachers
    owner to postgres;

create unique index if not exists teachers_id_uindex
    on teachers (id);