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
('Puerto Rico');


INSERT INTO state (state_name) VALUES
-- West Coast
('California'),
('Oregon'),
('Washington'),

-- Pacific Northwest
('Idaho'),

-- Southwest
('Nevada'),
('Arizona'),
('New Mexico'),
('Texas'),
('Oklahoma'),
('Utah'),

-- Rocky Mountains
('Montana'),
('Colorado'),
('Wyoming'),

-- Midwest
('North Dakota'),
('South Dakota'),
('Nebraska'),
('Kansas'),
('Minnesota'),
('Iowa'),
('Missouri'),
('Wisconsin'),
('Illinois'),
('Indiana'),
('Michigan'),
('Ohio'),

-- Southeast
('Arkansas'),
('Louisiana'),
('Kentucky'),
('Tennessee'),
('Mississippi'),
('Alabama'),
('Georgia'),
('Florida'),
('South Carolina'),
('North Carolina'),
('Virginia'),
('West Virginia'),

-- Northeast
('Maryland'),
('Delaware'),
('Pennsylvania'),
('New Jersey'),
('New York'),
('Connecticut'),
('Rhode Island'),
('Massachusetts'),
('Vermont'),
('New Hampshire'),
('Maine'),
('District of Columbia'),

-- Alaska
('Alaska'),

-- Hawaii
('Hawaii'),

-- Puerto Rico
('Puerto Rico'),

-- Non US
('Not in the USA');


INSERT INTO state_region_interaction (state_id, region_id) VALUES
-- West Coast
(1, 1),
(2, 1),
(3, 1),

-- Pacific Northwest
(4, 2),

-- Southwest
(5, 3),
(6, 3),
(7, 3),
(8, 3),
(9, 3),
(10, 3),

-- Rocky Mountains
(11, 4),
(12, 4),
(13, 4),

-- Midwest
(14, 5),
(15, 5),
(16, 5),
(17, 5),
(18, 5),
(19, 5),
(20, 5),
(21, 5),
(22, 5),
(23, 5),
(24, 5),
(25, 5),

-- Southeast
(26, 6),
(27, 6),
(28, 6),
(29, 6),
(30, 6),
(31, 6),
(32, 6),
(33, 6),
(34, 6),
(35, 6),
(36, 6),
(37, 6),

-- Northeast
(38, 7),
(39, 7),
(40, 7),
(41, 7),
(42, 7),
(43, 7),
(44, 7),
(45, 7),
(46, 7),
(47, 7),
(48, 7),
(49, 7),

-- Alaska
(50, 8),

-- Hawaii
(51, 9),

-- Puerto Rico
(52, 10);