# 🛒 MegaShop

Esse é o código base do projeto MegaShop, uma plataforma de e-commerce desenvolvida usando o framework [Django](https://www.djangoproject.com/).

## 📦 Requisitos

- 🐍 [Python 3.10+](https://www.python.org/)
- 📥 [pip](https://pip.pypa.io/)

## ⚙️ Instalando o Python com pyenv (opcional, recomendado)

Se você precisar de várias versões do Python, recomenda-se gerenciar usando [pyenv](https://github.com/pyenv/pyenv).

1. Instale o pyenv:

   ```bash
   curl -fsSL https://pyenv.run | bash
   ```

2. Adicione o pyenv ao seu shell (~/.bashrc, ~/.zshrc ou equivalente):

   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
   ```

3. Reinicie o terminal ou execute:

   ```bash
   source ~/.bashrc
   ```

4. Atualize o pyenv:

   ```bash
   pyenv update
   ```

5. Instale e defina a versão desejada do Python:

   ```bash
   pyenv install 3.12.11
   pyenv global 3.12.11
   ```

## 🚀 Rodando o projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/DenPaz/megashop_app.git
   cd megashop_app
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements/local.txt
   ```

4. Crie e aplique migrações:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Crie um superusuário:

   ```bash
   python manage.py createsuperuser
   ```

6. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

7. Acesse em: 👉 [http://localhost:8000](http://localhost:8000).

## ✨ Features Principais

- 🔐 Autenticação avançada com MFA → via `django-allauth` (login, registro, múltiplos fatores de autenticação).
- 🛡 Senhas seguras → suporte ao algoritmo Argon2 para hashing de senhas.
- 🎨 Formulários elegantes → com `django-crispy-forms` e Bootstrap 5.
- ⚡ Interatividade sem recarregar a página → via `django-htmx`.
- 🧵 Suporte de componentes → via `django-cotton`.
- 🗃 Cache e sessões otimizadas → usando `Redis` e `django-redis`.
- 🌐 Deploy simplificado → suporte a `Whitenoise` para servir arquivos estáticos em produção.

## 📂 Estrutura do projeto

- 📁 `apps`: Contém os aplicativos Django do projeto.
- ⚙️ `config`: Contém arquivos de configuração do projeto.
- 📄 `requirements`: Contém arquivos de requisitos para instalação de dependências.
- 🎨 `static`: Contém arquivos estáticos (CSS, JavaScript, imagens).
- 🖼 `templates`: Contém os arquivos de template HTML.

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
