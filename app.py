from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Chave secreta para segurança da sessão (ESSENCIAL!)
app.secret_key = 'iambatman'

# --- Simulação de Banco de Dados ---
USUARIOS = {
    "bruce.wayne": {"senha": "batman", "permissao": "administrador"},
    "alfred.pennyworth": {"senha": "butler", "permissao": "gerente"},
    "lucius.fox": {"senha": "tech", "permissao": "funcionario"}
}

RECURSOS = [
    {"id": 1, "nome": "Veículo Blindado #01", "tipo": "veiculo", "status": "disponível"},
    {"id": 2, "nome": "Câmera de Segurança IR", "tipo": "equipamento", "status": "em uso"},
    {"id": 3, "nome": "Portão Principal C2", "tipo": "dispositivo", "status": "ativo"}
]
# --- Fim da Simulação ---


@app.route('/')
def index():
    # Redireciona para o login se o usuário não estiver na sessão
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
    