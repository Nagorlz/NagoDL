# 🚀 TeleGrab DL — v1.0.0

**TeleGrab DL** é um userbot avançado para Telegram que permite baixar e clonar posts, álbuns, fotos e vídeos (inclusive de chats protegidos), preservando legendas, blockquotes e a ordem correta. Possui sistema anti-flood, reupload automático e controle preciso de quantidade.

> Criador: Nago.rlz  

---

## ✨ Funcionalidades

- 📥 Download de posts individuais ou álbuns  
- 🖼️ Suporte a foto + vídeo no mesmo post  
- 📝 Preserva legendas (inclusive com blockquote `>`)  
- 🔒 Reupload automático para chats protegidos  
- 🚫 Sistema ANTI-FLOOD (download e upload)  
- 📊 Logs de progresso (download / upload)  
- ⏱️ Ordem correta: do mais recente para o mais antigo  
- 🎯 Controle exato de quantidade  
- 🧹 Limpeza automática de arquivos após envio  
- ⚡ Funciona em chats privados, grupos e canais  

---

## 📌 Requisitos

- Conta Telegram logada  
- Python 3.9+  
- (Opcional) Telegram Premium para arquivos grandes  

---

## 📱 Instalação no Termux (Android)

### 1️⃣ Atualizar pacotes
```bash
pkg update && pkg upgrade
```

### 2️⃣ Instalar dependências
```bash
pkg install python git -y
```

### 3️⃣ Clonar o projeto
```bash
git clone https://github.com/Nagorlz/NagoDL.git
cd NagoDL
```

### 4️⃣ Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate
```

### 5️⃣ Instalar dependências Python
```bash
pip install telethon
```

---

## 🖥️ Instalação em VPS (Ubuntu / Debian)

### 1️⃣ Atualizar sistema
```bash
apt update && apt upgrade -y
```

### 2️⃣ Instalar dependências
```bash
apt install python3 python3-venv python3-pip git -y
```

### 3️⃣ Clonar o projeto
```bash
git clone https://github.com/Nagorlz/NagoDL.git
cd NagoDL
```

### 4️⃣ Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5️⃣ Instalar dependências Python
```bash
pip install telethon
```

---

## 🔑 Configuração do Telegram

### 1️⃣ Obter API ID e API HASH

Acesse:
https://my.telegram.org

- Faça login com sua conta Telegram  
- Vá em **API development tools**  
- Copie `api_id` e `api_hash`  

---

### 2️⃣ Gerar string_session

```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = SEU_API_ID
api_hash = "SEU_API_HASH"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
```

Copie a string gerada.

---

### 3️⃣ Configurar o bot

Edite o arquivo `main.py`:

```python
api_id = 123456
api_hash = "SEU_API_HASH"
string_session = "SUA_STRING_SESSION"
```

---

## ▶️ Execução

```bash
python main.py
```

Saída esperada:
```
🚀 Userbot /dl iniciado com ANTI-FLOOD
```

---

## 🧠 Uso

### Comando
```
/dl LINK QUANTIDADE
```

### Exemplo
```
/dl https://t.me/c/123456789/500 10
```

### Funcionamento

- Começa no post do link informado  
- Processa do mais recente para os mais antigos  
- Para exatamente ao atingir a quantidade pedida  
- Álbuns contam como **1 post**  
- Mensagens sem mídia são ignoradas  

---

## 🔒 Chats protegidos

- Detectados automaticamente  
- Download local das mídias  
- Reupload como mídia nova  
- Arquivos removidos após envio  

---

## 🎬 Vídeos

- Enviados como **vídeo (streamável)**  
- Não são enviados como documento  
- Permite assistir sem baixar tudo  

⚠️ Sem Telegram Premium, arquivos acima de ~2GB não serão baixados.

---

## 📁 Estrutura do Projeto

```
telegrab-dl/
├── main.py
├── venv/
├── README.md
└── LICENSE
```

---

## ⚠️ Aviso Legal

Este projeto é apenas para fins educacionais.  
O autor não se responsabiliza pelo uso indevido.

---

## 📄 Licença

MIT modificada — veja o arquivo LICENSE.

---

## 🤝 Créditos

Criador: Nago.rlz  
Biblioteca: Telethon  
Versão: v1.0.0
