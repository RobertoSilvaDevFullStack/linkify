# 🚀 Deploy Linkify para Vercel com OAuth Funcional

## 📋 Pré-requisitos

1. **Conta Vercel**: https://vercel.com
2. **Conta GitHub**: Para conectar o repositório
3. **Contas nos provedores OAuth**:
   - Google Cloud Console
   - GitHub Developer
   - Microsoft Azure
   - Apple Developer

## 🔧 1. Preparação do Projeto para Vercel

### Criar vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "./"
  }
}
```

### Criar requirements.txt
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
bcrypt==4.1.1
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
jinja2==3.1.2
authlib==1.3.0
requests-oauthlib==1.3.1
httpx==0.25.2
python-dotenv==1.0.0
starlette==0.27.0
itsdangerous==2.1.2
```

### Criar api/index.py (entrada para Vercel)
```python
from main import app

# Vercel requer que o app esteja em api/index.py
handler = app
```

## 🔐 2. Configuração OAuth Real

### Google OAuth
1. **Acesse**: https://console.cloud.google.com/
2. **Crie projeto** ou selecione existente
3. **APIs & Services** → **Credentials**
4. **Create Credentials** → **OAuth 2.0 Client IDs**
5. **Web application**:
   - **Authorized redirect URIs**: 
     - `https://seu-projeto.vercel.app/auth/google/callback`
   - **Authorized JavaScript origins**:
     - `https://seu-projeto.vercel.app`

### GitHub OAuth
1. **Acesse**: https://github.com/settings/developers
2. **New OAuth App**:
   - **Application name**: Linkify
   - **Homepage URL**: `https://seu-projeto.vercel.app`
   - **Authorization callback URL**: `https://seu-projeto.vercel.app/auth/github/callback`

### Microsoft OAuth
1. **Acesse**: https://portal.azure.com/
2. **Azure Active Directory** → **App registrations**
3. **New registration**:
   - **Redirect URI**: `https://seu-projeto.vercel.app/auth/microsoft/callback`

### Apple OAuth
1. **Acesse**: https://developer.apple.com/account/
2. **Certificates, Identifiers & Profiles**
3. **Services IDs** → **Configure Sign In with Apple**:
   - **Return URLs**: `https://seu-projeto.vercel.app/auth/apple/callback`

## 🌐 3. Deploy no Vercel

### Via GitHub (Recomendado)
1. **Suba código para GitHub**
2. **Conecte Vercel ao repositório**
3. **Configure Environment Variables no Vercel**

### Variáveis de Ambiente no Vercel
```env
# OAuth Credentials
GOOGLE_CLIENT_ID=seu-google-client-id-real
GOOGLE_CLIENT_SECRET=seu-google-client-secret-real
GITHUB_CLIENT_ID=seu-github-client-id-real
GITHUB_CLIENT_SECRET=seu-github-client-secret-real
MICROSOFT_CLIENT_ID=seu-microsoft-client-id-real
MICROSOFT_CLIENT_SECRET=seu-microsoft-client-secret-real
APPLE_CLIENT_ID=seu-apple-client-id-real
APPLE_CLIENT_SECRET=seu-apple-client-secret-real

# App Settings
SECRET_KEY=sua-chave-secreta-super-forte-aqui
DATABASE_URL=postgresql://user:pass@host/db
```

## 💾 4. Banco de Dados em Produção

### Opção 1: PostgreSQL (Recomendado)
- **Neon**: https://neon.tech (gratuito)
- **Supabase**: https://supabase.com (gratuito)
- **Railway**: https://railway.app

### Opção 2: PlanetScale (MySQL)
- **PlanetScale**: https://planetscale.com

### Atualizar main.py para produção:
```python
import os
from sqlalchemy import create_engine

# Usar PostgreSQL em produção
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./linkify.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
```

## 🔒 5. Configurações de Segurança

### CORS para produção
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://seu-projeto.vercel.app",
        "http://localhost:3000",  # desenvolvimento
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### HTTPS e Cookies Seguros
```python
response.set_cookie(
    key="linkify_token",
    value=access_token,
    httponly=True,
    secure=True,  # HTTPS obrigatório
    samesite="lax",
    max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
)
```

## 🧪 6. Teste Local de Produção

### Instalar Vercel CLI
```bash
npm i -g vercel
```

### Testar localmente
```bash
vercel dev
```

## 📝 7. Checklist de Deploy

- [ ] vercel.json criado
- [ ] requirements.txt atualizado
- [ ] api/index.py criado
- [ ] OAuth apps configurados em todos provedores
- [ ] Banco de dados PostgreSQL configurado
- [ ] Variáveis de ambiente no Vercel
- [ ] CORS configurado para domínio de produção
- [ ] Cookies seguros habilitados
- [ ] URLs de callback atualizadas

## 🎯 URLs Finais

Após deploy, suas URLs serão:
- **App**: `https://seu-projeto.vercel.app`
- **Login**: `https://seu-projeto.vercel.app/login`
- **API**: `https://seu-projeto.vercel.app/docs`
- **OAuth Callbacks**:
  - Google: `https://seu-projeto.vercel.app/auth/google/callback`
  - GitHub: `https://seu-projeto.vercel.app/auth/github/callback`
  - Microsoft: `https://seu-projeto.vercel.app/auth/microsoft/callback`
  - Apple: `https://seu-projeto.vercel.app/auth/apple/callback`

## 🚨 Troubleshooting

**Erro CORS**: Verifique origins permitidos
**OAuth Redirect Mismatch**: URLs devem ser exatas
**Database Connection**: Confirme string de conexão
**Environment Variables**: Verifique se todas estão configuradas

---

## 📞 Suporte

Se precisar de ajuda com qualquer passo, estarei aqui! 🚀
