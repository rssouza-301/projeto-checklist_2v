# projeto-checklist_2v
Sistema de Checklist de Segurança - Abertura e Fechamento
Um sistema web desenvolvido em Python com Flask para gerenciar digitalmente checklists de segurança, registrando procedimentos de abertura e fechamento de instalações com geolocalização.

🎯 Sobre o Projeto
Este sistema foi criado para resolver a falta de um registro digital e geolocalizado dos procedimentos de segurança. Ele garante que todas as etapas de verificação sejam seguidas e auditadas de forma centralizada, segura e eficiente, substituindo processos manuais em papel.

O público-alvo são líderes de equipe, fiscais, supervisores e vigilantes responsáveis pela segurança do local.

✨ Funcionalidades Principais
🔐 Autenticação de Usuários: Sistema seguro de login e senha para acesso.

👤 Cadastro de Usuários: Permite a criação de novas contas para os operadores do sistema.

📋 Gerenciamento de Checklists: Cadastro detalhado para registros de Abertura e Fechamento.

📍 Captura de Coordenadas Geográficas: Utiliza a API de Geolocalização do navegador para registrar a localização exata de cada checklist, garantindo a veracidade da informação.

📊 Listagem de Registros: Visualização clara e organizada do histórico de todos os checklists realizados.

🛠️ Tecnologias Utilizadas
Tecnologia

Descrição

Python

Linguagem principal do backend.

Flask

Micro-framework para a construção da aplicação web.

SQLite 3

Banco de dados relacional leve e baseado em arquivo.

HTML5 / CSS3

Estrutura e estilização do frontend.

Bootstrap 5

Framework CSS para criar uma interface moderna e responsiva.

JavaScript

Utilizado para interatividade no cliente, incluindo a API de Geolocalização.

🚀 Como Executar o Projeto
Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

Pré-requisitos
Python 3 instalado na máquina.

pip (gerenciador de pacotes do Python).

DB Browser for SQLite (ou um gerenciador similar) para criar o banco de dados.

Instalação e Execução
Clone o repositório:

git clone [URL-DO-SEU-REPOSITORIO]

Navegue até o diretório do projeto:

cd nome-da-pasta-do-projeto

Instale as dependências:

pip install Flask

Crie o Banco de Dados:

Abra o DB Browser for SQLite.

Crie um novo banco de dados com o nome database.db na raiz do projeto.

Vá para a aba "Executar SQL", abra o arquivo schema.sql e execute o script.

Importante: Clique em "Gravar alterações" para salvar a estrutura no arquivo.

Execute a aplicação:

python app.py

Acesse no navegador:

Abra seu navegador e acesse: http://127.0.0.1:5000

✒️ Autor
Ramon Souza de Santana
