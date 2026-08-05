import os
import json
import urllib.request
import urllib.parse

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# ── Token em variável de ambiente (NUNCA no HTML) ──
HUB_API = 'https://ws.hubdodesenvolvedor.com.br/v2/cadastropf/'
HUB_TOKEN = os.environ.get('HUB_TOKEN', '').strip()

if not HUB_TOKEN:
    app.logger.warning('HUB_TOKEN nao definido no ambiente. A consulta de CPF nao funcionara ate configurar.')


@app.route('/api/consulta')
def consulta():
    """Proxy seguro: o front chama aqui; o servidor usa o token e consulta o Hub."""
    cpf = ''.join(ch for ch in (request.args.get('cpf') or '') if ch.isdigit())
    if len(cpf) != 11:
        return jsonify({'status': False, 'message': 'CPF invalido (11 digitos).'}), 400

    if not HUB_TOKEN:
        return jsonify({'status': False, 'message': 'Token nao configurado no servidor (HUB_TOKEN).'}), 500

    url = f"{HUB_API}?cpf={cpf}&token={urllib.parse.quote(HUB_TOKEN)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            dados = json.loads(resp.read().decode('utf-8'))
        return jsonify(dados)
    except Exception:
        return jsonify({'status': False, 'message': 'Erro ao consultar o Hub do Desenvolvedor.'}), 502


@app.route('/')
def index():
    """Serve o frontend."""
    return send_from_directory('public', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))