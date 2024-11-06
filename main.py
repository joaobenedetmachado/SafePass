import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb 
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import utils.encrypt as enc
import utils.haveibeenpwned as hibp
import utils.geradordesenha as gds    
import utils.geolocal as ip
import pandas as pd
import webbrowser
import datetime
import csv
import os


DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "123123123"
DB_DATABASE = "vaultify"

DBconexao = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE,
    port=3307
)

cursor = DBconexao.cursor()


root = ttkb.Window(themename="darkly") #superhero, #cosmo, #solar
root.title("Cadastro e Login")
root.geometry("600x400")
root.resizable(False, False) # pra nao poder mudar o tamanho da janela
# root.iconbitmap('./assets/logo.ico') #icone da pagina

style = ttk.Style()
style.configure("TNotebook", borderwidth=5)
style.configure("TNotebook.Tab", padding=[10, 5]) 

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both', padx=20)  

aba_login = ttk.Frame(notebook, width=400, height=360)  
aba_login.pack(fill='both', expand=True) 

aba_cadastro = ttk.Frame(notebook, width=360, height=360)  
aba_cadastro.pack(fill='both', expand=True)  

notebook.add(aba_login, text='Login')
notebook.add(aba_cadastro, text='Cadastro')

def OpenSite(listbox_senhas): # ele pega a linha selecionada
    listselecionado = listbox_senhas.curselection()
    if not listselecionado:
        messagebox.showwarning("Aviso", "Selecione uma senha para editar.")
        return
        
    item = listbox_senhas.get(listselecionado) # separa e coloca numa lista
    print(item)
    parts = item.split()
    site = parts[3].lower()
    print(site) # ai a partir ele ve se tem as coisa que precisa pra ser um url ou nao
    if 'http' in site and '.com' in site:
        webbrowser.open(site)
    elif 'http://www' in site and ".com" not in site:
        webbrowser.open(site + '.com')
    elif "http" not in site and ".com" not in site:
        urlCorreto = 'http://www.' + site + ".com"
        webbrowser.open(urlCorreto)
        print(urlCorreto)
    elif  'http' not in site:
        urlCorreto = 'http://' + site
        print(urlCorreto)
        webbrowser.open(urlCorreto)
    
def ExportCSV(iduser):
    caminho_diretorio = filedialog.askdirectory(title="Selecione um diretório") # pede o diretorio
    if caminho_diretorio:  
        caminho_arquivo = os.path.join(caminho_diretorio, 'senhas.csv') # coloca esse senhas la
        print(f"Caminho do arquivo: {caminho_arquivo}")

        comandoSQL = f'SELECT passwordhash, sitename from passwords where userid = {iduser}' 
        cursor.execute(comandoSQL)
        resultado = cursor.fetchall()
        
        passwords = [line[0] for line in resultado]
        sitename = [line[1] for line in resultado]

        with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as csv_file: # abre o arquivo e edita ele
            writer = csv.writer(csv_file) # escreve o arquivo
            writer.writerow(['Site', 'Senha'])  # escreve o cabecalho

            for encrypted_password, site in zip(passwords, sitename): # pega a senha e o site e coloca no csv 
                decrypted_password = enc.descriptografar(encrypted_password) # descriptografa a senha 
                writer.writerow([site, decrypted_password]) # escreve na linha o site e a senha
    else:
        print("Nenhum diretório selecionado.")
    messagebox.showwarning("Aviso", f"Senhas exportadas com sucesso para '{caminho_arquivo}'.")
    logs = "Senhas exportadas"
    salvar_logs(logs , listbox_logs)



def uploadSCV(iduser, text_area, resultado): 
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])

    if file_path:
        df = pd.read_csv(file_path, sep=',', header=None) 
        print("Arquivo carregado com sucesso!")
        print(df)

        if df.empty:
            print("O arquivo CSV está vazio.")
            return  # retorna se o DataFrame estiver vazio
    
        for i, r in df.iterrows():
            password = r[0]
            siteName = r[1]
            print(password, siteName)
            senhasCriptografa = enc.criptografar(password)
            
            comandoSQL = f'INSERT INTO passwords(userid, passwordhash, sitename) VALUES({iduser}, "{senhasCriptografa}", "{siteName}")'
            print(iduser, password, siteName, type(password), type(siteName))
            
            try:
                cursor.execute(comandoSQL)
            except Exception as e:
                print(f"Erro ao inserir dados: {e}")
                messagebox.showwarning("Importar Dados", "Erro ao ler arquivo CSV!.")
        messagebox.showwarning("Importar Dados", "Arquivo CSV lido com sucesso!.")

        DBconexao.commit()
        recarregar(resultado, text_area)
        logs = "Senhas importadas"
        salvar_logs(logs, listbox_logs)
        
# funcao de cadastro
def cadastrar():
    usuario = entry_usuario_cadastro.get() # pega os valores dos entrys
    senha = entry_senha_cadastro.get()
    
    if usuario and senha: # se nao tiverem vazios:
        comandoSQL = "SELECT * FROM users"
        cursor.execute(comandoSQL)
        resultado = cursor.fetchall()
        nome_existentes = [line[1] for line in resultado]
        if usuario not in nome_existentes:
            comandoSQL = f"INSERT INTO users(nome, password) VALUES('{usuario}', '{senha}')"
            cursor.execute(comandoSQL)
            DBconexao.commit()
            messagebox.showwarning("Cadastro", "Pronto! Usuário cadastrado!")
        else:
            messagebox.showwarning("Cadastro", "Este nome já existe no banco de dados, escolha outro!")
    else:
        messagebox.showwarning("Cadastro", "Por favor, preencha todos os campos.")

def atualizar_label(valor, label_valor): # pra atualizar o label pra ver quantos caracteres o range pegou
    label_valor.config(text=valor)

# funcao de login
def logar():
    usuario = entry_usuario_login.get() # pegar os valores dos entrys
    senha = entry_senha_login.get()
    
    if usuario and senha: # se nao forem nulos: 
        comandoSQL = f"SELECT * FROM users WHERE nome = '{usuario}' AND password = '{senha}'"
        cursor.execute(comandoSQL)
        resultado = cursor.fetchone() # diferente to fetchall, pega so um valor, o primeiro no caso
        if resultado:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            afterLogin(usuario)
        else: # mensagem de erro: 
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos.")
    else:
        messagebox.showwarning("Login", "Por favor, preencha todos os campos.")

# funcao apos o login
def afterLogin(usuario):
    root.title(f"{usuario} | {ip.pegarIPCidade()}") # pega o nome do user o da cidade e coloca como titulo da pagina
    notebook.forget(aba_cadastro) # esquece / deleta a aba de login e cadastro
    notebook.forget(aba_login) # botao de deslogar para excluir as abas e "lembrar" de outras
    button_deslogar = tk.Button(root, text="Deslogar", command=lambda: deslogar(aba_senhas, aba_geradordesenhas, aba_haveibeenpwned, aba_login, aba_cadastro, button_deslogar))
    button_deslogar.place(x=522, y=10) # gambiarra pra ficar certinho
        
    aba_senhas = ttk.Frame(notebook) 
    notebook.add(aba_senhas, text='Senhas')
    aba_senhas.rowconfigure(0, weight=0)  # label
    aba_senhas.rowconfigure(1, weight=1) #text area
    aba_senhas.rowconfigure(2, weight=0)  # botao

    aba_senhas.columnconfigure(0, weight=1)  # col para label e área de texto
    aba_senhas.columnconfigure(1, weight=0)  # col p o botao
    
    listbox_senhas = tk.Listbox(aba_senhas, width=50, height=20, activestyle="none", font=('Arial', 12))
    listbox_senhas.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    

    comandoSQL = f"SELECT idusers FROM users WHERE nome = '{usuario}'" # pega o id do user a partir do seu nome/userna,e
    cursor.execute(comandoSQL)
    resultado = cursor.fetchone()
    iduser = resultado[0]
    if resultado:
        recarregar(resultado, listbox_senhas)
        
    # "div" pros botoes pra ficarem tudo juntinho
    frame_botoes = tk.Frame(aba_senhas)
    frame_botoes.grid(row=0, column=1, padx=10, pady=10, sticky='n')

    button_criarNovaSenha = tk.Button(frame_botoes, text="Cadastrar Nova Senha",fg="white", width=20, bg='#038f36', command=lambda: cadastrarNovaSenhaArea(iduser, resultado, listbox_senhas))
    button_criarNovaSenha.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    button_excluirSenha = tk.Button(frame_botoes, text="Excluir Senha", width=20,fg="white" ,bg='#e03d3d', command=lambda:  ExcluirSenha(listbox_senhas, usuario))
    button_excluirSenha.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    button_editarSenha = tk.Button(frame_botoes, text="Editar Senha", width=20, fg="white" ,bg='#099ceb' ,command=lambda: EditarSenhaArea(listbox_senhas, usuario))
    button_editarSenha.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
    
    button_importarSenha = tk.Button(frame_botoes, text="Importar Senhas", width=20, command=lambda: uploadSCV(iduser, listbox_senhas, resultado))
    button_importarSenha.grid(row=3, column=0, padx=5, pady=(140, 5), sticky='ew')

    # botao exportar senahs
    button_exportarSenhas = tk.Button(frame_botoes, text="Exportar Senhas", width=20, command=lambda: ExportCSV(iduser))
    button_exportarSenhas.grid(row=4, column=0, padx=5, pady=(5, 5), sticky='ew')

    # button abrir o site selecioonado
    button_abrirSite = tk.Button(frame_botoes, text="Abrir Site", width=20, command=lambda: OpenSite(listbox_senhas))
    button_abrirSite.grid(row=5, column=0, padx=5, pady=(5, 10), sticky='ew')

    aba_senhas.grid_columnconfigure(0, weight=1)
    aba_senhas.grid_rowconfigure(0, weight=1)

    
    # parte pra area do haveibeenpwned
    aba_haveibeenpwned = ttk.Frame(notebook) 
    notebook.add(aba_haveibeenpwned, text='Have I Been Pwned')
    
    # rows e columns p  aba_haveibeenpwned
    aba_haveibeenpwned.grid_rowconfigure(0, weight=1) # ele cria tres colunas verticais e duas horizontais
    aba_haveibeenpwned.grid_rowconfigure(1, weight=3)
    aba_haveibeenpwned.grid_rowconfigure(2, weight=3)

    aba_haveibeenpwned.grid_columnconfigure(0, weight=2)
    aba_haveibeenpwned.grid_columnconfigure(1, weight=2)

    label_senha = tk.Label(aba_haveibeenpwned, text="Senha:", bg="#f0f0f0")
    label_senha.grid(row=1, column=0, pady=(45, 0), sticky='e')  

    entry_senhahaveibeenpwned = tk.Entry(aba_haveibeenpwned, show="*", width=30)
    entry_senhahaveibeenpwned.grid(row=1, column=1, pady=(45, 0), sticky='w')  

    button_haveibeenpwned = tk.Button(aba_haveibeenpwned, text="Checar se senha já foi vazada", command=lambda: hibp.haveibeenpwned(entry_senhahaveibeenpwned.get()), width=25, bg="#4CAF50", fg="white", font=('Arial', 12))
    button_haveibeenpwned.grid(row=2, column=0, columnspan=2, pady=(20, 20)) 


    def atualizar_label(valor, label_valor): # pra atualizar o label pra ver quantos caracteres o range pegou 
        label_valor.config(text=valor) # label de quantos caracteres o range pegou

    # parte gerador de senhas
    aba_geradordesenhas = ttk.Frame(notebook)
    notebook.add(aba_geradordesenhas, text='Gerador De Senhas')

    # Configuração de linhas e colunas
    aba_geradordesenhas.grid_rowconfigure(0, weight=1) # 5 colunas horizontais e 3 verticais
    aba_geradordesenhas.grid_rowconfigure(1, weight=3)
    aba_geradordesenhas.grid_rowconfigure(2, weight=1)
    aba_geradordesenhas.grid_rowconfigure(3, weight=1)
    
    aba_geradordesenhas.grid_columnconfigure(0, weight=0)  
    aba_geradordesenhas.grid_columnconfigure(1, weight=1)  
    aba_geradordesenhas.grid_columnconfigure(2, weight=0)  
    
    label_caracteres = tk.Label(aba_geradordesenhas, text="Quantidade:", bg="#f0f0f0")
    label_caracteres.grid(row=1, column=0, pady=(20, 5), padx=(100,0), sticky='e')

    scale_caracteres = tk.Scale(aba_geradordesenhas, from_=7, to=30, orient='horizontal', command=lambda valor: atualizar_label(valor, label_valor), length=100)
    scale_caracteres.grid(row=1, column=1, pady=(20, 5), sticky='ew') 

    label_valor = tk.Label(aba_geradordesenhas, text="7", bg="#f0f0f0") 
    label_valor.grid(row=1, column=2, pady=(20, 5), padx=(0,100),sticky='w')

    text_area_gerada = tk.Text(aba_geradordesenhas, height=1, width=20, bg="#ffffff", relief="sunken", wrap=tk.WORD)
    text_area_gerada.grid(row=2, column=0,columnspan=2, pady=(20, 20), padx=(0,95),sticky='ne')
    text_area_gerada.config(state='disabled')

    button_gerarsenha = tk.Button(
        aba_geradordesenhas, 
        text="Gerar Senha", 
        command=lambda: gerar_senha(scale_caracteres.get(), text_area_gerada), # envia pra funcao os valores de scale e text area para gerar a senha e colocar no text area
        width=12, 
    )
    button_gerarsenha.grid(row=3, column=0, columnspan=2, pady=(20, 20), padx=(120,0))
    
    # parte pros log
    aba_logs = ttk.Frame(notebook) 
    notebook.add(aba_logs, text='Logs')
    
    frame_botoes = tk.Frame(aba_logs)
    frame_botoes.grid(row=0, column=1, padx=10, pady=10, sticky='n')
    
    aba_logs.rowconfigure(0, weight=0)
    aba_logs.rowconfigure(1, weight=1)
    aba_logs.rowconfigure(2, weight=0)

    aba_logs.columnconfigure(0, weight=1)
    aba_logs.columnconfigure(1, weight=0)
    
    global listbox_logs # ele pega a listbox e salva na variavel global
    listbox_logs = tk.Listbox(aba_logs, width=50, height=20, activestyle="none") # cria a listbox
    listbox_logs.grid(row=0, column=0, padx=10, pady=10, sticky='nsew') # posiciona a listbox
    listbox_logs.config(state='normal')

    aba_logs.grid_columnconfigure(0, weight=1)
    aba_logs.grid_rowconfigure(0, weight=1)
    

def salvar_logs(logs, listbox_logs): # ele so pega a string do logs e coloca no listbox
    log_text = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {logs}" # pega a data e hora e junta com o logs
    listbox_logs.insert(tk.END, log_text) # coloca no listbox
        

def deslogar(aba_senhas, aba_geradordesenhas, aba_haveibeenpwned, aba_login, aba_cadastro, button_deslogar):
    root.title("Cadastro e Login") # ele volta ao titulo, 
    notebook.forget(aba_senhas)  # delete todos os notebooks, e adiciona os normais de login e cadastro
    notebook.forget(aba_geradordesenhas) # e apaga o botao de deslogar
    notebook.forget(aba_haveibeenpwned)
    notebook.add(aba_login, text='Login')
    notebook.add(aba_cadastro, text='Cadastro')
    button_deslogar.destroy()
    
def gerar_senha(entry_geradordesenhas, text_area_gerada):
    try: # gera a senha com o GerarSenha, e coloca no text area q tem la na janelinha
        quantidade = int(entry_geradordesenhas)  
        senha_gerada = gds.GerarSenhas(quantidade)  
        text_area_gerada.config(state='normal')  
        text_area_gerada.delete(1.0, tk.END) 
        text_area_gerada.insert(tk.END, f"{senha_gerada}")  
        text_area_gerada.config(state='disable') 
    except ValueError: # except so pra ter, pq de vdd nao precisa
        text_area_gerada.config(state='normal')
        text_area_gerada.delete(1.0, tk.END)
        text_area_gerada.insert(tk.END, "Por favor, insira um número válido.") 
        text_area_gerada.config(state='disable')
    

def recarregar(resultado, listbox_senhas): # recarrega a listbox
    listbox_senhas.config(font=("Courier", 10)) # coloca um fonte monspacada pra ficar certinho
    listbox_senhas.delete(0, tk.END)
    
    larguraId = 10 # sem isso nao dava certo
    larguraSenha = 20
    larguraSite = 15

    cabecalho = f"{'ID:'.ljust(larguraId)}{'SENHA:'.ljust(larguraSenha)}{'SITE:'.ljust(larguraSite)}"
    listbox_senhas.insert(tk.END, cabecalho)
    listbox_senhas.insert(tk.END, "―" * (larguraId + larguraSenha + larguraSite)) 

    iduser = resultado[0]
    comandoSQL = f"SELECT idpassword, passwordhash, sitename FROM passwords WHERE userid = {iduser}"
    cursor.execute(comandoSQL)
    resultadoSenhas = cursor.fetchall()

    if resultadoSenhas:
        for id, senha, siteName in resultadoSenhas:
            senhaDescriptografada = enc.descriptografar(senha) # descripta a senha
            if senhaDescriptografada is not None: # e ve se tem algo nos resultados ne
                id_text = f"ID {id}".ljust(larguraId)
                senha_text = senhaDescriptografada.ljust(larguraSenha)
                site_text = siteName.ljust(larguraSite)
                listbox_senhas.insert(tk.END, f"{id_text}{senha_text}{site_text}")
            else:
                listbox_senhas.insert(tk.END, f"Erro na descriptografia | {siteName}")
    else:
        listbox_senhas.insert(tk.END, "Nenhuma senha encontrada.")

# func p cadastrar senha nova no db
def cadastrarNovaSenhaArea(iduser, resultado, text_area):
    janelaCriarSenha = tk.Toplevel(root)
    janelaCriarSenha.title("Criar Senha")
    janelaCriarSenha.geometry("300x300")
    
    label_senha = tk.Label(janelaCriarSenha, text="Senha:")
    label_senha.pack(pady=(20, 5))  
    entry_senha = tk.Entry(janelaCriarSenha)
    entry_senha.pack(pady=(0, 20))  
    
    label_sitename = tk.Label(janelaCriarSenha, text="Site:")
    label_sitename.pack(pady=(20, 5))  
    entry_sitename = tk.Entry(janelaCriarSenha)
    entry_sitename.pack(pady=(0, 20))  
    button_criarNovaSenha = tk.Button(janelaCriarSenha, text="Cadastrar Nova Senha", command=lambda: CadastrarNovaSenha(janelaCriarSenha, iduser, enc.criptografar(entry_senha.get()), (entry_sitename.get()).title(), resultado, text_area))
    button_criarNovaSenha.pack(pady=(20, 20))
    
def EditarSenhaArea(listbox_senhas, usuario): # pego a linha selecionada
    listselecionado = listbox_senhas.curselection()
    if not listselecionado:
        messagebox.showwarning("Aviso", "Selecione uma senha para editar.") # aviso caso nao tenha
        return
    
    item = listbox_senhas.get(listselecionado) # pega os valores dentro
    print(item)
    parts = item.split() # divide pelos espacos e transforma-os em uma lista
    id = int(parts[1]) # o primeiro index é um id
    senha = parts[2] # o segundo a senha
    site = parts[3] # o terceiro o site
    print(id)
    
    #vo fazxer uma janela pra colocar o bgl pq é melhor
    dialog = tk.Toplevel() # cria uma janela toplevel (que fica acima das outras, sem que ela precisa ser excluida)
    dialog.title("Editar Senha")
    dialog.geometry("400x225")
    
    tk.Label(dialog, text="Novo nome do site:").pack(pady=10) 
    entry_site = tk.Entry(dialog, width=50)
    entry_site.insert(0, site) 
    entry_site.pack(pady=5)
    
    tk.Label(dialog, text="Nova senha:").pack(pady=10)
    entry_senha = tk.Entry(dialog, width=50)
    entry_senha.insert(0, senha) 
    entry_senha.pack(pady=5)
        
    button_criarNovaSenha = tk.Button(dialog, text="Cadastrar Nova Senha", command=lambda: EditarSenha(entry_senha.get(), entry_site.get(), id, usuario, listbox_senhas)) # envia pra funcao os valores
    button_criarNovaSenha.pack(pady=(20, 20)) 
    
       
def EditarSenha(novaSenha, novoSite, id, usuario, listbox_senhas):
    comandoSQL=f'UPDATE passwords SET passwordhash = "{enc.criptografar(novaSenha)}", sitename="{novoSite}" where idpassword = {id}'
    cursor.execute(comandoSQL)
    DBconexao.commit()
    messagebox.showinfo("Sucesso", "Senha editada com sucesso.")
    comandoSQL = f"SELECT idusers FROM users WHERE nome = '{usuario}'"
    cursor.execute(comandoSQL)
    resultado = cursor.fetchone()
    if resultado:
        recarregar(resultado, listbox_senhas)
    logs = f" UPDATE | ID: {id} | Senha: {novaSenha} | Site: {novoSite}"
    salvar_logs(logs, listbox_logs)  
    
    
def ExcluirSenha(listbox_senhas, usuario):
    listselecionado = listbox_senhas.curselection() # pega o selecionado e caso nao tenha nenhum ele mostra o erro numa janelinha
    if not listselecionado:
        messagebox.showwarning("Aviso", "sem senha selecionada para excluir.")
        return

    item = listbox_senhas.get(listselecionado)
    parts = item.split() # splita eles a partir dos espacos
    id = int(parts[1])  # pega o id
    print(id)
    logs = " DELETE | ID: {id} | Excluído"
    salvar_logs(logs, listbox_logs) 
    
    confirm = messagebox.askyesno("confirmar delete", f"desejas excluir a senha do ID {id}?")
    if not confirm: # se o user apartar em NO ele fecha a janela
        return
    else: # se dar certo ele exclui pelo id
        comandosql = f'Delete from passwords where idpassword = {id}'
        cursor.execute(comandosql)
        DBconexao.commit()
        messagebox.showinfo("Sucesso", f"A senha do ID {id} foi excluída com sucesso")
        comandoSQL = f"SELECT idusers FROM users WHERE nome = '{usuario}'"
        cursor.execute(comandoSQL)
        resultado = cursor.fetchone()
        if resultado:
            recarregar(resultado, listbox_senhas)
    

def CadastrarNovaSenha(janelaCriarSenha, iduser, password, siteName, resultado, text_area):
    try:
        comandoSQL = f'INSERT INTO passwords(userid, passwordhash, sitename) VALUES({iduser}, "{password}", "{siteName}")'
        print(iduser, password, siteName, type(password), type(siteName))
        cursor.execute(comandoSQL)
        DBconexao.commit()
        print("Senha cadastrada")
        recarregar(resultado, text_area)
        janelaCriarSenha.destroy()
    except ValueError:
        messagebox.showerror("CadastroSenha", "Formato da senha incorreta!")
    logs = f"CADASTRO | ID: {iduser} | Senha: {enc.descriptografar(password)} | Site: {siteName}"
    salvar_logs(logs, listbox_logs)
    

aba_cadastro.grid_rowconfigure(1, weight=3) # cria row's e column's pra tipo, gerar um grid
aba_login.grid_rowconfigure(1, weight=3)
aba_cadastro.grid_rowconfigure(2, weight=3)
aba_login.grid_rowconfigure(2, weight=3)
aba_cadastro.grid_rowconfigure(3, weight=3)
aba_login.grid_rowconfigure(3, weight=3)

aba_cadastro.columnconfigure(0, weight=2)
aba_cadastro.columnconfigure(1, weight=2)

aba_login.columnconfigure(0, weight=2)
aba_login.columnconfigure(1, weight=2)


#cadstro
label_usuario_cadastro = tk.Label(aba_cadastro, text="Usuário:")
label_usuario_cadastro.grid(row=2, column=0, pady=(0, 25), sticky='e')

entry_usuario_cadastro = tk.Entry(aba_cadastro, width=30)  
entry_usuario_cadastro.grid(row=2, column=1, pady=(0, 25), sticky='w')

label_senha_cadastro = tk.Label(aba_cadastro, text="Senha:")
label_senha_cadastro.grid(row=2, column=0, pady=(45,0), sticky='e')

entry_senha_cadastro = tk.Entry(aba_cadastro, show="*", width=30)  
entry_senha_cadastro.grid(row=2, column=1, pady=(45, 0), sticky='w')

button_cadastrar = tk.Button(aba_cadastro, text="Cadastrar", command=cadastrar, width=15, font=('Arial', 12))
button_cadastrar.grid(row=3, column=0, columnspan=2, pady=(20, 20))

#logi
label_usuario_login = tk.Label(aba_login, text="Usuário:")
label_usuario_login.grid(row=2, column=0, pady=(0, 25), sticky='e')

entry_usuario_login = tk.Entry(aba_login, width=30)  
entry_usuario_login.grid(row=2, column=1, pady=(0, 25), sticky='w')

label_senha_login = tk.Label(aba_login, text="Senha:")
label_senha_login.grid(row=2, column=0, pady=(45, 0), sticky='e')

entry_senha_login = tk.Entry(aba_login, show="*", width=30)  
entry_senha_login.grid(row=2, column=1, pady=(45, 0), sticky='w') 

button_logar = tk.Button(aba_login, text="Login", command=logar, width=15, font=('Arial', 12))
button_logar.grid(row=3, column=0, columnspan=2, pady=(20, 20))

root.mainloop()