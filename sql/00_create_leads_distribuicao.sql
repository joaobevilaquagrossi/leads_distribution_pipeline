CREATE TABLE leads_distribuicao (
	id_log BIGINT NOT NULL,
    referencia VARCHAR(255),
    referencia_data DATETIME,
    ativo CHAR(1),
    recebido_em DATETIME,
    id_fila BIGINT,
    nome_fila VARCHAR(255),
    nome_grupo VARCHAR(255),
    idlead BIGINT,
    lead_nome VARCHAR(255),
    empreendimento TEXT,
    gestor VARCHAR(255),
    corretor VARCHAR(255),
    imobiliaria VARCHAR(255),
    repassado CHAR(1),
    represado CHAR(1),
    distribuido_em DATETIME,
    comunicador CHAR(1),
    
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id_log)
    );
    
    