USE cvdw;

INSERT INTO leads_distribuicao (
    id_log,
    referencia,
    referencia_data,
    ativo,
    recebido_em,
    id_fila,
    nome_fila,
    nome_grupo,
    idlead,
    lead_nome,
    empreendimento,
    gestor,
    corretor,
    imobiliaria,
    repassado,
    represado,
    distribuido_em,
    comunicador
)
SELECT
    s.id_log,
    s.referencia,
    s.referencia_data,
    s.ativo,
    s.recebido_em,
    s.id_fila,
    s.nome_fila,
    s.nome_grupo,
    s.idlead,
    s.lead_nome,
    s.empreendimento,
    s.gestor,
    s.corretor,
    s.imobiliaria,
    s.repassado,
    s.represado,
    s.distribuido_em,
    s.comunicador
FROM (
    SELECT
        sp.*,
        ROW_NUMBER() OVER (
            PARTITION BY sp.id_log
            ORDER BY sp.distribuido_em DESC, sp.referencia_data DESC
        ) AS row_num
    FROM stg_leads_sharepoint sp
) s
LEFT JOIN leads_distribuicao l
    ON s.id_log = l.id_log
WHERE l.id_log IS NULL
  AND s.row_num = 1;