import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import encrypt as enc
import haveibeenpwned as hibp
import geradordesenha as gds    

# Configurações do banco de dados
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "123123123"
DB_DATABASE = "vaultify"
DB_PORT = 3307 # deletar essa linha 

# Conexão com o banco de dados
DBconexao = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE,
    port = DB_PORT # deletar esse linha e a virgula de cima
)

cursor = DBconexao.cursor()

# Criação da janela principal
root = tk.Tk()
root.title("Cadastro e Login")
root.geometry("600x400")
root.configure(bg="#f0f0f0")  # Cor de fundo
root.resizable(False, False)

# Estilização do notebook
style = ttk.Style()
style.configure("TNotebook", borderwidth=5)
style.configure("TNotebook.Tab", padding=[10, 5])  # Ajuste de padding para as abas

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both', padx=20)  # Adicionado fill='both' e padx

# Criando as abas com tamanho específico
aba_login = ttk.Frame(notebook, width=400, height=360)  # Define tamanho específico
aba_login.pack(fill='both', expand=True)  # Faz a aba expandir para preencher o espaço

aba_cadastro = ttk.Frame(notebook, width=360, height=360)  # Define tamanho específico
aba_cadastro.pack(fill='both', expand=True)  # Faz a aba expandir para preencher o espaço

notebook.add(aba_login, text='Login')
notebook.add(aba_cadastro, text='Cadastro')

# Função de cadastro
def cadastrar():
    usuario = entry_usuario_cadastro.get()
    senha = entry_senha_cadastro.get()
    
    if usuario and senha:
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

# Função de login
def logar():
    usuario = entry_usuario_login.get()
    senha = entry_senha_login.get()
    
    if usuario and senha:
        comandoSQL = f"SELECT * FROM users WHERE nome = '{usuario}' AND password = '{senha}'"
        cursor.execute(comandoSQL)
        resultado = cursor.fetchone()
        if resultado:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            afterLogin(usuario)
        else:
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos.")
    else:
        messagebox.showwarning("Login", "Por favor, preencha todos os campos.")

# funcao apos o login
def afterLogin(usuario):
    notebook.forget(aba_cadastro)
    notebook.forget(aba_login)
    
    aba_senhas = ttk.Frame(notebook) 
    notebook.add(aba_senhas, text='Senhas')
    
    label_Senhas = tk.Label(aba_senhas, text="Senhas:", bg="#f0f0f0")
    label_Senhas.pack(pady=(25, 0))  
    text_area = tk.Text(aba_senhas, height=10, width=40, bg="#ffffff", bd=3, relief="sunken", wrap=tk.WORD)
    text_area.pack(pady=20)
    text_area.config(state='normal')  
    root.title(f"Conectado como: {usuario}")

    comandoSQL = f"SELECT idusers FROM users WHERE nome = '{usuario}'"
    cursor.execute(comandoSQL)
    resultado = cursor.fetchone()
    iduser = resultado[0]
    if resultado:
        recarregar(resultado, text_area)
    text_area.config(state='disabled')
    button_criarNovaSenha = tk.Button(aba_senhas, text="Cadastrar Nova Senha", command=lambda: cadastrarNovaSenhaArea(iduser, resultado, text_area))
    button_criarNovaSenha.pack(pady=(20, 20))
    
    # parte pra area do haveibeenpwned
    aba_haveibeenpwned = ttk.Frame(notebook) 
    notebook.add(aba_haveibeenpwned, text='Have I Been Pwned')
    
    label_senha = tk.Label(aba_haveibeenpwned, text="Senha:", bg="#f0f0f0")
    label_senha.pack(pady=(20, 5))  
    
    entry_senhahaveibeenpwned = tk.Entry(aba_haveibeenpwned)
    entry_senhahaveibeenpwned.pack(pady=(0, 20))  
    
    button_haveibeenpwned = tk.Button(aba_haveibeenpwned, text="Checar se senha ja foi vazada", command=lambda: hibp.haveibeenpwned(entry_senhahaveibeenpwned.get()))
    button_haveibeenpwned.pack(pady=(20, 20))
    
    # Parte para a área do gerador de senhas
    aba_geradordesenhas = ttk.Frame(notebook)
    notebook.add(aba_geradordesenhas, text='Gerador De Senhas')

    label_caracteres = tk.Label(aba_geradordesenhas, text="Quantidade:", bg="#f0f0f0")
    label_caracteres.pack(pady=(20, 5))  # Corrigido aqui

    entry_geradordesenhas = tk.Entry(aba_geradordesenhas)
    entry_geradordesenhas.pack(pady=(0, 20))

    label_resultado = tk.Label(aba_geradordesenhas, text="Senha Gerada:", bg="#f0f0f0")
    label_resultado.pack(pady=(0, 20))

    def gerar_senha():
        try:
            quantidade = int(entry_geradordesenhas.get())  # Captura a quantidade de caracteres
            senha_gerada = gds.GerarSenhas(quantidade)  # Chama a função para gerar a senha
            label_resultado.config(text=f"Senha Gerada: {senha_gerada}")  # Atualiza a label com a senha gerada
        except ValueError:
            label_resultado.config(text="Por favor, insira um número válido.")  # Tratamento de erro para entradas inválidas

    button_gerarsenha = tk.Button(aba_geradordesenhas, text="Gerar Senha", command=gerar_senha)
    button_gerarsenha.pack(pady=(20, 20))
    
    
    

def recarregar(resultado, text_area):
    text_area.config(state='normal')
    print(resultado, text_area)
    iduser = resultado[0]
    comandoSQL = f"SELECT passwordhash, sitename FROM passwords WHERE userid = {iduser}"
    cursor.execute(comandoSQL)
    resultadoSenhas = cursor.fetchall()

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"{'Senha'.ljust(24)} | {'Site'}\n")
    text_area.insert(tk.END, "-" * 40 + "\n")

    if resultadoSenhas:
        for senha, siteName in resultadoSenhas:
            senhaDescriptografada = enc.descriptografar(senha)
            text_area.insert(tk.END, f"{senhaDescriptografada.ljust(24)} | {siteName}\n")
    else:
        text_area.insert(tk.END, "Nenhuma senha encontrada.")
    text_area.config(state='disable')




# func p cadastrar senha nova no db
def cadastrarNovaSenhaArea(iduser, resultado, text_area):
    janelaCriarSenha = tk.Toplevel(root)
    janelaCriarSenha.title("Criar Senha")
    janelaCriarSenha.geometry("300x300")
    
    label_senha = tk.Label(janelaCriarSenha, text="Senha:", bg="#f0f0f0")
    label_senha.pack(pady=(20, 5))  
    entry_senha = tk.Entry(janelaCriarSenha)
    entry_senha.pack(pady=(0, 20))  
    
    label_sitename = tk.Label(janelaCriarSenha, text="Site:", bg="#f0f0f0")
    label_sitename.pack(pady=(20, 5))  
    entry_sitename = tk.Entry(janelaCriarSenha)
    entry_sitename.pack(pady=(0, 20))  
    button_criarNovaSenha = tk.Button(janelaCriarSenha, text="Cadastrar Nova Senha", command=lambda: CadastrarNovaSenha(janelaCriarSenha, iduser, enc.criptografar(entry_senha.get()), entry_sitename.get(), resultado, text_area))
    button_criarNovaSenha.pack(pady=(20, 20))

def CadastrarNovaSenha(janelaCriarSenha, iduser, password, siteName, resultado, text_area):
    comandoSQL = f'INSERT INTO passwords(userid, passwordhash, sitename) VALUES({iduser}, "{password}", "{siteName}")'
    cursor.execute(comandoSQL)
    DBconexao.commit()
    print("Senha cadastrada")
    recarregar(resultado, text_area)
    janelaCriarSenha.destroy()

# cadastro
label_usuario_cadastro = tk.Label(aba_cadastro, text="Usuário:", bg="#f0f0f0")
label_usuario_cadastro.pack(pady=(20, 5))  
entry_usuario_cadastro = tk.Entry(aba_cadastro)
entry_usuario_cadastro.pack(pady=(0, 20))  
label_senha_cadastro = tk.Label(aba_cadastro, text="Senha:", bg="#f0f0f0")
label_senha_cadastro.pack(pady=(20, 5))  
entry_senha_cadastro = tk.Entry(aba_cadastro, show="*")
entry_senha_cadastro.pack(pady=(0, 20))  

button_cadastrar = tk.Button(aba_cadastro, text="Cadastrar", command=cadastrar)
button_cadastrar.pack(pady=(20, 20))  

#login
label_usuario_login = tk.Label(aba_login, text="Usuário:", bg="#f0f0f0")
label_usuario_login.pack(pady=(20, 5))  
entry_usuario_login = tk.Entry(aba_login)
entry_usuario_login.pack(pady=(0, 20))  

label_senha_login = tk.Label(aba_login, text="Senha:", bg="#f0f0f0")
label_senha_login.pack(pady=(20, 5)) 
entry_senha_login = tk.Entry(aba_login, show="*")
entry_senha_login.pack(pady=(0, 20)) 

button_logar = tk.Button(aba_login, text="Login", command=logar)
button_logar.pack(pady=(20, 20)) 

root.mainloop()