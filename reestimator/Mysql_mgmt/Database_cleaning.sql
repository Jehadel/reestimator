DELETE FROM data_working_copy WHERE surface_reelle_bati < 10;
DELETE FROM data_working_copy WHERE valeur_fonciere NOT BETWEEN 5000 AND 5000000;
DELETE FROM data_working_copy WHERE type_local NOT IN('Appartement', 'Maison','Dépendance');
ALTER TABLE data_working_copy DROP COLUMN numero_disposition ,DROP COLUMN numero_volume, DROP COLUMN adresse_numero ;
DELETE FROM data_working_copy WHERE nature_mutation  <> 'Vente';
SELECT COUNT(id_mutation) FROM data_working_copy dwu;
SELECT * FROM data_working_copy dwu LIMIT 100;

ALTER TABLE data_working_update
DROP COLUMN code_type_local,
DROP COLUMN code_nature_culture,
DROP COLUMN nature_culture,
DROP COLUMN code_nature_culture_speciale,
DROP COLUMN nature_culture_speciale,
DROP COLUMN lot1_numero,
DROP COLUMN lot1_surface_carrez,
DROP COLUMN lot2_numero,
DROP COLUMN lot2_surface_carrez,
DROP COLUMN lot3_numero,
DROP COLUMN lot3_surface_carrez,
DROP COLUMN lot4_numero,
DROP COLUMN lot4_surface_carrez,
DROP COLUMN lot5_numero,
DROP COLUMN lot5_surface_carrez ,
DROP COLUMN nombre_lots;

