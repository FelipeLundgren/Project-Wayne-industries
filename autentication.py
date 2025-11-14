from flask import Flask, render_template, request, redirect, url_for, session
from app import*

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USUARIOS and USUARIOS[username]['senha'] == password:
            # Autenticação bem-sucedida
            session['username'] = username
            session['permissao'] = USUARIOS[username]['permissao']
            return redirect(url_for('dashboard'))
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
def login_required(f):
    """Decorator para exigir que o usuário esteja logado."""
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            # flash('Você precisa estar logado para acessar esta página.') # Opcional: Adicionar mensagens
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__ # Necessário para o Flask
    return decorated_function

# ... (código login e logout) ...


@app.route('/dashboard')
@login_required # Usa o decorator para proteger esta rota
def dashboard():
    # Prepara os dados para serem exibidos no dashboard
    
    # 1. Análise de Recursos
    total_recursos = len(RECURSOS)
    recursos_em_uso = sum(1 for r in RECURSOS if r['status'] == 'em uso')
    recursos_disponiveis = total_recursos - recursos_em_uso

    # 2. Análise de Usuários
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

if __name__ == '__main__':
    app.run(debug=True)