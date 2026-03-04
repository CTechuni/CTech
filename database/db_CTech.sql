--
-- PostgreSQL database dump
--

\restrict 8lSEqeaa21IEKvZAWDV2TYWKgSKh0fgdwvisIG3wmkgNSptYlfddmMZGCE6bBqg

-- Dumped from database version 16.10
-- Dumped by pg_dump version 16.10

-- Started on 2026-02-10 10:35:51

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 24711)
-- Name: communities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.communities (
    id_community integer NOT NULL,
    name_community character varying(150) NOT NULL,
    description_community text,
    status_community character varying(150) NOT NULL,
    code character varying(50) NOT NULL,
    access_code character varying(50)
);


ALTER TABLE public.communities OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24710)
-- Name: communities_id_community_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.communities_id_community_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.communities_id_community_seq OWNER TO postgres;

--
-- TOC entry 5049 (class 0 OID 0)
-- Dependencies: 217
-- Name: communities_id_community_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.communities_id_community_seq OWNED BY public.communities.id_community;


--
-- TOC entry 230 (class 1259 OID 24794)
-- Name: educational_content; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.educational_content (
    id_content integer NOT NULL,
    title character varying(255) NOT NULL,
    description_content text,
    url_file character varying(150) NOT NULL,
    type_content character varying(150) NOT NULL,
    area_id integer,
    level_id integer,
    author_id integer,
    upload_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status_content character varying(50)
);


ALTER TABLE public.educational_content OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 24793)
-- Name: educational_content_id_content_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.educational_content_id_content_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.educational_content_id_content_seq OWNER TO postgres;

--
-- TOC entry 5050 (class 0 OID 0)
-- Dependencies: 229
-- Name: educational_content_id_content_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.educational_content_id_content_seq OWNED BY public.educational_content.id_content;


--
-- TOC entry 238 (class 1259 OID 24902)
-- Name: event_registrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.event_registrations (
    id_event_registration integer NOT NULL,
    id_user integer,
    id_event integer,
    date_registration timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.event_registrations OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 24901)
-- Name: event_registrations_id_event_registration_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.event_registrations_id_event_registration_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.event_registrations_id_event_registration_seq OWNER TO postgres;

--
-- TOC entry 5051 (class 0 OID 0)
-- Dependencies: 237
-- Name: event_registrations_id_event_registration_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.event_registrations_id_event_registration_seq OWNED BY public.event_registrations.id_event_registration;


--
-- TOC entry 236 (class 1259 OID 24888)
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    id_event integer NOT NULL,
    title character varying(255) NOT NULL,
    description_event text,
    date_events date,
    time_events time without time zone,
    place character varying(155) NOT NULL,
    url_form character varying(255) NOT NULL,
    image character varying(255) NOT NULL,
    created_by integer,
    status character varying(50) NOT NULL
);


ALTER TABLE public.events OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 24887)
-- Name: events_id_event_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_id_event_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_id_event_seq OWNER TO postgres;

--
-- TOC entry 5052 (class 0 OID 0)
-- Dependencies: 235
-- Name: events_id_event_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_id_event_seq OWNED BY public.events.id_event;


--
-- TOC entry 224 (class 1259 OID 24761)
-- Name: invitation_codes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invitation_codes (
    id_code integer NOT NULL,
    code character varying(150) NOT NULL,
    community_id integer,
    creation_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    expiration_date timestamp without time zone
);


ALTER TABLE public.invitation_codes OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24760)
-- Name: invitation_codes_id_code_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invitation_codes_id_code_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invitation_codes_id_code_seq OWNER TO postgres;

--
-- TOC entry 5053 (class 0 OID 0)
-- Dependencies: 223
-- Name: invitation_codes_id_code_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invitation_codes_id_code_seq OWNED BY public.invitation_codes.id_code;


--
-- TOC entry 228 (class 1259 OID 24785)
-- Name: learning_levels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.learning_levels (
    id_level integer NOT NULL,
    name_level character varying(150) NOT NULL,
    description text
);


ALTER TABLE public.learning_levels OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 24784)
-- Name: learning_levels_id_level_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.learning_levels_id_level_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.learning_levels_id_level_seq OWNER TO postgres;

--
-- TOC entry 5054 (class 0 OID 0)
-- Dependencies: 227
-- Name: learning_levels_id_level_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.learning_levels_id_level_seq OWNED BY public.learning_levels.id_level;


--
-- TOC entry 234 (class 1259 OID 24870)
-- Name: mentorship_registrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mentorship_registrations (
    id_registration integer NOT NULL,
    id_user integer,
    id_mentorship integer,
    date_registration timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50) NOT NULL
);


ALTER TABLE public.mentorship_registrations OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 24869)
-- Name: mentorship_registrations_id_registration_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mentorship_registrations_id_registration_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mentorship_registrations_id_registration_seq OWNER TO postgres;

--
-- TOC entry 5055 (class 0 OID 0)
-- Dependencies: 233
-- Name: mentorship_registrations_id_registration_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mentorship_registrations_id_registration_seq OWNED BY public.mentorship_registrations.id_registration;


--
-- TOC entry 232 (class 1259 OID 24856)
-- Name: mentorships; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mentorships (
    id_mentorship integer NOT NULL,
    title character varying(255) NOT NULL,
    description_mentorship text,
    date_mentorship timestamp without time zone,
    hour_mentorship time without time zone,
    form_link character varying(255) NOT NULL,
    minimum_quota integer,
    maximum_capacity integer,
    area_id integer,
    status character varying(50) NOT NULL
);


ALTER TABLE public.mentorships OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 24855)
-- Name: mentorships_id_mentorship_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mentorships_id_mentorship_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mentorships_id_mentorship_seq OWNER TO postgres;

--
-- TOC entry 5056 (class 0 OID 0)
-- Dependencies: 231
-- Name: mentorships_id_mentorship_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mentorships_id_mentorship_seq OWNED BY public.mentorships.id_mentorship;


--
-- TOC entry 220 (class 1259 OID 24720)
-- Name: profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profiles (
    id_profile integer NOT NULL,
    biography text,
    photo_url character varying(255) NOT NULL,
    linkendin character varying(255) NOT NULL,
    skills text,
    interests text
);


ALTER TABLE public.profiles OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24719)
-- Name: profiles_id_profile_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.profiles_id_profile_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.profiles_id_profile_seq OWNER TO postgres;

--
-- TOC entry 5057 (class 0 OID 0)
-- Dependencies: 219
-- Name: profiles_id_profile_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.profiles_id_profile_seq OWNED BY public.profiles.id_profile;


--
-- TOC entry 216 (class 1259 OID 24663)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id_rol integer NOT NULL,
    name_rol character varying(150) NOT NULL,
    description text
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 24662)
-- Name: roles_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_rol_seq OWNER TO postgres;

--
-- TOC entry 5058 (class 0 OID 0)
-- Dependencies: 215
-- Name: roles_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_rol_seq OWNED BY public.roles.id_rol;


--
-- TOC entry 240 (class 1259 OID 24920)
-- Name: system_config; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.system_config (
    id_config integer NOT NULL,
    parameter_config character varying(100) NOT NULL,
    value_config character varying(150) NOT NULL,
    description_config text
);


ALTER TABLE public.system_config OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 24919)
-- Name: system_config_id_config_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.system_config_id_config_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_config_id_config_seq OWNER TO postgres;

--
-- TOC entry 5059 (class 0 OID 0)
-- Dependencies: 239
-- Name: system_config_id_config_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.system_config_id_config_seq OWNED BY public.system_config.id_config;


--
-- TOC entry 226 (class 1259 OID 24776)
-- Name: thematic_areas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.thematic_areas (
    id_area integer NOT NULL,
    name_area character varying(150) NOT NULL,
    description text
);


ALTER TABLE public.thematic_areas OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 24775)
-- Name: thematic_areas_id_area_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.thematic_areas_id_area_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.thematic_areas_id_area_seq OWNER TO postgres;

--
-- TOC entry 5060 (class 0 OID 0)
-- Dependencies: 225
-- Name: thematic_areas_id_area_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.thematic_areas_id_area_seq OWNED BY public.thematic_areas.id_area;


--
-- TOC entry 222 (class 1259 OID 24729)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name_user character varying(150) NOT NULL,
    email character varying(150) NOT NULL,
    password_hash character varying(150) NOT NULL,
    rol_id integer,
    community_id integer,
    profile_id integer,
    registration_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50) DEFAULT 'active'::character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24728)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4801 (class 2604 OID 24714)
-- Name: communities id_community; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communities ALTER COLUMN id_community SET DEFAULT nextval('public.communities_id_community_seq'::regclass);


--
-- TOC entry 4810 (class 2604 OID 24797)
-- Name: educational_content id_content; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.educational_content ALTER COLUMN id_content SET DEFAULT nextval('public.educational_content_id_content_seq'::regclass);


--
-- TOC entry 4816 (class 2604 OID 24905)
-- Name: event_registrations id_event_registration; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_registrations ALTER COLUMN id_event_registration SET DEFAULT nextval('public.event_registrations_id_event_registration_seq'::regclass);


--
-- TOC entry 4815 (class 2604 OID 24891)
-- Name: events id_event; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events ALTER COLUMN id_event SET DEFAULT nextval('public.events_id_event_seq'::regclass);


--
-- TOC entry 4806 (class 2604 OID 24764)
-- Name: invitation_codes id_code; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitation_codes ALTER COLUMN id_code SET DEFAULT nextval('public.invitation_codes_id_code_seq'::regclass);


--
-- TOC entry 4809 (class 2604 OID 24788)
-- Name: learning_levels id_level; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learning_levels ALTER COLUMN id_level SET DEFAULT nextval('public.learning_levels_id_level_seq'::regclass);


--
-- TOC entry 4813 (class 2604 OID 24873)
-- Name: mentorship_registrations id_registration; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentorship_registrations ALTER COLUMN id_registration SET DEFAULT nextval('public.mentorship_registrations_id_registration_seq'::regclass);


--
-- TOC entry 4812 (class 2604 OID 24859)
-- Name: mentorships id_mentorship; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentorships ALTER COLUMN id_mentorship SET DEFAULT nextval('public.mentorships_id_mentorship_seq'::regclass);


--
-- TOC entry 4802 (class 2604 OID 24723)
-- Name: profiles id_profile; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles ALTER COLUMN id_profile SET DEFAULT nextval('public.profiles_id_profile_seq'::regclass);


--
-- TOC entry 4800 (class 2604 OID 24666)
-- Name: roles id_rol; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id_rol SET DEFAULT nextval('public.roles_id_rol_seq'::regclass);


--
-- TOC entry 4818 (class 2604 OID 24923)
-- Name: system_config id_config; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_config ALTER COLUMN id_config SET DEFAULT nextval('public.system_config_id_config_seq'::regclass);


--
-- TOC entry 4808 (class 2604 OID 24779)
-- Name: thematic_areas id_area; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thematic_areas ALTER COLUMN id_area SET DEFAULT nextval('public.thematic_areas_id_area_seq'::regclass);


--
-- TOC entry 4803 (class 2604 OID 24732)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5018 (class 0 OID 24711)
-- Dependencies: 218
-- Data for Name: communities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.communities (id_community, name_community, description_community, status_community, code, access_code) FROM stdin;
\.


--
-- TOC entry 5030 (class 0 OID 24794)
-- Dependencies: 230
-- Data for Name: educational_content; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.educational_content (id_content, title, description_content, url_file, type_content, area_id, level_id, author_id, upload_date, status_content) FROM stdin;
\.


--
-- TOC entry 5038 (class 0 OID 24902)
-- Dependencies: 238
-- Data for Name: event_registrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event_registrations (id_event_registration, id_user, id_event, date_registration) FROM stdin;
\.


--
-- TOC entry 5036 (class 0 OID 24888)
-- Dependencies: 236
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events (id_event, title, description_event, date_events, time_events, place, url_form, image, created_by, status) FROM stdin;
\.


--
-- TOC entry 5024 (class 0 OID 24761)
-- Dependencies: 224
-- Data for Name: invitation_codes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invitation_codes (id_code, code, community_id, creation_date, expiration_date) FROM stdin;
\.


--
-- TOC entry 5028 (class 0 OID 24785)
-- Dependencies: 228
-- Data for Name: learning_levels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.learning_levels (id_level, name_level, description) FROM stdin;
1	Ciencia de Datos	Área enfocada en análisis y visualización de datos
2	Ciencia de Datos	Área enfocada en análisis y visualización de datos
3	Ciencia de Datos	Área enfocada en análisis y visualización de datos
4	Ciencia de Datos	Área enfocada en análisis y visualización de datos
5	Ciencia de Datos	Área enfocada en análisis y visualización de datos
\.


--
-- TOC entry 5034 (class 0 OID 24870)
-- Dependencies: 234
-- Data for Name: mentorship_registrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mentorship_registrations (id_registration, id_user, id_mentorship, date_registration, status) FROM stdin;
\.


--
-- TOC entry 5032 (class 0 OID 24856)
-- Dependencies: 232
-- Data for Name: mentorships; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mentorships (id_mentorship, title, description_mentorship, date_mentorship, hour_mentorship, form_link, minimum_quota, maximum_capacity, area_id, status) FROM stdin;
\.


--
-- TOC entry 5020 (class 0 OID 24720)
-- Dependencies: 220
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profiles (id_profile, biography, photo_url, linkendin, skills, interests) FROM stdin;
\.


--
-- TOC entry 5016 (class 0 OID 24663)
-- Dependencies: 216
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id_rol, name_rol, description) FROM stdin;
1	user	Usuario normal de una comunidad
2	mentor	Usuario promovido por el lider
3	leader	Lider de comunidad
4	admin	Administrador del sistema
\.


--
-- TOC entry 5040 (class 0 OID 24920)
-- Dependencies: 240
-- Data for Name: system_config; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.system_config (id_config, parameter_config, value_config, description_config) FROM stdin;
\.


--
-- TOC entry 5026 (class 0 OID 24776)
-- Dependencies: 226
-- Data for Name: thematic_areas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.thematic_areas (id_area, name_area, description) FROM stdin;
\.


--
-- TOC entry 5022 (class 0 OID 24729)
-- Dependencies: 222
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name_user, email, password_hash, rol_id, community_id, profile_id, registration_date, status) FROM stdin;
1	Administrador Ctech	ctech.uni@gmail.com	$pbkdf2-sha256$29000$jRGidC5FaM3Ze0.p1TpHiA$Qt2GGxme0cF3yQHU4CB1R.FPutOA.95jxkhAcXOOC6c	4	\N	\N	2026-02-10 09:17:08.886346	active
\.


--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 217
-- Name: communities_id_community_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.communities_id_community_seq', 1, true);


--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 229
-- Name: educational_content_id_content_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.educational_content_id_content_seq', 1, false);


--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 237
-- Name: event_registrations_id_event_registration_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.event_registrations_id_event_registration_seq', 1, false);


--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 235
-- Name: events_id_event_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_id_event_seq', 1, false);


--
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 223
-- Name: invitation_codes_id_code_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invitation_codes_id_code_seq', 1, false);


--
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 227
-- Name: learning_levels_id_level_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.learning_levels_id_level_seq', 5, true);


--
-- TOC entry 5069 (class 0 OID 0)
-- Dependencies: 233
-- Name: mentorship_registrations_id_registration_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mentorship_registrations_id_registration_seq', 1, false);


--
-- TOC entry 5070 (class 0 OID 0)
-- Dependencies: 231
-- Name: mentorships_id_mentorship_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mentorships_id_mentorship_seq', 1, false);


--
-- TOC entry 5071 (class 0 OID 0)
-- Dependencies: 219
-- Name: profiles_id_profile_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profiles_id_profile_seq', 1, false);


--
-- TOC entry 5072 (class 0 OID 0)
-- Dependencies: 215
-- Name: roles_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_rol_seq', 4, true);


--
-- TOC entry 5073 (class 0 OID 0)
-- Dependencies: 239
-- Name: system_config_id_config_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.system_config_id_config_seq', 1, false);


--
-- TOC entry 5074 (class 0 OID 0)
-- Dependencies: 225
-- Name: thematic_areas_id_area_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.thematic_areas_id_area_seq', 1, true);


--
-- TOC entry 5075 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- TOC entry 4827 (class 2606 OID 24991)
-- Name: communities communities_access_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communities
    ADD CONSTRAINT communities_access_code_key UNIQUE (access_code);


--
-- TOC entry 4829 (class 2606 OID 24989)
-- Name: communities communities_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communities
    ADD CONSTRAINT communities_code_key UNIQUE (code);


--
-- TOC entry 4831 (class 2606 OID 24718)
-- Name: communities communities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communities
    ADD CONSTRAINT communities_pkey PRIMARY KEY (id_community);


--
-- TOC entry 4845 (class 2606 OID 24802)
-- Name: educational_content educational_content_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.educational_content
    ADD CONSTRAINT educational_content_pkey PRIMARY KEY (id_content);


--
-- TOC entry 4853 (class 2606 OID 24908)
-- Name: event_registrations event_registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_pkey PRIMARY KEY (id_event_registration);


--
-- TOC entry 4851 (class 2606 OID 24895)
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id_event);


--
-- TOC entry 4837 (class 2606 OID 24769)
-- Name: invitation_codes invitation_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitation_codes
    ADD CONSTRAINT invitation_codes_code_key UNIQUE (code);


--
-- TOC entry 4839 (class 2606 OID 24767)
-- Name: invitation_codes invitation_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitation_codes
    ADD CONSTRAINT invitation_codes_pkey PRIMARY KEY (id_code);


--
-- TOC entry 4843 (class 2606 OID 24792)
-- Name: learning_levels learning_levels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learning_levels
    ADD CONSTRAINT learning_levels_pkey PRIMARY KEY (id_level);


--
-- TOC entry 4849 (class 2606 OID 24876)
-- Name: mentorship_registrations mentorship_registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentorship_registrations
    ADD CONSTRAINT mentorship_registrations_pkey PRIMARY KEY (id_registration);


--
-- TOC entry 4847 (class 2606 OID 24863)
-- Name: mentorships mentorships_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentorships
    ADD CONSTRAINT mentorships_pkey PRIMARY KEY (id_mentorship);


--
-- TOC entry 4833 (class 2606 OID 24727)
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id_profile);


--
-- TOC entry 4825 (class 2606 OID 24670)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_rol);


--
-- TOC entry 4855 (class 2606 OID 24927)
-- Name: system_config system_config_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_config
    ADD CONSTRAINT system_config_pkey PRIMARY KEY (id_config);


--
-- TOC entry 4841 (class 2606 OID 24783)
-- Name: thematic_areas thematic_areas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thematic_areas
    ADD CONSTRAINT thematic_areas_pkey PRIMARY KEY (id_area);


--
-- TOC entry 4835 (class 2606 OID 24738)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4862 (class 2606 OID 24803)
-- Name: educational_content educational_content_area_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.educational_content
    ADD CONSTRAINT educational_content_area_id_fkey FOREIGN KEY (area_id) REFERENCES public.thematic_areas(id_area);


--
-- TOC entry 4863 (class 2606 OID 24813)
-- Name: educational_content educational_content_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.educational_content
    ADD CONSTRAINT educational_content_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- TOC entry 4864 (class 2606 OID 24808)
-- Name: educational_content educational_content_level_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.educational_content
    ADD CONSTRAINT educational_content_level_id_fkey FOREIGN KEY (level_id) REFERENCES public.learning_levels(id_level);


--
-- TOC entry 4869 (class 2606 OID 24914)
-- Name: event_registrations event_registrations_id_event_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_id_event_fkey FOREIGN KEY (id_event) REFERENCES public.events(id_event);


--
-- TOC entry 4870 (class 2606 OID 24909)
-- Name: event_registrations event_registrations_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_registrations
    ADD CONSTRAINT event_registrations_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id);


--
-- TOC entry 4868 (class 2606 OID 24896)
-- Name: events events_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 4861 (class 2606 OID 24770)
-- Name: invitation_codes invitation_codes_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitation_codes
    ADD CONSTRAINT invitation_codes_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.communities(id_community);


--
-- TOC entry 4866 (class 2606 OID 24882)
-- Name: mentorship_registrations mentorship_registrations_id_mentorship_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentorship_registrations
    ADD CONSTRAINT mentorship_registrations_id_mentorship_fkey FOREIGN KEY (id_mentorship) REFERENCES public.mentorships(id_mentorship);


--
-- TOC entry 4867 (class 2606 OID 24877)
-- Name: mentorship_registrations mentorship_registrations_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentorship_registrations
    ADD CONSTRAINT mentorship_registrations_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id);


--
-- TOC entry 4865 (class 2606 OID 24864)
-- Name: mentorships mentorships_area_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentorships
    ADD CONSTRAINT mentorships_area_id_fkey FOREIGN KEY (area_id) REFERENCES public.thematic_areas(id_area);


--
-- TOC entry 4858 (class 2606 OID 24744)
-- Name: users users_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.communities(id_community);


--
-- TOC entry 4859 (class 2606 OID 24749)
-- Name: users users_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES public.profiles(id_profile);


--
-- TOC entry 4860 (class 2606 OID 24739)
-- Name: users users_rol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_rol_id_fkey FOREIGN KEY (rol_id) REFERENCES public.roles(id_rol);

-- GESTIÓN DE ROL ADMIN ÚNICO
CREATE UNIQUE INDEX unique_admin_role ON public.profiles (rol_id) 
WHERE rol_id = 4; -- 4 es el ID de admin seg£n COPY public.roles


-- TABLAS PARA SEGURIDAD EN PRODUCCIÓN

-- 1. Tabla para invalidar tokens JWT al cerrar sesión (Logout)
CREATE TABLE public.token_blocklist (
    id SERIAL PRIMARY KEY,
    token TEXT NOT NULL UNIQUE,
    blacklisted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla para tokens de recuperación de contraseña
CREATE TABLE public.password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Completed on 2026-02-10 10:35:51

--
-- PostgreSQL database dump complete
--

\unrestrict 8lSEqeaa21IEKvZAWDV2TYWKgSKh0fgdwvisIG3wmkgNSptYlfddmMZGCE6bBqg

