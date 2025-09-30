# app.py

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
import functools

# --- Configuração da Aplicação ---
app = Flask(__name__)
# Chave secreta para gerenciar sessões de usuário (em produção, use um valor mais seguro)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'
DATABASE = 'database.db'

# --- Conexão com o Banco de Dados ---
def get_db():
    """Cria e retorna uma conexão com o banco de dados."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Retorna linhas como dicionários para facilitar o acesso por nome de coluna
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Fecha a conexão com o banco de dados ao final de cada requisição."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """(Opcional) Função para inicializar o banco de dados usando o schema.sql."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- Decoradores e Funções de Autenticação ---
def login_required(view):
    """Decorador que exige que o usuário esteja logado para acessar uma view."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.before_request
def load_logged_in_user():
    """Carrega os dados do usuário logado da sessão em g.user antes de cada requisição."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()

# --- Rotas da Aplicação ---

@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Página de login."""
    if request.method == 'POST':
        login_user = request.form['login']
        senha = request.form['senha']
        db = get_db()
        error = None
        
        user = db.execute('SELECT * FROM usuarios WHERE login = ?', (login_user,)).fetchone()

        if user is None:
            error = 'Usuário incorreto.'
        elif not check_password_hash(user['senha'], senha):
            error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('login.html')

@app.route('/novo_usuario', methods=('GET', 'POST'))
def novo_usuario():
    """Página de cadastro de novo usuário (CRUD - Create)."""
    if request.method == 'POST':
        login_user = request.form['login']
        senha = request.form['senha']
        db = get_db()
        error = None

        if not login_user:
            error = 'Nome de usuário é obrigatório.'
        elif not senha:
            error = 'Senha é obrigatória.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO usuarios (login, senha) VALUES (?, ?)",
                    (login_user, generate_password_hash(senha)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Usuário {login_user} já está cadastrado."
            else:
                flash('Usuário criado com sucesso! Faça o login.', 'success')
                return redirect(url_for('login'))
        
        flash(error, 'danger')

    return render_template('novo_usuario.html')

@app.route('/index')
@login_required
def index():
    """Página inicial após o login."""
    return render_template('index.html')

@app.route('/registro_abertura', methods=('GET', 'POST'))
@login_required
def registro_abertura():
    """Formulário para registrar checklist de abertura."""
    if request.method == 'POST':
        db = get_db()
        db.execute(
            """INSERT INTO registros_abertura (lider_abertura, fiscal_abertura, luzes_ligadas, 
            equipamentos_checados, riscos_incendio, troca_vigilante, portoes_deslacrados, 
            lacres_registrados, latitude, longitude, autor_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                request.form['lider_abertura'], request.form['fiscal_abertura'],
                'luzes_ligadas' in request.form, 'equipamentos_checados' in request.form,
                'riscos_incendio' in request.form, request.form['troca_vigilante'],
                'portoes_deslacrados' in request.form, request.form['lacres_registrados'],
                request.form['latitude'], request.form['longitude'], g.user['id']
            )
        )
        db.commit()
        flash('Checklist de abertura salvo com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('registro_abertura.html')

@app.route('/registro_fechamento', methods=('GET', 'POST'))
@login_required
def registro_fechamento():
    """Formulário para registrar checklist de fechamento."""
    if request.method == 'POST':
        db = get_db()
        db.execute(
            """INSERT INTO registros_fechamento (lider_fechamento, fiscal_fechamento, luzes_desligadas,
            equipamentos_desligados, riscos_incendio, troca_vigilante, portoes_lacrados,
            lacres_registrados, latitude, longitude, autor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                request.form['lider_fechamento'], request.form['fiscal_fechamento'],
                'luzes_desligadas' in request.form, 'equipamentos_desligados' in request.form,
                'riscos_incendio' in request.form, request.form['troca_vigilante'],
                'portoes_lacrados' in request.form, request.form['lacres_registrados'],
                request.form['latitude'], request.form['longitude'], g.user['id']
            )
        )
        db.commit()
        flash('Checklist de fechamento salvo com sucesso!', 'info')
        return redirect(url_for('index'))
    return render_template('registro_fechamento.html')

@app.route('/registros')
@login_required
def listar_registros():
    """Página que lista todos os registros (CRUD - Read)."""
    db = get_db()
    aberturas = db.execute('SELECT * FROM registros_abertura ORDER BY data_hora_abertura DESC').fetchall()
    fechamentos = db.execute('SELECT * FROM registros_fechamento ORDER BY data_hora_fechamento DESC').fetchall()
    return render_template('listar_registros.html', aberturas=aberturas, fechamentos=fechamentos)

@app.route('/logout')
def logout():
    """Faz o logout do usuário."""
    session.clear()
    return redirect(url_for('login'))

# --- Execução da Aplicação ---
if __name__ == '__main__':
    # init_db() # Descomente esta linha na PRIMEIRA vez que rodar para criar o banco de dados.
    app.run(debug=True)