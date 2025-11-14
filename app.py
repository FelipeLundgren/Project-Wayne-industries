from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Chave secreta para segurança da sessão (ESSENCIAL!)
app.secret_key = 'iambatman'

# Variável auxiliar para gerar IDs únicos
next_resource_id = 4 # Começa após os 3 recursos iniciais

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


# --- Decorator de Autenticação ---
def login_required(f):
    """Decorator para exigir que o usuário esteja logado."""
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__ 
    return decorated_function
# --- Fim do Decorator ---


@app.route('/')
def index():
    # Redireciona para o login se o usuário não estiver na sessão
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USUARIOS and USUARIOS[username]['senha'] == password:
            # Autenticação bem-sucedida
            session['username'] = username
            session['permissao'] = USUARIOS[username]['permissao']
            return redirect(url_for('dashboard')) # <--- AGORA FUNCIONARÁ
        else:
            # Autenticação falhou
            return render_template('login.html', erro='Usuário ou senha inválidos.')

    # Se for GET, apenas exibe a página de login
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('permissao', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required # Usa o decorator para proteger esta rota
def dashboard():
    # Prepara os dados para serem exibidos no dashboard
    total_recursos = len(RECURSOS)
    recursos_em_uso = sum(1 for r in RECURSOS if r['status'] == 'em uso')
    recursos_disponiveis = total_recursos - recursos_em_uso
    total_usuarios = len(USUARIOS)
    
    # Passa todos os dados processados para o template
    return render_template(
        'dashboard.html',
        username=session.get('username'),
        permissao=session.get('permissao'),
        total_recursos=total_recursos,
        recursos_em_uso=recursos_em_uso,
        recursos_disponiveis=recursos_disponiveis,
        total_usuarios=total_usuarios
    )

@app.route('/inventario')
@login_required
def inventario():
    # Apenas administradores e gerentes podem acessar a gestão
    if session.get('permissao') not in ['administrador', 'gerente']:
        return redirect(url_for('dashboard')) 
        
    return render_template(
        'inventario.html', 
        recursos=RECURSOS, 
        permissao=session.get('permissao')
    )

# A rota adicionar_recurso() (POST/GET) viria logo abaixo.

# --- Execução do Aplicativo (DEVE ESTAR NO FINAL) ---
if __name__ == '__main__':
    app.run(debug=True)