# 🗄️ Configuração Supabase + Vercel - Linkify

## 📋 Passo a Passo Completo

### 1. Configurar Projeto Supabase

1. **Acesse [supabase.com](https://supabase.com)** e faça login
2. **Clique em "New Project"**
3. **Configure o projeto:**
   - Nome: `linkify-db`
   - Senha do banco: `escolha-uma-senha-forte`
   - Região: `São Paulo` (ou mais próxima)

### 2. Executar Migração do Banco

1. **No dashboard do Supabase, vá em "SQL Editor"**
2. **Cole o conteúdo do arquivo `supabase_migration.sql`**
3. **Execute o script** (clique em RUN)
4. **Verifique se as tabelas foram criadas** em "Table Editor"

### 3. Configurar Variáveis de Ambiente

**No dashboard do Supabase, vá em Settings > API:**

```bash
# Copie estas informações:
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_KEY=sua-service-role-key-aqui

# Em Settings > Database, copie a connection string:
DATABASE_URL=postgresql://postgres:SUA-SENHA@db.SEU-PROJETO.supabase.co:5432/postgres
```

### 4. Deploy na Vercel

#### 4.1 Via GitHub (Recomendado)
```bash
# 1. Commit suas mudanças
git add .
git commit -m "feat: add Supabase integration"
git push origin main

# 2. No dashboard da Vercel:
# - Import from GitHub
# - Selecione seu repositório
# - Configure as environment variables (ver seção abaixo)
```

#### 4.2 Via CLI
```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Deploy
vercel --prod

# 3. Configure as variáveis no dashboard da Vercel
```

### 5. Configurar Variáveis na Vercel

**No dashboard da Vercel, vá em Settings > Environment Variables:**

```bash
# OAuth
GOOGLE_CLIENT_ID=seu-google-client-id
GOOGLE_CLIENT_SECRET=seu-google-client-secret
GITHUB_CLIENT_ID=seu-github-client-id
GITHUB_CLIENT_SECRET=seu-github-client-secret
MICROSOFT_CLIENT_ID=seu-microsoft-client-id
MICROSOFT_CLIENT_SECRET=seu-microsoft-client-secret

# Security
SECRET_KEY=sua-chave-super-secreta-256bits

# Supabase
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_KEY=sua-anon-key
SUPABASE_SERVICE_KEY=sua-service-role-key
DATABASE_URL=postgresql://postgres:SUA-SENHA@db.SEU-PROJETO.supabase.co:5432/postgres

# Environment
VERCEL_ENV=production
```

### 6. Configurar OAuth Callbacks

**Para cada provedor OAuth, configure as URLs de callback:**

- **Google Console:** `https://seu-app.vercel.app/auth/google/callback`
- **GitHub Apps:** `https://seu-app.vercel.app/auth/github/callback`
- **Microsoft Azure:** `https://seu-app.vercel.app/auth/microsoft/callback`

### 7. Testar a Aplicação

1. **Acesse sua URL da Vercel**
2. **Teste o registro/login**
3. **Crie URLs encurtadas**
4. **Verifique analytics**

## 🔧 Comandos Úteis

### Desenvolvimento Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar .env (copie de .env.example)
cp .env.example .env

# Executar localmente
uvicorn main:app --reload
```

### Logs e Debug
```bash
# Ver logs da Vercel
vercel logs

# Ver logs do Supabase
# Dashboard > Logs
```

## 🔐 Segurança

- ✅ RLS (Row Level Security) configurado
- ✅ Políticas de acesso por usuário
- ✅ Variáveis de ambiente seguras
- ✅ Tokens JWT validados

## 📊 Monitoramento

**No Supabase Dashboard:**
- Database → Performance
- Logs → Real-time logs
- Settings → Usage

**Na Vercel:**
- Analytics → Performance
- Functions → Logs

## 🚨 Troubleshooting

### Erro de Conexão com DB
```bash
# Verifique se DATABASE_URL está correto
# Teste conexão no SQL Editor do Supabase
```

### Erro de OAuth
```bash
# Verifique URLs de callback
# Confirme client IDs e secrets
```

### Deploy Failed
```bash
# Verifique requirements.txt
# Confirme se api/index.py existe
# Veja logs: vercel logs
```

## 🎉 Pronto!

Sua aplicação estará rodando em:
- **Frontend**: `https://seu-app.vercel.app`
- **API**: `https://seu-app.vercel.app/api/`
- **Dashboard**: `https://seu-app.vercel.app/dashboard`
