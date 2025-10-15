INSERT INTO cidade (cod_cidade, nome_cidade, sigla_estado) VALUES
(1, 'Cachoeiro de Itapemirim', 'ES'),
(2, 'Marataizes', 'ES'),
(3, 'Rio de janeiro', 'RJ');

INSERT INTO usuario (cod_usuario, nome, email, senha, cpf, data_nascimento, status, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario, telefone, perfil, genero, data_cadastro, foto, token_redefinicao, data_token, estado_usuario) VALUES
(1, 'lucas', 'lucas@gmail.com', '123456', '12345678900', '2000-01-01', 1, 'Rua Horacio Leandro de Souza', 'Basileia', 1, '29302875', '11999999999', 'doador', 'Masculino', '2023-10-01', '', '', '', 'ES'),
(2, 'caua', 'caua@gmail.com', '123456', '12345678900', '2000-01-01', 1, 'Rua Projetada', 'Timbo I', 2, '29345000', '11999999999', 'doador', 'Masculino', '2023-10-01', '', '', '', 'ES');

INSERT INTO campanha (cod_campanha, titulo, descricao, data_inicio, data_fim, status, foto) VALUES
(1, 'Campanha de Verão', 'O verão, com suas férias e viagens, é uma época deliciosa, mas que traz um desafio crítico para os bancos de sangue: a demanda por transfusões aumenta, enquanto o número de doadores diminui drasticamente. Acidentes, cirurgias de emergência e o tratamento contínuo de pacientes não param no calor, e o suprimento de sangue é vital para a sobrevivência dessas pessoas. Por isso, lançamos a Campanha de Verão. Sua solidariedade não pode entrar de férias! Convidamos você a dedicar um pequeno tempo do seu verão para realizar um gesto grandioso: a doação de sangue. Manter os estoques abastecidos nesta época é crucial para garantir que hospitais e clínicas tenham recursos para salvar vidas a qualquer momento. Não deixe o calor diminuir a esperança de quem precisa. Participe, doe sangue e ajude a garantir que ninguém fique sem o suporte necessário durante a estação mais quente do ano!
A doação é um processo rápido e seguro. Para doar, você precisa estar em boas condições de saúde, ter entre 16 e 69 anos (com exceções para menores de 18 e maiores de 60, consulte as regras do seu hemocentro), pesar no mínimo 50 kg e estar alimentado. É fundamental também que o doador evite bebidas alcoólicas nas 12 horas que antecedem a doação e que esteja bem hidratado — especialmente no verão! Verifique no hemocentro mais próximo os horários de funcionamento e agende sua visita, se necessário.
Cada doação tem o potencial de salvar até quatro vidas. Ao participar da Campanha de Verão, você não está apenas contribuindo para uma estatística; você está garantindo que uma mãe, um pai, um filho ou um amigo possa ter a chance de se recuperar. O estoque de sangue é uma responsabilidade coletiva. Neste verão, seja o herói de alguém. Sua gota de generosidade é o presente mais valioso que você pode dar. Venha e faça parte desta corrente de vida!
Não espere por um chamado de emergência para agir! A necessidade é contínua e urgente, e o verão é o momento em que a sua presença no hemocentro faz toda a diferença. Reserve um horário na sua agenda de verão hoje mesmo e contribua. Ao doar, você leva esperança e a chance de um futuro a quem mais precisa. Localize o hemocentro mais próximo, compartilhe esta campanha com seus amigos e venha doar vida!', '2025-12-01', '2026-02-28', 1, '/static/uploads/campanhas/campanha4.jpg'),
(2, 'Campanha de Inverno', 'Com certeza! O inverno exige um apelo especial, pois o frio e as doenças sazonais realmente afastam os doadores.
Aqui está um texto corrido e persuasivo para a sua Campanha de Inverno:
Campanha de Inverno: Não Deixe o Frio Congelar a Solidariedade!
Com a chegada do inverno, a tendência é que as pessoas permaneçam mais tempo em casa, e o resultado é uma queda preocupante no número de doações de sangue. Em contrapartida, a necessidade de sangue nos hospitais não diminui, e muitas vezes, as doenças respiratórias típicas da estação, como gripes e resfriados, acabam criando ainda mais barreiras para os doadores. É um cenário de alerta: os estoques de sangue tendem a diminuir justamente quando a necessidade se mantém alta.
Ajude-nos a reverter essa tendência participando da nossa Campanha de Inverno! A sua doação é o calor que salva vidas. É um ato rápido, seguro e que tem o poder de garantir que pacientes em cirurgias de emergência, vítimas de acidentes ou que necessitam de transfusões contínuas (como pacientes oncológicos ou com anemias crônicas) tenham o suporte vital de que precisam. Não permita que o frio ou a preguiça de sair de casa se torne um fator de risco para quem está na luta pela vida.
Lembre-se: Se você está saudável, o inverno não é um impedimento, é uma OPORTUNIDADE para fazer a diferença.
Verifique as condições básicas para doação (estar bem de saúde, alimentado e ter o peso mínimo), encontre o hemocentro mais próximo e aqueça o coração de quem precisa. Sua presença é urgente e indispensável. Junte-se a nós nesta Campanha de Inverno e mantenha a corrente de vida em movimento. Doe sangue, e doe calor humano!', '2025-06-01', '2025-08-31', 1, '/static/uploads/campanhas/campanha5.jpg'),
(3, 'Campanha de Natal', 'O Natal é a época de celebrar a união, a esperança e, acima de tudo, a vida. Enquanto preparamos a ceia e trocamos presentes, centenas de pessoas nos hospitais dependem de um gesto de solidariedade para ter a chance de comemorar o próximo ano.
Neste Natal, seu presente pode ser o mais valioso de todos: o Dom da Vida.
A mobilização de doadores costuma cair durante as festividades de fim de ano e nas férias coletivas, mas a necessidade de sangue continua urgente para cirurgias, acidentes e tratamentos. É por isso que lançamos a Campanha de Natal, um convite especial para que você transforme a generosidade da época em uma ação que salva vidas.
Participe da nossa Campanha de Natal e faça a diferença! Dedique alguns minutos do seu tempo para a doação. Não há presente mais significativo do que garantir a esperança e o futuro de alguém que precisa. Leve um amigo, vista o espírito natalino e venha compartilhar a sua saúde.
Doe sangue. Doe vida. Faça um Natal mais feliz para todos.
Procure o hemocentro mais próximo e dê o presente que não tem preço!', '2025-12-01', '2025-12-31', 1, '/static/uploads/campanhas/campanha6.jpg'),
(4, 'Campanha Gota de Vida', 'Com certeza! Aqui está uma versão mais robusta e detalhada da Campanha Gota de Vida, ideal para ser usada em matérias de blog, comunicados completos ou e-mail marketing:
💧 Campanha Gota de Vida: Conscientização e Solidariedade Para Multiplicar a Esperança
Em um mundo onde as necessidades de saúde são constantes e urgentes, a doação de sangue permanece como um pilar insubstituível da medicina moderna. É com este propósito vital que lançamos a Campanha Gota de Vida, um movimento dedicado a conscientizar a população sobre a importância desse ato de generosidade e a mobilizar novos doadores.
A razão para o nome desta campanha é simples e poderosa: cada doação de sangue tem o potencial de salvar até 4 vidas. Sim, uma única "gota" de solidariedade, transformada em hemocomponentes (como plasma, plaquetas e glóbulos vermelhos), é capaz de fazer a diferença em quatro destinos diferentes, oferecendo uma nova chance a pacientes em estado grave, vítimas de acidentes, pessoas submetidas a cirurgias de grande porte e indivíduos em tratamento de doenças crônicas como a talassemia e o câncer. O sangue não tem substituto artificial, o que torna a sua contribuição indispensável.
Nosso principal objetivo é transformar a doação esporádica em um hábito contínuo. Para isso, incentivamos a população a se informar sobre os requisitos básicos: é preciso estar em boas condições de saúde, ter entre 16 e 69 anos (com exceções de idade a serem verificadas), pesar no mínimo 50 kg e estar bem alimentado. É fundamental quebrar mitos e mostrar que o processo de coleta é rápido, seguro e realizado por profissionais qualificados em um ambiente preparado. A solidariedade é contagiosa, e a Gota de Vida é o ponto de partida para essa corrente do bem.
Portanto, convidamos você a ir além da conscientização. Participe ativamente da Campanha Gota de Vida agendando sua doação hoje mesmo. Se você não puder doar no momento, ajude-nos a divulgar esta mensagem, compartilhando com amigos, familiares e colegas. Sua participação, seja doando ou informando, garante que os bancos de sangue permaneçam abastecidos e prontos para atender a qualquer emergência. Seja a Gota de Vida que irá florescer em esperança para quatro pessoas. Sua contribuição é um presente inestimável para a comunidade.', '2025-04-01', '2025-12-31', 1, '/static/uploads/campanhas/campanha1.jpg'),
(5, 'Doe Sangue, Salve Vidas', 'A necessidade de sangue nos hospitais é uma realidade 24 horas por dia. Em casos de emergência – como acidentes graves, hemorragias e complicações cirúrgicas – o tempo de resposta é crucial, e ter o estoque de sangue adequado faz a diferença entre a vida e a morte.
É por isso que lançamos a campanha "Doe Sangue, Salve Vidas".
Este é um chamado direto para a ação. Junte-se a nós e ajude a garantir que os hospitais e clínicas tenham sempre o suprimento vital necessário para emergências e para os inúmeros pacientes que dependem de transfusões regulares para seus tratamentos contínuos. Não há substituto artificial para o sangue humano; ele só pode ser obtido através da sua generosidade.
Seu compromisso é a nossa garantia de segurança.
Ao doar, você não está apenas enchendo uma bolsa; você está garantindo a continuidade de um tratamento, a chance de uma recuperação e a esperança de um futuro para até quatro pessoas. O processo é rápido, seguro e totalmente voluntário.
Participe da campanha "Doe Sangue, Salve Vidas".
Verifique os requisitos básicos de doação (estar bem de saúde, alimentado e com documento oficial com foto) e localize o hemocentro mais próximo. Não espere por uma crise para fazer a sua parte.
Doe Sangue. Salve Vidas. Seja o herói de alguém hoje!', '2025-05-01', '2025-11-30', 1, '/static/uploads/campanhas/campanha2.jpg'),
(6, 'Maratona da Solidariedade', 'A solidariedade não é uma corrida de curta distância; é uma verdadeira Maratona! E agora, mais do que nunca, precisamos da sua energia e do seu empenho para vencer o desafio de manter os bancos de sangue abastecidos.
Lançamos a Maratona da Solidariedade com um objetivo claro: mobilizar o máximo de doadores possível para arrecadar as doações de sangue necessárias para aqueles que mais precisam. Seja para pacientes em tratamentos contínuos, emergências cirúrgicas ou vítimas de acidentes, cada doação é um passo crucial na linha de chegada da recuperação.
Sua participação faz a diferença!
Convidamos você a "correr" conosco nesta causa vital. Não importa se você é um doador de primeira viagem ou um veterano: sua atitude é o combustível desta maratona. O processo de doação é rápido, seguro e a maior recompensa é saber que você está contribuindo diretamente para salvar até quatro vidas.
Como participar da nossa Maratona da Solidariedade:
Vista a Camisa: Verifique se você atende aos requisitos básicos de saúde.
Entre na Pista: Localize o hemocentro mais próximo.
Cruze a Linha de Chegada: Realize sua doação de sangue.
Passe o Bastão: Convide amigos, familiares e colegas para participarem também!
Não deixe que a falta de sangue seja um obstáculo. Junte-se à Maratona da Solidariedade. Sua doação é o troféu de esperança para quem aguarda nos hospitais.', '2025-06-01', '2025-10-31', 1, '/static/uploads/campanhas/campanha3.jpg');


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

INSERT INTO notificacao (cod_notificacao, cod_adm, tipo, mensagem, status, data_envio, titulo) VALUES
(1, 1, 'Estoque', 'O estoque de sangue tipo O negativo está baixo. Por favor, faça uma doação.', 1, '2025-10-01', 'Estoque Baixo'),
(2, 2, 'Agendamento', 'Você tem um agendamento de doação de sangue amanhã às 10:00.', 1, '2025-10-01', 'Agendamento de Doação'),
(3, 1, 'Campanha', 'Participe da nova campanha de doação de sangue "Doe Sangue, Salve Vidas".', 1, '2025-10-01', 'Doe Sangue'),
(4, 2, 'Agradecimento', 'Obrigado por sua doação de sangue! Sua contribuição é muito importante.', 1, '2025-10-01', 'Sua Doação é Importante');

INSERT INTO colaborador (cod_colaborador, funcao) VALUES
(1, 'Enfermeiro'),
(2, 'Técnico de Laboratório');

INSERT INTO doador (cod_doador, tipo_sanguineo, fator_rh, elegivel, altura, peso, profissao, contato_emergencia, telefone_emergencia) VALUES
(1, 'O', 'negativo', "elegivel", 1.75, 70.0, 'Estudante', 'Maria Silva', '11988887777'),
(2, 'A', 'positivo', "elegivel", 1.80, 80.0, 'Engenheiro', 'João Souza', '11977776666');

INSERT INTO agendamento (cod_agendamento, cod_colaborador, cod_doador, data_hora, status, tipo_agendamento, local_agendamento) VALUES
(1, 1, 1, '2023-10-05 10:00:00', 1, 'presencial', 1),
(2, NULL, 2, '2023-10-06 14:00:00', 1, 'online', 2),
(3, NULL, 1, '2023-10-07 09:00:00', 1, 'online', 1),
(4, 1, 2, '2023-10-08 11:00:00', 1, 'presencial', 2);

INSERT INTO doacao (cod_doacao, cod_doador, cod_agendamento, data_hora, quantidade, status) VALUES
(1, 1, 1, '2025-10-01', '490', 1),
(2, 2, 2, '2025-10-01', '520', 1),
(3, 1, 3, '2025-10-02', '480', 1),
(4, 2, 4, '2025-10-02', '500', 1);

INSERT INTO exame (cod_exame, cod_doacao, data_exame, tipo_exame, resultado, arquivo) VALUES
(1, 1, '2023-10-05', 'Hemograma Completo', 'Normal', 'hemograma_123.pdf'),
(2, 2, '2023-10-06', 'Teste de Hepatite B', 'Negativo', 'hepatiteB_456.pdf'),
(3, 3, '2023-10-07', 'Teste de HIV', 'Negativo', 'HIV_789.pdf'),
(4, 4, '2023-10-08', 'Teste de Sífilis', 'Negativo', 'sifilis_101.pdf');

INSERT INTO prontuario (cod_prontuario, cod_doacao, data_criacao, data_atualizacao, jejum, diabetes, hipertensao, cardiopatia, cancer, hepatite, outros, detalhes_outros, sintomas_gripais, medicamentos, detalhes_medicamentos, fumante, alcool, droga, ist, atividade, sono, tatuagem_e_outros) VALUES
(1,1, '2023-10-05', '2023-10-05', False, False, False, False, False, False, False, '', False, False, '', False, False, False, False, False, True, False),
(2,2, '2023-10-06', '2023-10-06', True, False, True, False, False, True, True, 'Hepatite A', True, True, 'Paracetamol', False, True, False, False, True, False, False);