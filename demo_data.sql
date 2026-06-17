-- ============================================================
-- DEMO DATA - Logistics Shipment Planner
-- ============================================================

-- USERS (3 rôles)
INSERT INTO logistics.users (name, user_role) VALUES
('Sophie Marchand', 'dispatcher'),
('Kevin Dubois',    'dispatcher'),
('Arnaud Lejeune',  'preparer'),
('Fatima Ouali',    'preparer'),
('Luc Renard',      'preparer'),
('Thomas Bastin',   'truck_admin'),
('Marie Collin',    'truck_admin');

-- GEO ZONES (codes postaux belges)
INSERT INTO logistics.geo_zone (post_code, zone_name) VALUES
(1000, 'Bruxelles'),
(1000, 'Bruxelles'),
(1050, 'Bruxelles'),
(1080, 'Bruxelles'),
(4000, 'Liège'),
(4020, 'Liège'),
(4100, 'Liège'),
(5000, 'Namur'),
(5100, 'Namur'),
(6000, 'Charleroi'),
(6001, 'Charleroi'),
(7000, 'Mons'),
(8000, 'Bruges'),
(8500, 'Bruges'),
(9000, 'Gand'),
(9050, 'Gand'),
(2000, 'Anvers'),
(2060, 'Anvers'),
(3000, 'Louvain'),
(3500, 'Hasselt');

-- PRODUCTS
INSERT INTO logistics.products (sku, name, length_per_unit, width_per_unit, height_per_unit, weight_per_unit) VALUES
(1001, 'Palette standard bois',         1.200, 0.800, 0.150,  22.000),
(1002, 'Boite carton S',                0.300, 0.200, 0.200,   0.500),
(1003, 'Boite carton M',                0.500, 0.400, 0.300,   1.200),
(1004, 'Boite carton L',                0.600, 0.500, 0.400,   2.500),
(1005, 'Boite carton XL',               0.800, 0.600, 0.600,   4.000),
(1006, 'Colis fragile électronique',    0.400, 0.300, 0.300,   3.500),
(1007, 'Équipement industriel A',       1.000, 0.800, 0.800,  45.000),
(1008, 'Équipement industriel B',       1.200, 1.000, 1.000,  80.000),
(1009, 'Mobilier plat pack',            1.800, 0.400, 0.100,  18.000),
(1010, 'Produit alimentaire sec',       0.400, 0.300, 0.250,   5.000),
(1011, 'Matériel médical',              0.500, 0.400, 0.350,   7.500),
(1012, 'Pièces auto emballées',         0.600, 0.400, 0.300,  12.000),
(1013, 'Vêtements carton',              0.600, 0.400, 0.500,   3.000),
(1014, 'Livres et imprimés',            0.400, 0.300, 0.300,   8.000),
(1015, 'Matériaux construction léger',  1.200, 0.600, 0.100,  15.000);

-- VEHICLES
INSERT INTO logistics.vehicles (plate, max_weight, max_length, max_width, max_height, is_available) VALUES
('1ABC001',  3500.00,  4.20, 1.80, 1.80, TRUE),   -- Camionnette légère
('1ABC002',  7500.00,  6.00, 2.20, 2.20, TRUE),   -- Fourgon moyen
('1ABC003', 12000.00,  8.00, 2.40, 2.40, TRUE),   -- Camion 12T
('1ABC004', 19000.00, 10.00, 2.40, 2.60, TRUE),   -- Camion 19T
('1ABC005', 24000.00, 13.60, 2.40, 2.70, TRUE),   -- Semi-remorque
('1ABC006', 24000.00, 13.60, 2.40, 2.70, FALSE),  -- Semi-remorque (indispo)
('1ABC007',  3500.00,  4.20, 1.80, 1.80, TRUE),   -- Camionnette légère 2
('1ABC008', 12000.00,  8.00, 2.40, 2.40, TRUE);   -- Camion 12T 2

-- ORDERS (commandes avec différents statuts)
INSERT INTO logistics.orders (customer, address, postcode, city, status, geo_zone_id, validated_by, validated_at, assigned_to, created_at) VALUES
-- Bruxelles - prêtes
('Entreprise Alpha',     'Rue de la Loi 42',         1000, 'Bruxelles', 'ready',          1, 1, NOW() - INTERVAL '2 days', 3, NOW() - INTERVAL '3 days'),
('Société Beta',         'Avenue Louise 123',         1050, 'Bruxelles', 'ready',          3, 1, NOW() - INTERVAL '2 days', 3, NOW() - INTERVAL '3 days'),
('SPRL Gamma',           'Boulevard Anspach 56',      1000, 'Bruxelles', 'ready',          2, 2, NOW() - INTERVAL '1 day',  4, NOW() - INTERVAL '2 days'),
-- Liège - en préparation
('Delta Industries',     'Quai de Rome 89',           4000, 'Liège',     'in_preparation', 5, 1, NOW() - INTERVAL '1 day',  4, NOW() - INTERVAL '2 days'),
('Epsilon SA',           'Rue Léopold 34',            4020, 'Liège',     'in_preparation', 6, 2, NOW() - INTERVAL '1 day',  5, NOW() - INTERVAL '2 days'),
-- Namur - validées
('Zeta Commerce',        'Place Saint-Aubain 7',      5000, 'Namur',     'validated',      8, 1, NOW() - INTERVAL '1 day',  NULL, NOW() - INTERVAL '1 day'),
('Eta Logistics',        'Rue de Fer 22',             5100, 'Namur',     'validated',      9, 2, NOW(),                     NULL, NOW()),
-- Charleroi - draft
('Theta Group',          'Boulevard Tirou 100',       6000, 'Charleroi', 'draft',          NULL, NULL, NULL,                NULL, NOW()),
('Iota BVBA',            'Rue de Marcinelle 55',      6001, 'Charleroi', 'draft',          NULL, NULL, NULL,                NULL, NOW()),
-- Gand
('Kappa NV',             'Veldstraat 12',             9000, 'Gand',      'ready',          15, 1, NOW() - INTERVAL '1 day', 3, NOW() - INTERVAL '2 days'),
('Lambda BV',            'Korenmarkt 8',              9050, 'Gand',      'ready',          16, 2, NOW() - INTERVAL '1 day', 4, NOW() - INTERVAL '2 days'),
-- Anvers
('Mu Shipping',          'Nationalestraat 45',        2000, 'Anvers',    'validated',      17, 1, NOW(),                    NULL, NOW()),
('Nu Trading',           'Meir 78',                   2060, 'Anvers',    'draft',          NULL, NULL, NULL,                NULL, NOW()),
-- Déjà expédiées
('Xi Retail',            'Rue Rogier 15',             1080, 'Bruxelles', 'shipped',        4, 1, NOW() - INTERVAL '5 days', 3, NOW() - INTERVAL '6 days'),
('Omicron SA',           'Rue Saint-Gilles 33',       4100, 'Liège',     'shipped',        7, 2, NOW() - INTERVAL '4 days', 5, NOW() - INTERVAL '5 days');

-- ORDER LINES
INSERT INTO logistics.order_lines (order_id, product_id, qty, weight_total) VALUES
-- Order 1 (Alpha - Bruxelles)
(1, 1003, 10,  12.000),
(1, 1006,  5,  17.500),
-- Order 2 (Beta - Bruxelles)
(2, 1004,  8,  20.000),
(2, 1013, 12,  36.000),
-- Order 3 (Gamma - Bruxelles)
(3, 1002, 20,  10.000),
(3, 1010, 15,  75.000),
-- Order 4 (Delta - Liège)
(4, 1007,  3, 135.000),
(4, 1012,  6,  72.000),
-- Order 5 (Epsilon - Liège)
(5, 1008,  2, 160.000),
(5, 1005,  4,  16.000),
-- Order 6 (Zeta - Namur)
(6, 1009,  5,  90.000),
(6, 1014, 10,  80.000),
-- Order 7 (Eta - Namur)
(7, 1003,  6,   7.200),
(7, 1011,  3,  22.500),
-- Order 10 (Kappa - Gand)
(10, 1004, 4,  10.000),
(10, 1015, 6,  90.000),
-- Order 11 (Lambda - Gand)
(11, 1002, 30, 15.000),
(11, 1006,  8, 28.000),
-- Order 12 (Mu - Anvers)
(12, 1005,  5, 20.000),
(12, 1003,  8,  9.600);

-- PALLETS (pour les commandes ready/shipped)
INSERT INTO logistics.pallets (geo_zone_id, pallet_length, pallet_width, total_weight, pallet_height, status) VALUES
(1, 1.200, 0.800,  57.500, 1.200, 'closed'),  -- Bruxelles palette 1
(1, 1.200, 0.800,  56.000, 1.100, 'closed'),  -- Bruxelles palette 2
(1, 1.200, 0.800,  85.000, 1.500, 'loaded'),  -- Bruxelles palette 3 (expédiée)
(5, 1.200, 0.800, 207.000, 1.800, 'closed'),  -- Liège palette 1
(5, 1.200, 0.800, 176.000, 1.600, 'closed'),  -- Liège palette 2
(15,1.200, 0.800, 100.000, 1.400, 'closed'),  -- Gand palette 1
(15,1.200, 0.800,  43.000, 1.000, 'open');    -- Gand palette 2 (en cours)

-- PALETTE LINES
INSERT INTO logistics.pallet_lines (pallet_id, order_line_id) VALUES
(1, 1), (1, 2),   -- palette 1 : order 1
(2, 3), (2, 4),   -- palette 2 : order 2
(3, 5), (3, 6),   -- palette 3 : order 3 (expédiée)
(4, 7), (4, 8),   -- palette 4 : order 4
(5, 9), (5, 10),  -- palette 5 : order 5
(6, 15),(6, 16),  -- palette 6 : order 10
(7, 17),(7, 18);  -- palette 7 : order 11

-- SHIPMENTS
INSERT INTO logistics.shipments (vehicle_id, geo_zone_id, departure_date, status, total_weight, created_by, departed_at, length_used, fill_rate) VALUES
(3, 1,  CURRENT_DATE + 1, 'planned', 113.500, 6, NULL,          2.400, 30.00),  -- Bruxelles demain
(4, 5,  CURRENT_DATE + 1, 'loading', 383.000, 7, NULL,          2.400, 24.00),  -- Liège demain
(5, 4,  CURRENT_DATE - 2, 'departed', 85.000, 6, NOW() - INTERVAL '2 days', 1.200, 8.82),   -- Expédié
(2, 15, CURRENT_DATE + 2, 'planned', 143.000, 7, NULL,          2.400, 40.00);  -- Gand après-demain

-- SHIPMENT PALLETS
INSERT INTO logistics.shipment_pallet (shipment_id, pallet_id, load_order) VALUES
(1, 1, 1),  -- shipment Bruxelles : palette 1 en premier
(1, 2, 2),  -- shipment Bruxelles : palette 2 en second
(2, 4, 1),  -- shipment Liège : palette 4
(2, 5, 2),  -- shipment Liège : palette 5
(3, 3, 1),  -- shipment expédié : palette 3
(4, 6, 1),  -- shipment Gand : palette 6
(4, 7, 2);  -- shipment Gand : palette 7


UPDATE logistics.orders SET eta = NOW() + INTERVAL '1 day'  WHERE order_number = 1;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '1 day'  WHERE order_number = 2;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '2 days' WHERE order_number = 3;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '1 day'  WHERE order_number = 4;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '3 days' WHERE order_number = 5;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '2 days' WHERE order_number = 6;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '4 days' WHERE order_number = 7;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '5 days' WHERE order_number = 8;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '5 days' WHERE order_number = 9;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '1 day'  WHERE order_number = 10;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '2 days' WHERE order_number = 11;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '3 days' WHERE order_number = 12;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '6 days' WHERE order_number = 13;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '7 days' WHERE order_number = 14;
UPDATE logistics.orders SET eta = NOW() + INTERVAL '7 days' WHERE order_number = 15;