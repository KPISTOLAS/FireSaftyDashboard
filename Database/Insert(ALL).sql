INSERT INTO public.nodes (node_id, title, location, description, is_parent, lat, lng) VALUES
('N1', 'Node 1', 'Αμυγδαλεώνας, Κεντρικο', NULL, 'true', 40.97, 24.37),
('N1_1', 'Node 1.1', 'Αμυγδαλεώνας, Δυτικά', NULL, 'false', 40.959556, 24.353472),
('N1_2', 'Node 1.2', 'Αμυγδαλεώνας, Κεντρικά', NULL, 'false', 40.983277, 24.380628),
('N1_3', 'Node 1.3', 'Αμυγδαλεώνας, Ανατολικά', NULL, 'false', 40.963, 24.362999),
('N2', 'Node 2', 'Χρυσούπολη, Κεντρικό', NULL, 'true', 40.995, 24.7),
('N2_1', 'Node 2.1', 'Χρυσούπολη, Ανατολικά', NULL, 'false', 40.978577, 24.686108),
('N2_2', 'Node 2.2', 'Χρυσούπολη, Βόρεια', NULL, 'false', 41.01721, 24.711714);

INSERT INTO public.fire_regions (region_id, name) VALUES
('FR1', 'ΠΕΚΕ Ανατολικής Μακεδονίας και Θράκης'),
('FR10', 'ΠΕΚΕ Αττικής'),
('FR11', 'ΠΕΚΕ Βορείου Αιγαίου'),
('FR12', 'ΠΕΚΕ Νοτίου Αιγαίου'),
('FR13', 'ΠΕΚΕ Κρήτης'),
('FR2', 'ΠΕΚΕ Κεντρικής Μακεδονίας'),
('FR3', 'ΠΕΚΕ Δυτικής Μακεδονίας'),
('FR4', 'ΠΕΚΕ Ηπείρου'),
('FR5', 'ΠΕΚΕ Θεσσαλίας'),
('FR6', 'ΠΕΚΕ Ιονίων Νήσων'),
('FR7', 'ΠΕΚΕ Δυτικής Ελλάδας'),
('FR8', 'ΠΕΚΕ Στερεάς Ελλάδας'),
('FR9', 'ΠΕΚΕ Πελοποννήσου');

INSERT INTO public.node_hierarchy (parent_id, child_id) VALUES
('N1', 'N1_1'), ('N1', 'N1_2'), ('N1', 'N1_3'),
('N2', 'N2_1'), ('N2', 'N2_2');

INSERT INTO public.sensor_readings (reading_id, node_id, timestamp, danger_level, temperature, humidity, gas_and_smoke, rain, wind_speed, flora_density, slope, vegetation_type) VALUES
(11, 'N1_1', '2025-05-15 08:57:49.815107', 2, 25.50, 45.30, 12.45, false, 5.20, 75.30, 10.50, 'Deciduous'),
(12, 'N1_1', '2025-05-15 08:57:49.815107', 3, 28.75, 40.20, 15.80, false, 6.50, 74.80, 10.60, 'Deciduous'),
(13, 'N2_1', '2025-05-15 08:57:49.815107', 1, 22.30, 50.10, 8.90, true, 8.20, 60.50, 15.30, 'Coniferous'),
(14, 'N2_2', '2025-05-15 08:57:49.815107', 4, 30.10, 35.60, 25.30, false, 12.40, 45.20, 5.80, 'Mixed'),
(15, 'N1_3', '2025-05-15 09:16:59.531068', 1, 22.50, 60.00, 10.20, false, 5.50, 65.00, 12.00, NULL),
(16, 'N1_3', '2025-05-15 09:16:59.531068', 2, 24.10, 58.50, 15.70, true, 8.20, 63.50, 12.00, NULL),
(17, 'N1_3', '2025-05-15 09:16:59.531068', 1, 21.80, 62.30, 8.90, false, 4.80, 66.20, 12.00, NULL);

INSERT INTO public."Parent_Node_Reports" (report_id, parent_id, child_id, timestamp, data_received, data_valid, status_message) VALUES
(1, 'N1', 'N1_1', '2025-05-15 15:57:11.958786', true, true, 'All OK'),
(2, 'N1', 'N1_2', '2025-05-15 15:57:11.958786', true, false, 'Invalid reading'),
(3, 'N1', 'N1_3', '2025-05-15 15:57:11.958786', false, NULL, 'No data received'),
(4, 'N2', 'N2_1', '2025-05-15 15:59:19.862867', true, true, 'Data received and validated successfully.'),
(5, 'N2', 'N2_2', '2025-05-15 15:59:19.862867', true, false, 'Gas and smoke level too high.'),
(6, 'N2', 'N2_1', '2025-05-19 19:29:54.604956', true, true, 'Data received and validated successfully.'),
(7, 'N2', 'N2_2', '2025-05-19 19:29:54.604956', true, false, 'Gas and smoke level too high.');

INSERT INTO public.node_regions (node_id, region_id) VALUES
('N1', 'FR1'), ('N1_1', 'FR1'), ('N1_2', 'FR1'), ('N1_3', 'FR1'),
('N2', 'FR1'), ('N2_1', 'FR1'), ('N2_2', 'FR1');