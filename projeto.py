from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import urllib.parse

# -------------------
# 1) Configurações
# -------------------
app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer'  # necessário para sessão

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://{user}:{pw}@{host}:3306/{db}'
    .format(
        user='root',
        pw='adminfecaf123!',
        host='localhost',
        db='db_controle'
    )
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -------------------
# 2) Modelos 
# -------------------

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id     = db.Column(db.Integer,   primary_key=True, autoincrement=True)
    nome   = db.Column(db.String(100), nullable=False)
    login  = db.Column(db.String(50),  unique=True,  nullable=False)
    senha  = db.Column(db.String(100), nullable=False)  #texto-plano!
    perfil = db.Column(db.Enum('ADM','COMUM'), nullable=False, default='COMUM')


class Produto(db.Model):
    __tablename__ = 'produto'
    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome              = db.Column(db.String(45), nullable=False)
    qtde              = db.Column(db.Integer,    nullable=False)
    quantidade_minima = db.Column(db.Integer,    nullable=False, default=0)
    descricao         = db.Column(db.String(400), nullable=True)


# -------------------
# 3) Decorators
# -------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_perfil') != 'ADM':
            flash('Acesso negado: somente Administrador.', 'danger')
            return redirect(url_for('lista_produtos'))
        return f(*args, **kwargs)
    return decorated


# -------------------
# 4) Rotas de Autenticação
# -------------------

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        l = request.form['login']
        s = request.form['senha']
        user = Usuario.query.filter_by(login=l).first()
        if user and user.senha == s:
            session['user_id']     = user.id
            session['user_nome']   = user.nome
            session['user_perfil'] = user.perfil
            # antes: redirect(lista_produtos)
            return redirect(url_for('index'))
        flash('Login ou senha incorretos.', 'warning')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """
    Dashboard após o login.
    Se ADM, mostra links para produtos, usuários e novo usuário.
    Se COMUM, redireciona direto para a lista de produtos.
    """
    perfil = session.get('user_perfil')
    if perfil == 'ADM':
        return render_template('index.html', user_nome=session.get('user_nome'))
    else:
        # usuário comum vai direto para a lista
        return redirect(url_for('lista_produtos'))


# -------------------
# 5) Rotas de Usuário (ADM apenas)
# -------------------

@app.route('/usuarios')
@login_required
@admin_required
def lista_usuarios():
    todos = Usuario.query.all()
    return render_template('usuarios.html', usuarios=todos)


@app.route('/usuarios/novo', methods=['GET','POST'])
@login_required
@admin_required
def cadastrar_usuario():
    if request.method == 'POST':
        nome   = request.form['nome'].strip()
        login_ = request.form['login'].strip()
        senha  = request.form['senha']
        perfil = request.form['perfil']

        # 1) Verifica duplicidade de login
        existe = Usuario.query.filter_by(login=login_).first()
        if existe:
            flash(f"Já existe usuário com login “{login_}”. Escolha outro.", "danger")
            # reexibe o formulário, rodam os dados preenchidos
            return render_template(
                'cadastrar_usuario.html',
                nome=nome,
                login=login_,
                perfil=perfil
            )

        # 2) Se não existe, cria e salva
        u = Usuario(nome=nome, login=login_, senha=senha, perfil=perfil)
        db.session.add(u)
        db.session.commit()
        flash('Usuário criado com sucesso.', 'success')
        return redirect(url_for('lista_usuarios'))

    # GET: exibe form vazio
    return render_template('cadastrar_usuario.html')


# -------------------
# 6) Rotas de Produto
# -------------------

@app.route('/lista')
@login_required
def lista_produtos():
    lista = Produto.query.order_by(Produto.id).all()
    return render_template(
        'lista.html',
        titulo="Lista de produtos",
        todos_produtos=lista
    )


@app.route('/cadastrar')
@login_required
def form_cadastrar_produto():
    return render_template("cadastrar.html")


@app.route('/adicionar', methods=["POST"])
@login_required
def adicionar_produto():
    nome      = request.form['txtNome']
    qtde      = int(request.form['txtQtde'])
    qt_minima = int(request.form.get('txtQtMin', 0))
    descricao = request.form['txtDescricao']
    p = Produto(
        nome=nome,
        qtde=qtde,
        quantidade_minima=qt_minima,
        descricao=descricao
    )
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('lista_produtos'))


@app.route('/produtos/remover/<int:produto_id>')
@login_required
def remover_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto removido com sucesso.', 'success')
    return redirect(url_for('lista_produtos'))


# Rota para editar (GET exibe form, POST atualiza)
@app.route('/produtos/editar/<int:produto_id>', methods=['GET','POST'])
@login_required
def editar_produto(produto_id):
    p = Produto.query.get_or_404(produto_id)

    if request.method == 'POST':
        # pega valores do form
        p.nome               = request.form['txtNome']
        p.qtde               = int(request.form['txtQtde'])
        p.quantidade_minima  = int(request.form.get('txtQtMin', 0))
        p.descricao          = request.form['txtDescricao']

        db.session.commit()
        flash(f'Produto “{p.nome}” atualizado com sucesso.', 'success')
        return redirect(url_for('lista_produtos'))

    # GET: renderiza o form com produto já carregado
    return render_template('editar_produto.html', produto=p)


# -------------------
# 7) Inicialização
# -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # cria tabelas se não existirem
    app.run(debug=True)