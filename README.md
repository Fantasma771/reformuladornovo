# ⚖️ Equipe Fantasma — Reformulador de Processos Jurídicos (Python + Render)

Site com:
- Reformulação de textos de processos jurídicos
- Consulta de Nome por CPF (Hub do Desenvolvedor — cadastropf)
- Botões de WhatsApp com saudação automática
- Links para consulta pública PJE

> 🔒 **Versão segura em Python 3:** o token do Hub do Desenvolvedor **NÃO fica no HTML**. Ele é guardado no servidor em uma variável de ambiente (`HUB_TOKEN`) e o front consulta o backend via `/api/consulta`. O navegador nunca vê o token.

## 1) Configurar o token

### No Render (produção)
1. Acesse o painel do seu serviço.
2. **Settings → Environment → Add Environment Variable**:
   - **Key:** `HUB_TOKEN`
   - **Value:** `SEU_TOKEN_AQUI`
3. Clique em **Save** — o Render reimplanta automaticamente.

O `render.yaml` já declara `HUB_TOKEN` como variável (não sincronizada com Git), então você pode cadastrá-la ao criar o serviço ou depois em Settings → Environment.

### Local (testes)
Crie um arquivo `.env` (ou exporte a variável) com:
```
HUB_TOKEN=SEU_TOKEN_AQUI
```
> O arquivo `.env` é local e não deve ser enviado para o Git.

## 2) Subir no Render

### Opção A — Blueprint (render.yaml)
1. Envie os arquivos para um repositório Git (GitHub/GitLab). **Não inclua o `.env`** (use o `.gitignore`).
2. No Render: **New → Blueprint** e selecione o repositório.
3. Ao ser criado, defina a variável `HUB_TOKEN`.

### Opção B — Web Service manual (Python)
1. Envie os arquivos para um repositório Git.
2. No Render: **New → Web Service**, conecte o repositório.
3. O Render detecta o ambiente **Python 3** automaticamente. Preencha:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:${PORT}`
4. Configure a variável `HUB_TOKEN` em **Environment**.
5. **Create Web Service.**

Acesso em `https://SEU-SERVICO.onrender.com`.

## Teste local
```bash
pip install -r requirements.txt
export HUB_TOKEN=SEU_TOKEN_AQUI   # ou use um arquivo .env
gunicorn app:app --bind 0.0.0.0:3000
# ou, sem gunicorn:
python app.py
```
Acesse `http://localhost:3000`.

## Estrutura
```
equipe-fantasma-render/
├── public/
│   └── index.html      ← front (sem token, chama /api/consulta)
├── app.py              ← Flask + proxy seguro da consulta (Python 3)
├── requirements.txt    ← flask + gunicorn
├── render.yaml         ← deploy Python no Render (declara HUB_TOKEN)
├── .gitignore          ← ignora .env, __pycache__ e .venv
└── README.md
```