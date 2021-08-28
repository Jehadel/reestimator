#Get All Data with Geospatial attributes
SELECT dwu.nom_commune as nom, MAX(dwu.latitude) AS lat, dwu.longitude AS lon , COUNT(id_mutation) as transactions
FROM data_working_update dwu 
GROUP BY dwu.nom_commune
ORDER BY transactions DESC;


#Get aggregate data by commune
SELECT code_commune, ROUND(AVG(dwu.valeur_fonciere/dwu.surface_reelle_bati),0), sum(dwu.nombre_lots),AVG(dwu.nombre_pieces_principales) FROM data_working_update dwu
WHERE year(dwu.date_mutation) = 2016
AND dwu.type_local = 'Maison'
AND dwu.code_departement = 75
GROUP BY dwu.code_commune;

#Query to get all sqm values in a specific year and department
SELECT code_commune, ROUND(dwu.valeur_fonciere/dwu.surface_reelle_bati,0), dwu.nombre_lots,dwu.nombre_pieces_principales FROM data_working_update dwu
WHERE year(dwu.date_mutation) = 2016
AND dwu.type_local = 'Maison'
AND dwu.code_departement = 75
;