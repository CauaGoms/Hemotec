INSERT INTO cidade (cod_cidade, nome_cidade, sigla_estado) VALUES
(1, 'Cachoeiro de Itapemirim', 'ES'),
(2, 'Marataizes', 'ES'),
(3, 'Rio de janeiro', 'RJ');

INSERT INTO usuario (cod_usuario, nome, email, senha, cpf, data_nascimento, status, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario, telefone, perfil, data_cadastro, foto, token_redefinicao, data_token) VALUES
(1, 'lucas', 'lucas@gmail.com', '123456', '12345678900', '2000-01-01', 1, 'Rua Horacio Leandro de Souza', 'Basileia', 1, '29302875', '11999999999', 'doador', '2023-10-01', '', '', ''),
(2, 'caua', 'caua@gmail.com', '123456', '12345678900', '2000-01-01', 1, 'Rua Projetada', 'Timbo I', 2, '29345000', '11999999999', 'doador', '2023-10-01', '', '', '');

INSERT INTO campanha (cod_campanha, titulo, descricao, data_inicio, data_fim, status, foto) VALUES
(1, 'Campanha de Verão', 'Durante o verão, a demanda por sangue aumenta. Participe da nossa Campanha de Verão e ajude a manter os estoques abastecidos!', '2025-12-01', '2026-02-28', 1, '/static/uploads/campanhas/campanha4.jpg'),
(2, 'Campanha de Inverno', 'No inverno, as doações de sangue tendem a diminuir. Ajude-nos a reverter essa tendência participando da nossa Campanha de Inverno!', '2025-06-01', '2025-08-31', 1, '/static/uploads/campanhas/campanha5.jpg'),
(3, 'Campanha de Natal', 'Neste Natal, presenteie alguém com o dom da vida. Participe da nossa Campanha de Natal e faça a diferença!', '2025-12-01', '2025-12-31', 1, '/static/uploads/campanhas/campanha6.jpg'),
(4, 'Campanha Gota de Vida', 'Participe da nossa campanha de conscientização sobre a importância da doação de sangue. Cada doação pode salvar até 4 vidas!', '2025-04-01', '2025-12-31', 1, '/static/uploads/campanhas/campanha1.jpg'),
(5, 'Doe Sangue, Salve Vidas', 'Junte-se a nós na campanha "Doe Sangue, Salve Vidas" e ajude a garantir que os hospitais tenham sangue suficiente para emergências e tratamentos.', '2025-05-01', '2025-11-30', 1, '/static/uploads/campanhas/campanha2.jpg'),
(6, 'Maratona da Solidariedade', 'Participe da Maratona da Solidariedade e ajude a arrecadar doações de sangue para aqueles que mais precisam. Sua participação faz a diferença!', '2025-06-01', '2025-10-31', 1, '/static/uploads/campanhas/campanha3.jpg');


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
(2, 1, 1),
(3, 1, 0),
(4, 2, 1),
(5, 2, 0),
(6, 2, 0),
(7, 2, 0),
(8, 2, 0),
(9, 2, 0),
(10, 2, 0),
(11, 2, 0);

INSERT INTO unidade_coleta (cod_unidade, cod_licenca, nome, email, rua_unidade, bairro_unidade, cidade_unidade, cep_unidade, latitude, longitude, telefone) VALUES
(1, 1, 'Unidade Santa Casa', 'santacasa@gmail.com', 'Rua Dr. Raulino de Oliveira, 67', 'Centro', 1, '29300150', -20.851036695247654, -41.11357974762678, '2821012121'),
(2, 2, 'Unidade Hospital Evangélico', 'hospitalevangelico@gmail.com', 'Rua Manoel Braga Machado, 2', 'Nossa Sra. da Penha', 1, '29308020', -20.843394853600433, -41.11323388995651, '2835266166'),
(3, 4, 'Unidade Banco de Sangue Serum', 'bancosangue@gmail.com', 'Av. Mal. Floriano, 99', 'Centro', 3, '20080004', -22.901594868768438, -43.18392399971006, '2130306761');

INSERT INTO estoque (cod_estoque, cod_unidade, tipo_sanguineo, fator_rh, quantidade, data_atualizacao) VALUES
(1, 1, 'O', 'negativo', 15, '2025-10-01'),
(2, 1, 'O', 'positivo', 26, '2025-10-01'),
(3, 1, 'A', 'negativo', 30, '2025-10-01'),
(4, 1, 'A', 'positivo', 67, '2025-10-01'),
(5, 1, 'B', 'negativo', 120, '2025-10-01'),
(6, 1, 'B', 'positivo', 47, '2025-10-01'),
(7, 1, 'AB', 'negativo', 120, '2025-10-01'),
(8, 1, 'AB', 'positivo', 150, '2025-10-01'),
(9, 2, 'O', 'negativo', 50, '2025-10-01'),
(10, 2, 'O', 'positivo', 148, '2025-10-01'),
(11, 2, 'A', 'negativo', 38, '2025-10-01'),
(12, 2, 'A', 'positivo', 70, '2025-10-01'),
(13, 2, 'B', 'negativo', 125, '2025-10-01'),
(14, 2, 'B', 'positivo', 29, '2025-10-01'),
(15, 2, 'AB', 'negativo', 90, '2025-10-01'),
(16, 2, 'AB', 'positivo', 102, '2025-10-01'),
(17, 3, 'O', 'negativo', 80, '2025-10-01'),
(18, 3, 'O', 'positivo', 200, '2025-10-01'),
(19, 3, 'A', 'negativo', 60, '2025-10-01'),
(20, 3, 'A', 'positivo', 150, '2025-10-01'),
(21, 3, 'B', 'negativo', 110, '2025-10-01'),
(22, 3, 'B', 'positivo', 90, '2025-10-01'),
(23, 3, 'AB', 'negativo', 70, '2025-10-01'),
(24, 3, 'AB', 'positivo', 130, '2025-10-01');

INSERT INTO adm_unidade (cod_adm, cod_unidade) VALUES
(1, 1),
(2, 2);

INSERT INTO adm_campanha (cod_adm, cod_campanha, papel) VALUES
(1, 1, 'gestor'),
(2, 2, 'gestor'),
(1, 2, 'gestor');

INSERT INTO notificacao (cod_notificacao, cod_adm, tipo, mensagem, status, data_envio) VALUES
(1, 1, 'Estoque baixo', 'O estoque de sangue tipo O negativo está baixo. Por favor, faça uma doação.', 1, '2025-10-01'),
(2, 2, 'Lembrete de agendamento', 'Você tem um agendamento de doação de sangue amanhã às 10:00.', 1, '2025-10-01')
(3, 1, 'Nova campanha', 'Participe da nova campanha de doação de sangue "Doe Sangue, Salve Vidas".', 1, '2025-10-01'),
(4, 2, 'Agradecimento', 'Obrigado por sua doação de sangue! Sua contribuição é muito importante.', 1, '2025-10-01');

INSERT INTO colaborador (cod_colaborador, funcao) VALUES
(1, 'Enfermeiro'),
(2, 'Técnico de Laboratório'),
(3, 'Recepcionista'),
(4, 'Médico');

INSERT INTO doador (cod_doador, tipo_sanguineo, fator_rh, elegivel, altura, peso, profissao, contato_emergencia, telefone_emergencia) VALUES
(1, 'O', 'negativo', "elegivel", 1.75, 70.0, 'Estudante', 'Maria Silva', '11988887777'),
(2, 'A', 'positivo', "elegivel", 1.80, 80.0, 'Engenheiro', 'João Souza', '11977776666');

INSERT INTO agendamento (cod_agendamento, cod_colaborador, cod_doador, data_hora, status, observacoes, tipo_agendamento, local_agendamento) VALUES
(1, 1, 1, '2023-10-05 10:00:00', 1, 'Primeira doação de sangue', 'presencial', 1),
(2, 2, 2, '2023-10-06 14:00:00', 1, 'Doação regular', 'presencial', 2),
(3, 2, 1, '2023-10-07 09:00:00', 1, 'Primeira doação de sangue', 'presencial', 1),
(4, 1, 2, '2023-10-08 11:00:00', 1, 'Doação regular', 'presencial', 2);

INSERT INTO doacao (cod_doacao, cod_doador, data_hora, quantidade, status) VALUES
(1, 1, '2025-10-01', '490', 1),
(2, 2, '2025-10-01', '520', 1),
(3, 1, '2025-10-02', '480', 1),
(4, 2, '2025-10-02', '500', 1);

INSERT INTO exame (cod_exame, cod_doacao, data_exame, tipo_exame, resultado, arquivo) VALUES
(1, 1, '2023-10-05', 'Hemograma Completo', 'Normal', 'hemograma_123.pdf'),
(2, 2, '2023-10-06', 'Teste de Hepatite B', 'Negativo', 'hepatiteB_456.pdf'),
(3, 3, '2023-10-07', 'Teste de HIV', 'Negativo', 'HIV_789.pdf'),
(4, 4, '2023-10-08', 'Teste de Sífilis', 'Negativo', 'sifilis_101.pdf');

INSERT INTO prontuario (cod_prontuario, cod_doacao, data_criacao, data_atualizacao, jejum, diabetes, hipertensao, cardiopatia, cancer, hepatite, outros, detalhes_outros, sintomas_gripais, medicamentos, detalhes_medicamentos, fumante, alcool, droga, ist, atividade, sono, tatuagem_e_outros) VALUES
(1,1, '2023-10-05', '2023-10-05', False, False, False, False, False, False, False, '', False, False, '', False, False, False, False, False, True, False),
(2,2, '2023-10-06', '2023-10-06', True, False, True, False, False, True, True, 'Hepatite A', True, True, 'Paracetamol', False, True, False, False, True, False, False);