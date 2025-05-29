from flask import Flask, render_template, request, redirect, flash, url_for



app = Flask(__name__)
app.secret_key = 'senhasupersecretacomçparahackeramericanoerussonaoconseguirinvadir'
usuarios = []
receitas = []
despesas = []

# rota da home
@app.route('/')
def index():
    # aparecer o nome na home
    nome = ''
    if len(usuarios) > 0:
        for usuario in usuarios:
            nome = usuario["nome"]
    return render_template('index.html', nome=nome)

# rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        codigo = str(len(usuarios) +1)
# validação reforçada da senha
        tem_maiuscula = False
        tem_minuscula = False
        tem_numero = False
        tem_especial = False

        for c in senha:
            if c.isupper(): # se tem maiuscula
                tem_maiuscula = True
            elif c.islower(): #se tem minuscula
                tem_minuscula = True
            elif c.isdigit(): #se tem numero
                tem_numero = True
            elif not c.isalnum(): #se tem caracter especial
                tem_especial = True
        
        if not tem_maiuscula:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('cadastro.html')
        
        elif not tem_minuscula:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('cadastro.html')
        
        elif not tem_numero:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('cadastro.html')
        
        elif not tem_especial:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('cadastro.html')
        
        elif len(senha) < 8:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('cadastro.html')
        
        elif not nome:
            flash('Nome obrigatório')
            return render_template('cadastro.html')


        #Verificar se email já existe
        for usuario in usuarios:
            if usuario['email'] == email:
                flash("Este email já está cadastrado")
                return render_template('cadastro.html')

        # cadastro do usuario
        usuario = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "codigo": codigo,
            "logado": 0 #nao loguei
        }
        usuarios.append(usuario)
        flash('Cadastro realizado com sucesso')
        return redirect(url_for('login'))

    else:
        return render_template('cadastro.html')


# rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        for usuario in usuarios:
            if usuario['email'] == email:
                if usuario['senha'] == senha:
                    usuario['logado'] = 1 # logado
                    flash("Login realizado com sucesso")
                    return render_template('perfil.html', usuario=usuario)

                flash("Email ou senha inválidos")
                return render_template('login.html')


    return render_template('login.html')

# rota de perfil
@app.route('/perfil')
def perfil():
    # aparecer o nome na home
    nome = ''
    if len(usuarios) > 0:
        for usuario in usuarios:
            nome = usuario["nome"]
    for usuario in usuarios:
        if usuario['logado'] == 1:
            nome = usuario['nome']
            email = usuario['email']
            return render_template('perfil.html', nome=nome, email=email, usuario=usuario)
    return render_template('login.html')

# rota para abrir a edição
@app.route('/abrir_editar/<codigo>')
def abrir_editar(codigo):
    for usuario in usuarios:
        if usuario['codigo'] == codigo:
            return render_template('editar.html', usuario=usuario)

# rota de editar
@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar(codigo):
    if request.method == 'POST':
        for usuario in usuarios:
            if usuario['codigo'] == codigo:
                if usuario['logado'] == 1:
                    usuario['nome'] = request.form['nome']
                    usuario['email'] = request.form['email']
                    usuario['senha'] = request.form['senha']
                senha = usuario['senha']
                # senha forte
                tem_maiuscula = False
                tem_minuscula = False
                tem_numero = False
                tem_especial = False

                for c in senha:
                    if c.isupper(): # se tem maiuscula
                        tem_maiuscula = True
                    elif c.islower(): #se tem minuscula
                        tem_minuscula = True
                    elif c.isdigit(): #se tem numero
                        tem_numero = True
                    elif not c.isalnum(): #se tem caracter especial
                        tem_especial = True
                
                if not tem_maiuscula:
                    flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
                    return render_template('editar.html')
                
                elif not tem_minuscula:
                    flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
                    return render_template('editar.html')
                
                elif not tem_numero:
                    flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
                    return render_template('editar.html')
                
                elif not tem_especial:
                    flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
                    return render_template('editar.html')
                
                elif len(usuario['senha']) < 8:
                    flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
                    return render_template('editar.html')
                
                elif not usuario['nome']:
                    flash('Nome obrigatório')
                    return render_template('editar.html')

        return redirect(url_for('perfil'))

    return render_template('editar.html', usuario=usuario)

# Rota da carteira
@app.route('/carteira')
def carteira():
    # aparecer o nome na home
    # nome = ''
    # if len(usuarios) > 0:
    #     for usuario in usuarios:
    #         nome = usuario["nome"]

    return render_template('carteira.html', receitas=receitas)

@app.route('/adicionar_receita', methods=['GET', 'POST'])
def adicionar_receita():
    if request.method == 'POST':
        valor = request.form['valor']
        descricao = request.form['descricao']
        data = request.form['data']
        codigo = str(len(usuarios) +1)
        receita = {
            'valor': valor,
            'descricao': descricao,
            'data': data,
            'codigo': codigo
        }
        print(receita)
        receitas.append(receita)
        print(receitas)
        return redirect('/carteira')
    return render_template('adicionar_receita.html')

@app.route('/adicionar_despesa', methods=['GET', 'POST'])
def adicionar_despesa():
    if request.method == 'POST':
        valor = request.form['valor']
        descricao = request.form['descricao']
        data = request.form['data']
        codigo = str(len(usuarios) +1)
        despesa = {
            'valor': valor,
            'descricao': descricao,
            'data': data,
            'codigo': codigo
        }
        print(despesa)
        print(despesas)
        despesas.append(despesa)
        return redirect('/carteira')
    return render_template('adicionar_despesa.html')

if __name__ == '__main__':
    app.run(debug=True)