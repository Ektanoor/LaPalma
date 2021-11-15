--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: acceleration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acceleration (
    event character varying(16) NOT NULL,
    tstamp timestamp with time zone,
    coors public.geography(PointZM,4326),
    intensity character varying(16),
    type integer,
    location character varying(32),
    direction character varying(2),
    station character varying(50),
    distance real,
    accel_ns real,
    accel_v real,
    accel_ew real
);


ALTER TABLE public.acceleration OWNER TO postgres;

--
-- Name: geonames; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.geonames (
    geonameid integer NOT NULL,
    name character varying(200),
    asciiname character varying(200),
    alternatename text,
    coors public.geography(Point,4326),
    feature_class character(1),
    feature_code character varying(10),
    country_code character varying(2),
    cc2 character varying(200),
    admin1 character varying(20),
    admin2 character varying(80),
    admin3 character varying(20),
    admin4 character varying(20),
    population bigint,
    elevation integer,
    dem integer,
    timezone character varying(40),
    date timestamp with time zone
);


ALTER TABLE public.geonames OWNER TO postgres;

--
-- Name: intensities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.intensities (
    event character varying(16) NOT NULL,
    min integer,
    max integer
);


ALTER TABLE public.intensities OWNER TO postgres;

--
-- Name: intensities_accel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.intensities_accel (
    event character varying(16) NOT NULL,
    min integer,
    max integer
);


ALTER TABLE public.intensities_accel OWNER TO postgres;

--
-- Name: intensity_coors; Type: TABLE; Schema: public; Owner: quakewatcher
--

CREATE TABLE public.intensity_coors (
    event character varying(16) NOT NULL,
    coors public.geography(Point,4326) NOT NULL,
    min integer NOT NULL,
    max integer NOT NULL
);


ALTER TABLE public.intensity_coors OWNER TO quakewatcher;

--
-- Name: intensity_maps; Type: TABLE; Schema: public; Owner: quakewatcher
--

CREATE TABLE public.intensity_maps (
    event character varying(16) NOT NULL,
    min integer NOT NULL,
    max integer NOT NULL,
    location character varying(150) NOT NULL,
    province character varying(10),
    checking character varying(3)
);


ALTER TABLE public.intensity_maps OWNER TO quakewatcher;

--
-- Name: quakes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quakes (
    event character varying(16) NOT NULL,
    tstamp timestamp with time zone,
    coors public.geography(PointZM,4326),
    intensity character varying(16),
    type integer,
    location character varying(32),
    direction character varying(2)
);


ALTER TABLE public.quakes OWNER TO postgres;

--
-- Name: acceleration acceleration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceleration
    ADD CONSTRAINT acceleration_pkey PRIMARY KEY (event);


--
-- Name: geonames geonames_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geonames
    ADD CONSTRAINT geonames_pkey PRIMARY KEY (geonameid);


--
-- Name: intensities_accel intensities_accel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intensities_accel
    ADD CONSTRAINT intensities_accel_pkey PRIMARY KEY (event);


--
-- Name: intensities intensities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intensities
    ADD CONSTRAINT intensities_pkey PRIMARY KEY (event);


--
-- Name: intensity_coors intensity_coors_pkey; Type: CONSTRAINT; Schema: public; Owner: quakewatcher
--

ALTER TABLE ONLY public.intensity_coors
    ADD CONSTRAINT intensity_coors_pkey PRIMARY KEY (event, coors, min, max);


--
-- Name: intensity_maps intensity_maps_pkey; Type: CONSTRAINT; Schema: public; Owner: quakewatcher
--

ALTER TABLE ONLY public.intensity_maps
    ADD CONSTRAINT intensity_maps_pkey PRIMARY KEY (event, location, min, max);


--
-- Name: quakes quakes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quakes
    ADD CONSTRAINT quakes_pkey PRIMARY KEY (event);


--
-- Name: event_coors_idx; Type: INDEX; Schema: public; Owner: quakewatcher
--

CREATE INDEX event_coors_idx ON public.intensity_coors USING btree (event);


--
-- Name: event_maps_idx; Type: INDEX; Schema: public; Owner: quakewatcher
--

CREATE INDEX event_maps_idx ON public.intensity_maps USING btree (event);


--
-- Name: TABLE acceleration; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.acceleration TO quakewatcher;


--
-- Name: TABLE geography_columns; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.geography_columns TO quakewatcher;


--
-- Name: TABLE geometry_columns; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.geometry_columns TO quakewatcher;


--
-- Name: TABLE geonames; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.geonames TO quakewatcher;


--
-- Name: TABLE intensities; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.intensities TO quakewatcher;


--
-- Name: TABLE intensities_accel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.intensities_accel TO quakewatcher;


--
-- Name: TABLE quakes; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.quakes TO quakewatcher;


--
-- Name: TABLE spatial_ref_sys; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.spatial_ref_sys TO quakewatcher;


--
-- PostgreSQL database dump complete
--

