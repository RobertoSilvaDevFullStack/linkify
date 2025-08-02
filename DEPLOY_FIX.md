# 🚀 Deploy Vercel - Guia Rápido de Correção

## ✅ Problemas Corrigidos:

1. **Configuração Vercel**: Atualizada para usar `api/index.py`
2. **Aplicação Robusta**: Criada versão simplificada com fallback
3. **Templates**: Criado template básico de carregamento
4. **Dependências**: Requirements.txt atualizado

## 📝 Próximos Passos:

### 1. Fazer novo deploy
```bash
# Se usando Vercel CLI
vercel --prod

# Ou fazer push para GitHub se conectado
git add .
git commit -m "Fix: Corrigir configuração Vercel"
git push origin main
```

### 2. Configurar Variáveis de Ambiente no Vercel

Vá para o painel do Vercel > Settings > Environment Variables e adicione:

```env
# Database (use Neon.tech ou Supabase)
DATABASE_URL=postgresql://usuario:senha@host/database

# OAuth (configure nos provedores primeiro)
GOOGLE_CLIENT_ID=sua-google-client-id
GOOGLE_CLIENT_SECRET=seu-google-client-secret
GITHUB_CLIENT_ID=sua-github-client-id
GITHUB_CLIENT_SECRET=seu-github-client-secret
```

### 3. URLs de Callback para OAuth

Configure estas URLs nos provedores OAuth:

- **Google**: `https://seu-dominio.vercel.app/auth/google/callback`
- **GitHub**: `https://seu-dominio.vercel.app/auth/github/callback`

## 🔍 Debug

Se ainda der erro, acesse:
- `https://seu-dominio.vercel.app/health` - Status da aplicação
- `https://seu-dominio.vercel.app/` - Página principal
- Vercel Dashboard > Functions > Logs para ver erros

## 📋 Checklist de Deploy:

- [x] vercel.json configurado
- [x] api/index.py criado
- [x] Aplicação simplificada criada
- [x] Templates básicos criados
- [x] .vercelignore adicionado
- [ ] Variáveis de ambiente configuradas
- [ ] Database configurado
- [ ] OAuth configurado
- [ ] Deploy realizado

## 🆘 Se persistir o erro:

1. Verifique os logs no Vercel Dashboard
2. Teste localmente com `python api/index.py`
3. Verifique se todas as dependências estão no requirements.txt
