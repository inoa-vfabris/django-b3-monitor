# Django B3 Monitor

Este é um projeto de monitoramento de cotações de ativos da B3, com alertas via email caso algum ativo monitorado ultrapasse os limites cadastrados.

A fonte pública utilizada para obter e armazenar os nomes, códigos e cotações de cada ativo é [dadosmercado](https://www.dadosdemercado.com.br/bolsa/acoes)

## Comportamento do sistema

O sistema funciona da seguinte forma:

- Através de um usuário administrador (que tem acesso total ao sistema), um usuário investidor é cadastrado
- Com seu cadastro criado, o investor consegue acessar o painel administrativo (com permissões restritas)
- Neste painel o investidor consegue visualizar todos os ativos (nome e código) cadastrados no sistemas.
  - Esses ativos são cadastrados todos os dias à meia noite, através de scraping na fonte pública citada inicialmente, utilizando a lib Beautiful Soup. Isto é feito através de um agendamento de tarefa com o Celery.
- O investidor pode selecionar um (ou mais) ativo para ser monitorado, escolhendo entre os ativos cadastrados no sistema, uma periodicidade da checagem, e o limite inferior e superior.
  - O monitoramento do ativo é feito através da criação de um job com o APScheduler.
- A cada período de checagem, o sistema faz um scrap na fonte pública pela última atualização de cotação do ativo, salva esta cotação e checa se os limites foram ultrapassados.
  - Caso tenha sido ultrapassado, o investidor recebe um email sugerindo a compra do ativo sempre que o seu preço cruzar o limite inferior, e sugerindo a venda do ativo sempre que o seu preço cruzar o limite superior.
  - O email utilizado para enviar esta informação é o email utilizado no cadastro do investidor (o mesmo utilizado para entrar no sistema).

## Configuração do ambiente

### Dependências

- [Python](https://www.python.org/)
- [Pip](https://pypi.org/project/pip/)
- [Django](https://docs.djangoproject.com/en/4.0/)
- [Jazzmin - Admin](https://github.com/farridav/django-jazzmin)
- [APScheduler](https://apscheduler.readthedocs.io/en/3.x/)
- [Celery](https://docs.celeryq.dev/en/stable/index.html)
- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Django CORS Headers](https://pypi.org/project/django-cors-headers/)
- [Docker](https://www.docker.com/)
- [DockerCompose](https://docs.docker.com/compose/)

### Instruções

1. Este projeto requer python3.11 para rodar.

2. Utiliza-se o [PDM](https://pdm.fming.dev/latest/). Passos para a instalação:

   > pip install pdm
   
   > pdm install

3. Passos para setar as variáveis de ambiente:

   > cp .env.example .env

   Mude os valores dentro do arquivo para as definições necessárias.

4. Utiliza-se [docker](https://www.docker.com/) e [docker-compose](https://docs.docker.com/compose/) para buildar e rodar o projeto. Os passos são:

   > docker compose -f docker-compose.yml --env-file .env build

   > docker compose -f docker-compose.yml --env-file .env up

   ou usamos os atalhos criados no Makefile:

   > make build

   > make up

## Melhorias para o futuro

Para aperfeiçoar o projeto, os seguintes pontos foram considerados para um desenvolvimento futuro:

- Adicionar logs e reportes de erros
- Adicionar tratamento de erros em serviços que utilizam serviços externos
- Criar abstração para o serviço de scraping, evitando uma dependência direta com o serviço externo
- Adicionar testes unitários para serviços
- Adicionar injeção de dependência para os serviços externos, para tornar os testes mais fáceis assim como a mudança no comportamento da aplicação dependendo
- Implementar outros tipos de alerta, por exemplo, via SMS ou mensagens no WhatsApp, podendo utilizar serviços como [Twillio](https://www.twilio.com/pt-br)
- Aperfeiçoar a visualização do admin dashboard, com mais informações e gráficos
