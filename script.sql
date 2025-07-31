-- Criação do banco de dados (opcional)
CREATE DATABASE IF NOT EXISTS db_controle;
USE db_controle;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    perfil ENUM('ADM', 'COMUM') NOT NULL DEFAULT 'COMUM'
);

-- Tabela de produtos
CREATE TABLE IF NOT EXISTS produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(45) NOT NULL,
    qtde INT NOT NULL,
    quantidade_minima INT DEFAULT 0,
    descricao VARCHAR(400)
);

-- (Opcional) Inserir um usuário admin para testes
INSERT INTO usuario (nome, login, senha, perfil) VALUES
('Administrador', 'admin', '123456', 'ADM');