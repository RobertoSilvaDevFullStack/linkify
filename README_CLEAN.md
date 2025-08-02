# 🔗 Linkify - Encurtador de URLs Inteligente

> **Encurtador de URLs moderno com OAuth, analytics e dashboard completo**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/RobertoSilvaDevFullStack/linkify)

## ✨ Funcionalidades

- 🔐 **Autenticação Completa**: Login tradicional + OAuth (Google, GitHub, Microsoft, Apple)
- 📊 **Analytics Avançado**: Estatísticas detalhadas de cliques, localização e dispositivos
- 🎨 **Interface Moderna**: Design responsivo com dark mode
- ⚡ **Alta Performance**: FastAPI + PostgreSQL otimizado
- 🌐 **Deploy Simples**: Pronto para Vercel com um clique

## 🚀 Deploy Rápido

### 1. Clone o projeto
```bash
git clone https://github.com/RobertoSilvaDevFullStack/linkify.git
cd linkify
```

### 2. Deploy no Vercel
```bash
npm i -g vercel
vercel --prod
```

### 3. Configure as variáveis no Vercel Dashboard:
```env
DATABASE_URL=postgresql://user:pass@host:5432/linkify
GOOGLE_CLIENT_ID=sua-google-client-id
GOOGLE_CLIENT_SECRET=seu-google-client-secret
GITHUB_CLIENT_ID=sua-github-client-id
GITHUB_CLIENT_SECRET=seu-github-client-secret
```

## 🛠️ Tecnologias

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Auth**: OAuth2, JWT, Authlib
- **Deploy**: Vercel, Neon Database

## 📋 OAuth Setup

Para configurar OAuth, veja o guia completo: [OAUTH_PRODUCTION.md](./OAUTH_PRODUCTION.md)

**URLs de Callback**:
- Google: `https://seu-dominio.vercel.app/auth/google/callback`
- GitHub: `https://seu-dominio.vercel.app/auth/github/callback`

## 🏃‍♂️ Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis (copie .env.example para .env)
cp .env.example .env

# Executar servidor
python main.py
```

Acesse: http://localhost:8000

## 📁 Estrutura do Projeto

```
linkify/
├── main.py                 # Aplicação principal FastAPI
├── oauth_config.py         # Configuração OAuth
├── api/index.py           # Entrada Vercel
├── frontend/templates/    # Templates HTML
├── requirements.txt       # Dependências Python  
├── vercel.json           # Configuração Vercel
└── README.md             # Este arquivo
```

## 🎯 Páginas Principais

- `/` - Página inicial com encurtamento
- `/login` - Autenticação
- `/dashboard` - Painel de controle
- `/analytics` - Estatísticas detalhadas
- `/profile` - Perfil do usuário

## 🔧 API Endpoints

- `GET /docs` - Documentação Swagger
- `POST /shorten` - Encurtar URL
- `GET /{short_code}` - Redirecionar URL
- `GET /stats/{short_code}` - Estatísticas

## 📈 Próximas Funcionalidades

- [ ] QR Code automático
- [ ] URLs customizadas
- [ ] Integração com Telegram
- [ ] API pública
- [ ] Temas personalizados

## 🤝 Contribuindo

1. Fork o projeto  
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 💡 Autor

**Roberto Silva** - [GitHub](https://github.com/RobertoSilvaDevFullStack)
