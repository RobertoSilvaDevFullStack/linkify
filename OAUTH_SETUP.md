# 🔐 Configuração OAuth2 - Linkify

Este documento explica como configurar a autenticação OAuth2 com Google, GitHub, Microsoft e Apple.

## 📋 URLs de Callback

Configure estas URLs nos seus provedores OAuth:
- **Desenvolvimento**: `http://localhost:3000/auth/{provider}/callback`
- **Produção**: `https://seudominio.com/auth/{provider}/callback`

Substitua `{provider}` por: `google`, `github`, `microsoft`, ou `apple`

## 🔧 Configuração por Provedor

### 1. Google OAuth

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione existente
3. Ative a "Google+ API" ou "People API"
4. Vá em "Credenciais" → "Criar Credenciais" → "ID do cliente OAuth 2.0"
5. Configure:
   - **Tipo de aplicação**: Aplicação Web
   - **URIs de redirect autorizados**: `http://localhost:3000/auth/google/callback`
6. Copie Client ID e Client Secret para o arquivo `.env`

### 2. GitHub OAuth

1. Acesse [GitHub Developer Settings](https://github.com/settings/developers)
2. Clique em "New OAuth App"
3. Configure:
   - **Application name**: Linkify
   - **Homepage URL**: `http://localhost:3000`
   - **Authorization callback URL**: `http://localhost:3000/auth/github/callback`
4. Copie Client ID e Client Secret para o arquivo `.env`

### 3. Microsoft OAuth

1. Acesse [Azure Portal](https://portal.azure.com/)
2. Vá em "Azure Active Directory" → "Registros de aplicativo"
3. Clique em "Novo registro"
4. Configure:
   - **Nome**: Linkify
   - **Tipos de conta suportados**: Contas em qualquer diretório organizacional e contas pessoais da Microsoft
   - **URI de redirecionamento**: Web - `http://localhost:3000/auth/microsoft/callback`
5. Após criar, vá em "Certificados e segredos" → "Novo segredo do cliente"
6. Copie Application (client) ID e o valor do segredo para o arquivo `.env`

### 4. Apple OAuth

1. Acesse [Apple Developer](https://developer.apple.com/account/)
2. Vá em "Certificates, Identifiers & Profiles"
3. Em "Identifiers", clique no "+" para criar um novo
4. Selecione "Services IDs" e configure:
   - **Description**: Linkify
   - **Identifier**: com.seudominio.linkify
5. Configure "Sign In with Apple":
   - **Domains and Subdomains**: localhost (desenvolvimento)
   - **Return URLs**: `http://localhost:3000/auth/apple/callback`
6. Gere uma chave privada em "Keys" para usar como Client Secret

## 📝 Arquivo .env

Atualize o arquivo `.env` com suas credenciais reais:

```env
# Google OAuth
GOOGLE_CLIENT_ID=seu-google-client-id-real
GOOGLE_CLIENT_SECRET=seu-google-client-secret-real

# GitHub OAuth  
GITHUB_CLIENT_ID=seu-github-client-id-real
GITHUB_CLIENT_SECRET=seu-github-client-secret-real

# Microsoft OAuth
MICROSOFT_CLIENT_ID=seu-microsoft-client-id-real
MICROSOFT_CLIENT_SECRET=seu-microsoft-client-secret-real

# Apple OAuth
APPLE_CLIENT_ID=seu-apple-client-id-real
APPLE_CLIENT_SECRET=seu-apple-client-secret-real
```

## ⚡ Testando OAuth

1. Inicie o servidor: `python main.py`
2. Acesse: `http://localhost:3000`
3. Clique nos botões de login social
4. Complete o fluxo OAuth no provedor
5. Você será redirecionado de volta para o dashboard

## 🔒 Segurança em Produção

- Use HTTPS em produção
- Configure domínios corretos nos provedores
- Use secrets seguros e únicos
- Implemente rate limiting
- Valide e sanitize dados de entrada

## 🐛 Troubleshooting

**Erro: "redirect_uri_mismatch"**
- Verifique se a URL de callback está exatamente igual nos provedores

**Erro: "invalid_client"**  
- Verifique Client ID e Client Secret no arquivo `.env`

**Erro: "access_denied"**
- Usuário cancelou o login ou não autorizou a aplicação

## 📱 Escopos Solicitados

- **Google**: `openid email profile`
- **GitHub**: `user:email`  
- **Microsoft**: `openid email profile`
- **Apple**: `openid email name`

Estes escopos permitem obter informações básicas do perfil do usuário.
