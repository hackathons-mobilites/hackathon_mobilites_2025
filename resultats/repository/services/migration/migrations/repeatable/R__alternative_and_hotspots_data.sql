-- Script SQL pour insérer des données de test
-- pour tester l'endpoint /v1/alternatives

-- Suppression des données existantes pour un test propre
BEGIN;
DELETE FROM alternatives;
DELETE FROM hotspots;

-- Insertion des hotspots de test avec id en dur
INSERT INTO hotspots (
    id, gare_code, gare_name, datetime_debut, datetime_fin, 
    nb_trajets_affectes, prob_retard_max, prob_retard_moyenne, 
    risk_level, created_at
) VALUES 
-- Hotspot 1: Plaisir-Grignon (matin)
(1, '8775810', 'Plaisir - Grignon', 
 '2025-11-14 08:00:00+01:00', '2025-11-14 10:00:00+01:00',
 150, 0.85, 0.65, 'high', 
 '2025-11-14 07:30:00+01:00'),

-- Hotspot 2: La Défense (soir)
(2, '8738221', 'La Défense', 
 '2025-11-14 17:30:00+01:00', '2025-11-14 19:30:00+01:00',
 85, 0.65, 0.45, 'medium', 
 '2025-11-14 17:00:00+01:00'),

-- Hotspot 3: Gare du Nord (matin)
(3, '8727100', 'Paris Gare du Nord', 
 '2025-11-14 07:45:00+01:00', '2025-11-14 09:15:00+01:00',
 220, 0.78, 0.58, 'high', 
 '2025-11-14 07:15:00+01:00'),

-- Hotspot 4: Châtelet Les Halles (midi)
(4, '8775860', 'Châtelet Les Halles', 
 '2025-11-14 12:30:00+01:00', '2025-11-14 14:00:00+01:00',
 120, 0.55, 0.35, 'medium', 
 '2025-11-14 12:00:00+01:00');

-- Insertion des alternatives pour chaque hotspot avec hotspot_id en dur
INSERT INTO alternatives (
    hotspot_id, type, offre, partenaire, 
    places_disponibles, deeplink, score_rse, created_at
) VALUES 
-- Alternatives pour Hotspot 1 (Plaisir-Grignon)
(1, 'covoiturage', 
 'Covoiturage Plaisir-Grignon → La Défense, départ 8h15', 
 'BlaBlaCar', 3, 
 'https://blablacar.com/ride/12345', 8.5, 
 '2025-11-14 07:45:00+01:00'),

(1, 'velo', 
 'Vélib'' disponible à 200m de la gare', 
 'Vélib''', 5, 
 'https://velib-metropole.fr/map', 9.0, 
 '2025-11-14 07:50:00+01:00'),

(1, 'transport_public', 
 'Bus 258 - ligne de substitution', 
 'RATP', NULL, 
 'https://citymapper.com/bus/258', 7.5, 
 '2025-11-14 07:40:00+01:00');

-- Vérification des données insérées
SELECT 
    h.id as hotspot_id,
    h.gare_name,
    h.risk_level,
    COUNT(a.id) as nb_alternatives,
    STRING_AGG(DISTINCT a.type, ', ') as types_disponibles,
    AVG(a.score_rse) as score_rse_moyen
FROM hotspots h
LEFT JOIN alternatives a ON h.id = a.hotspot_id
GROUP BY h.id, h.gare_name, h.risk_level
ORDER BY h.id;

-- Test de requête pour vérifier l'endpoint
SELECT 
    a.id,
    a.hotspot_id,
    a.type,
    a.offre,
    a.partenaire,
    a.places_disponibles,
    a.score_rse,
    h.gare_name as hotspot_gare
FROM alternatives a
JOIN hotspots h ON a.hotspot_id = h.id
WHERE a.type = 'covoiturage'
ORDER BY a.score_rse DESC;

COMMIT;