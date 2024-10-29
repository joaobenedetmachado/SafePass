import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "vaultify"

DBconexao = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

cursor = DBconexao.cursor()

def cadastrar():
    usuario = entry_usuario_cadastro.get()
    senha = entry_senha_cadastro.get()
    
    if usuario and senha:
        comandoSQL = "Select * from users"
        cursor.execute(comandoSQL)
        resultado = cursor.fetchall()
        nome_existentes = [line[1] for line in resultado]
        if usuario not in nome_existentes:
          comandoSQL = f"Insert into users(nome, password) values('{usuario}', '{senha}')"
          cursor.execute(comandoSQL)
          DBconexao.commit()
          messagebox.showwarning("Cadastro", "Pronto! usuario cadastrado!")
        else:
          messagebox.showwarning("Cadastro", "Este nome ja possui no banco de dados, coloque outro!")
    else:
        messagebox.showwarning("Cadastro", "Por favor, preencha todos os campos.")

def logar():
    usuario = entry_usuario_login.get()
    senha = entry_senha_login.get()
    
    if usuario and senha:
        comandoSQL = f"SELECT * FROM users WHERE nome = '{usuario}' AND password = '{senha}'"
        cursor.execute(comandoSQL)
        resultado = cursor.fetchone()
        if resultado:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
        else:
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos.")
    else:
        messagebox.showwarning("Login", "Por favor, preencha todos os campos.")

root = tk.Tk()
root.title("Cadastro e Login")
root.geometry("800x600") 

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

aba_cadastro = ttk.Frame(notebook)
notebook.add(aba_cadastro, text='Cadastro')

label_usuario_cadastro = tk.Label(aba_cadastro, text="Usuário:")
label_usuario_cadastro.pack(pady=(20, 5)) 
entry_usuario_cadastro = tk.Entry(aba_cadastro)
entry_usuario_cadastro.pack(pady=(0, 20))  

label_senha_cadastro = tk.Label(aba_cadastro, text="Senha:")
label_senha_cadastro.pack(pady=(20, 5))  
entry_senha_cadastro = tk.Entry(aba_cadastro, show="*")
entry_senha_cadastro.pack(pady=(0, 20))  

button_cadastrar = tk.Button(aba_cadastro, text="Cadastrar", command=cadastrar)
button_cadastrar.pack(pady=(20, 20))  
# Criar a aba de login
aba_login = ttk.Frame(notebook)
notebook.add(aba_login, text='Login')

# Campos de login
label_usuario_login = tk.Label(aba_login, text="Usuário:")
label_usuario_login.pack(pady=(20, 5))  
entry_usuario_login = tk.Entry(aba_login)
entry_usuario_login.pack(pady=(0, 20))  

label_senha_login = tk.Label(aba_login, text="Senha:")
label_senha_login.pack(pady=(20, 5)) 
entry_senha_login = tk.Entry(aba_login, show="*")
entry_senha_login.pack(pady=(0, 20)) 

button_logar = tk.Button(aba_login, text="Login", command=logar)
button_logar.pack(pady=(20, 20)) 

root.mainloop()