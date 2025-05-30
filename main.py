from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'senhasupersecretacomçparahackeramericanoerussonaoconseguirinvadir'
usuarios = []

# função para verificar qual usuário está logado
def usuario_logado():
    for usuario in usuarios:
        if usuario['logado'] == 1:
            return usuario
    return None

# função de pegar o nome do usuário logado
def nome_usuario_logado():
    usuario = usuario_logado()
    if usuario != None:
        nome = usuario['nome']
        return nome
    return None


# rota da home
@app.route('/')
def index():
    # aparecer o nome na home
    nome = nome_usuario_logado()
    usuario = usuario_logado()
    return render_template('index.html', nome=nome, usuario=usuario)

# rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    usuario = usuario_logado()
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
            "logado": 0, #nao loguei
            "receitas": [],
            "despesas": []
        }
        usuarios.append(usuario)
        flash('Cadastro realizado com sucesso')
        return redirect(url_for('login'))

    return render_template('cadastro.html', usuario=usuario)


# rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    usuario = usuario_logado()
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
    return render_template('login.html', usuario=usuario)
    


    return render_template('login.html', usuario=usuario)

# rota logout
@app.route('/logout')
def logout():
    usuario = usuario_logado()
    if usuario:
        usuario['logado'] = 0
        flash('Usuário deslogado com sucesso')

        return redirect(url_for('index'))
    return redirect('index')

# rota de perfil
@app.route('/perfil')
def perfil():
    # aparecer o nome na home
    usuario = usuario_logado()
    nome = nome_usuario_logado()
    for usuario in usuarios:
        if usuario['logado'] == 1:
            nome = usuario['nome']
            email = usuario['email']
            return render_template('perfil.html', nome=nome, email=email, usuario=usuario)
    return redirect('login')

# rota para abrir a edição
@app.route('/abrir_editar/<codigo>')
def abrir_editar(codigo):
    for usuario in usuarios:
        if usuario['codigo'] == codigo:
            return render_template('editar.html', usuario=usuario)

# rota de editar
@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar(codigo):
    usuario = usuario_logado()
    if request.method == 'POST':
        usuario['nome'] = request.form['nome']
        usuario['email'] = request.form['email']
        usuario['senha'] = request.form['senha']
        senha = usuario['senha']
        email = usuario['email']
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
            return render_template('editar.html', usuario=usuario)

        elif not tem_minuscula:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('editar.html', usuario=usuario)

        elif not tem_numero:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('editar.html', usuario=usuario)

        elif not tem_especial:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('editar.html', usuario=usuario)

        elif len(usuario['senha']) < 8:
            flash('A senha deve ter pelo menos 8 dígitos, uma maiúscula, uma minúscula, um número e um caractere especial')
            return render_template('editar.html', usuario=usuario)

        elif not usuario['nome']:
            flash('Nome obrigatório')
            return render_template('editar.html', usuario=usuario)

        # Verificar se email já existe
        for usuario in usuarios:
            if usuario['email'] == email:
                flash("Este email já está cadastrado por outro usuário")
                return render_template('editar.html', usuario=usuario)
        
        return redirect(url_for('perfil'))

    return render_template('editar.html')

# Rota da carteira
@app.route('/carteira')
def carteira():
    # aparecer o nome na home
    nome = nome_usuario_logado()
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))
    for usuario in usuarios:
        if usuario['logado'] == 1:
            nome = usuario['nome']
            email = usuario['email']

            saldo = 0
            receita_total = 0
            despesa_total = 0
# validação da receita
            for receita in usuario['receitas']:
                saldo += float(receita['valor'])
                receita_total += float(receita['valor'])
# validação da despesa
            for despesa in usuario['despesas']:
                saldo -= float(despesa['valor'])
                despesa_total -= float(despesa['valor'])
            return render_template('carteira.html', receita_total=receita_total, despesa_total=despesa_total, saldo=saldo, nome=nome)
    return render_template('login.html')


@app.route('/lista_receitas')
def lista_receitas():
    usuario = usuario_logado()
    if usuario:
        receitas=usuario['receitas']
    return render_template('lista_receitas.html', receitas=receitas)


@app.route('/lista_despesas')
def lista_despesas():
    usuario = usuario_logado()
    if usuario:
        despesas = usuario['despesas']
    return render_template('lista_despesas.html', despesas=despesas)

# rota adicionar receita
@app.route('/adicionar_receita', methods=['GET', 'POST'])
def adicionar_receita():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))

    if request.method == 'POST':
        valor = float(request.form['valor'])
        
        if valor <= 0:
            flash('O valor da receita não pode ser 0 ou negativo')
            return render_template('adicionar_receita.html')

        descricao = request.form['descricao']
        data_nf = request.form['data']
        codigo = str(len(usuario['receitas']) +1)
        data_pre_formatada = datetime.strptime(data_nf, '%Y-%m-%d')  # Converte string para datetime
        data_formatada = data_pre_formatada.strftime('%d/%m/%Y')

        receita = {
            'valor': valor,
            'descricao': descricao,
            'data': data_formatada,
            'data_nf': data_nf,
            'codigo': codigo
        }
        usuario['receitas'].append(receita)
        flash('Receita cadastrada com sucesso')
        return redirect('/lista_receitas')
    return render_template('adicionar_receita.html')



# rota adicionar despesa
@app.route('/adicionar_despesa', methods=['GET', 'POST'])
def adicionar_despesa():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))

    if request.method == 'POST':
        valor = float(request.form['valor'])

        if valor <= 0:
            flash('O valor da despesa não pode ser 0 ou negativo')
            return render_template('adicionar_despesa.html')

        descricao = request.form['descricao']
        data_nf = request.form['data']
        codigo = str(len(usuario['despesas']) +1)
        data_pre_formatada = datetime.strptime(data_nf, '%Y-%m-%d')  # Converte string para datetime
        data_formatada = data_pre_formatada.strftime('%d/%m/%Y')
        despesa = {
            'valor': valor,
            'descricao': descricao,
            'data': data_formatada,
            'data_nf': data_nf,
            'codigo': codigo
        }
        usuario['despesas'].append(despesa)
        flash('Despesa cadastrada com sucesso')
        return redirect('/lista_despesas')
    return render_template('adicionar_despesa.html')

# abrir a página de editar receita
@app.route('/abrir_editar_receita/<codigo>')
def abrir_editar_receita(codigo):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))
    for receita in usuario['receitas']:
        if receita['codigo'] == codigo:
            return render_template('editar_receita.html', receita=receita)

# editar receita
@app.route('/editar_receita/<codigo>', methods=['GET', 'POST'])
def editar_receita(codigo):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))
    if request.method == 'POST':
        for receita in usuario['receitas']:
            if receita['codigo'] == codigo:
                valor = float(request.form['valor'])

                if valor <= 0:
                    flash('O valor da receita não pode ser 0 ou negativo')
                    return redirect('/lista_receitas')
                receita['valor'] = valor
                receita['descricao'] = request.form['descricao']
                receita['data_nf'] = request.form['data']
                data_pre_formatada = datetime.strptime(receita['data_nf'], '%Y-%m-%d')  # Converte string para datetime
                data_formatada = data_pre_formatada.strftime('%d/%m/%Y')
                receita['data'] = data_formatada
                
        flash('Receita editada com sucesso')
        return redirect(url_for('lista_receitas'))

    return render_template('editar_receita.html', receita=receita)

# abrir editar despesa
@app.route('/abrir_editar_despesa/<codigo>')
def abrir_editar_despesa(codigo):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))
    for despesa in usuario['despesas']:
        if despesa['codigo'] == codigo:
            return render_template('editar_despesa.html', despesa=despesa)

# editar despesa
@app.route('/editar_despesa/<codigo>', methods=['GET', 'POST'])
def editar_despesa(codigo):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))
    if request.method == 'POST':
        for despesa in usuario['despesas']:
            if despesa['codigo'] == codigo:
                valor = float(request.form['valor'])

                if valor <= 0:
                    flash('O valor da despesa não pode ser 0 ou negativo')
                    return redirect('/lista_despesas')

                despesa['valor'] = valor
                despesa['descricao'] = request.form['descricao']
                despesa['data_nf'] = request.form['data']
                data_pre_formatada = datetime.strptime(despesa['data_nf'], '%Y-%m-%d')  # Converte string para datetime
                data_formatada = data_pre_formatada.strftime('%d/%m/%Y')
                despesa['data'] = data_formatada
        flash('Despesa editada com sucesso')
        return redirect(url_for('lista_despesas'))

    return render_template('editar_despesa.html', despesa=despesa)


# rota excluir receita
@app.route('/excluir_receita/<codigo>')
def excluir_receita(codigo):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))
    for i, receita in enumerate(usuario['receitas']):
        if receita['codigo'] == codigo:
            del usuario['receitas'][i]
            flash('Receita excluída com sucesso!')
            break
    return redirect(url_for('lista_receitas'))


# rota excluir despesa
@app.route('/excluir_despesa/<codigo>')
def excluir_despesa(codigo):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for('login'))
    for i, despesa in enumerate(usuario['despesas']):
        if despesa['codigo'] == codigo:
            del usuario['despesas'][i]
            flash('Despesa excluída com sucesso!')
            break
    return redirect(url_for('lista_despesas'))




if __name__ == '__main__':
    app.run(debug=True)