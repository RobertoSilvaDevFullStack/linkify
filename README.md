# 🔗 Linkify - URL Shortener

Um encurtador de URLs moderno e completo com sistema de gerenciamento de usuários, construído com Python + FastAPI + PostgreSQL + Redis.

![Linkify Logo](https://via.placeholder.com/800x200/667eea/ffffff?text=Linkify+-+URL+Shortener)

## 🚀 Funcionalidades

### ✨ Principais
- **Encurtamento de URLs**: Transforme links longos em URLs curtas e profissionais
- **Sistema de Usuários**: Registro, login e autenticação via JWT
- **Dashboard Completo**: Gerencie todos os seus links em um painel intuitivo
- **Estatísticas**: Acompanhe cliques e performance dos seus links
- **Cache Inteligente**: Redis para redirecionamentos ultra-rápidos
- **Expiração Automática**: Links expiram automaticamente em 30 dias

### 🛡️ Segurança
- Autenticação JWT robusta
- Validação de URLs
- Proteção contra ataques comuns
- Senhas criptografadas com bcrypt

### 📱 Interface
- Design responsivo com Tailwind CSS
- Interface moderna e intuitiva
- Experiência otimizada para mobile e desktop

## 🏗️ Arquitetura

```
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Aplicação principal
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   ├── schemas.py      # Validação Pydantic
│   │   ├── database.py     # Configuração DB
│   │   ├── auth.py         # Autenticação
│   │   └── routes/         # Rotas da API
│   ├── requirements.txt    # Dependências
│   └── .env               # Configurações
└── frontend/              # Interface web
    ├── templates/         # Templates HTML
    └── static/           # CSS e JavaScript
```

## 🛠️ Tecnologias

- **Backend**: Python 3.8+, FastAPI, SQLAlchemy
- **Banco de Dados**: PostgreSQL (principal), Redis (cache)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Autenticação**: JWT (JSON Web Tokens)
- **Deploy**: Uvicorn (ASGI server)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12+
- Redis 6+
- pip (gerenciador de pacotes Python)

## ⚡ Instalação Rápida

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/linkify.git
cd linkify
```

### 2. Configure o PostgreSQL
```sql
-- Conecte ao PostgreSQL e execute:
CREATE DATABASE linkify_db;
CREATE USER linkify WITH PASSWORD 'linkify123';
GRANT ALL PRIVILEGES ON DATABASE linkify_db TO linkify;
```

### 3. Configure o Redis
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server

# macOS com Homebrew
brew install redis
brew services start redis

# Windows
# Baixe e instale do site oficial: https://redis.io/download
```

### 4. Instale as dependências
```bash
cd backend
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente
Edite o arquivo `backend/.env`:
```env
DATABASE_URL=postgresql://linkify:linkify123@localhost:5432/linkify_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=sua-chave-super-secreta-aqui
DEBUG=True
```

### 6. Execute a aplicação
```bash
cd backend/app
python main.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Acesse a aplicação
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 📖 Como Usar

### 1. Registro de Usuário
1. Acesse http://localhost:8000/register
2. Preencha os dados e crie sua conta
3. Faça login em http://localhost:8000/login

### 2. Encurtar URLs
1. Na página inicial ou no dashboard
2. Cole a URL longa no campo
3. Clique em "Encurtar"
4. Copie e compartilhe a URL curta!

### 3. Gerenciar Links
1. Acesse o dashboard em http://localhost:8000/dashboard
2. Veja todos os seus links, estatísticas e cliques
3. Exclua links desnecessários
4. Monitore a performance

## 📊 API Endpoints

### Autenticação
- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Dados do usuário atual

### Links
- `POST /api/shorten` - Encurtar URL
- `GET /{short_slug}` - Redirecionar para URL original
- `GET /api/user/links` - Listar links do usuário
- `DELETE /api/user/links/{id}` - Excluir link
- `GET /api/user/stats` - Estatísticas do usuário

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```env
# Banco de dados
DATABASE_URL=postgresql://user:pass@localhost:5432/db_name
REDIS_URL=redis://localhost:6379/0

# Segurança
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Aplicação
APP_NAME=Linkify
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Links
LINK_EXPIRY_DAYS=30
SHORT_URL_LENGTH=6
```

### Personalização
- Modifique `SHORT_URL_LENGTH` para alterar o tamanho dos slugs
- Ajuste `LINK_EXPIRY_DAYS` para mudar o tempo de expiração
- Personalize os templates em `frontend/templates/`
- Modifique estilos em `frontend/static/css/style.css`

## 🚀 Deploy em Produção

### Docker (Recomendado)
```dockerfile
# Dockerfile exemplo
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Heroku
```bash
# Adicione um Procfile:
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Servidor Linux
```bash
# Use um gerenciador de processos como supervisord ou systemd
# Configure nginx como proxy reverso
# Configure SSL com Let's Encrypt
```

## 🧪 Testes

```bash
# Instale dependências de teste
pip install pytest pytest-asyncio httpx

# Execute os testes
pytest tests/
```

## 📈 Monitoramento

- Use PostgreSQL logs para monitorar queries
- Configure Redis monitoring
- Implemente logging com Python logging
- Use ferramentas como Sentry para error tracking

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Documentação**: Acesse `/api/docs` para documentação completa da API
- **Issues**: Reporte bugs no GitHub Issues
- **Discussões**: Use GitHub Discussions para dúvidas

## 🎯 Roadmap

- [ ] Analytics avançados com gráficos
- [ ] URLs customizadas
- [ ] Sistema de QR Codes
- [ ] API rate limiting
- [ ] Notificações por email
- [ ] Integração com Google Analytics
- [ ] Modo escuro
- [ ] Exportação de dados
- [ ] Bulk URL shortening
- [ ] Team collaboration features

## 👨‍💻 Autor

Desenvolvido com ❤️ por [Seu Nome]

---

⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!

🔗 **Linkify** - Encurte. Gerencie. Monitore.
