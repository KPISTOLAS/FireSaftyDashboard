-- Insert parent nodes
INSERT INTO Nodes (node_id, title, is_parent) VALUES
('N1', 'Node 1', TRUE),
('N2', 'Node 2', TRUE);

-- Insert child nodes
INSERT INTO Nodes (node_id, title, is_parent) VALUES
('N1_1', 'Node 1.1', FALSE),
('N1_2', 'Node 1.2', FALSE),
('N1_3', 'Node 1.3', FALSE),
('N2_1', 'Node 2.1', FALSE),
('N2_2', 'Node 2.2', FALSE);

-- Establish hierarchy relationships
INSERT INTO Node_Hierarchy (parent_id, child_id) VALUES
('N1', 'N1_1'),
('N1', 'N1_2'),
('N1', 'N1_3'),
('N2', 'N2_1'),
('N2', 'N2_2');

-- Sample sensor readings for one of the nodes
INSERT INTO Sensor_Readings (
    node_id, danger_level, temperature, humidity,
    gas_and_smoke, rain, wind_speed,
    flora_density, slope, vegetation_type
) VALUES
('N1_1', 2, 25.50, 45.30, 12.45, FALSE, 5.20, 75.30, 10.50, 'Deciduous'),
('N1_1', 3, 28.75, 40.20, 15.80, FALSE, 6.50, 74.80, 10.60, 'Deciduous'),
('N2_1', 1, 22.30, 50.10, 8.90, TRUE, 8.20, 60.50, 15.30, 'Coniferous'),
('N2_2', 4, 30.10, 35.60, 25.30, FALSE, 12.40, 45.20, 5.80, 'Mixed');

-- Sample sensor readings for N1_3 (Node 1.3)
INSERT INTO Sensor_Readings (node_id, danger_level, temperature, humidity, gas_and_smoke, rain, wind_speed, flora_density, slope)
VALUES
('N1_3', 1, 22.5, 60.0, 10.2, FALSE, 5.5, 65.0, 12.0),
('N1_3', 2, 24.1, 58.5, 15.7, TRUE, 8.2, 63.5, 12.0),
('N1_3', 1, 21.8, 62.3, 8.9, FALSE, 4.8, 66.2, 12.0);

-- Reports for Parent N1
INSERT INTO Parent_Node_Reports (parent_id, child_id, data_received, data_valid, status_message) VALUES
('N1', 'N1_1', TRUE, TRUE, 'Data received successfully and validated.'),
('N1', 'N1_2', TRUE, FALSE, 'Temperature reading exceeded safe limit.'),
('N1', 'N1_3', TRUE, TRUE, 'Data looks normal and valid.');

-- Reports for Parent N2
INSERT INTO Parent_Node_Reports (parent_id, child_id, data_received, data_valid, status_message) VALUES
('N2', 'N2_1', TRUE, TRUE, 'All readings within expected range.'),
('N2', 'N2_2', FALSE, NULL, 'No data received from node.');
