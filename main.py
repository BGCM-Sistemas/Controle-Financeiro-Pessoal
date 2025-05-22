from flask import Flask, render_template, request, redirect, flash, url_for



app = Flask(__name__)
app.secret_key = 'senhasupersecretacomçparahackeramericanoerussonaoconseguirinvadir'
usuarios = {
'nome':[],
'email':[],
'senha':[]
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

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
            flash('A senha deve ter pelo menos uma letra maiúscula!')
            return render_template('cadastro.html')

        elif not tem_minuscula:
            flash('A senha deve ter pelo menos uma letra minúscula!')
            return render_template('cadastro.html')

        elif not tem_numero:
            flash('A senha deve ter pelo menos um número!')
            return render_template('cadastro.html')

        elif not tem_especial:
            flash('A senha deve ter pelo menos um caractere especial!')
            return render_template('cadastro.html')

        elif len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres!')
            return render_template('cadastro.html')

        elif not nome:
            flash('Nome e sobrenome obrigatório')


        # Verificar se email já existe
        # for usuario in usuarios:
        #     if usuario['email'] == email:
        #         return "Erro: Este email já está cadastrado"

        usuarios['nome'].append(nome)
        usuarios['email'].append(email)
        usuarios['senha'].append(senha)


        return redirect(url_for('login'))

    else:
        return render_template('cadastro.html')







@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        for emails in usuarios['email']:
            if emails == email:
                indice_email = usuarios['email'].index(email)
                if senha == usuarios['senha'][indice_email]:
                    return redirect('/perfil')

        if usuarios['email'] == email and usuarios['senha'] == senha:
            return redirect('/perfil')
        else:
            flash('Email ou senha incorretos')

    return render_template('login.html')

@app.route('/perfil')
def perfil():
    email = usuarios['email'][0]
    nome = usuarios['nome'][0]
    return render_template('perfil.html', nome=nome, email=email)

if __name__ == '__main__':
    app.run(debug=True)