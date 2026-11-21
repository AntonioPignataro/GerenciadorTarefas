PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categoria (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tarefa (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo       TEXT NOT NULL,
    descricao    TEXT,
    prazo        TEXT,                       -- formato AAAA-MM-DD
    concluida    INTEGER NOT NULL DEFAULT 0, -- 0 = pendente, 1 = concluída
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categoria (id) ON DELETE SET NULL
);
