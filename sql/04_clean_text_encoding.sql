USE cvdw;

SET SQL_SAFE_UPDATES = 0;

UPDATE leads_distribuicao
SET
    nome_fila = CASE
        WHEN LOCATE('\\u', nome_fila) > 0
        THEN JSON_UNQUOTE(CONCAT('"', nome_fila, '"'))
        ELSE nome_fila
    END,

    empreendimento = CASE
        WHEN LOCATE('\\u', empreendimento) > 0
        THEN JSON_UNQUOTE(CONCAT('"', empreendimento, '"'))
        ELSE empreendimento
    END,

    corretor = CASE
        WHEN LOCATE('\\u', corretor) > 0
        THEN JSON_UNQUOTE(CONCAT('"', corretor, '"'))
        ELSE corretor
    END,

    imobiliaria = CASE
        WHEN LOCATE('\\u', imobiliaria) > 0
        THEN JSON_UNQUOTE(CONCAT('"', imobiliaria, '"'))
        ELSE imobiliaria
    END,

    nome_grupo = CASE
        WHEN LOCATE('\\u', nome_grupo) > 0
        THEN JSON_UNQUOTE(CONCAT('"', nome_grupo, '"'))
        ELSE nome_grupo
    END,

    lead_nome = CASE
        WHEN LOCATE('\\u', lead_nome) > 0
        THEN JSON_UNQUOTE(CONCAT('"', lead_nome, '"'))
        ELSE lead_nome
    END

WHERE
    LOCATE('\\u', nome_fila) > 0
    OR LOCATE('\\u', empreendimento) > 0
    OR LOCATE('\\u', corretor) > 0
    OR LOCATE('\\u', imobiliaria) > 0
    OR LOCATE('\\u', nome_grupo) > 0
    OR LOCATE('\\u', lead_nome) > 0;

SET SQL_SAFE_UPDATES = 1;