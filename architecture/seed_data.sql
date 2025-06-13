INSERT INTO region (region_name) VALUES
('West Coast'),
('Pacific Northwest'),
('Southwest'),
('Rocky Mountains'),
('Midwest'),
('Southeast'),
('Northeast'),
('Alaska'),
('Hawaii'),
('Puerto Rico'),
('Other/Offshore');


INSERT INTO state (state_name, region_id) VALUES
-- West Coast
('California', 1),
('Oregon', 1),
('Washington', 1),

-- Pacific Northwest
('Idaho', 2),

-- Southwest
('Nevada', 3),
('Arizona', 3),
('New Mexico', 3),
('Texas', 3),
('Oklahoma', 3),
('Utah', 3),

-- Rocky Mountains
('Montana', 4),
('Colorado', 4),
('Wyoming', 4),

-- Midwest
('North Dakota', 5),
('South Dakota', 5),
('Nebraska', 5),
('Kansas', 5),
('Minnesota', 5),
('Iowa', 5),
('Missouri', 5),
('Wisconsin', 5),
('Illinois', 5),
('Indiana', 5),
('Michigan', 5),
('Ohio', 5),

-- Southeast
('Arkansas', 6),
('Louisiana', 6),
('Kentucky', 6),
('Tennessee', 6),
('Mississippi', 6),
('Alabama', 6),
('Georgia', 6),
('Florida', 6),
('South Carolina', 6),
('North Carolina', 6),
('Virginia', 6),
('West Virginia', 6),

-- Northeast
('Maryland', 7),
('Delaware', 7),
('Pennsylvania', 7),
('New Jersey', 7),
('New York', 7),
('Connecticut', 7),
('Rhode Island', 7),
('Massachusetts', 7),
('Vermont', 7),
('New Hampshire', 7),
('Maine', 7),
('District of Columbia', 7),

-- Alaska
('Alaska', 8),

-- Hawaii
('Hawaii', 9),

-- Puerto Rico
('Puerto Rico', 10)
