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
    a.id_log,
    a.referencia,
    a.referencia_data,
    a.ativo,
    a.recebido_em,
    a.id_fila,
    a.nome_fila,
    a.nome_grupo,
    a.idlead,
    a.lead_nome,
    a.empreendimento,
    a.gestor,
    a.corretor,
    a.imobiliaria,
    a.repassado,
    a.represado,
    a.distribuido_em,
    a.comunicador
FROM stg_leads_access a
LEFT JOIN leads_distribuicao l
    ON a.id_log = l.id_log
WHERE l.id_log IS NULL;