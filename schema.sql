-- schema.sql

-- Apaga as tabelas se elas já existirem, para um começo limpo
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS registros_abertura;
DROP TABLE IF EXISTS registros_fechamento;

-- Tabela para armazenar os dados dos usuários
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

-- Tabela para os checklists de abertura
CREATE TABLE registros_abertura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lider_abertura TEXT NOT NULL,
    fiscal_abertura TEXT NOT NULL,
    data_hora_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    luzes_ligadas BOOLEAN NOT NULL,
    equipamentos_checados BOOLEAN NOT NULL,
    riscos_incendio BOOLEAN NOT NULL,
    troca_vigilante TEXT NOT NULL, -- Ex: "Noturno para Diurno"
    portoes_deslacrados BOOLEAN NOT NULL,
    lacres_registrados TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    autor_id INTEGER,
    FOREIGN KEY (autor_id) REFERENCES usuarios (id)
);

-- Tabela para os checklists de fechamento
CREATE TABLE registros_fechamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lider_fechamento TEXT NOT NULL,
    fiscal_fechamento TEXT NOT NULL,
    data_hora_fechamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    luzes_desligadas BOOLEAN NOT NULL,
    equipamentos_desligados BOOLEAN NOT NULL,
    riscos_incendio BOOLEAN NOT NULL,
    troca_vigilante TEXT NOT NULL, -- Ex: "Diurno para Noturno"
    portoes_lacrados BOOLEAN NOT NULL,
    lacres_registrados TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    autor_id INTEGER,
    FOREIGN KEY (autor_id) REFERENCES usuarios (id)
);

-- Inserção dos usuários iniciais (a senha será "hasheada" pela aplicação)
INSERT INTO usuarios (login, senha) VALUES ('admin', 'scrypt:32768:8:1$hYutg1fEwbSI8ifD$152fe444f1533036d07c087900b99f243a75850935515096da46698b64a2f143a57161e1498638b9d3c52a36b515d4826d833c81e35d1f86f34316d8a39e31d3'); -- senha: admin123
INSERT INTO usuarios (login, senha) VALUES ('Carlos José', 'scrypt:32768:8:1$K5HjB4lGf2nB8oT9$2d6e409f872c47898b965c7f8a7f1a3a3b934b9d03487c0c1b742e20b33c3933ef4a89a0b1f3c3d5f9d1d1a1b1a1c1e1f1a1b1c1d1e1f1a1b1c1d1e1f1a1b1c1'); -- senha: cjs123