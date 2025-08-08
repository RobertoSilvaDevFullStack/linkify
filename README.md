# 🔗 Linkify - Encurtador de URLs Profissional

Um encurtador de URLs moderno e completo construído com FastAPI, otimizado para deploy no Vercel.

## ✨ Funcionalidades

- 🔗 **Encurtamento de URLs** com códigos personalizados
- 👤 **Sistema de Autenticação** completo (registro/login)
- 🔐 **OAuth Social** (Google, GitHub, Microsoft, Apple)
- 📊 **Analytics Avançado** com contagem de cliques
- ⏰ **Links com Expiração** configurável
- 🎨 **Interface Moderna** responsiva
- 🚀 **Alta Performance** (FastAPI + PostgreSQL)
- ☁️ **Deploy Simples** no Vercel

## 🚀 Deploy no Vercel

### 1. Preparação

1. **Fork este repositório** no GitHub
2. **Conecte sua conta Vercel** ao GitHub
3. **Importe o projeto** no Vercel

### 2. Configuração de Variáveis de Ambiente

No painel do Vercel, adicione as seguintes variáveis:

#### Obrigatórias:
```bash
SECRET_KEY=sua-chave-super-secreta-256-bits
DATABASE_URL=postgresql://user:pass@host:5432/db
```

#### Opcionais (OAuth):
```bash
GOOGLE_CLIENT_ID=seu-google-client-id
GOOGLE_CLIENT_SECRET=seu-google-client-secret
GITHUB_CLIENT_ID=seu-github-client-id
GITHUB_CLIENT_SECRET=seu-github-client-secret
```

### 3. Configuração do Banco de Dados (Supabase)

1. **Crie uma conta** no [Supabase](https://supabase.com)
2. **Crie um novo projeto**
3. **Copie a URL de conexão** PostgreSQL
4. **Execute o SQL** para criar as tabelas:

```sql
-- Criar tabela de usuários
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de links
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    clicks INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Índices para performance
CREATE INDEX idx_links_short_code ON links(short_code);
CREATE INDEX idx_links_owner_id ON links(owner_id);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

### 4. Deploy

1. **Faça push** das alterações para o GitHub
2. **Vercel fará deploy automaticamente**
3. **Acesse sua aplicação** na URL fornecida

## 🛠️ Desenvolvimento Local

### Pré-requisitos

- Python 3.11+
- PostgreSQL (ou use Supabase)
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/linkify.git
cd linkify

# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Execute a aplicação
uvicorn main:app --reload
```

### Estrutura do Projeto

```
linkify/
├── api/
│   └── index.py          # API principal (otimizada para Vercel)
├── frontend/
│   └── templates/        # Templates HTML
├── main.py              # Aplicação local
├── oauth_config.py      # Configuração OAuth
├── requirements.txt     # Dependências
├── vercel.json         # Configuração Vercel
└── README.md
```

## 📚 API Endpoints

### Públicos
- `GET /` - Página inicial
- `GET /health` - Status da API
- `POST /api/links/demo` - Criar link (demo)
- `GET /{short_code}` - Redirecionar link

### Autenticados
- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Login
- `POST /api/links` - Criar link
- `GET /api/links` - Listar links do usuário
- `DELETE /api/links/{id}` - Deletar link
- `GET /api/stats` - Estatísticas do usuário

## 🔧 Configuração OAuth

### Google OAuth
1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um projeto ou selecione existente
3. Ative a API Google+ 
4. Crie credenciais OAuth 2.0
5. Adicione URLs de redirecionamento:
   - `https://seu-dominio.vercel.app/auth/google/callback`

### GitHub OAuth
1. Acesse GitHub Settings > Developer settings > OAuth Apps
2. Crie uma nova OAuth App
3. Configure:
   - Homepage URL: `https://seu-dominio.vercel.app`
   - Callback URL: `https://seu-dominio.vercel.app/auth/github/callback`

## 🚨 Solução de Problemas

### Deploy não funciona?
1. Verifique se todas as variáveis de ambiente estão configuradas
2. Confirme se o `DATABASE_URL` está correto
3. Verifique os logs no painel do Vercel

### Erro de banco de dados?
1. Confirme se as tabelas foram criadas
2. Teste a conexão com o banco
3. Verifique as permissões do usuário

### OAuth não funciona?
1. Verifique se as URLs de callback estão corretas
2. Confirme se as credenciais estão válidas
3. Teste em modo de desenvolvimento primeiro

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a [documentação](https://github.com/seu-usuario/linkify/wiki)
2. Abra uma [issue](https://github.com/seu-usuario/linkify/issues)
3. Entre em contato via [email](mailto:seu-email@exemplo.com)

---

**Desenvolvido com ❤️ usando FastAPI e Vercel**
