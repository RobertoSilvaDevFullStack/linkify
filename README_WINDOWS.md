# 🪟 Linkify - Setup Windows

## ⚠️ Problema com psycopg2-binary no Windows

Se você encontrou o erro:
```
error: command 'C:\Program Files (x86)\Microsoft Visual Studio\...\link.exe' failed with exit code 1120
```

### 🔧 Soluções:

#### **Opção 1: Usar SQLite para desenvolvimento (Recomendado)**
```bash
# 1. Instalar dependências sem PostgreSQL
python setup.py

# 2. A aplicação usará SQLite automaticamente
python main.py
```

#### **Opção 2: Instalar Visual Studio Build Tools**
```bash
# Baixe e instale: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Selecione: "C++ build tools" e "Windows 10 SDK"
# Depois execute:
pip install psycopg2-binary
```

#### **Opção 3: Usar conda**
```bash
# Se você tem Anaconda/Miniconda:
conda install psycopg2
```

#### **Opção 4: Wheel pré-compilado**
```bash
# Para Python 3.11 Windows x64:
pip install https://download.lfd.uci.edu/pythonlibs/archived/psycopg2_binary-2.9.9-cp311-cp311-win_amd64.whl
```

## 🚀 Início Rápido

```bash
# 1. Clonar e entrar no diretório
git clone https://github.com/RobertoSilvaDevFullStack/linkify.git
cd linkify

# 2. Executar setup automático
python setup.py

# 3. Configurar variáveis (copie .env.example para .env)
copy .env.example .env
# Edite .env com suas credenciais

# 4. Executar aplicação
python main.py
```

## 🗄️ Banco de Dados

### **Desenvolvimento (Local)**
- ✅ **SQLite** - Automático, sem configuração
- ⚙️ **PostgreSQL** - Requer psycopg2 (opcional)

### **Produção (Vercel)**
- 🔗 **Supabase** - PostgreSQL na nuvem
- 📋 Veja: [SUPABASE_SETUP.md](./SUPABASE_SETUP.md)

## 🔍 Verificação

```bash
# Testar se tudo está funcionando:
python -c "import main; print('✅ OK!')"

# Executar aplicação:
python main.py
```

## 📱 URLs de Desenvolvimento

- **Frontend**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Login Teste**: testuser / testpass123

## 🆘 Ajuda

Se ainda tiver problemas:

1. **Verifique Python**: `python --version` (3.8+)
2. **Atualize pip**: `pip install --upgrade pip`
3. **Use ambiente virtual**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   python setup.py
   ```

## 🌐 Deploy

Para deploy na Vercel:
- A aplicação usará PostgreSQL (Supabase) automaticamente
- Windows não afeta o deploy (roda em Linux na Vercel)
- Siga: [SUPABASE_SETUP.md](./SUPABASE_SETUP.md)
