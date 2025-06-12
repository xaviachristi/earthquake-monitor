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
    region_id SMALLINT PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL
);

CREATE TABLE state (
    state_id SMALLINT PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL,
    region_id SMALLINT REFERENCES region(region_id)
);

CREATE TABLE earthquake (
    earthquake_id BIGINT PRIMARY KEY,
    magnitude DECIMAL(3,1) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    time TIMESTAMPTZ NOT NULL,
    updated TIMESTAMPTZ,
    depth DECIMAL(5,2),
    url VARCHAR(255),
    felt INTEGER,
    tsunami BOOLEAN,
    cdi DECIMAL(3,1),
    mmi DECIMAL(3,1),
    nst SMALLINT,
    sig SMALLINT,
    net VARCHAR(10),
    dmin DECIMAL(4,3),
    alert alert_level,
    location_source location_source,
    magnitude_type magnitude_type,
    state_id SMALLINT REFERENCES state(state_id)
);