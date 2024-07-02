# API_Flask
API RESTful utilizando Flask para gerenciar um sistema de  biblioteca.

Este projeto é uma API RESTful desenvolvida em Flask, utilizando SQLite como banco de dados.

**Requisitos:**

- Python 3
- pip (gerenciador de pacotes do Python)
- Git

**Configuração e Execução:**

**Passos Gerais:**

**1. Clonar o Repositório:**
   </br></br>git clone https://github.com/Ander20n/API_Flask.git
   </br>Depois abrir o repositório no local onde você salvou no seu computador
   
**2. Configurar Ambiente Virtual:**
   </br></br>python -m venv venv
   </br></br>**# No Windows**
   </br>venv\Scripts\activate
   </br></br>**# No Linux/MacOS**
   </br>source venv/bin/activate

**3. Instalar Dependências:**
   </br></br>pip install -r requirements.txt

**4. Configurar Variáveis de Ambiente:**

   Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

   FLASK_APP=app.py
   </br>FLASK_ENV=development
   </br>DATABASE_URL=sqlite:///database.db

**5. Inicializar o Banco de Dados:**

   flask db init
   </br>flask db migrate
   </br>flask db upgrade

**6. Executar a Aplicação:**

   flask run

**Acessar a Documentação Swagger:**
</br>
- Acesse a documentação Swagger em http://localhost:5000/apidocs

**Instruções por Sistema Operacional:**
</br>
- Windows: Utilize o prompt de comando.
- Linux/MacOS: Utilize o terminal.

**Notas Adicionais:**
</br>
- Certifique-se de que o SQLite está configurado corretamente e acessível.
- Ajuste as permissões de arquivo conforme necessário para o ambiente de produção.

Qualquer dúvida: https://www.linkedin.com/in/ander20n/
