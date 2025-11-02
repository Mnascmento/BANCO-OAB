-- ==========================================
-- CRIAÇÃO DO SCHEMA E USO DO BANCO
-- ==========================================
CREATE SCHEMA IF NOT EXISTS MIDDLEWARE_OAB;
USE MIDDLEWARE_OAB;

-- ==========================================
-- TABELA: Cadastro
-- ==========================================
CREATE TABLE IF NOT EXISTS Cadastro (
    cadastro_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    cpf VARCHAR(14) NOT NULL UNIQUE,
    rg VARCHAR(20),
    endereco VARCHAR(255),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABELA: Usuario_advogado
-- ==========================================
CREATE TABLE IF NOT EXISTS Usuario_advogado (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    registro_oab VARCHAR(20) NOT NULL UNIQUE,
    codigo_de_seguranca VARCHAR(50) NOT NULL,
    adimplencia_oab BOOLEAN DEFAULT TRUE,
    cadastro_id INT,
    FOREIGN KEY (cadastro_id) REFERENCES Cadastro(cadastro_id)
);

-- ==========================================
-- TABELA: Analista_de_ti
-- ==========================================
CREATE TABLE IF NOT EXISTS Analista_de_ti (
    analista_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    cadastro_id INT,
    FOREIGN KEY (cadastro_id) REFERENCES Cadastro(cadastro_id)
);

-- ==========================================
-- TABELA: Administrador_sala_coworking
-- ==========================================
CREATE TABLE IF NOT EXISTS Administrador_sala_coworking (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    adm_local BOOLEAN DEFAULT FALSE,
    admin_central BOOLEAN DEFAULT FALSE,
    cadastro_id INT,
    FOREIGN KEY (cadastro_id) REFERENCES Cadastro(cadastro_id)
);

-- ==========================================
-- TABELA: Subsecional
-- ==========================================
CREATE TABLE IF NOT EXISTS Subsecional (
    subsecional_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- ==========================================
-- TABELA: Unidade
-- ==========================================
CREATE TABLE IF NOT EXISTS Unidade (
    unidade_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    hierarquia ENUM('SEDE', 'FILIAL') NOT NULL,
    endereco VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    subsecional_id INT,
    FOREIGN KEY (subsecional_id) REFERENCES Subsecional(subsecional_id)
);

-- ==========================================
-- TABELA: Sala_coworking
-- ==========================================
CREATE TABLE IF NOT EXISTS Sala_coworking (
    coworking_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_da_sala VARCHAR(100) NOT NULL,
    subsecional_id INT,
    unidade_id INT,
    administrador_id INT,
    FOREIGN KEY (subsecional_id) REFERENCES Subsecional(subsecional_id),
    FOREIGN KEY (unidade_id) REFERENCES Unidade(unidade_id),
    FOREIGN KEY (administrador_id) REFERENCES Administrador_sala_coworking(admin_id)
);

-- ==========================================
-- TABELA: Computador
-- ==========================================
CREATE TABLE IF NOT EXISTS Computador (
    computador_id INT AUTO_INCREMENT PRIMARY KEY,
    ip_da_maquina VARCHAR(15) NOT NULL UNIQUE,
    numero_de_tombamento VARCHAR(50) NOT NULL UNIQUE,
    coworking_id INT,
    FOREIGN KEY (coworking_id) REFERENCES Sala_coworking(coworking_id)
);

-- ==========================================
-- TABELA: Sessao
-- ==========================================
CREATE TABLE IF NOT EXISTS Sessao (
    sessao_id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    inicio_de_sessao DATETIME NOT NULL,
    final_de_sessao DATETIME,
    ativado BOOLEAN DEFAULT TRUE,
    computador_id INT,
    usuario_id INT,
    administrador_id INT,
    FOREIGN KEY (computador_id) REFERENCES Computador(computador_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario_advogado(usuario_id),
    FOREIGN KEY (administrador_id) REFERENCES Administrador_sala_coworking(admin_id)
);

-- ==========================================
-- TABELA: Sessoes_analistas
-- ==========================================
CREATE TABLE IF NOT EXISTS Sessoes_analistas (
    analista_id INT,
    sessao_id INT,
    PRIMARY KEY (analista_id, sessao_id),
    FOREIGN KEY (analista_id) REFERENCES Analista_de_ti(analista_id),
    FOREIGN KEY (sessao_id) REFERENCES Sessao(sessao_id)
);
