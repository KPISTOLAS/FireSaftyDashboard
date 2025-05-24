CREATE TABLE Nodes (
    node_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(50),
    location VARCHAR(50),
    description TEXT,
    is_parent BOOLEAN DEFAULT FALSE
);
CREATE TABLE Node_Hierarchy (
    parent_id VARCHAR(20),
    child_id VARCHAR(20),
    PRIMARY KEY (parent_id, child_id),
    FOREIGN KEY (parent_id) REFERENCES Nodes(node_id),
    FOREIGN KEY (child_id) REFERENCES Nodes(node_id)
);
CREATE TABLE Sensor_Readings (
    reading_id SERIAL PRIMARY KEY,
    node_id VARCHAR(20),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    danger_level INT,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    gas_and_smoke DECIMAL(5,2),
    rain BOOLEAN,
    wind_speed DECIMAL(5,2),
    flora_density DECIMAL(5,2),
    slope DECIMAL(5,2),
    vegetation_type VARCHAR(50),
    FOREIGN KEY (node_id) REFERENCES Nodes(node_id)
);

-- not necessary
CREATE TABLE Metadata (
    metadata_id SERIAL PRIMARY KEY,
    description TEXT,
    temperature_unit VARCHAR(20),
    mq2_unit VARCHAR(20),
    wind_speed_unit VARCHAR(20),
    rain_sensor_type TEXT,
    timestamp_format VARCHAR(50)
);

CREATE TABLE Parent_Node_Reports (
    report_id SERIAL PRIMARY KEY,
    parent_id VARCHAR(20),
    child_id VARCHAR(20),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_received BOOLEAN,
    data_valid BOOLEAN,
    status_message TEXT,
    FOREIGN KEY (parent_id) REFERENCES Nodes(node_id),
    FOREIGN KEY (child_id) REFERENCES Nodes(node_id)
);
