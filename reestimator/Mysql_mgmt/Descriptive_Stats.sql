#Some Basic descriptive Statistics over time for each commune
SELECT dwu.code_commune AS code,
dwu.type_local AS type,  
year(dwu.date_mutation) AS 'Year', 
dwu.nom_commune AS commune,
dwu.code_postal AS Code_post,
ROUND(AVG(dwu.valeur_fonciere/dwu.surface_reelle_bati),0) AS Prixm2,
ROUND(AVG(dwu.valeur_fonciere),0) AS Price,
ROUND(AVG(dwu.surface_reelle_bati),0) AS Avg_sqm,
COUNT(dwu.id_mutation) AS transactions,
MAX(dwu.latitude) AS lat,
MAX(dwu.longitude) AS lon,
AVG(dwu.nombre_pieces_principales) AS No_rooms
FROM data_working_update dwu
WHERE dwu.type_local IN('Appartement', 'Maison')
GROUP BY code_commune, nom_commune, dwu.type_local, year(dwu.date_mutation);


#First Geojson try
SELECT dwu.code_departement AS code,
ROUND(AVG(dwu.valeur_fonciere/dwu.surface_reelle_bati),0) AS Prixm2,
ROUND(AVG(dwu.valeur_fonciere),0) AS Price,
ROUND(AVG(dwu.surface_reelle_bati),0) AS Avg_sqm,
COUNT(dwu.id_mutation) AS transactions,
MAX(dwu.latitude) AS lat,
MAX(dwu.longitude) AS lon
FROM data_working_update dwu
WHERE dwu.type_local IN('Appartement', 'Maison')
GROUP BY dwu.code_departement;

#House price and transactions evolution over years
SELECT dwu.code_commune AS code,
dwu.type_local AS type,  
year(dwu.date_mutation) AS 'Year', 
dwu.nom_commune AS commune,
dwu.code_postal AS Code_post,
ROUND(AVG(dwu.valeur_fonciere/dwu.surface_reelle_bati),0) AS Prixm2,
ROUND(AVG(dwu.valeur_fonciere),0) AS Price,
ROUND(AVG(dwu.surface_reelle_bati),0) AS Avg_sqm,
COUNT(dwu.id_mutation) AS transactions,
MAX(dwu.latitude) AS lat,
MAX(dwu.longitude) AS lon
FROM data_working_update dwu
WHERE dwu.type_local IN('Appartement', 'Maison')
GROUP BY code_commune, nom_commune, dwu.type_local, year(dwu.date_mutation);