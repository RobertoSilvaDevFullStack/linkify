# 🔐 Configuração OAuth Para Produção - Linkify

## 🌐 URLs de Produção

Quando seu projeto estiver no Vercel, use estas URLs de callback:
- **Seu domínio**: `https://seu-projeto.vercel.app`
- **Callbacks OAuth**: `https://seu-projeto.vercel.app/auth/{provider}/callback`

---

## 🔧 1. Google OAuth Setup

### Passo a passo:

1. **Acesse**: https://console.cloud.google.com/
2. **Crie um projeto** ou selecione existente
3. **Ative APIs necessárias**:
   - Google+ API
   - People API
4. **Vá em "APIs & Services" → "Credentials"**
5. **"Create Credentials" → "OAuth 2.0 Client IDs"**
6. **Configure**:
   ```
   Application type: Web application
   Name: Linkify
   
   Authorized JavaScript origins:
   - https://seu-projeto.vercel.app
   - http://localhost:8000 (para desenvolvimento)
   
   Authorized redirect URIs:
   - https://seu-projeto.vercel.app/auth/google/callback
   - http://localhost:8000/auth/google/callback (para desenvolvimento)
   ```

7. **Copie**: Client ID e Client Secret

---

## 🐙 2. GitHub OAuth Setup

### Passo a passo:

1. **Acesse**: https://github.com/settings/developers
2. **"New OAuth App"**
3. **Configure**:
   ```
   Application name: Linkify
   Homepage URL: https://seu-projeto.vercel.app
   Application description: Encurtador de URLs inteligente
   Authorization callback URL: https://seu-projeto.vercel.app/auth/github/callback
   ```

4. **Após criar**:
   - Copie Client ID
   - Generate a new client secret
   - Copie Client Secret

---

## 🪟 3. Microsoft OAuth Setup

### Passo a passo:

1. **Acesse**: https://portal.azure.com/
2. **Azure Active Directory** → **App registrations**
3. **"New registration"**
4. **Configure**:
   ```
   Name: Linkify
   Supported account types: Accounts in any organizational directory and personal Microsoft accounts
   Redirect URI: Web - https://seu-projeto.vercel.app/auth/microsoft/callback
   ```

5. **Após criar**:
   - Copie Application (client) ID
   - Vá em "Certificates & secrets"
   - "New client secret"
   - Copie o valor do secret

---

## 🍎 4. Apple OAuth Setup

### Passo a passo:

1. **Acesse**: https://developer.apple.com/account/
2. **Certificates, Identifiers & Profiles**
3. **Identifiers** → **"+"** → **Services IDs**
4. **Configure**:
   ```
   Description: Linkify
   Identifier: com.linkify.oauth (use seu domínio)
   ```

5. **Configure "Sign In with Apple"**:
   ```
   Primary App ID: (selecione existente ou crie)
   Domains and Subdomains: seu-projeto.vercel.app
   Return URLs: https://seu-projeto.vercel.app/auth/apple/callback
   ```

6. **Gere chave privada**:
   - Vá em "Keys" → "+"
   - Enable "Sign in with Apple"
   - Download a chave (.p8)

---

## ⚙️ 5. Configurar Variáveis no Vercel

### No painel do Vercel:

1. **Vá em Settings** → **Environment Variables**
2. **Adicione estas variáveis**:

```env
# OAuth Credentials
GOOGLE_CLIENT_ID=sua-google-client-id-real
GOOGLE_CLIENT_SECRET=seu-google-client-secret-real

GITHUB_CLIENT_ID=seu-github-client-id-real
GITHUB_CLIENT_SECRET=seu-github-client-secret-real

MICROSOFT_CLIENT_ID=seu-microsoft-client-id-real
MICROSOFT_CLIENT_SECRET=seu-microsoft-client-secret-real

APPLE_CLIENT_ID=seu-apple-client-id-real
APPLE_CLIENT_SECRET=seu-apple-client-secret-real

# App Security
SECRET_KEY=uma-chave-super-secreta-e-unica-aqui-256bits

# Database (use um dos serviços abaixo)
DATABASE_URL=postgresql://usuario:senha@host:5432/linkify

# Opcional: Analytics
VERCEL_ANALYTICS_ID=sua-vercel-analytics-id
```

---

## 💾 6. Banco de Dados Recomendado

### Neon (PostgreSQL - Gratuito)
1. **Acesse**: https://neon.tech
2. **Crie conta e database**
3. **Copie connection string**
4. **Adicione no Vercel como DATABASE_URL**

### Supabase (PostgreSQL - Gratuito)
1. **Acesse**: https://supabase.com
2. **Novo projeto**
3. **Settings** → **Database**
4. **Copie URI de conexão**

---

## 🧪 7. Teste Local com Produção

### Instalar Vercel CLI:
```bash
npm i -g vercel
```

### Baixar env de produção:
```bash
vercel env pull .env.local
```

### Testar localmente:
```bash
vercel dev
```

---

## 🚀 8. Deploy Final

### Comandos:
```bash
# Fazer deploy
vercel --prod

# Ver logs
vercel logs

# Ver domínio
vercel ls
```

---

## ✅ 9. Checklist Final

Antes de marcar como concluído:

- [ ] ✅ Google OAuth configurado e testado
- [ ] ✅ GitHub OAuth configurado e testado  
- [ ] ✅ Microsoft OAuth configurado e testado
- [ ] ✅ Apple OAuth configurado e testado
- [ ] ✅ Banco PostgreSQL funcionando
- [ ] ✅ Deploy no Vercel concluído
- [ ] ✅ SSL/HTTPS funcionando
- [ ] ✅ Todas as pages carregando
- [ ] ✅ Login tradicional funcionando
- [ ] ✅ Login OAuth funcionando
- [ ] ✅ Dashboard acessível
- [ ] ✅ Encurtamento de URLs funcionando
- [ ] ✅ Analytics funcionando

---

## 🎯 URLs Finais

Após completar tudo:
- **App**: https://seu-projeto.vercel.app
- **Login**: https://seu-projeto.vercel.app/login
- **Dashboard**: https://seu-projeto.vercel.app/dashboard
- **API Docs**: https://seu-projeto.vercel.app/docs

---

## 🚨 Troubleshooting

**❌ "OAuth Error"**: Verifique URLs de callback
**❌ "Database Error"**: Confirme DATABASE_URL
**❌ "CORS Error"**: Atualize domínios permitidos
**❌ "Cookie não salva"**: Verifique configurações de secure/samesite

**✅ Tudo funcionando**: Parabéns! Seu Linkify está online! 🎉
