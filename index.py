from flask import Flask, render_template, request, jsonify, session, redirect, url_for41
import json
import os

app = Flask(__name__)
app.secret_key = 'WilsonPinheiro'


#FUNÇÕES E PARÂMETROS DO SISTEMA
# -----------------------------------------------------------------------
def carregar_usuarios_dp():
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo usuarios.json não encontrado, criando um novo.")
        return []  # Retorna uma lista vazia
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo usuarios.json. Arquivo corrompido.")
        return []  # Retorna uma lista vazia, caso o arquivo seja corrompido

    
def salvar_usuarios(usuarios):
    0
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

# Função para salvar os dados no arquivo usuarios.json
def salvar_usuarios_dp(usuarios):
    try:
        with open('usuarios.json', 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)
            print("Usuários salvos com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")
        raise  # Levanta o erro novamente para ser tratado no nível superior
# -----------------------------------------------------------------------
# Função para salvar os dados no arquivo JSON
def salvar_dados_json(dados):
    try:
        # Tenta abrir e carregar os dados existentes
        with open('dados.json', 'r') as file:
            dados_existentes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não for encontrado ou estiver vazio/corrompido, cria uma lista vazia
        dados_existentes = []

    # Adiciona os novos dados
    dados_existentes.append(dados)

    # Salva os dados no arquivo JSON
    with open('dados.json', 'w') as file:
        json.dump(dados_existentes, file, indent=4)
# -----------------------------------------------------------------------
# Função para carregar os treinos do arquivo JSON
def load_treinos():
    with open('treinos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para salvar os treinos no arquivo JSON
def save_treinos(treinos):
    with open('treinos.json', 'w', encoding='utf-8') as f:
        json.dump(treinos, f, ensure_ascii=False, indent=4)
# -----------------------------------------------------------------------
def salvar_dados(dados):
    with open('dados.json', 'w', encoding='utf-8') as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)        
# -----------------------------------------------------------------------
# Função para carregar administradores
def load_admins():
    if os.path.exists("admin.json"):
        # Verifica se o arquivo não está vazio
        if os.path.getsize("admin.json") > 0:
            with open("admin.json", "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []  # Retorna uma lista vazia caso o arquivo esteja corrompido
        else:
            return []  # Arquivo existe, mas está vazio
    return []  # Arquivo não existe, retorna lista vazia
# Função para salvar administradores
# -----------------------------------------------------------------------

def save_admins(admins):
    with open("admin.json", "w") as file:
        json.dump(admins, file, indent=4)
# -----------------------------------------------------------------------
def carregar_administradores():
    try:
        with open('admin.json', 'r') as f:  # Caminho do arquivo JSON
            administradores = json.load(f)
        return administradores
    except Exception as e:
        print(f"Erro ao carregar administradores: {e}")
        return []
# -----------------------------------------------------------------------
# Função para salvar os administradores no arquivo JSON
def salvar_administradores(administradores):
    try:
        with open('admin.json', 'w') as f:
            json.dump(administradores, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar administradores: {e}")
# -----------------------------------------------------------------------
def carregar_treinos():
    try:
        with open('treinos.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao carregar treinos: {e}")
        return {}
# -----------------------------------------------------------------------

def salvar_treinos(treinos):
    try:
        with open('treinos.json', 'w', encoding='utf-8') as f:
            json.dump(treinos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar os treinos: {e}")
# -----------------------------------------------------------------------
def carregar_usuarios():
        if os.path.exists('usuarios.json'):
            with open('usuarios.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
# -----------------------------------------------------------------------
def carregar_dados():
    try:
        with open('dados.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return []
# -----------------------------------------------------------------------
def salvar_usuarios(lista):
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)
# -----------------------------------------------------------------------

#PÁGINAS DO USUARIO
######################### MEUS TREINOS ################################
@app.route('/meus_treinos')
def meus_treinos():
    user_data = session.get('user')  # Obtém os dados do usuário logado na sessão

    if not user_data:  # Se não encontrar dados do usuário na sessão, redireciona para o login
        return redirect(url_for('login'))

    cpf_usuario = user_data.get("cpf")  # Corrigido para minúsculas

    # Carrega os dados dos usuários
    with open('usuarios.json', 'r', encoding='utf-8') as f:
        usuarios_data = json.load(f)

    treino_atribuido = None

    # Busca o treino do usuário logado
    for usuario in usuarios_data:
        if usuario["cpf"] == cpf_usuario:  # Aqui também corrigimos para minúsculas
            treino_atribuido = usuario.get("treinoAtribuido")  # Pegando os treinos
            break

    # Debug para verificar se encontrou o treino correto
    print("Treino atribuído:", treino_atribuido)

    return render_template('meus_treinos.html', user_data=user_data, treino_atribuido=treino_atribuido)


################################### PERFIL ###############################################

@app.route('/perfil')
def perfil():
    user_data = session.get('user')  # Obtém os dados do usuário logado na sessão
    if user_data is None:
        return redirect(url_for('login'))  # Se o usuário não estiver logado, redireciona para o login
    return render_template('perfil.html', user_data=user_data)  # Passa os dados para o template
################################### CONSULTAR AVALIAÇÃO FÍSICA###############################
@app.route('/consulta_alunos')
def consulta_alunos():
    return render_template('consulta_alunos.html')



#PÁGINAS ADMINISTRADOR

# Caminho do arquivo admin.json
ADMIN_FILE = "admin.json"

@app.route('/cadastro')
def cadastro():
     return render_template('cadastro.html')

@app.route('/enviar-cadastro', methods=['POST'])
def enviar_cadastro():
    dados = request.get_json()  # Pega os dados enviados em formato JSON
    print("Dados recebidos:", dados)  # Imprime os dados para verificação

    # Carregar os usuários existentes
    usuarios = carregar_usuarios_dp()

    # Verifica se o CPF já está cadastrado
    for usuario in usuarios:
        if usuario['cpf'] == dados['cpf']:
            return jsonify({"message": "Usuário já cadastrado"}), 400  # Retorna erro se o CPF já existe

    # Adicionar o novo usuário aos dados existentes
    usuarios.append(dados)

    # Salvar os usuários no arquivo
    salvar_usuarios_dp(usuarios)

    # Retornar uma resposta em JSON com mensagem de sucesso
    return jsonify({"message": "Cadastro realizado com sucesso!"})

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/inicio')
def inicio():
    return render_template('inicio.html')
# Rota para servir o arquivo index.html
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')


# Rota para cadastrar os dados
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.get_json()

    if not dados:
        print("Nenhum dado recebido!")
        return jsonify({"message": "Nenhum dado recebido!"}), 400

    print("Dados recebidos:", dados)

    try:
        # Tenta carregar os dados existentes
        with open('dados.json', 'r') as file:
            registros = json.load(file)
    except FileNotFoundError:
        registros = []  # Se o arquivo não existir, começa com lista vazia

    # Verifica o último ID cadastrado e gera o próximo
    if registros:
        ultimo_id = max(item.get("id", 0) for item in registros)
    else:
        ultimo_id = 0

    novo_id = ultimo_id + 1
    dados["id"] = novo_id  # Adiciona o novo ID ao registro

    # Adiciona o novo registro à lista
    registros.append(dados)

    # Salva de volta no arquivo JSON
    with open('dados.json', 'w') as file:
        json.dump(registros, file, indent=4)

    return jsonify({
        "success": True,
        "message": f"Cadastro realizado com sucesso! ID: {novo_id}"
    }), 200


# Rota para buscar dados pelo CPF
@app.route('/buscar', methods=['GET'])
def buscar():
    cpf = request.args.get('cpf')  # Obtém o CPF da URL
    if not cpf:
        return jsonify({"message": "CPF não fornecido"}), 400

    try:
        # Lê os dados do arquivo JSON
        with open('dados.json', 'r') as file:
            dados = json.load(file)

        # Filtra todas as pessoas com o mesmo CPF
        pessoas = [item for item in dados if item['cpf'] == cpf]

        if not pessoas:
            return jsonify({"message": "Nenhum resultado encontrado"}), 404

        return jsonify(pessoas), 200

    except FileNotFoundError:
        return jsonify({"message": "Arquivo de dados não encontrado"}), 500
    except Exception as e:
        print("Erro:", e)
        return jsonify({"message": "Erro ao buscar os dados"}), 500
    
@app.route('/listar', methods=['GET'])
def listar():
    try:
        with open('dados.json', 'r') as file:
            dados = json.load(file)
        return jsonify(dados), 200
    except FileNotFoundError:
        return jsonify([]), 200  # Retorna lista vazia se o arquivo não existir
    except Exception as e:
        print("Erro ao listar registros:", e)
        return jsonify({"message": "Erro ao listar registros"}), 500

@app.route('/excluir', methods=['DELETE'])
def excluir():
    id_param = request.args.get('id')  # Pega o ID da query string
    if not id_param:
        return jsonify({"success": False, "message": "ID não fornecido"}), 400

    try:
        id_int = int(id_param)
    except ValueError:
        return jsonify({"success": False, "message": "ID inválido"}), 400

    try:
        with open('dados.json', 'r') as file:
            dados = json.load(file)

        # Filtra os registros que **não** possuem o ID fornecido
        novos_dados = [p for p in dados if p.get('id') != id_int]

        if len(novos_dados) == len(dados):
            return jsonify({"success": False, "message": "Registro não encontrado"}), 404

        with open('dados.json', 'w') as file:
            json.dump(novos_dados, file, indent=4)

        return jsonify({"success": True, "message": "Registro excluído com sucesso"}), 200

    except FileNotFoundError:
        return jsonify({"success": False, "message": "Arquivo de dados não encontrado"}), 500
    except Exception as e:
        print("Erro ao excluir registro:", e)
        return jsonify({"success": False, "message": "Erro ao excluir registro"}), 500

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login')
def login():
    return render_template('login.html')
# Função para carregar os dados do arquivo JSON

# Rota para autenticar o login
@app.route('/autenticar', methods=['POST'])
def autenticar():
    dados_login = request.get_json()
    cpf = dados_login.get('cpf')
    senha = dados_login.get('senha')  # Senha é o próprio CPF

    # Função para carregar os dados dos administradores
    def carregar_admins():
        try:
            with open('admin.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # Função para carregar os dados dos usuários
    def carregar_usuarios():
        if os.path.exists('usuarios.json'):
            with open('usuarios.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    # Verifica se o usuário é administrador
    admins = carregar_admins()
    for admin in admins:
        if admin['cpf'] == cpf and admin['cpf'] == senha:  # CPF é igual à senha
            return jsonify({"redirect_url": url_for('inicio')}), 200

    # Verifica se o usuário é um usuário normal
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['cpf'] == cpf and usuario['cpf'] == senha:
            # Armazena os dados do usuário na sessão
            session['user'] = usuario
            return jsonify({"redirect_url": url_for('meus_treinos')}), 200

    # Caso nenhum login seja válido
    return jsonify({"message": "CPF ou senha inválidos!"}), 401

@app.route('/logout')
def logout():
    return render_template('login.html', message="Você foi deslogado com sucesso!")

# Rota para registrar administradores
@app.route("/registrar_adm", methods=["POST", "GET"])
def registrar_adm():
    administradores = carregar_administradores()
    print(">> DEBUG - Administradores carregados:", administradores)

    if request.method == "POST":
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        email = request.form.get("email")

        if not cpf or not nome or not email:
            return render_template("registrar_adm.html", error="Todos os campos devem ser preenchidos!", administradores=administradores)

        # Verificação duplicidade
        if any(admin["cpf"] == cpf for admin in administradores):
            print(">> DEBUG - CPF duplicado detectado:", cpf)
            return render_template("registrar_adm.html", error="ADMINISTRADOR JÁ CADASTRADO", administradores=administradores)

        # Cadastro
        novo_admin = {
            "cpf": cpf,
            "nome": nome,
            "email": email,
            "senha": cpf  # senha padrão = CPF
        }
        administradores.append(novo_admin)
        salvar_administradores(administradores)
        print(">> DEBUG - Novo admin salvo:", novo_admin)

        session["success"] = "Administrador cadastrado com sucesso!"
        return redirect(url_for('registrar_adm'))

    # GET
    success = session.pop("success", None)
    return render_template("registrar_adm.html", administradores=administradores, success=success)


@app.route("/excluir_adm/<cpf>", methods=["GET", "POST"])
def excluir_adm(cpf):
    administradores = carregar_administradores()
    
    # Verifica se existe mais de um administrador antes de permitir a exclusão
    if len(administradores) <= 1:
        return redirect(url_for('registrar_adm', error="Não é possível excluir o último administrador."))
    
    # Filtra o administrador com o CPF fornecido
    administradores = [admin for admin in administradores if admin["cpf"] != cpf]

    # Salvar novamente os administradores no arquivo
    salvar_administradores(administradores)

    # Redirecionar para a página de registro com a lista atualizada
    return redirect(url_for('registrar_adm', success="Administrador excluído com sucesso!"))

@app.route('/dashboard')
def dashboard():
    dados = carregar_dados()
    return render_template('dashboard.html', dados=dados)
# Rota para exibir "minha-avaliacao.html"

@app.route('/minha-avaliacao')
def minha_avaliacao():
    # Verifica se o usuário está logado
    user_data = session.get('user')
    if user_data is None:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver logado

    cpf_usuario = user_data.get('cpf')  # Obtém o CPF do usuário logado

    try:
        # Lê os dados do arquivo JSON
        with open('dados.json', 'r') as file:
            dados = json.load(file)

        # Filtra os registros com o mesmo CPF do usuário logado
        avaliacoes_usuario = [item for item in dados if item['cpf'] == cpf_usuario]

        if not avaliacoes_usuario:
            message = "Nenhuma avaliação encontrada para o seu CPF."
            return render_template('minha-avaliacao.html', avaliacoes=[], message=message)

        # Renderiza a página com as avaliações do usuário
        return render_template('minha-avaliacao.html', avaliacoes=avaliacoes_usuario)

    except FileNotFoundError:
        message = "O arquivo de dados não foi encontrado."
        return render_template('minha-avaliacao.html', avaliacoes=[], message=message)
    except Exception as e:
        print("Erro ao carregar avaliações:", e)
        message = "Erro ao carregar suas avaliações. Tente novamente mais tarde."
        return render_template('minha-avaliacao.html', avaliacoes=[], message=message)

@app.route('/listar_alunos', methods=['GET'])
def listar_alunos():
    try:
        with open('dados.json', 'r') as file:
            alunos = json.load(file)
        # Retorna os alunos com os campos 'cpf' e 'nome' para popular o select
        alunos_info = [{"cpf": aluno['cpf'], "nome": aluno['nome']} for aluno in alunos]
        return jsonify(alunos_info), 200
    except FileNotFoundError:
        return jsonify({"message": "Arquivo de dados não encontrado"}), 500
    except Exception as e:
        print("Erro ao listar alunos:", e)
        return jsonify({"message": "Erro ao listar alunos"}), 500
    
# Rota para gerenciar os treinos
@app.route('/gerenciar_treinos', methods=['GET', 'POST'])
def gerenciar_treinos():
    treino_selecionado = None
    dias_da_semana = {}
    tipo_treino = None  # Variável para o tipo de treino
    nivel = None  # Variável para o nível

    if request.method == 'POST':
        tipo_treino = request.form['treino']
        nivel = request.form['nivel']

        # Carregar os treinos e filtrar de acordo com o tipo e nível
        treinos = carregar_treinos()
        if tipo_treino in treinos and nivel in treinos[tipo_treino]:
            treino_selecionado = treinos[tipo_treino][nivel]
            dias_da_semana = treino_selecionado['diasDaSemana']

    return render_template('gerenciar_treinos.html', treino_selecionado=treino_selecionado, dias_da_semana=dias_da_semana, tipo_treino=tipo_treino, nivel=nivel)

@app.route('/editar_exercicio', methods=['POST'])
def editar_exercicio():
    try:
        dia = request.form['dia']
        index = int(request.form['index'])
        nome = request.form['nome']
        grupo_muscular = request.form['grupoMuscular']
        series = int(request.form['series'])
        repeticoes = int(request.form['repeticoes'])
        tipo_treino = request.form['tipo_treino']
        nivel = request.form['nivel']

        treinos = carregar_treinos()

        try:
            exercicios = treinos[tipo_treino][nivel]['diasDaSemana'][dia]['exercicios']
            if 0 <= index < len(exercicios):
                exercicio = exercicios[index]
                exercicio['nome'] = nome
                exercicio['grupoMuscular'] = grupo_muscular
                exercicio['series'] = series
                exercicio['repeticoes'] = repeticoes

                salvar_treinos(treinos)
                return jsonify({"status": "sucesso", "mensagem": "Exercício atualizado com sucesso!"})
            else:
                return jsonify({"status": "erro", "mensagem": "Índice de exercício inválido!"})
        except KeyError as e:
            return jsonify({"status": "erro", "mensagem": f"Chave não encontrada: {e}"})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})

################# ATRIBUIR TREINO #########################################################################################
@app.route('/atribuir_treino')
def atribuir_treino():
    alunos = carregar_usuarios_dp()
    treinos = carregar_treinos()
    return render_template("atribuir_treino.html", usuarios=alunos, treinos=treinos)

@app.route('/salvar_treino', methods=['POST'])
def salvar_treino():
    cpf = request.form.get('cpf')
    tipo = request.form.get('tipo')
    nivel = request.form.get('nivel')

    treinos = carregar_treinos()
    treino_selecionado = treinos.get(tipo, {}).get(nivel, {})

    if treino_selecionado:
        dados_alunos = carregar_usuarios_dp()
        
        # Percorrer a lista de alunos de trás para frente
        for aluno in reversed(dados_alunos):
            if aluno.get('cpf') == cpf:
                aluno['treinoAtribuido'] = {
                    "tipo": tipo,
                    "nivel": nivel,
                    "diasDaSemana": treino_selecionado.get('diasDaSemana', [])
                }
                break  # Para de procurar após atualizar o último aluno
        
        # Salvar os dados atualizados no arquivo de usuários
        salvar_usuarios(dados_alunos)
    
    return redirect(url_for('atribuir_treino'))

@app.route('/excluir_treino/<cpf>', methods=['POST'])
def excluir_treino(cpf):
    dados_alunos = carregar_usuarios_dp()
    for aluno in dados_alunos:
        if aluno.get('cpf') == cpf:
            aluno.pop('treinoAtribuido', None)  # Remove o treino atribuído
            break
    salvar_usuarios(dados_alunos)
    return redirect(url_for('atribuir_treino'))

@app.route('/editar_treino', methods=['POST'])
def editar_treino():
    cpf = request.form.get('cpf')
    treino_selecionado = request.form.get('treino')

    if not cpf or not treino_selecionado:
        return "CPF ou treino não fornecido.", 400

    tipo, nivel = treino_selecionado.split('_')
    dados = carregar_usuarios_dp()
    treinos = carregar_treinos()

    for aluno in dados:
        if aluno['cpf'] == cpf:
            aluno['treinoAtribuido'] = {
                "tipo": tipo,
                "nivel": nivel,
                "diasDaSemana": treinos[tipo][nivel]['diasDaSemana']
            }
            break

    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    return redirect(url_for('atribuir_treino'))

@app.route('/alunos_cadastrados')
def alunos_cadastrados():
    with open('usuarios.json', 'r', encoding='utf-8') as f:
        usuarios = carregar_usuarios()
    return render_template('alunos_cadastrados.html', usuarios=usuarios)


@app.route('/alunos_cadastrados/delete/<cpf>', methods=['POST'])
def deletar_usuario(cpf):
    print(f"[DEBUG] CPF recebido: {cpf}")
    
    # Normaliza CPF recebido
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    
    usuarios = carregar_usuarios()
    print("[DEBUG] Lista de usuários:")
    for u in usuarios:
        print("  -", u.get("cpf"), "=>", ''.join(filter(str.isdigit, str(u.get("cpf")))))

    novos_usuarios = [
        u for u in usuarios 
        if ''.join(filter(str.isdigit, str(u.get("cpf")))) != cpf
    ]

    if len(usuarios) == len(novos_usuarios):
        print("[DEBUG] Nenhum usuário removido.")
        return jsonify({'status': 'error', 'message': 'Usuário não encontrado'}), 404

    salvar_usuarios(novos_usuarios)
    print("[DEBUG] Usuário removido com sucesso.")
    return jsonify({'status': 'success', 'message': f'Usuário {cpf} excluído com sucesso'})

@app.route('/adicionar_exercicio', methods=['POST'])
def adicionar_exercicio():
    # Recebe os dados enviados via POST
    dados = request.get_json()

    nome = dados.get('nome')
    grupoMuscular = dados.get('grupoMuscular')
    series = dados.get('series')
    repeticoes = dados.get('repeticoes')
    tipo_treino = dados.get('tipo_treino')
    nivel = dados.get('nivel')
    dia = dados.get('dia')

    if not nome or not grupoMuscular or not series or not repeticoes or not tipo_treino or not nivel or not dia:
        return jsonify({"success": False, "message": "Dados incompletos"}), 400

    # Carrega os treinos do JSON
    treinos = carregar_treinos()

    # Adiciona o exercício na estrutura do JSON
    if tipo_treino in treinos and nivel in treinos[tipo_treino]:
        # Adicionando o exercício no dia correto da semana
        novo_exercicio = {
            "nome": nome,
            "grupoMuscular": grupoMuscular,
            "series": series,
            "repeticoes": repeticoes
        }

        # Verifica se o dia da semana existe
        if dia in treinos[tipo_treino][nivel]["diasDaSemana"]:
            # Agora, adicionamos o exercício na lista "exercicios" do dia
            treinos[tipo_treino][nivel]["diasDaSemana"][dia]["exercicios"].append(novo_exercicio)

            # Salva as alterações no arquivo JSON
            salvar_treinos(treinos)

            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "message": "Dia da semana não encontrado"}), 404
    else:
        return jsonify({"success": False, "message": "Treino ou nível não encontrado"}), 404

@app.route('/excluir_exercicio', methods=['POST'])
def excluir_exercicio():
    try:
        data = request.get_json()
        tipo_treino = data.get('tipo_treino')
        nivel = data.get('nivel')
        dia = data.get('dia')
        index = int(data.get('index'))

        # Carregar treinos
        treinos = carregar_treinos()

        print(f"[DEBUG] tipo_treino: {tipo_treino}, nivel: {nivel}, dia: {dia}, index: {index}")
        
        treino_dia = treinos.get(tipo_treino, {}).get(nivel, {}).get("diasDaSemana", {}).get(dia)

        if not treino_dia:
            return jsonify({'success': False, 'message': 'Treino não encontrado para o dia especificado.'})

        exercicios = treino_dia.get('exercicios', [])

        if not (0 <= index < len(exercicios)):
            return jsonify({'success': False, 'message': 'Índice de exercício inválido.'})

        # Excluir exercício
        exercicio_removido = exercicios.pop(index)
        print(f"[INFO] Exercício removido: {exercicio_removido}")

        # Salvar alterações
        salvar_treinos(treinos)

        return jsonify({'success': True, 'message': 'Exercício excluído com sucesso!'})

    except Exception as e:
        print(f"[ERRO] {e}")
        return jsonify({'success': False, 'message': f'Erro ao excluir exercício: {str(e)}'})

@app.route('/alunos')
def get_alunos():
    with open('dados.json', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
