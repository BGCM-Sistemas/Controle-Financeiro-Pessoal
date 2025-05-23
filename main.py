from flask import Flask, render_template, request, redirect, flash, url_for



app = Flask(__name__)
app.secret_key = 'senhasupersecretacomçparahackeramericanoerussonaoconseguirinvadir'
usuarios = []
# usuarios = {
# 'nome':[],
# 'email':[],
# 'senha':[],
# 'logado': []
# }
INDICE = 0


@app.route('/')
def index():
    nome = ''
    if len(usuarios) > 0:
        nome = usuarios["nome"]
    return render_template('index.html',usuarios = usuarios, nome=nome)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        codigo = str(len(usuarios) +1)

        tem_maiuscula = False
        tem_minuscula = False
        tem_numero = False
        tem_especial = False

        # for c in senha:
        #     if c.isupper(): # se tem maiuscula
        #         tem_maiuscula = True
        #     elif c.islower(): #se tem minuscula
        #         tem_minuscula = True
        #     elif c.isdigit(): #se tem numero
        #         tem_numero = True
        #     elif not c.isalnum(): #se tem caracter especial
        #         tem_especial = True
        #
        # if not tem_maiuscula:
        #     flash('A senha deve ter pelo menos uma letra maiúscula!')
        #     return render_template('cadastro.html')
        #
        # elif not tem_minuscula:
        #     flash('A senha deve ter pelo menos uma letra minúscula!')
        #     return render_template('cadastro.html')
        #
        # elif not tem_numero:
        #     flash('A senha deve ter pelo menos um número!')
        #     return render_template('cadastro.html')
        #
        # elif not tem_especial:
        #     flash('A senha deve ter pelo menos um caractere especial!')
        #     return render_template('cadastro.html')
        #
        # elif len(senha) < 8:
        #     flash('A senha deve ter pelo menos 8 caracteres!')
        #     return render_template('cadastro.html')
        #
        # elif not nome:
        #     flash('Nome e sobrenome obrigatório')


        #Verificar se email já existe
        for usuario in usuarios:
            if usuario['email'] == email:
                flash("Este email já está cadastrado")

        
        usuario = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "codigo": codigo,
            "logado": 0 #nao loguei
        }
        usuarios.append(usuario)

        print(usuarios)

        return redirect(url_for('login'))

    else:
        return render_template('cadastro.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        for usuario in usuarios:
            if usuario['email'] == email:
                if usuario['senha'] == senha:
                    usuario['logado'] = 1 # logado
                    print(usuarios)
                    flash("Login realizado com sucesso")
                    return render_template('perfil.html', usuario=usuario)

                flash("Email ou senha inválidos")
                return render_template('login.html')


    return render_template('login.html')

@app.route('/perfil')
def perfil():
    for usuario in usuarios:
        if usuario['logado'] == 1:
            nome = usuario['nome']
            email = usuario['email']
            return render_template('perfil.html', nome=nome, email=email, usuario=usuario)
    return render_template('login.html')


@app.route('/abrir_editar/<codigo>')
def abrir_editar(codigo):
    for usuario in usuarios:
        if usuario['codigo'] == codigo:
            return render_template('editar.html', usuario=usuario)

@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar(codigo):
    if request.method == 'POST':
        for usuario in usuarios:
            if usuario['codigo'] == codigo:
                if usuario['logado'] == 1:
                    usuario['nome'] = request.form['nome']
                    usuario['email'] = request.form['email']
                    usuario['senha'] = request.form['senha']

                tem_maiuscula = False
                tem_minuscula = False
                tem_numero = False
                tem_especial = False

                # for c in usuario['senha']:
                #     if c.isupper(): # se tem maiuscula
                #         tem_maiuscula = True
                #     elif c.islower(): #se tem minuscula
                #         tem_minuscula = True
                #     elif c.isdigit(): #se tem numero
                #         tem_numero = True
                #     elif not c.isalnum(): #se tem caracter especial
                #         tem_especial = True
                
                # if not tem_maiuscula:
                #     flash('A senha deve ter pelo menos uma letra maiúscula!')
                #     return render_template('cadastro.html')
                
                # elif not tem_minuscula:
                #     flash('A senha deve ter pelo menos uma letra minúscula!')
                #     return render_template('cadastro.html')
                
                # elif not tem_numero:
                #     flash('A senha deve ter pelo menos um número!')
                #     return render_template('cadastro.html')
                
                # elif not tem_especial:
                #     flash('A senha deve ter pelo menos um caractere especial!')
                #     return render_template('cadastro.html')
                
                # elif len(senha) < 8:
                #     flash('A senha deve ter pelo menos 8 caracteres!')
                #     return render_template('cadastro.html')
                
                # elif not nome:
                #     flash('Nome e sobrenome obrigatório')

        return redirect(url_for('perfil'))

    return render_template('editar.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)