INSERT INTO region (region_id, region_name) VALUES
(1, 'West Coast'),
(2, 'Pacific Northwest'),
(3, 'Southwest'),
(4, 'Rocky Mountains'),
(5, 'Midwest'),
(6, 'Southeast'),
(7, 'Northeast'),
(8, 'Alaska'),
(9, 'Hawaii'),
(10, 'Puerto Rico'),
(11, 'Other/Offshore');


INSERT INTO state (state_id, state_name, region_id) VALUES
-- West Coast
(1, 'California', 1),
(2, 'Oregon', 1),
(3, 'Washington', 1),

-- Pacific Northwest
(4, 'Idaho', 2),

-- Southwest
(5, 'Nevada', 3),
(6, 'Arizona', 3),
(7, 'New Mexico', 3),
(8, 'Texas', 3),
(9, 'Oklahoma', 3),
(10, 'Utah', 3),

-- Rocky Mountains
(11, 'Montana', 4),
(12, 'Colorado', 4),
(13, 'Wyoming', 4),

-- Midwest
(14, 'North Dakota', 5),
(15, 'South Dakota', 5),
(16, 'Nebraska', 5),
(17, 'Kansas', 5),
(18, 'Minnesota', 5),
(19, 'Iowa', 5),
(20, 'Missouri', 5),
(21, 'Wisconsin', 5),
(22, 'Illinois', 5),
(23, 'Indiana', 5),
(24, 'Michigan', 5),
(25, 'Ohio', 5),

-- Southeast
(26, 'Arkansas', 6),
(27, 'Louisiana', 6),
(28, 'Kentucky', 6),
(29, 'Tennessee', 6),
(30, 'Mississippi', 6),
(31, 'Alabama', 6),
(32, 'Georgia', 6),
(33, 'Florida', 6),
(34, 'South Carolina', 6),
(35, 'North Carolina', 6),
(36, 'Virginia', 6),
(37, 'West Virginia', 6),

-- Northeast
(38, 'Maryland', 7),
(39, 'Delaware', 7),
(40, 'Pennsylvania', 7),
(41, 'New Jersey', 7),
(42, 'New York', 7),
(43, 'Connecticut', 7),
(44, 'Rhode Island', 7),
(45, 'Massachusetts', 7),
(46, 'Vermont', 7),
(47, 'New Hampshire', 7),
(48, 'Maine', 7),

-- Alaska
(49, 'Alaska', 8),

-- Hawaii
(50, 'Hawaii', 9),

-- Puerto Rico
(51, 'Puerto Rico', 10),

-- Other/Offshore
(52, 'District of Columbia', 7);