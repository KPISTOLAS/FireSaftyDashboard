
CREATE TABLE public.nodes (
  node_id character varying(20) NOT NULL,
  title character varying(50) NULL,
  location character varying(50) NULL,
  description text NULL,
  is_parent boolean NULL DEFAULT false,
  lat double precision NULL,
  lng double precision NULL,
  CONSTRAINT nodes_pkey PRIMARY KEY (node_id)
) TABLESPACE pg_default;

CREATE TABLE public.fire_regions (
  region_id character varying(10) NOT NULL,
  name text NOT NULL,
  CONSTRAINT fire_regions_pkey PRIMARY KEY (region_id)
) TABLESPACE pg_default;

CREATE TABLE public.node_hierarchy (
  parent_id character varying(20) NOT NULL,
  child_id character varying(20) NOT NULL,
  CONSTRAINT node_hierarchy_pkey PRIMARY KEY (parent_id, child_id),
  CONSTRAINT node_hierarchy_child_id_fkey FOREIGN KEY (child_id) REFERENCES nodes (node_id),
  CONSTRAINT node_hierarchy_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES nodes (node_id)
) TABLESPACE pg_default;

CREATE TABLE public.sensor_readings (
  reading_id serial NOT NULL,
  node_id character varying(20) NULL,
  timestamp timestamp without time zone NULL DEFAULT CURRENT_TIMESTAMP,
  danger_level integer NULL,
  temperature numeric(5, 2) NULL,
  humidity numeric(5, 2) NULL,
  gas_and_smoke numeric(5, 2) NULL,
  rain boolean NULL,
  wind_speed numeric(5, 2) NULL,
  flora_density numeric(5, 2) NULL,
  slope numeric(5, 2) NULL,
  vegetation_type character varying(50) NULL,
  CONSTRAINT sensor_readings_pkey PRIMARY KEY (reading_id),
  CONSTRAINT sensor_readings_node_id_fkey FOREIGN KEY (node_id) REFERENCES nodes (node_id)
) TABLESPACE pg_default;

CREATE TABLE public.metadata (
  metadata_id serial NOT NULL,
  description text NULL,
  temperature_unit character varying(20) NULL,
  mq2_unit character varying(20) NULL,
  wind_speed_unit character varying(20) NULL,
  rain_sensor_type text NULL,
  timestamp_format character varying(50) NULL,
  CONSTRAINT metadata_pkey PRIMARY KEY (metadata_id)
) TABLESPACE pg_default;

CREATE TABLE public."Parent_Node_Reports" (
  report_id serial NOT NULL,
  parent_id character varying(20) NULL,
  child_id character varying(20) NULL,
  timestamp timestamp without time zone NULL DEFAULT CURRENT_TIMESTAMP,
  data_received boolean NULL,
  data_valid boolean NULL,
  status_message text NULL,
  CONSTRAINT Parent_Node_Reports_pkey PRIMARY KEY (report_id),
  CONSTRAINT Parent_Node_Reports_child_id_fkey FOREIGN KEY (child_id) REFERENCES nodes (node_id),
  CONSTRAINT Parent_Node_Reports_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES nodes (node_id)
) TABLESPACE pg_default;

CREATE TABLE public.drones (
  drone_id character varying(20) NOT NULL,
  node_id character varying(20) NULL,
  model character varying(50) NULL,
  operational_status character varying(20) NULL,
  last_maintenance date NULL,
  max_flight_time integer NULL,
  CONSTRAINT drones_pkey PRIMARY KEY (drone_id),
  CONSTRAINT drones_node_id_fkey FOREIGN KEY (node_id) REFERENCES nodes (node_id)
) TABLESPACE pg_default;

CREATE TABLE public.node_regions (
  node_id character varying(10) NOT NULL,
  region_id character varying(10) NULL,
  CONSTRAINT node_regions_pkey PRIMARY KEY (node_id),
  CONSTRAINT node_regions_node_id_fkey FOREIGN KEY (node_id) REFERENCES nodes (node_id),
  CONSTRAINT node_regions_region_id_fkey FOREIGN KEY (region_id) REFERENCES fire_regions (region_id)
) TABLESPACE pg_default;