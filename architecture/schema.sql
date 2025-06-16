DROP TABLE IF EXISTS earthquake;
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS region;

DROP TYPE IF EXISTS alert_level;
DROP TYPE IF EXISTS location_source;
DROP TYPE IF EXISTS magnitude_type;

CREATE TYPE alert_level AS ENUM ('green', 'yellow', 'orange', 'red');
CREATE TYPE location_source AS ENUM ('ak', 'at', 'ci', 'hv', 'ld', 'mb', 'nc', 'nm', 'nn', 'pr', 'pt', 'se', 'us', 'uu', 'uw');
CREATE TYPE magnitude_type AS ENUM ('Md', 'Ml', 'Ms', 'Mw', 'Me', 'Mi', 'Mb', 'MLg');


CREATE TABLE region (
    region_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL
);

CREATE TABLE state (
    state_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL
);

CREATE TABLE state_region_interaction (
    state_region_interaction_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    state_id SMALLINT REFERENCES state(state_id)
    region_id SMALLINT REFERENCES region(region_id)
);

CREATE TABLE earthquake (
    earthquake_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    magnitude DECIMAL NOT NULL,
    latitude DECIMAL,
    longitude DECIMAL,
    time TIMESTAMPTZ NOT NULL,
    updated TIMESTAMPTZ,
    depth DECIMAL,
    url VARCHAR(255),
    felt INTEGER,
    tsunami BOOLEAN,
    cdi DECIMAL,
    mmi DECIMAL,
    nst SMALLINT,
    sig SMALLINT,
    net CHAR(2),
    dmin DECIMAL,
    alert alert_level,
    location_source location_source,
    magnitude_type magnitude_type,
    state_region_interaction_id SMALLINT REFERENCES state_region_interaction(state_region_interaction_id)
);