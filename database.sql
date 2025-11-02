# Cria um banco de dados chamado "MIDDLEWARE_OAB"
CREATE DATABASE MIDDLEWARE_OAB;
USE MIDDLEWARE_OAB;

# Crie a tabela "Cadastro" com os campos (cadastro_id, nome, email, telefone, cpf, rg, endereco, data_cadastro)
CREATE TABLE Cadastro (
    cadastro_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    cpf VARCHAR(14) NOT NULL UNIQUE,
    rg VARCHAR(20),
    endereco VARCHAR(255),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

# Crie uma tabela "Usuario_advogado" com os campos (usuario_id, registro_oab, codigo_de_seguranca, adimplencia_oab, cadastro_id)
CREATE TABLE Usuario_advogado (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    registro_oab VARCHAR(20) NOT NULL UNIQUE,
    codigo_de_seguranca VARCHAR(50) NOT NULL,
    adimplencia_oab BOOLEAN DEFAULT TRUE,
    cadastro_id INT,
    FOREIGN KEY (cadastro_id) REFERENCES Cadastro(cadastro_id)
);

# Crie uma tabela "Analista_de_ti" com os campos (analista_id, usuario, senha, cadastro_id)
CREATE TABLE Analista_de_ti (
    analista_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    cadastro_id INT,
    FOREIGN KEY (cadastro_id) REFERENCES Cadastro(cadastro_id)
)

# Crie uma tabela "Administrador_sala_coworking" com os campos (admin_id, usuario, senha, adm_local, admin_central, cadastro_id)
CREATE TABLE Administrador_sala_coworking (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    adm_local BOOLEAN DEFAULT FALSE,
    admin_central BOOLEAN DEFAULT FALSE,
    cadastro_id INT,
    FOREIGN KEY (cadastro_id) REFERENCES Cadastro(cadastro_id)
);

# Crie uma tabela "Subsecional" com os campos (subsecional_id, nome)
CREATE TABLE Subsecional (
    subsecional_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

# Crie uma tabela "Unidade" com os campos (unidade_id, nome, hierarquia - ENUM para SEDE e FILIAL -, endereco, latitude, longitude, subsecional_id)
CREATE TABLE Unidade (
    unidade_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    hierarquia ENUM('SEDE', 'FILIAL') NOT NULL,
    endereco VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    subsecional_id INT,
    FOREIGN KEY (subsecional_id) REFERENCES Subsecional(subsecional_id)
);

# Crie uma tabela "Sala_coworking" com os campos (coworking_id, nome_da_sala, subsecional_id, unidade_id, administrador_id)
CREATE TABLE Sala_coworking (
    coworking_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_da_sala VARCHAR(100) NOT NULL,
    subsecional_id INT,
    unidade_id INT,
    administrador_id INT,
    FOREIGN KEY (subsecional_id) REFERENCES Subsecional(subsecional_id),
    FOREIGN KEY (unidade_id) REFERENCES Unidade(unidade_id),
    FOREIGN KEY (administrador_id) REFERENCES Administrador_sala_coworking(admin_id)
);

# Crie uma tabela "Computador" com os campos (computador_id, ip_da_maquina, numero_de_tombamento, coworking_id)
CREATE TABLE Computador (
    computador_id INT AUTO_INCREMENT PRIMARY KEY,
    ip_da_maquina VARCHAR(15) NOT NULL UNIQUE,
    numero_de_tombamento VARCHAR(50) NOT NULL UNIQUE,
    coworking_id INT,
    FOREIGN KEY (coworking_id) REFERENCES Sala_coworking(coworking_id)
);

# Crie uma tabela "Sessao" com os campos (sessao_id, data, inicio_de_sessao, final_de_sessao, ativado, computador_id, usuario_id, administrador_id)
CREATE TABLE Sessao (
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

# Crie uma tabela "Sessoes_analistas" com os campos (analista_id, sessao_id)
CREATE TABLE Sessoes_analistas (
    analista_id INT,
    sessao_id INT,
    PRIMARY KEY (analista_id, sessao_id),
    FOREIGN KEY (analista_id) REFERENCES Analista_de_ti(analista_id),
    FOREIGN KEY (sessao_id) REFERENCES Sessao(sessao_id)
);