INSERT INTO cidade (cod_cidade, nome_cidade, sigla_estado) VALUES
(1, 'Cachoeiro de Itapemirim', 'ES'),
(2, 'Marataizes', 'ES'),
(3, 'Rio de janeiro', 'RJ');

INSERT INTO usuario (cod_usuario, nome, email, senha, cpf, data_nascimento, status, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario, telefone, perfil, data_cadastro, foto, token_redefinicao, data_token) VALUES
(1, 'lucas', 'lucas@gmail.com', '123456', '12345678900', '2000-01-01', 1, 'Rua Horacio Leandro de Souza', 'Basileia', 1, '29302875', '11999999999', 'doador', '2023-10-01', '', '', ''),
(2, 'caua', 'caua@gmail.com', '123456', '12345678900', '2000-01-01', 1, 'Rua Projetada', 'Timbo I', 2, '29345000', '11999999999', 'doador', '2023-10-01', '', '', '');

INSERT INTO campanha (cod_campanha, titulo, descricao, data_inicio, data_fim, status) VALUES
(1, 'Campanha de Doação de Sangue', 'Doe sangue e salve vidas!', '2023-10-01', '2023-12-31', 1),
(2, 'Campanha de Conscientização sobre Doação', 'Participe da nossa campanha para conscientizar sobre a importância da doação de sangue.', '2023-11-01', '2024-01-31', 1);

INSERT INTO plano (cod_plano, qtd_licenca, nome, valor, validade) VALUES
(1, 1, 'Plano Básico', 399.0, 10),
(2, 3, 'Plano Profissional', 799.0, 10),
(3, 8, 'Plano Empresarial', 1599.0, 10),
(4, 15, 'Plano Premium', 3199.0, 10),
(5, 100, 'Plano Enterprise', 3199.0, 10);

INSERT INTO instituicao (cod_instituicao, cnpj, nome, email, rua_instituicao, bairro_instituicao, cidade_instituicao, cep_instituicao, telefone) VALUES
(1, '12345678000199', 'Hemoes', 'hemoes@gmail.com', 'Rua Dr. Luiz Palmier', 'Marbrasa', 1, '29050010', '2733333333'),
(2, '98765432000188', 'Hemorio', 'hemorio@gmail.com', 'Rua Mario de Andrade', 'Botafogo', 3, '29307000', '2133333333');

INSERT INTO gestor (cod_gestor, cod_instituicao, instituicao) VALUES
(1, 1, 'hemoes'),
(2, 2, 'hemorio');

INSERT INTO assinatura (cod_assinatura, cod_instituicao, cod_plano, data_inicio, data_fim, valor, qtd_licenca) VALUES
(1, 1, 1, '2023-10-01', '2023-10-31', 399.00, 3),
(2, 2, 3, '2023-10-01', '2023-10-31', 1599.00, 8);

INSERT INTO licenca (cod_licenca, cod_assinatura, status) VALUES
(1, 1, 1),
(2, 2, 1);

INSERT INTO unidade_coleta (cod_unidade, cod_licenca, nome, email, rua_unidade, bairro_unidade, cidade_unidade, cep_unidade, latitude, longitude, telefone) VALUES
(1, 1, 'Unidade de Coleta Central', 'unidade@gmail.com', 'Rua Dr. Luiz Palmier', 'Marbrasa', 1, '29050010', -20.3155, -40.3378, '2733333333'),
(2, 2, 'Unidade de Coleta Botafogo', 'unidade2@gmail.com', 'Rua Mario de Andrade', 'Botafogo', 3, '29307000', -22.1234, -43.1234, '2133333333');

INSERT INTO estoque (cod_estoque, cod_unidade, tipo_sanguineo, fator_rh, quantidade, data_atualizacao) VALUES
(1, 1, 'O', 'negativo', 35, '2023-10-01'),
(2, 1, 'O', 'positivo', 40, '2023-10-01'),
(3, 1, 'A', 'negativo', 25, '2023-10-01'),
(4, 1, 'A', 'positivo', 30, '2023-10-01'),
(5, 1, 'B', 'negativo', 20, '2023-10-01'),
(6, 1, 'B', 'positivo', 25, '2023-10-01'),
(7, 1, 'AB', 'negativo', 15, '2023-10-01'),
(8, 1, 'AB', 'positivo', 20, '2023-10-01'),
(9, 2, 'O', 'negativo', 50, '2023-10-01'),
(10, 2, 'O', 'positivo', 60, '2023-10-01'),
(11, 2, 'A', 'negativo', 40, '2023-10-01'),
(12, 2, 'A', 'positivo', 50, '2023-10-01'),
(13, 2, 'B', 'negativo', 30, '2023-10-01'),
(14, 2, 'B', 'positivo', 40, '2023-10-01'),
(15, 2, 'AB', 'negativo', 20, '2023-10-01'),
(16, 2, 'AB', 'positivo', 30, '2023-10-01');

INSERT INTO adm_unidade (cod_adm, cod_unidade) VALUES
(1, 1),
(2, 2);

INSERT INTO adm_campanha (cod_adm, cod_campanha, papel) VALUES
(1, 1, 'doador'),
(2, 2, 'gestor');

INSERT INTO notificacao (cod_notificacao, cod_adm, tipo, mensagem, status, data_envio) VALUES
(1, 1, 'Estoque baixo', 'O estoque de sangue tipo O negativo está baixo. Por favor, faça uma doação.', 1, '2023-10-01'),
(2, 2, 'Lembrete de agendamento', 'Você tem um agendamento de doação de sangue amanhã às 10:00.', 1, '2023-10-01');

INSERT INTO colaborador (cod_colaborador, funcao) VALUES
(1, 'Enfermeiro'),
(2, 'Técnico de Laboratório');

INSERT INTO doador (cod_doador, tipo_sanguineo, fator_rh, elegivel, altura, peso, profissao, contato_emergencia, telefone_emergencia) VALUES
(1, 'O', 'negativo', "elegivel", 1.75, 70.0, 'Estudante', 'Maria Silva', '11988887777'),
(2, 'A', 'positivo', "elegivel", 1.80, 80.0, 'Engenheiro', 'João Souza', '11977776666');

INSERT INTO agendamento (cod_agendamento, cod_colaborador, cod_doador, data_hora, status, observacoes, tipo_agendamento, local_agendamento) VALUES
(1, 1, 1, '2023-10-05 10:00:00', 1, 'Primeira doação de sangue', 'presencial', 1),
(2, 2, 2, '2023-10-06 14:00:00', 1, 'Doação regular', 'presencial', 2),
(3, 2, 1, '2023-10-07 09:00:00', 1, 'Primeira doação de sangue', 'presencial', 1),
(4, 1, 2, '2023-10-08 11:00:00', 1, 'Doação regular', 'presencial', 2);

INSERT INTO doacao (cod_doacao, cod_doador, data_hora, quantidade, status) VALUES
(1, 1, '2023-10-05 10:30:00', 450, 1),
(2, 2, '2023-10-06 14:30:00', 550, 1),
(3, 1, '2023-10-07 09:30:00', 500, 1),
(4, 2, '2023-10-08 11:30:00', 490, 1);

INSERT INTO exame (cod_exame, cod_doacao, data_exame, tipo_exame, resultado, arquivo) VALUES
(1, 1, '2023-10-05', 'Hemograma Completo', 'Normal', 'hemograma_123.pdf'),
(2, 2, '2023-10-06', 'Teste de Hepatite B', 'Negativo', 'hepatiteB_456.pdf'),
(3, 3, '2023-10-07', 'Teste de HIV', 'Negativo', 'HIV_789.pdf'),
(4, 4, '2023-10-08', 'Teste de Sífilis', 'Negativo', 'sifilis_101.pdf');

INSERT INTO prontuario (cod_prontuario, cod_doacao, data_criacao, data_atualizacao, diabetes, hipertensao, cardiopatia, cancer, nenhuma, outros, medicamentos, fumante, alcool, atividade, jejum, sono, bebida, sintomas_gripais, tatuagem, termos, alerta) VALUES
(1, 1, '2023-10-01', '2023-10-01', 'nao', 'nao', 'nao', 'nao', 'sim', 'nao', 'nao', 'nao', 'nao', 'nao', 'nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'sim'),
(2, 2, '2023-10-01', '2023-10-01', 'nao', 'sim', 'nao', 'nao', 'sim', 'nao', 'sim', 'nao', 'sim', 'sim', 'nao', 'sim', 'nao', 'nao', 'nao', 'sim', 'sim'),
(3, 3, '2023-10-01', '2023-10-01', 'sim', 'nao', 'nao', 'nao', 'nao', 'sim', 'sim', 'sim', 'nao', 'sim', 'sim', 'nao', 'sim', 'nao', 'nao', 'sim', 'sim'),
(4, 4, '2023-10-01', '2023-10-01', 'nao', 'nao', 'sim', 'nao', 'sim', 'nao', 'nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'nao', 'sim', 'nao', 'sim', 'sim');