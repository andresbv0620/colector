--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.0
-- Dumped by pg_dump version 9.6.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO colectoruser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO colectoruser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO colectoruser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO colectoruser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO colectoruser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO colectoruser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_token_middleware_token; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE auth_token_middleware_token (
    id integer NOT NULL,
    valor character varying(50) NOT NULL,
    empresa_id integer NOT NULL
);


ALTER TABLE auth_token_middleware_token OWNER TO colectoruser;

--
-- Name: auth_token_middleware_token_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE auth_token_middleware_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_token_middleware_token_id_seq OWNER TO colectoruser;

--
-- Name: auth_token_middleware_token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE auth_token_middleware_token_id_seq OWNED BY auth_token_middleware_token.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO colectoruser;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO colectoruser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO colectoruser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO colectoruser;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO colectoruser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO colectoruser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO colectoruser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO colectoruser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO colectoruser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO colectoruser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO colectoruser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO colectoruser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO colectoruser;

--
-- Name: registro_asignacionentrada; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_asignacionentrada (
    id integer NOT NULL,
    orden integer NOT NULL,
    requerido boolean NOT NULL,
    oculto boolean NOT NULL,
    solo_lectura boolean NOT NULL,
    defecto character varying(50) NOT NULL,
    defecto_previo boolean NOT NULL,
    maximo integer,
    minimo integer,
    validacion character varying(50) NOT NULL,
    entrada_id integer NOT NULL,
    ficha_id integer NOT NULL,
    regla_visibilidad_id integer,
    formulario_asociado_id integer,
    agregar_nuevo boolean NOT NULL,
    CONSTRAINT registro_asignacionentrada_maximo_check CHECK ((maximo >= 0)),
    CONSTRAINT registro_asignacionentrada_minimo_check CHECK ((minimo >= 0)),
    CONSTRAINT registro_asignacionentrada_orden_check CHECK ((orden >= 0))
);


ALTER TABLE registro_asignacionentrada OWNER TO colectoruser;

--
-- Name: registro_asignacionentrada_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_asignacionentrada_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_asignacionentrada_id_seq OWNER TO colectoruser;

--
-- Name: registro_asignacionentrada_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_asignacionentrada_id_seq OWNED BY registro_asignacionentrada.id;


--
-- Name: registro_colector; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_colector (
    id integer NOT NULL,
    usuario_id integer NOT NULL
);


ALTER TABLE registro_colector OWNER TO colectoruser;

--
-- Name: registro_colector_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_colector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_colector_id_seq OWNER TO colectoruser;

--
-- Name: registro_colector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_colector_id_seq OWNED BY registro_colector.id;


--
-- Name: registro_colector_respuesta; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_colector_respuesta (
    id integer NOT NULL,
    colector_id integer NOT NULL,
    respuesta_id integer NOT NULL
);


ALTER TABLE registro_colector_respuesta OWNER TO colectoruser;

--
-- Name: registro_colector_respuesta_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_colector_respuesta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_colector_respuesta_id_seq OWNER TO colectoruser;

--
-- Name: registro_colector_respuesta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_colector_respuesta_id_seq OWNED BY registro_colector_respuesta.id;


--
-- Name: registro_empresa; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_empresa (
    id integer NOT NULL,
    codigo_secreto character varying(50) NOT NULL,
    nombre character varying(50) NOT NULL,
    industria character varying(50) NOT NULL,
    pais character varying(50) NOT NULL,
    ciudad character varying(50) NOT NULL,
    correo_empresarial text NOT NULL,
    email character varying(50) NOT NULL,
    descripcion text NOT NULL,
    nit integer,
    correo_facturacion character varying(50) NOT NULL,
    telefono integer,
    plan_id integer,
    usuario_id integer NOT NULL
);


ALTER TABLE registro_empresa OWNER TO colectoruser;

--
-- Name: registro_empresa_colector; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_empresa_colector (
    id integer NOT NULL,
    empresa_id integer NOT NULL,
    colector_id integer NOT NULL
);


ALTER TABLE registro_empresa_colector OWNER TO colectoruser;

--
-- Name: registro_empresa_colector_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_empresa_colector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_empresa_colector_id_seq OWNER TO colectoruser;

--
-- Name: registro_empresa_colector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_empresa_colector_id_seq OWNED BY registro_empresa_colector.id;


--
-- Name: registro_empresa_formulario; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_empresa_formulario (
    id integer NOT NULL,
    empresa_id integer NOT NULL,
    formulario_id integer NOT NULL
);


ALTER TABLE registro_empresa_formulario OWNER TO colectoruser;

--
-- Name: registro_empresa_formulario_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_empresa_formulario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_empresa_formulario_id_seq OWNER TO colectoruser;

--
-- Name: registro_empresa_formulario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_empresa_formulario_id_seq OWNED BY registro_empresa_formulario.id;


--
-- Name: registro_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_empresa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_empresa_id_seq OWNER TO colectoruser;

--
-- Name: registro_empresa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_empresa_id_seq OWNED BY registro_empresa.id;


--
-- Name: registro_empresa_tablets; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_empresa_tablets (
    id integer NOT NULL,
    empresa_id integer NOT NULL,
    tablet_id integer NOT NULL
);


ALTER TABLE registro_empresa_tablets OWNER TO colectoruser;

--
-- Name: registro_empresa_tablets_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_empresa_tablets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_empresa_tablets_id_seq OWNER TO colectoruser;

--
-- Name: registro_empresa_tablets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_empresa_tablets_id_seq OWNED BY registro_empresa_tablets.id;


--
-- Name: registro_entrada; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_entrada (
    id integer NOT NULL,
    tipo character varying(2) NOT NULL,
    nombre character varying(500) NOT NULL,
    descripcion text NOT NULL
);


ALTER TABLE registro_entrada OWNER TO colectoruser;

--
-- Name: registro_entrada_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_entrada_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_entrada_id_seq OWNER TO colectoruser;

--
-- Name: registro_entrada_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_entrada_id_seq OWNED BY registro_entrada.id;


--
-- Name: registro_entrada_respuesta; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_entrada_respuesta (
    id integer NOT NULL,
    entrada_id integer NOT NULL,
    respuesta_id integer NOT NULL
);


ALTER TABLE registro_entrada_respuesta OWNER TO colectoruser;

--
-- Name: registro_entrada_respuesta_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_entrada_respuesta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_entrada_respuesta_id_seq OWNER TO colectoruser;

--
-- Name: registro_entrada_respuesta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_entrada_respuesta_id_seq OWNED BY registro_entrada_respuesta.id;


--
-- Name: registro_ficha; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_ficha (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text NOT NULL,
    repetible boolean NOT NULL
);


ALTER TABLE registro_ficha OWNER TO colectoruser;

--
-- Name: registro_ficha_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_ficha_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_ficha_id_seq OWNER TO colectoruser;

--
-- Name: registro_ficha_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_ficha_id_seq OWNED BY registro_ficha.id;


--
-- Name: registro_formulario; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_formulario (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text NOT NULL,
    titulo_reporte_id integer,
    titulo_reporte2_id integer
);


ALTER TABLE registro_formulario OWNER TO colectoruser;

--
-- Name: registro_formulario_ficha; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_formulario_ficha (
    id integer NOT NULL,
    formulario_id integer NOT NULL,
    ficha_id integer NOT NULL
);


ALTER TABLE registro_formulario_ficha OWNER TO colectoruser;

--
-- Name: registro_formulario_ficha_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_formulario_ficha_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_formulario_ficha_id_seq OWNER TO colectoruser;

--
-- Name: registro_formulario_ficha_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_formulario_ficha_id_seq OWNED BY registro_formulario_ficha.id;


--
-- Name: registro_formulario_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_formulario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_formulario_id_seq OWNER TO colectoruser;

--
-- Name: registro_formulario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_formulario_id_seq OWNED BY registro_formulario.id;


--
-- Name: registro_formularioasociado; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_formularioasociado (
    id integer NOT NULL,
    seleccionar_existentes boolean NOT NULL,
    crear_nuevo boolean NOT NULL,
    actualizar_existente boolean NOT NULL,
    seleccionar_multiples boolean NOT NULL,
    form_asociado_id integer NOT NULL
);


ALTER TABLE registro_formularioasociado OWNER TO colectoruser;

--
-- Name: registro_formularioasociado_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_formularioasociado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_formularioasociado_id_seq OWNER TO colectoruser;

--
-- Name: registro_formularioasociado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_formularioasociado_id_seq OWNED BY registro_formularioasociado.id;


--
-- Name: registro_formulariodiligenciado; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_formulariodiligenciado (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    gps character varying(50) NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    colector_id integer,
    empresa_id integer,
    entrada_id integer,
    respuesta_id integer
);


ALTER TABLE registro_formulariodiligenciado OWNER TO colectoruser;

--
-- Name: registro_formulariodiligenciado_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_formulariodiligenciado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_formulariodiligenciado_id_seq OWNER TO colectoruser;

--
-- Name: registro_formulariodiligenciado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_formulariodiligenciado_id_seq OWNED BY registro_formulariodiligenciado.id;


--
-- Name: registro_permisoformulario; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_permisoformulario (
    id integer NOT NULL,
    formulario_id integer NOT NULL
);


ALTER TABLE registro_permisoformulario OWNER TO colectoruser;

--
-- Name: registro_permisoformulario_colectores; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_permisoformulario_colectores (
    id integer NOT NULL,
    permisoformulario_id integer NOT NULL,
    colector_id integer NOT NULL
);


ALTER TABLE registro_permisoformulario_colectores OWNER TO colectoruser;

--
-- Name: registro_permisoformulario_colectores_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_permisoformulario_colectores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_permisoformulario_colectores_id_seq OWNER TO colectoruser;

--
-- Name: registro_permisoformulario_colectores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_permisoformulario_colectores_id_seq OWNED BY registro_permisoformulario_colectores.id;


--
-- Name: registro_permisoformulario_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_permisoformulario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_permisoformulario_id_seq OWNER TO colectoruser;

--
-- Name: registro_permisoformulario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_permisoformulario_id_seq OWNED BY registro_permisoformulario.id;


--
-- Name: registro_plan; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_plan (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    almacenamiento character varying(50) NOT NULL,
    cantidad_colectores integer NOT NULL,
    valor character varying(50) NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL
);


ALTER TABLE registro_plan OWNER TO colectoruser;

--
-- Name: registro_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_plan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_plan_id_seq OWNER TO colectoruser;

--
-- Name: registro_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_plan_id_seq OWNED BY registro_plan.id;


--
-- Name: registro_reglaautollenado; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_reglaautollenado (
    id integer NOT NULL,
    asociacion_id integer NOT NULL,
    entrada_destino_id integer,
    entrada_fuente_id integer
);


ALTER TABLE registro_reglaautollenado OWNER TO colectoruser;

--
-- Name: registro_reglaautollenado_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_reglaautollenado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_reglaautollenado_id_seq OWNER TO colectoruser;

--
-- Name: registro_reglaautollenado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_reglaautollenado_id_seq OWNED BY registro_reglaautollenado.id;


--
-- Name: registro_reglavisibilidad; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_reglavisibilidad (
    id integer NOT NULL,
    operador character varying(50) NOT NULL,
    valor character varying(100) NOT NULL,
    elemento_id integer NOT NULL
);


ALTER TABLE registro_reglavisibilidad OWNER TO colectoruser;

--
-- Name: registro_reglavisibilidad_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_reglavisibilidad_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_reglavisibilidad_id_seq OWNER TO colectoruser;

--
-- Name: registro_reglavisibilidad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_reglavisibilidad_id_seq OWNED BY registro_reglavisibilidad.id;


--
-- Name: registro_respuesta; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_respuesta (
    id integer NOT NULL,
    valor character varying(500) NOT NULL,
    pregunta_id integer,
    respuesta character varying(500),
    usuario_id integer,
    CONSTRAINT registro_respuesta_pregunta_id_check CHECK ((pregunta_id >= 0))
);


ALTER TABLE registro_respuesta OWNER TO colectoruser;

--
-- Name: registro_respuesta_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_respuesta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_respuesta_id_seq OWNER TO colectoruser;

--
-- Name: registro_respuesta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_respuesta_id_seq OWNED BY registro_respuesta.id;


--
-- Name: registro_tablet; Type: TABLE; Schema: public; Owner: colectoruser
--

CREATE TABLE registro_tablet (
    id integer NOT NULL,
    codigo character varying(50) NOT NULL
);


ALTER TABLE registro_tablet OWNER TO colectoruser;

--
-- Name: registro_tablet_id_seq; Type: SEQUENCE; Schema: public; Owner: colectoruser
--

CREATE SEQUENCE registro_tablet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE registro_tablet_id_seq OWNER TO colectoruser;

--
-- Name: registro_tablet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: colectoruser
--

ALTER SEQUENCE registro_tablet_id_seq OWNED BY registro_tablet.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: auth_token_middleware_token id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_token_middleware_token ALTER COLUMN id SET DEFAULT nextval('auth_token_middleware_token_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: registro_asignacionentrada id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_asignacionentrada ALTER COLUMN id SET DEFAULT nextval('registro_asignacionentrada_id_seq'::regclass);


--
-- Name: registro_colector id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector ALTER COLUMN id SET DEFAULT nextval('registro_colector_id_seq'::regclass);


--
-- Name: registro_colector_respuesta id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector_respuesta ALTER COLUMN id SET DEFAULT nextval('registro_colector_respuesta_id_seq'::regclass);


--
-- Name: registro_empresa id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa ALTER COLUMN id SET DEFAULT nextval('registro_empresa_id_seq'::regclass);


--
-- Name: registro_empresa_colector id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_colector ALTER COLUMN id SET DEFAULT nextval('registro_empresa_colector_id_seq'::regclass);


--
-- Name: registro_empresa_formulario id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_formulario ALTER COLUMN id SET DEFAULT nextval('registro_empresa_formulario_id_seq'::regclass);


--
-- Name: registro_empresa_tablets id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_tablets ALTER COLUMN id SET DEFAULT nextval('registro_empresa_tablets_id_seq'::regclass);


--
-- Name: registro_entrada id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_entrada ALTER COLUMN id SET DEFAULT nextval('registro_entrada_id_seq'::regclass);


--
-- Name: registro_entrada_respuesta id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_entrada_respuesta ALTER COLUMN id SET DEFAULT nextval('registro_entrada_respuesta_id_seq'::regclass);


--
-- Name: registro_ficha id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_ficha ALTER COLUMN id SET DEFAULT nextval('registro_ficha_id_seq'::regclass);


--
-- Name: registro_formulario id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario ALTER COLUMN id SET DEFAULT nextval('registro_formulario_id_seq'::regclass);


--
-- Name: registro_formulario_ficha id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario_ficha ALTER COLUMN id SET DEFAULT nextval('registro_formulario_ficha_id_seq'::regclass);


--
-- Name: registro_formularioasociado id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formularioasociado ALTER COLUMN id SET DEFAULT nextval('registro_formularioasociado_id_seq'::regclass);


--
-- Name: registro_formulariodiligenciado id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado ALTER COLUMN id SET DEFAULT nextval('registro_formulariodiligenciado_id_seq'::regclass);


--
-- Name: registro_permisoformulario id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario ALTER COLUMN id SET DEFAULT nextval('registro_permisoformulario_id_seq'::regclass);


--
-- Name: registro_permisoformulario_colectores id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario_colectores ALTER COLUMN id SET DEFAULT nextval('registro_permisoformulario_colectores_id_seq'::regclass);


--
-- Name: registro_plan id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_plan ALTER COLUMN id SET DEFAULT nextval('registro_plan_id_seq'::regclass);


--
-- Name: registro_reglaautollenado id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglaautollenado ALTER COLUMN id SET DEFAULT nextval('registro_reglaautollenado_id_seq'::regclass);


--
-- Name: registro_reglavisibilidad id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglavisibilidad ALTER COLUMN id SET DEFAULT nextval('registro_reglavisibilidad_id_seq'::regclass);


--
-- Name: registro_respuesta id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_respuesta ALTER COLUMN id SET DEFAULT nextval('registro_respuesta_id_seq'::regclass);


--
-- Name: registro_tablet id; Type: DEFAULT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_tablet ALTER COLUMN id SET DEFAULT nextval('registro_tablet_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add empresa	7	add_empresa
20	Can change empresa	7	change_empresa
21	Can delete empresa	7	delete_empresa
22	Can add tablet	8	add_tablet
23	Can change tablet	8	change_tablet
24	Can delete tablet	8	delete_tablet
25	Can add colector	9	add_colector
26	Can change colector	9	change_colector
27	Can delete colector	9	delete_colector
28	Can add plan	10	add_plan
29	Can change plan	10	change_plan
30	Can delete plan	10	delete_plan
31	Can add formulario	11	add_formulario
32	Can change formulario	11	change_formulario
33	Can delete formulario	11	delete_formulario
34	Can add permiso formulario	12	add_permisoformulario
35	Can change permiso formulario	12	change_permisoformulario
36	Can delete permiso formulario	12	delete_permisoformulario
37	Can add ficha	13	add_ficha
38	Can change ficha	13	change_ficha
39	Can delete ficha	13	delete_ficha
40	Can add entrada	14	add_entrada
41	Can change entrada	14	change_entrada
42	Can delete entrada	14	delete_entrada
43	Can add asignacion entrada	15	add_asignacionentrada
44	Can change asignacion entrada	15	change_asignacionentrada
45	Can delete asignacion entrada	15	delete_asignacionentrada
46	Can add regla visibilidad	16	add_reglavisibilidad
47	Can change regla visibilidad	16	change_reglavisibilidad
48	Can delete regla visibilidad	16	delete_reglavisibilidad
49	Can add formulario asociado	17	add_formularioasociado
50	Can change formulario asociado	17	change_formularioasociado
51	Can delete formulario asociado	17	delete_formularioasociado
52	Can add regla autollenado	18	add_reglaautollenado
53	Can change regla autollenado	18	change_reglaautollenado
54	Can delete regla autollenado	18	delete_reglaautollenado
55	Can add respuesta	19	add_respuesta
56	Can change respuesta	19	change_respuesta
57	Can delete respuesta	19	delete_respuesta
58	Can add formulario diligenciado	20	add_formulariodiligenciado
59	Can change formulario diligenciado	20	change_formulariodiligenciado
60	Can delete formulario diligenciado	20	delete_formulariodiligenciado
61	Can add token	21	add_token
62	Can change token	21	change_token
63	Can delete token	21	delete_token
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('auth_permission_id_seq', 63, true);


--
-- Data for Name: auth_token_middleware_token; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY auth_token_middleware_token (id, valor, empresa_id) FROM stdin;
1	52b53da1364888f824d59327190c7444	1
\.


--
-- Name: auth_token_middleware_token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('auth_token_middleware_token_id_seq', 1, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$20000$Fia8tiE0oTBG$YXa0FRXwk/yDeUq24EysKBBYKuPV6SIZdAQQdgSYkos=	\N	f	andres				f	t	2016-11-14 16:19:07.944446+00
3	test	\N	f	Test			test@test.com	f	t	2017-02-09 23:23:02.44966+00
4	test	\N	f	test1			test1@test.com	f	t	2017-02-09 23:23:37.856251+00
5	test	\N	f	test2			test2@test.com	f	t	2017-02-09 23:25:11.747404+00
6	test	\N	f	test3			test3@test.com	f	t	2017-02-09 23:26:08.357607+00
7	test	\N	f	test4			test4@test.com	f	t	2017-02-09 23:26:33.171046+00
8	test	\N	f	test5			test5@test.com	f	t	2017-02-09 23:27:18.778763+00
1	pbkdf2_sha256$20000$gokyxEAiTPbT$ne5cnRNR2den91FU3kRsyUq1IoRlE4OPwTvYs78vqAA=	2017-02-15 13:26:19.931191+00	t	ma0			ma0@contraslash.com	t	t	2016-10-07 21:35:11.835572+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('auth_user_id_seq', 8, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2016-10-07 21:37:37.038646+00	1	ma0	1		9	1
2	2016-10-07 21:38:20.700228+00	1	Entrada 1	1		14	1
3	2016-10-07 21:38:35.167388+00	1	Ficha 1	1		13	1
4	2016-10-07 21:38:43.456925+00	1	F1	1		11	1
5	2016-10-07 21:38:56.847185+00	1	001	1		8	1
6	2016-10-07 21:39:01.815323+00	1	Contraslash	1		7	1
7	2016-10-07 21:39:21.775168+00	1	Contraslash	1		21	1
8	2016-10-07 21:40:09.552278+00	1	F1	2	Modificado/a titulo_reporte.	11	1
9	2016-10-07 21:40:16.376847+00	1	F1	2	Modificado/a titulo_reporte2.	11	1
10	2016-10-07 21:40:42.584155+00	1	F1	1		12	1
11	2016-10-07 21:44:36.700935+00	1	ma0	2	Modificado/a password.	4	1
12	2016-10-19 22:15:11.135984+00	2	Pregunta tipo 1	1		14	1
13	2016-10-19 22:15:22.796427+00	3	Pregunta tipo 2	1		14	1
14	2016-10-19 22:15:32.581299+00	4	Pregunta tipo 3	1		14	1
15	2016-10-19 22:15:41.368655+00	5	Pregunta 4	1		14	1
16	2016-10-19 22:15:52.767087+00	6	Pregunta 5	1		14	1
17	2016-10-19 22:16:00.011234+00	7	Pregunta 6	1		14	1
18	2016-10-19 22:16:13.657083+00	8	Pregunta 7	1		14	1
19	2016-10-19 22:16:20.266508+00	9	Pregunta 8	1		14	1
20	2016-10-19 22:16:26.187729+00	10	Pregunta 9	1		14	1
21	2016-10-19 22:16:34.194023+00	11	Pregunta 10	1		14	1
22	2016-10-19 22:16:43.261189+00	12	Pregunta 11	1		14	1
23	2016-10-19 22:16:53.62523+00	13	Pregunta 12	1		14	1
24	2016-10-19 22:17:09.763672+00	14	Pregunta 13	1		14	1
25	2016-10-19 22:17:16.085472+00	15	Pregunta 14	1		14	1
26	2016-10-19 22:17:22.273706+00	16	Pregunta 15	1		14	1
27	2016-10-19 22:17:29.71836+00	17	Pregunta 16	1		14	1
28	2016-10-19 22:17:36.452894+00	18	Pregunta 17	1		14	1
29	2016-10-19 22:18:28.781174+00	2	Primer segmento	1		13	1
30	2016-10-19 22:19:29.542996+00	3	Segundo segmento	1		13	1
31	2016-10-19 22:20:50.39266+00	4	Tercer Segmento	1		13	1
32	2016-10-19 22:21:26.730894+00	2	Form completo	1		11	1
33	2016-10-19 22:22:47.359764+00	2	Form completo	1		12	1
34	2016-10-19 22:23:15.558487+00	2	002	1		8	1
35	2016-10-19 22:28:06.633442+00	1	Respuesta 1	1		19	1
36	2016-10-19 22:28:13.210109+00	2	Respuesta 2	1		19	1
37	2016-10-19 22:28:17.870978+00	3	Respuesta 3	1		19	1
38	2016-10-19 22:31:11.172054+00	4	Pregunta tipo 3	2	Modificado/a respuesta.	14	1
39	2016-10-19 22:31:46.872731+00	5	Pregunta 4	2	Modificado/a respuesta.	14	1
40	2016-10-19 22:31:57.499803+00	6	Pregunta 5	2	Modificado/a respuesta.	14	1
41	2016-10-19 23:48:58.60695+00	3	Formulario Funcional	1		11	1
42	2016-10-20 00:43:53.534002+00	5	Ficha Simplificada 1	1		13	1
43	2016-10-20 00:44:53.190608+00	6	Segmento Simplificado 2	1		13	1
44	2016-10-20 00:45:33.482135+00	6	Segmento Simplificado 2	2	Añadido/a "Asignacion de entrada Pregunta 16 a Segmento Simplificado 2" asignacion entrada.	13	1
45	2016-10-20 00:46:05.650706+00	7	Fragmento Simplificado 3	1		13	1
46	2016-10-20 00:46:23.86599+00	3	Formulario Funcional	2	Modificado/a ficha.	11	1
47	2016-10-20 00:46:38.678362+00	3	Formulario Funcional	1		12	1
48	2016-10-20 00:50:24.876781+00	1	Contraslash	2	Modificado/a formulario.	7	1
49	2016-10-25 18:33:02.848498+00	4	Formulario Agregar OTro	1		11	1
50	2016-10-25 18:34:07.381073+00	4	Formulario Agregar OTro	1		12	1
51	2016-10-25 18:36:19.043052+00	1	Contraslash	2	Modificado/a formulario.	7	1
52	2016-11-14 14:43:18.920623+00	19	Esta pregunta es demasiado, demasiado larga y no se puede ver en el dispositivo movil porque tiene muchisimos caracteres, por esta razon estamos realizando el ajuste de texto	1		14	1
53	2016-11-14 14:43:31.547322+00	8	Testing Preguntas largas	1		13	1
54	2016-11-14 14:43:52.293183+00	5	Testing Preguntas largas	1		11	1
55	2016-11-14 14:43:56.719432+00	1	Contraslash	2	Modificado/a formulario.	7	1
56	2016-11-14 14:44:18.080298+00	5	Testing Preguntas largas	2	Modificado/a titulo_reporte.	11	1
57	2016-11-14 14:44:35.470332+00	5	Testing Preguntas largas	1		12	1
58	2016-11-14 16:12:18.953166+00	20	Ñ	1		14	1
59	2016-11-14 16:13:40.944291+00	1	Ficha 1	2	Añadido/a "Asignacion de entrada Ñ a Ficha 1" asignacion entrada.	13	1
60	2016-11-14 16:16:14.986783+00	21	ÑÓ%	1		14	1
61	2016-11-14 16:16:23.216713+00	8	Testing Preguntas largas	2	Añadido/a "Asignacion de entrada ÑÓ% a Testing Preguntas largas" asignacion entrada.	13	1
62	2016-11-14 16:19:08.039338+00	2	andres	1		4	1
63	2016-11-14 16:19:42.381224+00	2	andres	1		9	1
64	2016-11-14 16:20:13.712304+00	1	Contraslash	2	Modificado/a colector.	7	1
65	2016-11-14 16:21:16.180605+00	22	pregunta andres	1		14	1
66	2016-11-14 16:21:22.475766+00	9	Andres	1		13	1
67	2016-11-14 16:21:26.150713+00	6	Andres	1		11	1
68	2016-11-14 16:21:31.044136+00	1	Contraslash	2	Modificado/a formulario.	7	1
69	2016-11-14 16:21:56.059307+00	6	Andres	2	Modificado/a titulo_reporte.	11	1
70	2016-11-14 16:22:16.686814+00	6	Andres	1		12	1
71	2016-11-14 18:02:04.257005+00	23	ciudad	1		14	1
72	2016-11-14 18:02:18.173209+00	9	Andres	2	Añadido/a "Asignacion de entrada ciudad a Andres" asignacion entrada.	13	1
73	2016-11-14 18:02:41.519591+00	6	Andres	2	Modificado/a titulo_reporte2.	11	1
74	2016-11-23 17:27:51.801517+00	10	PFM 1	1		13	1
75	2016-11-23 17:28:11.909117+00	11	PFM	1		13	1
76	2016-11-23 17:28:27.214559+00	12	PFM 2	1		13	1
77	2016-11-23 17:28:35.525278+00	7	Prueba Secciones Multiples	1		11	1
78	2016-11-23 17:29:33.203557+00	7	Prueba Secciones Multiples	1		12	1
79	2016-12-05 14:17:36.962901+00	24	Fecha 	1		14	1
80	2016-12-05 14:17:45.894876+00	13	Ficha de Fecha	1		13	1
81	2016-12-05 14:18:25.968843+00	8	Formulario de Fecha	1		11	1
82	2016-12-05 14:21:49.176763+00	8	Formulario de Fecha	1		12	1
83	2016-12-05 14:29:54.673704+00	25	Tiempo	1		14	1
84	2016-12-05 14:30:01.318192+00	13	Ficha de Fecha	2	Añadido/a "Asignacion de entrada Tiempo a Ficha de Fecha" asignacion entrada.	13	1
85	2017-01-09 20:58:51.140996+00	1	Ficha 1	2	Modificado/a repetible.	13	1
86	2017-02-01 16:38:42.137244+00	26	Foto 1	1		14	1
87	2017-02-01 16:38:57.506788+00	27	Foto 2	1		14	1
88	2017-02-01 16:39:07.168602+00	28	Foto 3	1		14	1
89	2017-02-01 16:39:38.999419+00	14	Fotos	1		13	1
90	2017-02-01 16:40:27.403653+00	9	Formulario Fotos	1		11	1
91	2017-02-01 16:40:52.200373+00	9	Formulario Fotos	1		12	1
92	2017-02-02 14:04:45.207785+00	29	a	1		14	1
93	2017-02-02 14:05:02.649145+00	30	b	1		14	1
94	2017-02-02 14:05:26.428977+00	15	Formula simple	1		13	1
95	2017-02-02 14:05:39.857419+00	10	Formulas	1		11	1
96	2017-02-02 14:07:13.708881+00	31	Formula 	1		14	1
97	2017-02-02 14:07:36.681218+00	15	Formula simple	2	Añadido/a "Asignacion de entrada b a Formula simple" asignacion entrada. Añadido/a "Asignacion de entrada Formula  a Formula simple" asignacion entrada.	13	1
98	2017-02-02 14:08:40.656777+00	10	Formulas	2	No ha cambiado ningún campo.	11	1
99	2017-02-02 14:08:56.157883+00	10	Formulas	1		12	1
100	2017-02-02 20:34:47.779517+00	31	Formula 	2	Modificado/a descripcion.	14	1
101	2017-02-02 22:04:57.221409+00	32	c	1		14	1
102	2017-02-02 22:05:07.302849+00	33	d	1		14	1
103	2017-02-02 22:05:34.788825+00	34	Formula 2	1		14	1
104	2017-02-02 22:05:51.687523+00	35	Formula 3	1		14	1
105	2017-02-02 22:06:22.595413+00	15	Formula simple	2	Añadido/a "Asignacion de entrada c a Formula simple" asignacion entrada. Añadido/a "Asignacion de entrada d a Formula simple" asignacion entrada. Añadido/a "Asignacion de entrada Formula 2 a Formula simple" asignacion entrada. Añadido/a "Asignacion de entrada Formula 3 a Formula simple" asignacion entrada.	13	1
106	2017-02-02 22:07:17.095392+00	32	c	2	Modificado/a tipo.	14	1
107	2017-02-02 22:07:27.048699+00	35	Formula 3	2	Modificado/a tipo.	14	1
108	2017-02-02 22:07:36.046037+00	34	Formula 2	2	Modificado/a tipo.	14	1
109	2017-02-02 22:07:43.588808+00	33	d	2	Modificado/a tipo.	14	1
110	2017-02-14 02:58:08.371166+00	9	Andres	3		13	1
111	2017-02-14 02:58:52.976269+00	16	Andres	1		13	1
112	2017-02-14 02:59:05.464357+00	6	Andres	2	Modificado/a ficha, titulo_reporte y titulo_reporte2.	11	1
113	2017-02-14 03:09:36.727838+00	6	Andres	3		11	1
114	2017-02-15 19:17:56.193522+00	11	Farmacias	1		12	1
115	2017-02-15 19:22:38.978532+00	10	Formulas	3		12	1
116	2017-02-15 19:22:38.996117+00	9	Formulario Fotos	3		12	1
117	2017-02-15 19:22:39.0111+00	8	Formulario de Fecha	3		12	1
118	2017-02-15 19:22:39.026251+00	7	Prueba Secciones Multiples	3		12	1
119	2017-02-15 19:22:39.039735+00	5	Testing Preguntas largas	3		12	1
120	2017-02-15 19:22:39.052758+00	4	Formulario Agregar OTro	3		12	1
121	2017-02-15 19:22:39.070503+00	3	Formulario Funcional	3		12	1
122	2017-02-15 19:22:39.08403+00	2	Form completo	3		12	1
123	2017-02-15 19:22:39.098187+00	1	F1	3		12	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 123, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	registro	empresa
8	registro	tablet
9	registro	colector
10	registro	plan
11	registro	formulario
12	registro	permisoformulario
13	registro	ficha
14	registro	entrada
15	registro	asignacionentrada
16	registro	reglavisibilidad
17	registro	formularioasociado
18	registro	reglaautollenado
19	registro	respuesta
20	registro	formulariodiligenciado
21	auth_token_middleware	token
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('django_content_type_id_seq', 21, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2016-10-07 21:23:56.804513+00
2	auth	0001_initial	2016-10-07 21:23:57.470535+00
3	admin	0001_initial	2016-10-07 21:23:57.633831+00
4	contenttypes	0002_remove_content_type_name	2016-10-07 21:23:57.715834+00
5	auth	0002_alter_permission_name_max_length	2016-10-07 21:23:57.760272+00
6	auth	0003_alter_user_email_max_length	2016-10-07 21:23:57.814297+00
7	auth	0004_alter_user_username_opts	2016-10-07 21:23:57.846844+00
8	auth	0005_alter_user_last_login_null	2016-10-07 21:23:57.890546+00
9	auth	0006_require_contenttypes_0002	2016-10-07 21:23:57.909393+00
10	registro	0001_initial	2016-10-07 21:24:00.859636+00
11	auth_token_middleware	0001_initial	2016-10-07 21:24:01.037202+00
12	registro	0002_auto_20160302_1243	2016-10-07 21:24:01.481308+00
13	registro	0003_auto_20160323_0521	2016-10-07 21:24:01.644415+00
14	registro	0004_auto_20160324_1436	2016-10-07 21:24:01.759632+00
15	registro	0005_formulario_titulo_reporte	2016-10-07 21:24:01.879177+00
16	registro	0006_auto_20160706_1620	2016-10-07 21:24:02.00619+00
17	registro	0007_auto_20160713_1403	2016-10-07 21:24:02.101117+00
18	registro	0008_auto_20160713_1523	2016-10-07 21:24:02.269526+00
19	registro	0009_auto_20160723_1526	2016-10-07 21:24:02.363321+00
20	registro	0010_auto_20160723_1926	2016-10-07 21:24:02.772184+00
21	registro	0011_auto_20160727_1810	2016-10-07 21:24:03.001974+00
22	registro	0012_auto_20160820_0435	2016-10-07 21:24:03.071321+00
23	registro	0013_auto_20160830_2258	2016-10-07 21:24:03.168014+00
24	registro	0014_auto_20160913_1111	2016-10-07 21:24:03.264597+00
25	registro	0015_colector_respuesta	2016-10-07 21:24:03.473848+00
26	sessions	0001_initial	2016-10-07 21:24:03.635704+00
27	registro	0016_asignacionentrada_agregar_nuevo	2016-11-22 03:20:12.698365+00
28	registro	0017_ficha_repetible	2017-01-09 20:47:28.014299+00
29	registro	0018_auto_20170215_0821	2017-02-15 13:22:01.506285+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('django_migrations_id_seq', 29, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
3i0wmlet5pfk2ohg65x86ln7wp7tv7b6	NzViZWJiZWYzOTkxOTNhMzU1MTY5MDJlMzcxZjMzZTVmY2Y2NWIwMjp7IjEiOiI1N2Y4MTdkYzU0MTJiZDRhZjBjNzU0NzUiLCJfYXV0aF91c2VyX2lkIjoiMSIsImNvbGVjdG9yX05vbmUiOjIsIl9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9	2016-10-21 21:49:20.168146+00
na4mfhnmaqivhltnpq7tnfxd1v76rqo9	MDZlMmZkNTU4ZDc5Y2UzYTg5MTEzNjcwYTQ3MWIzZDcyMTc0ZTQ4Zjp7IjEiOiI1N2Y4MTdkYzU0MTJiZDRhZjBjNzU0NzUiLCJfYXV0aF91c2VyX2lkIjoiMSIsImNvbGVjdG9yX05vbmUiOjYsIl9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9	2016-10-24 15:13:39.174795+00
0twta6b7s2i0yuhig3eerk1oo702nelk	ODIxZjk4Yzg0ZGU5NjVkOWQ2ZTc3OWEyZWExZWJjMmFkNTljNzBmYTp7IjEiOiI1N2Y4MTdkYzU0MTJiZDRhZjBjNzU0NzUiLCJjb2xlY3Rvcl9Ob25lIjo4LCJfYXV0aF91c2VyX2hhc2giOiI3OTQxZjJmMzM0ZGU3MDBlMDI5Y2U2NDMxMDIxYjEyY2IyMjJhZGVjIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9	2016-11-03 00:50:47.793753+00
wuxket8qqw5cnvj41h13i89bte5do3cu	MmYxZTYyN2EwODNlZjQ0MDAwNDY3Y2JkOTQ2NDQ1MWU1ODgzNTA5Mzp7IjEiOiI1ODBmYTVjNDU0MTJiZDA2ZjhhMGZjMjMiLCJfYXV0aF91c2VyX2lkIjoiMSIsImNvbGVjdG9yX05vbmUiOjEsIl9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9	2016-11-08 18:36:24.178274+00
dpt2lcehxk8f3552te0eezrz8y91sonn	YWMwN2EzNzk5YWU2MTQ5ZGMyOTg0ZjhiNzE3ODFiMTc1MDc4YTEwODp7IjEiOiI1ODBmYTVjNDU0MTJiZDA2ZjhhMGZjMjMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImNvbGVjdG9yX05vbmUiOjQsIl9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2lkIjoiMSJ9	2016-11-10 01:00:39.509439+00
bf919qn92mutjp00hmvp9wd56ck0lgvh	MjY3MjU5MGU5MDM1MGE2NGZjODJmZWFkMDA2NDFiMTNjYmMyNDkwOTp7IjEiOiI1ODI5ZjdjODU0MTJiZDU2NWRlOTczZWMiLCJjb2xlY3Rvcl9Ob25lIjoyLCJfYXV0aF91c2VyX2hhc2giOiI3OTQxZjJmMzM0ZGU3MDBlMDI5Y2U2NDMxMDIxYjEyY2IyMjJhZGVjIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9	2016-11-28 17:44:15.290336+00
zyvbe1wg5a2pdvlazpxzl550goagug4n	NzFhZWE5YzhjMmQ5NWJiNDJkOGFlYTYyOWIyYTFlZmYyZTE2MjhmMzp7IjEiOiI1ODI5ZjdjODU0MTJiZDU2NWRlOTczZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImNvbGVjdG9yX05vbmUiOjMsIl9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2lkIjoiMSJ9	2016-11-28 18:10:41.378654+00
5wk67de5a83qr83v7lnwoao62t4hgzo2	MWVlMDg3N2FiZTA4NGU3NTJlYTFmZDllOGE2NjcwYmRjOGUxYWI1NDp7fQ==	2016-12-06 14:32:01.806045+00
8dt3xocnd3yfq1r2c6ht3u3bxi7lnwou	ZTFkMjY5ZGY1Nzc5MWY5MDYwZjQ2MzEzMGJhZTg5NGY4ZGMzNDliMzp7IjEiOiI1N2Y4MjU4NzU0MTJiZDU1M2IwNTc0ZTkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImNvbGVjdG9yX05vbmUiOjEzLCJfYXV0aF91c2VyX2hhc2giOiI3OTQxZjJmMzM0ZGU3MDBlMDI5Y2U2NDMxMDIxYjEyY2IyMjJhZGVjIiwiX2F1dGhfdXNlcl9pZCI6IjEifQ==	2016-12-07 01:24:10.720897+00
hce2cfkg611ft5ormp62oeykavp2nfzz	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-12-19 14:15:26.510836+00
s7w8osxqn6nzuym90cewbfrfs5e0mhm1	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2017-01-23 19:06:43.23163+00
vbb2uz51icbrf10h7emfvmbs30swyryu	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2017-01-23 20:58:12.185582+00
uri3fpa7ugvcl2y9nkm1gv7lw8nb81a2	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2017-02-15 16:37:31.182817+00
ikxn6u5gl5zpb8a8xlso021cltoo9t0f	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2017-02-15 20:56:25.329849+00
23vh5528kjonrif2nndo7yy86sx3qr79	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2017-02-23 13:25:36.826879+00
14lqydewu2exy0h9820k0tx5qa77dc2s	MWVlMDg3N2FiZTA4NGU3NTJlYTFmZDllOGE2NjcwYmRjOGUxYWI1NDp7fQ==	2017-02-23 20:46:47.349941+00
f3bsi07fub1xzbh51e7ws89cqltbv8xl	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2017-02-27 19:42:49.203443+00
6yyu9duinrlscha0jqhzog23cl8uwsck	YjYxNGM0ZTc0YTFiOWMzMTAxZmFkMDUwZTk4NWMyZmE4NzYyYTFmODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5NDFmMmYzMzRkZTcwMGUwMjljZTY0MzEwMjFiMTJjYjIyMmFkZWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2017-03-01 13:26:19.947495+00
\.


--
-- Data for Name: registro_asignacionentrada; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_asignacionentrada (id, orden, requerido, oculto, solo_lectura, defecto, defecto_previo, maximo, minimo, validacion, entrada_id, ficha_id, regla_visibilidad_id, formulario_asociado_id, agregar_nuevo) FROM stdin;
1	10	f	f	f		f	\N	\N		1	1	\N	\N	f
2	1	f	f	f		f	\N	\N		2	2	\N	\N	f
3	2	f	f	f		f	\N	\N		3	2	\N	\N	f
4	3	f	f	f		f	\N	\N		4	2	\N	\N	f
5	1	f	f	f		f	\N	\N		5	3	\N	\N	f
7	3	f	f	f		f	\N	\N		7	3	\N	\N	f
8	4	f	f	f		f	\N	\N		8	3	\N	\N	f
9	5	f	f	f		f	\N	\N		9	3	\N	\N	f
10	6	f	f	f		f	\N	\N		10	3	\N	\N	f
11	7	f	f	f		f	\N	\N		11	3	\N	\N	f
12	1	f	f	f		f	\N	\N		12	4	\N	\N	f
13	2	f	f	f		f	\N	\N		13	4	\N	\N	f
14	3	f	f	f		f	\N	\N		14	4	\N	\N	f
15	4	f	f	f		f	\N	\N		15	4	\N	\N	f
16	5	f	f	f		f	\N	\N		16	4	\N	\N	f
17	6	f	f	f		f	\N	\N		17	4	\N	\N	f
18	7	f	f	f		f	\N	\N		18	4	\N	\N	f
19	1	f	f	f		f	\N	\N		2	5	\N	\N	f
20	2	f	f	f		f	\N	\N		3	5	\N	\N	f
21	3	f	f	f		f	\N	\N		5	5	\N	\N	f
23	1	f	f	f		f	\N	\N		8	6	\N	\N	f
24	2	f	f	f		f	\N	\N		13	6	\N	\N	f
25	3	f	f	f		f	\N	\N		15	6	\N	\N	f
26	4	f	f	f		f	\N	\N		17	6	\N	\N	f
27	1	f	f	f		f	\N	\N		8	7	\N	\N	f
28	2	f	f	f		f	\N	\N		18	7	\N	\N	f
29	10	f	f	f		f	\N	\N		19	8	\N	\N	f
31	20	f	f	f		f	\N	\N		20	1	\N	\N	f
32	20	f	f	f		f	\N	\N		21	8	\N	\N	f
35	1	f	f	f		f	\N	\N		1	10	\N	\N	f
36	1	f	f	f		f	\N	\N		2	11	\N	\N	f
37	1	f	f	f		f	\N	\N		3	12	\N	\N	f
38	1	f	f	f		f	\N	\N		24	13	\N	\N	f
39	2	f	f	f		f	\N	\N		25	13	\N	\N	f
40	1	f	f	f		f	\N	\N		26	14	\N	\N	f
41	2	f	f	f		f	\N	\N		27	14	\N	\N	f
42	3	f	f	f		f	\N	\N		28	14	\N	\N	f
43	1	f	f	f		f	\N	\N		29	15	\N	\N	f
44	2	f	f	f		f	\N	\N		30	15	\N	\N	f
45	3	f	f	f		f	\N	\N		31	15	\N	\N	f
46	4	f	f	f		f	\N	\N		32	15	\N	\N	f
47	5	f	f	f		f	\N	\N		33	15	\N	\N	f
48	6	f	f	f		f	\N	\N		34	15	\N	\N	f
49	7	f	f	f		f	\N	\N		35	15	\N	\N	f
50	1	f	f	f		f	\N	\N		6	16	\N	\N	f
6	2	f	f	f		f	\N	\N		6	3	\N	\N	f
22	4	f	f	f		f	\N	\N		6	5	\N	\N	f
1170	10	f	f	f		f	\N	\N		999	298	\N	\N	f
1168	10	f	f	f		f	\N	\N		997	297	\N	\N	f
1174	10	f	f	f		f	\N	\N		1003	299	\N	\N	f
1181	10	f	f	f		f	\N	\N		1010	300	\N	\N	f
1187	10	f	f	f		f	\N	\N		1016	301	\N	\N	f
1188	10	f	f	f		f	\N	\N		1017	302	\N	\N	f
1191	10	f	f	f		f	\N	\N		1020	303	\N	\N	f
1195	10	f	f	f		f	\N	\N		1024	304	\N	\N	f
1182	20	f	f	f		f	\N	\N		1011	300	\N	\N	f
1175	20	f	f	f		f	\N	\N		1004	299	\N	\N	f
1171	20	f	f	f		f	\N	\N		1000	298	\N	\N	f
1189	20	f	f	f		f	\N	\N		1018	302	\N	\N	f
1169	20	f	f	f		f	\N	\N		998	297	\N	\N	f
1192	20	f	f	f		f	\N	\N		1021	303	\N	\N	f
1176	30	f	f	f		f	\N	\N		1005	299	\N	\N	f
1183	30	f	f	f		f	\N	\N		1012	300	\N	\N	f
1193	30	f	f	f		f	\N	\N		1022	303	\N	\N	f
1172	30	f	f	f		f	\N	\N		1001	298	\N	\N	f
1190	30	f	f	f		f	\N	\N		1019	302	\N	\N	f
1194	40	f	f	f		f	\N	\N		1023	303	\N	\N	f
1173	40	f	f	f		f	\N	\N		1002	298	\N	\N	f
1184	40	f	f	f		f	\N	\N		1013	300	\N	\N	f
1177	40	f	f	f		f	\N	\N		1006	299	\N	\N	f
1178	50	f	f	f		f	\N	\N		1007	299	\N	\N	f
1185	50	f	f	f		f	\N	\N		1014	300	\N	\N	f
1186	60	f	f	f		f	\N	\N		1015	300	\N	\N	f
1179	60	f	f	f		f	\N	\N		1008	299	\N	\N	f
1180	70	f	f	f		f	\N	\N		1009	299	\N	\N	f
\.


--
-- Name: registro_asignacionentrada_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_asignacionentrada_id_seq', 50, true);


--
-- Data for Name: registro_colector; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_colector (id, usuario_id) FROM stdin;
1	1
2	2
\.


--
-- Name: registro_colector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_colector_id_seq', 2, true);


--
-- Data for Name: registro_colector_respuesta; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_colector_respuesta (id, colector_id, respuesta_id) FROM stdin;
\.


--
-- Name: registro_colector_respuesta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_colector_respuesta_id_seq', 1, false);


--
-- Data for Name: registro_empresa; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_empresa (id, codigo_secreto, nombre, industria, pais, ciudad, correo_empresarial, email, descripcion, nit, correo_facturacion, telefono, plan_id, usuario_id) FROM stdin;
1	contraslash	Contraslash	tech	Colombia	CAli				\N	ma0@contraslash.com	\N	\N	1
\.


--
-- Data for Name: registro_empresa_colector; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_empresa_colector (id, empresa_id, colector_id) FROM stdin;
7	1	1
8	1	2
\.


--
-- Name: registro_empresa_colector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_empresa_colector_id_seq', 8, true);


--
-- Data for Name: registro_empresa_formulario; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_empresa_formulario (id, empresa_id, formulario_id) FROM stdin;
19	1	1
20	1	2
21	1	3
22	1	4
23	1	5
\.


--
-- Name: registro_empresa_formulario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_empresa_formulario_id_seq', 24, true);


--
-- Name: registro_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_empresa_id_seq', 1, true);


--
-- Data for Name: registro_empresa_tablets; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_empresa_tablets (id, empresa_id, tablet_id) FROM stdin;
6	1	1
\.


--
-- Name: registro_empresa_tablets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_empresa_tablets_id_seq', 6, true);


--
-- Data for Name: registro_entrada; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_entrada (id, tipo, nombre, descripcion) FROM stdin;
1	1	Entrada 1	
2	1	Pregunta tipo 1	
3	2	Pregunta tipo 2	
7	6	Pregunta 6	
8	7	Pregunta 7	
9	8	Pregunta 8	
10	9	Pregunta 9	
11	10	Pregunta 10	
12	11	Pregunta 11	
13	12	Pregunta 12	
14	13	Pregunta 13	
15	14	Pregunta 14	
16	15	Pregunta 15	
17	16	Pregunta 16	
18	17	Pregunta 17	
4	3	Pregunta tipo 3	
5	4	Pregunta 4	
1012	8	Telefono	
19	1	Esta pregunta es demasiado, demasiado larga y no se puede ver en el dispositivo movil porque tiene muchisimos caracteres, por esta razon estamos realizando el ajuste de texto	
20	1	Ñ	
21	1	ÑÓ%	
22	1	pregunta andres	
23	4	ciudad	
24	7	Fecha 	Esta es una fecha
25	17	Tiempo	Tiempo
26	6	Foto 1	Foto no 1
27	6	Foto 2	Foto 2
28	6	Foto 3	Foton3
29	8	a	Numero uno
30	8	b	Numero b
31	13	Formula 	/ + #29 #30 10
32	8	c	numero 3
35	13	Formula 3	+ #31 #34
34	13	Formula 2	+ #32 #33
33	8	d	Numero 4
6	5	Pregunta 5	
1013	8	Celular	
1014	8	Telefono Farmacia	
1015	4	Medio de contacto preferido	
1016	4	¿Tiene título tecnico de Aux en servicios farmaceuticos?	
1017	1	Nombres conyuge	
1018	1	Apellidos conyuge	
1019	7	Fecha de nacimiento conyuge	
1020	1	Nombres hijo	
1021	1	Apellidos hijo	
1022	7	Fecha de nacimiento hijo	
1023	4	Genero Hijo	
1024	14	Autorizo y consiento expresamente a que la empresa Tecnoquímicas S.A. registre en un archivo informático , mis datos personales y/o me contacte telefónicamente, por vía electrónica o personalmente, con el fin de informarme sobre las marcas y productos que comercializa, así como de las actividades promocionales que lleva a cabo, todo dentro de los términos autorizados por la legislación respectiva; mantenerme al tanto sobre actividades de educación continuada en las áreas de medicina y el cuidado	
997	4	Seleccione Farmacia	
998	4	Seleccione Dependiente	
999	4	Departamento	
1000	4	Ciudad	
1001	4	¿Es propietario de la farmacia?	
1002	4	¿Tiene facilidad de acceso a internet desde la farmacia?	
1003	4	Tipo de Identificacion	
1004	8	Número de Identificacion	
1005	1	Nombres	
1006	1	Apellidos	
1007	7	Fecha de Nacimiento	
1008	4	Genero	
1009	4	Estado Civil	
1010	1	Correo electronico	
1011	1	Confirmar Correo electrónico	
\.


--
-- Name: registro_entrada_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_entrada_id_seq', 35, true);


--
-- Data for Name: registro_entrada_respuesta; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_entrada_respuesta (id, entrada_id, respuesta_id) FROM stdin;
195	1001	297
196	1001	298
197	1002	297
198	1002	298
199	1003	193848
200	1003	193849
201	1008	193850
202	1008	193851
203	1009	193856
204	1009	193857
205	1009	193852
206	1009	193853
207	1009	193854
208	1009	193855
209	1015	193858
210	1015	193859
211	1015	193860
212	1016	297
213	1016	298
214	1016	193861
215	1016	193862
216	1023	193850
217	1023	193851
218	997	193863
219	998	193864
220	1016	193865
221	1010	193866
222	1014	193867
223	1009	193868
224	1008	193869
225	1007	193870
226	1006	193871
227	1005	193872
228	1004	193873
229	1003	193874
230	1012	193875
231	1013	193876
232	998	193877
233	1016	193878
234	1010	193879
235	1014	193880
236	1009	193881
237	1008	193882
238	1007	193883
239	1006	193884
240	1005	193885
241	1004	193886
242	1003	193887
243	1012	193888
244	1013	193889
245	998	193890
246	1016	193891
247	1010	193892
248	1014	193893
249	1009	193894
250	1008	193895
251	1007	193896
252	1006	193897
253	1005	193898
254	1004	193899
255	1003	193900
256	1012	193901
257	1013	193902
258	998	193903
259	1016	193904
260	1010	193905
261	1014	193906
262	1009	193907
263	1008	193908
264	1007	193909
265	1006	193910
266	1005	193911
267	1004	193912
268	1003	193913
269	1012	193914
270	1013	193915
271	997	193916
272	998	193917
273	1016	193918
274	1010	193919
275	1014	193920
276	1009	193921
277	1008	193922
278	1007	193923
279	1006	193924
280	1005	193925
281	1004	193926
282	1003	193927
283	1012	193928
284	1013	193929
285	998	193930
286	1016	193931
287	1010	193932
288	1014	193933
289	1009	193934
290	1008	193935
291	1007	193936
292	1006	193937
293	1005	193938
294	1004	193939
295	1003	193940
296	1012	193941
297	1013	193942
298	998	193943
299	1016	193944
300	1010	193945
301	1014	193946
302	1009	193947
303	1008	193948
304	1007	193949
305	1006	193950
306	1005	193951
307	1004	193952
308	1003	193953
309	1012	193954
310	1013	193955
311	997	193956
312	998	193957
313	1016	193958
314	1010	193959
315	1014	193960
316	1009	193961
317	1008	193962
318	1007	193963
319	1006	193964
320	1005	193965
321	1004	193966
322	1003	193967
323	1012	193968
324	1013	193969
\.


--
-- Name: registro_entrada_respuesta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_entrada_respuesta_id_seq', 324, true);


--
-- Data for Name: registro_ficha; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_ficha (id, nombre, descripcion, repetible) FROM stdin;
2	Primer segmento		f
3	Segundo segmento		f
4	Tercer Segmento		f
5	Ficha Simplificada 1		f
6	Segmento Simplificado 2		f
7	Fragmento Simplificado 3		f
8	Testing Preguntas largas		f
10	PFM 1		f
11	PFM		f
12	PFM 2		f
13	Ficha de Fecha	Ficha de Fecha	f
1	Ficha 1		t
14	Fotos	Formulario de Fotos	f
15	Formula simple	Esta es una formula simple	f
16	Andres		f
297	1 Farmacias	Tecnoquimicas	f
298	2 Datos de la farmacia		f
299	3 Informacion Personal		f
300	4 Informacion de contacto	Tecnoquimicas	f
301	5 Datos de educacion y laborales	Tecnoquimicas	f
302	6 Datos del conyuge		f
303	7 Datos de los hijos	Tecnoquimicas	t
304	8 Terminos y condiciones		f
\.


--
-- Name: registro_ficha_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_ficha_id_seq', 16, true);


--
-- Data for Name: registro_formulario; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_formulario (id, nombre, descripcion, titulo_reporte_id, titulo_reporte2_id) FROM stdin;
1	F1	rtykl	1	1
2	Form completo		1	1
3	Formulario Funcional		\N	\N
4	Formulario Agregar OTro		\N	\N
5	Testing Preguntas largas		19	\N
7	Prueba Secciones Multiples	Pruena de los super formularios con respuesta multiple	1	2
8	Formulario de Fecha	Form de Fecha	\N	\N
9	Formulario Fotos	Formulario de las Fotos	\N	\N
10	Formulas	Formulario con las Formulas	\N	\N
6	Andres	testing	\N	\N
229	Farmacias	Tecnoquimicas	997	998
\.


--
-- Data for Name: registro_formulario_ficha; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_formulario_ficha (id, formulario_id, ficha_id) FROM stdin;
3	1	1
4	2	2
5	2	3
6	2	4
7	3	5
8	3	6
9	3	7
10	4	5
12	5	8
16	7	10
17	7	11
18	7	12
19	8	13
20	9	14
22	10	15
24	6	16
49	229	297
50	229	298
51	229	299
52	229	300
53	229	301
54	229	302
55	229	303
56	229	304
\.


--
-- Name: registro_formulario_ficha_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_formulario_ficha_id_seq', 56, true);


--
-- Name: registro_formulario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_formulario_id_seq', 10, true);


--
-- Data for Name: registro_formularioasociado; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_formularioasociado (id, seleccionar_existentes, crear_nuevo, actualizar_existente, seleccionar_multiples, form_asociado_id) FROM stdin;
\.


--
-- Name: registro_formularioasociado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_formularioasociado_id_seq', 1, false);


--
-- Data for Name: registro_formulariodiligenciado; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_formulariodiligenciado (id, nombre, gps, fecha_creacion, colector_id, empresa_id, entrada_id, respuesta_id) FROM stdin;
\.


--
-- Name: registro_formulariodiligenciado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_formulariodiligenciado_id_seq', 1, false);


--
-- Data for Name: registro_permisoformulario; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_permisoformulario (id, formulario_id) FROM stdin;
11	229
\.


--
-- Data for Name: registro_permisoformulario_colectores; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_permisoformulario_colectores (id, permisoformulario_id, colector_id) FROM stdin;
11	11	1
\.


--
-- Name: registro_permisoformulario_colectores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_permisoformulario_colectores_id_seq', 11, true);


--
-- Name: registro_permisoformulario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_permisoformulario_id_seq', 11, true);


--
-- Data for Name: registro_plan; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_plan (id, nombre, almacenamiento, cantidad_colectores, valor, activo, fecha_creacion) FROM stdin;
\.


--
-- Name: registro_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_plan_id_seq', 1, false);


--
-- Data for Name: registro_reglaautollenado; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_reglaautollenado (id, asociacion_id, entrada_destino_id, entrada_fuente_id) FROM stdin;
\.


--
-- Name: registro_reglaautollenado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_reglaautollenado_id_seq', 1, false);


--
-- Data for Name: registro_reglavisibilidad; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_reglavisibilidad (id, operador, valor, elemento_id) FROM stdin;
\.


--
-- Name: registro_reglavisibilidad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_reglavisibilidad_id_seq', 1, false);


--
-- Data for Name: registro_respuesta; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_respuesta (id, valor, pregunta_id, respuesta, usuario_id) FROM stdin;
297	Si	\N	\N	\N
298	No	\N	\N	\N
193848	CC Cedula de ciudadania	\N	\N	\N
193849	CE Cedula de Extranjeria	\N	\N	\N
193850	MASCULINO	\N	\N	\N
193851	FEMENINO	\N	\N	\N
193852	CASADO	\N	\N	\N
193853	DIVORCIADO	\N	\N	\N
193854	SEPARADO	\N	\N	\N
193855	SOLTERO	\N	\N	\N
193856	UNION LIBRE	\N	\N	\N
193857	VIUDO(A)	\N	\N	\N
193858	Correo electronico	\N	\N	\N
193859	Telefono fijo	\N	\N	\N
193860	Celular	\N	\N	\N
193861	En curso	\N	\N	\N
193862	Sin dato	\N	\N	\N
193863	300519	\N	\N	\N
193864	386856	997	300519	\N
193865	Si	998	386856	\N
193866	aurorap3927@hotmail.com	998	386856	\N
193867	2585435	998	386856	\N
193868	UNION LIBRE	998	386856	\N
193869	FEMENINO	998	386856	\N
193870	12/7/60 0:00	998	386856	\N
193871	PEÑA WALTEROS 	998	386856	\N
193872	AURORA	998	386856	\N
193873	51577879	998	386856	\N
193874	CC	998	386856	\N
193875		998	386856	\N
193876	NULL	998	386856	\N
193877	386859	997	300519	\N
193878	Si	998	386859	\N
193879	cristianperez.ld@gmail.com	998	386859	\N
193880	2585435	998	386859	\N
193881	UNION LIBRE	998	386859	\N
193882	MASCULINO	998	386859	\N
193883	2/3/93 0:00	998	386859	\N
193884	PEREZ MEZA 	998	386859	\N
193885	CRISTIAN LUIS	998	386859	\N
193886	1104014178	998	386859	\N
193887	CC	998	386859	\N
193888		998	386859	\N
193889	NULL	998	386859	\N
193890	388562	997	300519	\N
193891	Si	998	388562	\N
193892	carlop708@hotmail.com	998	388562	\N
193893	2585435	998	388562	\N
193894	CASADO	998	388562	\N
193895	MASCULINO	998	388562	\N
193896	2/8/77 0:00	998	388562	\N
193897	PINZON GOMEZ 	998	388562	\N
193898	CARLOS EDUARDO	998	388562	\N
193899	79804150	998	388562	\N
193900	CC	998	388562	\N
193901		998	388562	\N
193902	NULL	998	388562	\N
193903	388758	997	300519	\N
193904	Si	998	388758	\N
193905	lulu954@hotmail.com	998	388758	\N
193906	2585435	998	388758	\N
193907	UNION LIBRE	998	388758	\N
193908	FEMENINO	998	388758	\N
193909	7/13/82 0:00	998	388758	\N
193910	MADRIGAL VIANCHA 	998	388758	\N
193911	OLGA LUCIA	998	388758	\N
193912	52952333	998	388758	\N
193913	CC	998	388758	\N
193914		998	388758	\N
193915	NULL	998	388758	\N
193916	300520	\N	\N	\N
193917	385301	997	300520	\N
193918	Sin Dato	998	385301	\N
193919		998	385301	\N
193920	2748443	998	385301	\N
193921	CASADO	998	385301	\N
193922	FEMENINO	998	385301	\N
193923	12/9/85 0:00	998	385301	\N
193924	QUIROGA RUEDA 	998	385301	\N
193925	CONSUELO	998	385301	\N
193926	1099202246	998	385301	\N
193927	CC	998	385301	\N
193928		998	385301	\N
193929	NULL	998	385301	\N
193930	385302	997	300520	\N
193931	Si	998	385302	\N
193932	monic9028@hotmail.com	998	385302	\N
193933	2748443	998	385302	\N
193934	SOLTERO	998	385302	\N
193935	FEMENINO	998	385302	\N
193936	12/25/86 0:00	998	385302	\N
193937	ARDILA RAMIREZ 	998	385302	\N
193938	MONICA ANDREA	998	385302	\N
193939	1022329028	998	385302	\N
193940	CC	998	385302	\N
193941		998	385302	\N
193942	NULL	998	385302	\N
193943	403793	997	300520	\N
193944	Si	998	403793	\N
193945	samyandres67@hotmail.com	998	403793	\N
193946	2748443	998	403793	\N
193947	UNION LIBRE	998	403793	\N
193948	FEMENINO	998	403793	\N
193949	11/6/84 0:00	998	403793	\N
193950	VILLEGAS LOPEZ 	998	403793	\N
193951	NAIBETH DEL CARMEN	998	403793	\N
193952	43890793	998	403793	\N
193953	CC	998	403793	\N
193954		998	403793	\N
193955	NULL	998	403793	\N
193956	300529	\N	\N	\N
193957	388167	997	300529	\N
193958	Si	998	388167	\N
193959	nomanejacorreo@hotmail.com	998	388167	\N
193960	3602315	998	388167	\N
193961	SOLTERO	998	388167	\N
193962	FEMENINO	998	388167	\N
193963	6/8/82 0:00	998	388167	\N
193964	RIVERA RIVERA 	998	388167	\N
193965	ADRIANA MILENA	998	388167	\N
193966	52905503	998	388167	\N
193967	CC	998	388167	\N
193968		998	388167	\N
193969	NULL	998	388167	\N
\.


--
-- Name: registro_respuesta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_respuesta_id_seq', 193969, true);


--
-- Data for Name: registro_tablet; Type: TABLE DATA; Schema: public; Owner: colectoruser
--

COPY registro_tablet (id, codigo) FROM stdin;
1	001
2	002
\.


--
-- Name: registro_tablet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: colectoruser
--

SELECT pg_catalog.setval('registro_tablet_id_seq', 2, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_token_middleware_token auth_token_middleware_token_empresa_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_token_middleware_token
    ADD CONSTRAINT auth_token_middleware_token_empresa_id_key UNIQUE (empresa_id);


--
-- Name: auth_token_middleware_token auth_token_middleware_token_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_token_middleware_token
    ADD CONSTRAINT auth_token_middleware_token_pkey PRIMARY KEY (id);


--
-- Name: auth_token_middleware_token auth_token_middleware_token_valor_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_token_middleware_token
    ADD CONSTRAINT auth_token_middleware_token_valor_key UNIQUE (valor);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: registro_asignacionentrada registro_asignacionentrada_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_asignacionentrada
    ADD CONSTRAINT registro_asignacionentrada_pkey PRIMARY KEY (id);


--
-- Name: registro_colector registro_colector_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector
    ADD CONSTRAINT registro_colector_pkey PRIMARY KEY (id);


--
-- Name: registro_colector_respuesta registro_colector_respuesta_colector_id_respuesta_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector_respuesta
    ADD CONSTRAINT registro_colector_respuesta_colector_id_respuesta_id_key UNIQUE (colector_id, respuesta_id);


--
-- Name: registro_colector_respuesta registro_colector_respuesta_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector_respuesta
    ADD CONSTRAINT registro_colector_respuesta_pkey PRIMARY KEY (id);


--
-- Name: registro_colector registro_colector_usuario_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector
    ADD CONSTRAINT registro_colector_usuario_id_key UNIQUE (usuario_id);


--
-- Name: registro_empresa_colector registro_empresa_colector_empresa_id_colector_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_colector
    ADD CONSTRAINT registro_empresa_colector_empresa_id_colector_id_key UNIQUE (empresa_id, colector_id);


--
-- Name: registro_empresa_colector registro_empresa_colector_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_colector
    ADD CONSTRAINT registro_empresa_colector_pkey PRIMARY KEY (id);


--
-- Name: registro_empresa registro_empresa_correo_facturacion_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa
    ADD CONSTRAINT registro_empresa_correo_facturacion_key UNIQUE (correo_facturacion);


--
-- Name: registro_empresa_formulario registro_empresa_formulario_empresa_id_formulario_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_formulario
    ADD CONSTRAINT registro_empresa_formulario_empresa_id_formulario_id_key UNIQUE (empresa_id, formulario_id);


--
-- Name: registro_empresa_formulario registro_empresa_formulario_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_formulario
    ADD CONSTRAINT registro_empresa_formulario_pkey PRIMARY KEY (id);


--
-- Name: registro_empresa registro_empresa_nombre_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa
    ADD CONSTRAINT registro_empresa_nombre_key UNIQUE (nombre);


--
-- Name: registro_empresa registro_empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa
    ADD CONSTRAINT registro_empresa_pkey PRIMARY KEY (id);


--
-- Name: registro_empresa_tablets registro_empresa_tablets_empresa_id_tablet_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_tablets
    ADD CONSTRAINT registro_empresa_tablets_empresa_id_tablet_id_key UNIQUE (empresa_id, tablet_id);


--
-- Name: registro_empresa_tablets registro_empresa_tablets_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_tablets
    ADD CONSTRAINT registro_empresa_tablets_pkey PRIMARY KEY (id);


--
-- Name: registro_empresa registro_empresa_usuario_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa
    ADD CONSTRAINT registro_empresa_usuario_id_key UNIQUE (usuario_id);


--
-- Name: registro_entrada registro_entrada_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_entrada
    ADD CONSTRAINT registro_entrada_pkey PRIMARY KEY (id);


--
-- Name: registro_entrada_respuesta registro_entrada_respuesta_entrada_id_respuesta_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_entrada_respuesta
    ADD CONSTRAINT registro_entrada_respuesta_entrada_id_respuesta_id_key UNIQUE (entrada_id, respuesta_id);


--
-- Name: registro_entrada_respuesta registro_entrada_respuesta_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_entrada_respuesta
    ADD CONSTRAINT registro_entrada_respuesta_pkey PRIMARY KEY (id);


--
-- Name: registro_ficha registro_ficha_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_ficha
    ADD CONSTRAINT registro_ficha_pkey PRIMARY KEY (id);


--
-- Name: registro_formulario_ficha registro_formulario_ficha_formulario_id_ficha_id_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario_ficha
    ADD CONSTRAINT registro_formulario_ficha_formulario_id_ficha_id_key UNIQUE (formulario_id, ficha_id);


--
-- Name: registro_formulario_ficha registro_formulario_ficha_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario_ficha
    ADD CONSTRAINT registro_formulario_ficha_pkey PRIMARY KEY (id);


--
-- Name: registro_formulario registro_formulario_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario
    ADD CONSTRAINT registro_formulario_pkey PRIMARY KEY (id);


--
-- Name: registro_formularioasociado registro_formularioasociado_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formularioasociado
    ADD CONSTRAINT registro_formularioasociado_pkey PRIMARY KEY (id);


--
-- Name: registro_formulariodiligenciado registro_formulariodiligenciado_gps_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado
    ADD CONSTRAINT registro_formulariodiligenciado_gps_key UNIQUE (gps);


--
-- Name: registro_formulariodiligenciado registro_formulariodiligenciado_nombre_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado
    ADD CONSTRAINT registro_formulariodiligenciado_nombre_key UNIQUE (nombre);


--
-- Name: registro_formulariodiligenciado registro_formulariodiligenciado_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado
    ADD CONSTRAINT registro_formulariodiligenciado_pkey PRIMARY KEY (id);


--
-- Name: registro_permisoformulario_colectores registro_permisoformulario_co_permisoformulario_id_colector_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario_colectores
    ADD CONSTRAINT registro_permisoformulario_co_permisoformulario_id_colector_key UNIQUE (permisoformulario_id, colector_id);


--
-- Name: registro_permisoformulario_colectores registro_permisoformulario_colectores_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario_colectores
    ADD CONSTRAINT registro_permisoformulario_colectores_pkey PRIMARY KEY (id);


--
-- Name: registro_permisoformulario registro_permisoformulario_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario
    ADD CONSTRAINT registro_permisoformulario_pkey PRIMARY KEY (id);


--
-- Name: registro_plan registro_plan_almacenamiento_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_plan
    ADD CONSTRAINT registro_plan_almacenamiento_key UNIQUE (almacenamiento);


--
-- Name: registro_plan registro_plan_cantidad_colectores_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_plan
    ADD CONSTRAINT registro_plan_cantidad_colectores_key UNIQUE (cantidad_colectores);


--
-- Name: registro_plan registro_plan_nombre_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_plan
    ADD CONSTRAINT registro_plan_nombre_key UNIQUE (nombre);


--
-- Name: registro_plan registro_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_plan
    ADD CONSTRAINT registro_plan_pkey PRIMARY KEY (id);


--
-- Name: registro_plan registro_plan_valor_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_plan
    ADD CONSTRAINT registro_plan_valor_key UNIQUE (valor);


--
-- Name: registro_reglaautollenado registro_reglaautollenado_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglaautollenado
    ADD CONSTRAINT registro_reglaautollenado_pkey PRIMARY KEY (id);


--
-- Name: registro_reglavisibilidad registro_reglavisibilidad_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglavisibilidad
    ADD CONSTRAINT registro_reglavisibilidad_pkey PRIMARY KEY (id);


--
-- Name: registro_respuesta registro_respuesta_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_respuesta
    ADD CONSTRAINT registro_respuesta_pkey PRIMARY KEY (id);


--
-- Name: registro_tablet registro_tablet_codigo_key; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_tablet
    ADD CONSTRAINT registro_tablet_codigo_key UNIQUE (codigo);


--
-- Name: registro_tablet registro_tablet_pkey; Type: CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_tablet
    ADD CONSTRAINT registro_tablet_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_253ae2a6331666e8_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_group_name_253ae2a6331666e8_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_token_middleware_token_valor_641326bdafffd8d8_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_token_middleware_token_valor_641326bdafffd8d8_like ON auth_token_middleware_token USING btree (valor varchar_pattern_ops);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_51b3b110094b8aae_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX auth_user_username_51b3b110094b8aae_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_461cfeaa630ca218_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX django_session_session_key_461cfeaa630ca218_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: registro_asignacionentrada_2ad1438c; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_asignacionentrada_2ad1438c ON registro_asignacionentrada USING btree (entrada_id);


--
-- Name: registro_asignacionentrada_2f0ae1d1; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_asignacionentrada_2f0ae1d1 ON registro_asignacionentrada USING btree (regla_visibilidad_id);


--
-- Name: registro_asignacionentrada_312489a9; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_asignacionentrada_312489a9 ON registro_asignacionentrada USING btree (formulario_asociado_id);


--
-- Name: registro_asignacionentrada_c3d5c3d9; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_asignacionentrada_c3d5c3d9 ON registro_asignacionentrada USING btree (ficha_id);


--
-- Name: registro_colector_respuesta_b4ab1600; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_colector_respuesta_b4ab1600 ON registro_colector_respuesta USING btree (colector_id);


--
-- Name: registro_colector_respuesta_d8b57d2a; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_colector_respuesta_d8b57d2a ON registro_colector_respuesta USING btree (respuesta_id);


--
-- Name: registro_empresa_60fb6a05; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_60fb6a05 ON registro_empresa USING btree (plan_id);


--
-- Name: registro_empresa_colector_b4ab1600; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_colector_b4ab1600 ON registro_empresa_colector USING btree (colector_id);


--
-- Name: registro_empresa_colector_e8f8b1ef; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_colector_e8f8b1ef ON registro_empresa_colector USING btree (empresa_id);


--
-- Name: registro_empresa_correo_facturacion_31ceab1cc65ac862_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_correo_facturacion_31ceab1cc65ac862_like ON registro_empresa USING btree (correo_facturacion varchar_pattern_ops);


--
-- Name: registro_empresa_formulario_3fe51010; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_formulario_3fe51010 ON registro_empresa_formulario USING btree (formulario_id);


--
-- Name: registro_empresa_formulario_e8f8b1ef; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_formulario_e8f8b1ef ON registro_empresa_formulario USING btree (empresa_id);


--
-- Name: registro_empresa_nombre_24bf6b8bbdf81a79_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_nombre_24bf6b8bbdf81a79_like ON registro_empresa USING btree (nombre varchar_pattern_ops);


--
-- Name: registro_empresa_tablets_8ca10402; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_tablets_8ca10402 ON registro_empresa_tablets USING btree (tablet_id);


--
-- Name: registro_empresa_tablets_e8f8b1ef; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_empresa_tablets_e8f8b1ef ON registro_empresa_tablets USING btree (empresa_id);


--
-- Name: registro_entrada_nombre_4d9916f57b5c6c7b_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_entrada_nombre_4d9916f57b5c6c7b_like ON registro_entrada USING btree (nombre varchar_pattern_ops);


--
-- Name: registro_entrada_respuesta_2ad1438c; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_entrada_respuesta_2ad1438c ON registro_entrada_respuesta USING btree (entrada_id);


--
-- Name: registro_entrada_respuesta_d8b57d2a; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_entrada_respuesta_d8b57d2a ON registro_entrada_respuesta USING btree (respuesta_id);


--
-- Name: registro_ficha_nombre_48ccf372cc78fe53_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_ficha_nombre_48ccf372cc78fe53_like ON registro_ficha USING btree (nombre varchar_pattern_ops);


--
-- Name: registro_formulario_af7ea66d; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulario_af7ea66d ON registro_formulario USING btree (titulo_reporte_id);


--
-- Name: registro_formulario_f32bead0; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulario_f32bead0 ON registro_formulario USING btree (titulo_reporte2_id);


--
-- Name: registro_formulario_ficha_3fe51010; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulario_ficha_3fe51010 ON registro_formulario_ficha USING btree (formulario_id);


--
-- Name: registro_formulario_ficha_c3d5c3d9; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulario_ficha_c3d5c3d9 ON registro_formulario_ficha USING btree (ficha_id);


--
-- Name: registro_formulario_nombre_7e73945a21029e9f_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulario_nombre_7e73945a21029e9f_like ON registro_formulario USING btree (nombre varchar_pattern_ops);


--
-- Name: registro_formularioasociado_88a5c16b; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formularioasociado_88a5c16b ON registro_formularioasociado USING btree (form_asociado_id);


--
-- Name: registro_formulariodiligenciado_2ad1438c; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulariodiligenciado_2ad1438c ON registro_formulariodiligenciado USING btree (entrada_id);


--
-- Name: registro_formulariodiligenciado_b4ab1600; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulariodiligenciado_b4ab1600 ON registro_formulariodiligenciado USING btree (colector_id);


--
-- Name: registro_formulariodiligenciado_d8b57d2a; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulariodiligenciado_d8b57d2a ON registro_formulariodiligenciado USING btree (respuesta_id);


--
-- Name: registro_formulariodiligenciado_e8f8b1ef; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulariodiligenciado_e8f8b1ef ON registro_formulariodiligenciado USING btree (empresa_id);


--
-- Name: registro_formulariodiligenciado_gps_5a78e4d51fc1585_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulariodiligenciado_gps_5a78e4d51fc1585_like ON registro_formulariodiligenciado USING btree (gps varchar_pattern_ops);


--
-- Name: registro_formulariodiligenciado_nombre_2e349e1edb2f0da9_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_formulariodiligenciado_nombre_2e349e1edb2f0da9_like ON registro_formulariodiligenciado USING btree (nombre varchar_pattern_ops);


--
-- Name: registro_permisoformulario_3fe51010; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_permisoformulario_3fe51010 ON registro_permisoformulario USING btree (formulario_id);


--
-- Name: registro_permisoformulario_colectores_7e70c868; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_permisoformulario_colectores_7e70c868 ON registro_permisoformulario_colectores USING btree (permisoformulario_id);


--
-- Name: registro_permisoformulario_colectores_b4ab1600; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_permisoformulario_colectores_b4ab1600 ON registro_permisoformulario_colectores USING btree (colector_id);


--
-- Name: registro_plan_almacenamiento_3079f5ee7751e7f7_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_plan_almacenamiento_3079f5ee7751e7f7_like ON registro_plan USING btree (almacenamiento varchar_pattern_ops);


--
-- Name: registro_plan_nombre_74df3f3cd8dec192_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_plan_nombre_74df3f3cd8dec192_like ON registro_plan USING btree (nombre varchar_pattern_ops);


--
-- Name: registro_plan_valor_5fdb09c0e7e13e34_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_plan_valor_5fdb09c0e7e13e34_like ON registro_plan USING btree (valor varchar_pattern_ops);


--
-- Name: registro_reglaautollenado_02228b53; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_reglaautollenado_02228b53 ON registro_reglaautollenado USING btree (entrada_destino_id);


--
-- Name: registro_reglaautollenado_a3e3b0e7; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_reglaautollenado_a3e3b0e7 ON registro_reglaautollenado USING btree (asociacion_id);


--
-- Name: registro_reglaautollenado_e1091b8d; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_reglaautollenado_e1091b8d ON registro_reglaautollenado USING btree (entrada_fuente_id);


--
-- Name: registro_reglavisibilidad_114045bd; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_reglavisibilidad_114045bd ON registro_reglavisibilidad USING btree (elemento_id);


--
-- Name: registro_respuesta_abfe0f96; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_respuesta_abfe0f96 ON registro_respuesta USING btree (usuario_id);


--
-- Name: registro_respuesta_valor_1edd5513f3a3cc1c_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_respuesta_valor_1edd5513f3a3cc1c_like ON registro_respuesta USING btree (valor varchar_pattern_ops);


--
-- Name: registro_tablet_codigo_691444214f439837_like; Type: INDEX; Schema: public; Owner: colectoruser
--

CREATE INDEX registro_tablet_codigo_691444214f439837_like ON registro_tablet USING btree (codigo varchar_pattern_ops);


--
-- Name: registro_reglaautollenado D0cd9c389889cd1cc1b5a401eb4f0a1b; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglaautollenado
    ADD CONSTRAINT "D0cd9c389889cd1cc1b5a401eb4f0a1b" FOREIGN KEY (asociacion_id) REFERENCES registro_formularioasociado(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_asignacionentrada D2bf308a56f8fdf0025c8a8a0779c013; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_asignacionentrada
    ADD CONSTRAINT "D2bf308a56f8fdf0025c8a8a0779c013" FOREIGN KEY (regla_visibilidad_id) REFERENCES registro_reglavisibilidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_asignacionentrada D42248afa68d2f7cc72e87ede4e47acf; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_asignacionentrada
    ADD CONSTRAINT "D42248afa68d2f7cc72e87ede4e47acf" FOREIGN KEY (formulario_asociado_id) REFERENCES registro_formularioasociado(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_token_middleware_token auth_token_m_empresa_id_414704926444926e_fk_registro_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_token_middleware_token
    ADD CONSTRAINT auth_token_m_empresa_id_414704926444926e_fk_registro_empresa_id FOREIGN KEY (empresa_id) REFERENCES registro_empresa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_permisoformulario_colectores ba5bfa8a0e5618acacde385872bffee1; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario_colectores
    ADD CONSTRAINT ba5bfa8a0e5618acacde385872bffee1 FOREIGN KEY (permisoformulario_id) REFERENCES registro_permisoformulario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formularioasociado reg_form_asociado_id_21413be186086cef_fk_registro_formulario_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formularioasociado
    ADD CONSTRAINT reg_form_asociado_id_21413be186086cef_fk_registro_formulario_id FOREIGN KEY (form_asociado_id) REFERENCES registro_formulario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_reglaautollenado regi_entrada_destino_id_45f92e1ef400eae7_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglaautollenado
    ADD CONSTRAINT regi_entrada_destino_id_45f92e1ef400eae7_fk_registro_entrada_id FOREIGN KEY (entrada_destino_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulario regi_titulo_reporte2_id_619ba5d185b784a7_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario
    ADD CONSTRAINT regi_titulo_reporte2_id_619ba5d185b784a7_fk_registro_entrada_id FOREIGN KEY (titulo_reporte2_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_reglaautollenado regis_entrada_fuente_id_6c26aeace4b5afd5_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglaautollenado
    ADD CONSTRAINT regis_entrada_fuente_id_6c26aeace4b5afd5_fk_registro_entrada_id FOREIGN KEY (entrada_fuente_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulario regis_titulo_reporte_id_63ff04dfc9a88014_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario
    ADD CONSTRAINT regis_titulo_reporte_id_63ff04dfc9a88014_fk_registro_entrada_id FOREIGN KEY (titulo_reporte_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_permisoformulario regist_formulario_id_17a15a9d619670d1_fk_registro_formulario_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario
    ADD CONSTRAINT regist_formulario_id_17a15a9d619670d1_fk_registro_formulario_id FOREIGN KEY (formulario_id) REFERENCES registro_formulario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulario_ficha regist_formulario_id_28c136d8969d2317_fk_registro_formulario_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario_ficha
    ADD CONSTRAINT regist_formulario_id_28c136d8969d2317_fk_registro_formulario_id FOREIGN KEY (formulario_id) REFERENCES registro_formulario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa_formulario regist_formulario_id_407f3a648a49d29d_fk_registro_formulario_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_formulario
    ADD CONSTRAINT regist_formulario_id_407f3a648a49d29d_fk_registro_formulario_id FOREIGN KEY (formulario_id) REFERENCES registro_formulario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_asignacionentrada registro_asi_entrada_id_382a9520dbd0132f_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_asignacionentrada
    ADD CONSTRAINT registro_asi_entrada_id_382a9520dbd0132f_fk_registro_entrada_id FOREIGN KEY (entrada_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_asignacionentrada registro_asignac_ficha_id_7a42db5ba5d33e6d_fk_registro_ficha_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_asignacionentrada
    ADD CONSTRAINT registro_asignac_ficha_id_7a42db5ba5d33e6d_fk_registro_ficha_id FOREIGN KEY (ficha_id) REFERENCES registro_ficha(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_colector_respuesta registro_c_colector_id_171f148b26e8bddc_fk_registro_colector_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector_respuesta
    ADD CONSTRAINT registro_c_colector_id_171f148b26e8bddc_fk_registro_colector_id FOREIGN KEY (colector_id) REFERENCES registro_colector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_colector registro_colector_usuario_id_6a3a74424c6b8d3b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector
    ADD CONSTRAINT registro_colector_usuario_id_6a3a74424c6b8d3b_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa_colector registro_e_colector_id_5ee674775c300deb_fk_registro_colector_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_colector
    ADD CONSTRAINT registro_e_colector_id_5ee674775c300deb_fk_registro_colector_id FOREIGN KEY (colector_id) REFERENCES registro_colector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_entrada_respuesta registro_e_respuesta_id_6190d89d6a11c3_fk_registro_respuesta_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_entrada_respuesta
    ADD CONSTRAINT registro_e_respuesta_id_6190d89d6a11c3_fk_registro_respuesta_id FOREIGN KEY (respuesta_id) REFERENCES registro_respuesta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa_tablets registro_emp_empresa_id_6244fcfc9b65eadf_fk_registro_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_tablets
    ADD CONSTRAINT registro_emp_empresa_id_6244fcfc9b65eadf_fk_registro_empresa_id FOREIGN KEY (empresa_id) REFERENCES registro_empresa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa_colector registro_emp_empresa_id_68c53fb0d1ffd8f6_fk_registro_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_colector
    ADD CONSTRAINT registro_emp_empresa_id_68c53fb0d1ffd8f6_fk_registro_empresa_id FOREIGN KEY (empresa_id) REFERENCES registro_empresa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa_formulario registro_emp_empresa_id_707f09d14eaa523f_fk_registro_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_formulario
    ADD CONSTRAINT registro_emp_empresa_id_707f09d14eaa523f_fk_registro_empresa_id FOREIGN KEY (empresa_id) REFERENCES registro_empresa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa_tablets registro_empre_tablet_id_40c4f26dd82f3ec3_fk_registro_tablet_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa_tablets
    ADD CONSTRAINT registro_empre_tablet_id_40c4f26dd82f3ec3_fk_registro_tablet_id FOREIGN KEY (tablet_id) REFERENCES registro_tablet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa registro_empresa_plan_id_6d6d4cd8a10c5b88_fk_registro_plan_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa
    ADD CONSTRAINT registro_empresa_plan_id_6d6d4cd8a10c5b88_fk_registro_plan_id FOREIGN KEY (plan_id) REFERENCES registro_plan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_empresa registro_empresa_usuario_id_5de0264360325f56_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_empresa
    ADD CONSTRAINT registro_empresa_usuario_id_5de0264360325f56_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_entrada_respuesta registro_entr_entrada_id_e975abed22bf762_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_entrada_respuesta
    ADD CONSTRAINT registro_entr_entrada_id_e975abed22bf762_fk_registro_entrada_id FOREIGN KEY (entrada_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulariodiligenciado registro_f_colector_id_62e44d9ce7f80b4e_fk_registro_colector_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado
    ADD CONSTRAINT registro_f_colector_id_62e44d9ce7f80b4e_fk_registro_colector_id FOREIGN KEY (colector_id) REFERENCES registro_colector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulariodiligenciado registro_for_empresa_id_7429b3f2c40fc46d_fk_registro_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado
    ADD CONSTRAINT registro_for_empresa_id_7429b3f2c40fc46d_fk_registro_empresa_id FOREIGN KEY (empresa_id) REFERENCES registro_empresa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulariodiligenciado registro_for_entrada_id_52a1704e2220bbd1_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado
    ADD CONSTRAINT registro_for_entrada_id_52a1704e2220bbd1_fk_registro_entrada_id FOREIGN KEY (entrada_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulario_ficha registro_formula_ficha_id_338bb2a2115d285b_fk_registro_ficha_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulario_ficha
    ADD CONSTRAINT registro_formula_ficha_id_338bb2a2115d285b_fk_registro_ficha_id FOREIGN KEY (ficha_id) REFERENCES registro_ficha(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_permisoformulario_colectores registro_pe_colector_id_686ebd902d92e5b_fk_registro_colector_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_permisoformulario_colectores
    ADD CONSTRAINT registro_pe_colector_id_686ebd902d92e5b_fk_registro_colector_id FOREIGN KEY (colector_id) REFERENCES registro_colector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_reglavisibilidad registro_re_elemento_id_1c1b0de8a527f98d_fk_registro_entrada_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_reglavisibilidad
    ADD CONSTRAINT registro_re_elemento_id_1c1b0de8a527f98d_fk_registro_entrada_id FOREIGN KEY (elemento_id) REFERENCES registro_entrada(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_formulariodiligenciado registro_respuesta_id_4c85f89f1f0cc63c_fk_registro_respuesta_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_formulariodiligenciado
    ADD CONSTRAINT registro_respuesta_id_4c85f89f1f0cc63c_fk_registro_respuesta_id FOREIGN KEY (respuesta_id) REFERENCES registro_respuesta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_colector_respuesta registro_respuesta_id_53f547fd3f2e8952_fk_registro_respuesta_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_colector_respuesta
    ADD CONSTRAINT registro_respuesta_id_53f547fd3f2e8952_fk_registro_respuesta_id FOREIGN KEY (respuesta_id) REFERENCES registro_respuesta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registro_respuesta registro_respuesta_usuario_id_4d28a4eefff5d933_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: colectoruser
--

ALTER TABLE ONLY registro_respuesta
    ADD CONSTRAINT registro_respuesta_usuario_id_4d28a4eefff5d933_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

