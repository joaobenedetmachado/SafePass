import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import encrypt as enc

# Configurações do banco de dados
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "vaultify"

# Conexão com o banco de dados
DBconexao = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

cursor = DBconexao.cursor()

# Criação da janela principal
root = tk.Tk()
root.title("Cadastro e Login")
root.geometry("400x400")
root.configure(bg="#f0f0f0")  # Cor de fundo

# Estilização do notebook
style = ttk.Style()
style.configure("TNotebook", borderwidth=5)
style.configure("TNotebook.Tab", padding=[10, 5])  # Ajuste de padding para as abas

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both', padx=20)  # Adicionado fill='both' e padx

# Criando as abas com tamanho específico
aba_login = ttk.Frame(notebook, width=360, height=360)  # Define tamanho específico
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

# Função após login
def afterLogin(usuario):
    notebook.forget(aba_cadastro)
    notebook.forget(aba_login)
    
    aba_senhas = ttk.Frame(notebook) 
    notebook.add(aba_senhas, text='Senhas')
    
    text_area = tk.Text(aba_senhas, height=10, width=40, bg="#ffffff", bd=3, relief="sunken", wrap=tk.WORD)
    text_area.pack(pady=20)
    text_area.config(state='normal')  
    root.title(f"Conectado como: {usuario}")

    comandoSQL = f"SELECT idusers FROM users WHERE nome = '{usuario}'"
    cursor.execute(comandoSQL)
    resultado = cursor.fetchone()

    if resultado:
        iduser = resultado[0]
        comandoSQL = f"SELECT passwordhash FROM passwords WHERE userid = {iduser}"
        cursor.execute(comandoSQL)
        resultadoSenhas = cursor.fetchall()
        text_area.delete(1.0, tk.END)
        if resultadoSenhas: 
            for senha in resultadoSenhas:
                senhaEncriptografada = senha[0]
                text_area.insert(tk.END, f"{enc.descriptografar(senhaEncriptografada)}\n")
        else:
            text_area.insert(tk.END, "Nenhuma senha encontrada.")

    text_area.config(state='disabled')
    button_criarNovaSenha = tk.Button(aba_senhas, text="Cadastrar Nova Senha", command=lambda: cadastrarNovaSenhaArea(iduser))
    button_criarNovaSenha.pack(pady=(20, 20))

# Função para cadastrar nova senha
def cadastrarNovaSenhaArea(iduser):
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
    button_criarNovaSenha = tk.Button(janelaCriarSenha, text="Cadastrar Nova Senha", command=lambda: CadastrarNovaSenha(janelaCriarSenha, iduser, enc.criptografar(entry_senha.get()), entry_sitename.get()))
    button_criarNovaSenha.pack(pady=(20, 20))

def CadastrarNovaSenha(janelaCriarSenha, iduser, password, siteName):
    comandoSQL = f'INSERT INTO passwords(userid, passwordhash, sitename) VALUES({iduser}, "{password}", "{siteName}")'
    cursor.execute(comandoSQL)
    DBconexao.commit()
    print("Senha cadastrada")
    janelaCriarSenha.destroy()

# Área de cadastro
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

# Área de login
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

# Iniciar o loop principal
root.mainloop()
