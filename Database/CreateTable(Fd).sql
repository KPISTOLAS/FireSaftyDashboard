CREATE TABLE Fire_Regions (
    region_id VARCHAR(10) PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE Node_Regions (
    node_id VARCHAR(10),
    region_id VARCHAR(10),
    PRIMARY KEY (node_id),
    FOREIGN KEY (node_id) REFERENCES Nodes(node_id),
    FOREIGN KEY (region_id) REFERENCES Fire_Regions(region_id)
);