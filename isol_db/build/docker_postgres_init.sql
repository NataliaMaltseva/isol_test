CREATE USER postgres WITH PASSWORD 'test123';

CREATE DATABASE IF NOT EXISTS isoldb_test
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE IF NOT EXISTS public.detect_video
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    x_top_left double precision,
    y_top_left double precision,
    width double precision,
    height double precision,
    id_obj integer,
    time_stp timestamp with time zone,
    time_ex double precision
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.detect_video
    OWNER to postgres;