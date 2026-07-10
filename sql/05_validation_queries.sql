USE cvdw;

-- 1. Final row count in the main table
SELECT COUNT(*) AS total_rows
FROM leads_distribuicao;


-- 2. Check if there are duplicate id_log values in the main table
SELECT 
    id_log,
    COUNT(*) AS total
FROM leads_distribuicao
GROUP BY id_log
HAVING COUNT(*) > 1;


-- 3. Check if all Access staging rows exist in the main table
SELECT COUNT(*) AS access_rows_still_missing
FROM stg_leads_access a
LEFT JOIN leads_distribuicao l
    ON a.id_log = l.id_log
WHERE l.id_log IS NULL;


-- 4. Check if all distinct SharePoint staging id_logs exist in the main table
SELECT COUNT(DISTINCT s.id_log) AS distinct_sharepoint_idlogs_still_missing
FROM stg_leads_sharepoint s
LEFT JOIN leads_distribuicao l
    ON s.id_log = l.id_log
WHERE l.id_log IS NULL;


-- 5. Check duplicate id_log values in Access staging
SELECT 
    id_log,
    COUNT(*) AS total
FROM stg_leads_access
GROUP BY id_log
HAVING COUNT(*) > 1;


-- 6. Check duplicate id_log values in SharePoint staging
SELECT 
    id_log,
    COUNT(*) AS total
FROM stg_leads_sharepoint
GROUP BY id_log
HAVING COUNT(*) > 1;


-- 7. Check remaining unicode-escaped text in important columns
SELECT
    SUM(CASE WHEN LOCATE('\\u', nome_fila) > 0 THEN 1 ELSE 0 END) AS nome_fila_wrong,
    SUM(CASE WHEN LOCATE('\\u', empreendimento) > 0 THEN 1 ELSE 0 END) AS empreendimento_wrong,
    SUM(CASE WHEN LOCATE('\\u', corretor) > 0 THEN 1 ELSE 0 END) AS corretor_wrong,
    SUM(CASE WHEN LOCATE('\\u', imobiliaria) > 0 THEN 1 ELSE 0 END) AS imobiliaria_wrong,
    SUM(CASE WHEN LOCATE('\\u', nome_grupo) > 0 THEN 1 ELSE 0 END) AS nome_grupo_wrong,
    SUM(CASE WHEN LOCATE('\\u', lead_nome) > 0 THEN 1 ELSE 0 END) AS lead_nome_wrong
FROM leads_distribuicao;


-- 8. Check sample rows from the final table
SELECT *
FROM leads_distribuicao
LIMIT 10;