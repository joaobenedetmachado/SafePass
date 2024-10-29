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

root = tk.Tk()
root.title("Cadastro e Login")
root.geometry("800x600") 

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)
print(notebook)

aba_login = ttk.Frame(notebook)
notebook.add(aba_login, text='Login')

aba_senhas = ttk.Frame(notebook)


aba_cadastro = ttk.Frame(notebook)
notebook.add(aba_cadastro, text='Cadastro')

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
    usuario = entry_usuario_login.get() # pega o valor do user e senha
    senha = entry_senha_login.get()
    
    if usuario and senha:
        comandoSQL = f"SELECT * FROM users WHERE nome = '{usuario}' AND password = '{senha}'" # faz e checagem
        cursor.execute(comandoSQL)
        resultado = cursor.fetchone()
        if resultado:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            afterLogin(usuario)
        else:
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos.") # caso de errado ele mostra
    else:
        messagebox.showwarning("Login", "Por favor, preencha todos os campos.")

def afterLogin(usuario): # ele tira as abas de login e cadastro
  notebook.forget(aba_cadastro)
  notebook.forget(aba_login)
  aba_senhas = ttk.Frame(notebook) 
  notebook.add(aba_senhas, text='Senhas')
  text_area = tk.Text(aba_senhas, height=10, width=40)
  text_area.pack(pady=20)
  text_area.config(state='normal')  

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
              print(senha[0])  
              text_area.insert(tk.END, f"{senha[0]}\n")  # inseri a senha no caixa
      else:
          text_area.insert(tk.END, "Nenhuma senha encontrada.")  # se nao tiver senha ele mostra dai ne

  text_area.config(state='disabled')
  button_criarNovaSenha = tk.Button(aba_senhas, text="Cadastrar Nova Senha", command=cadastrarNovaSenha(usuario))
  button_criarNovaSenha.pack(pady=(20, 20)) # desabilita pra q o user nao mexa mais


def cadastrarNovaSenha(usuario):
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
  password = entry_senha.get()
  siteName = entry_sitename.get()
  print(usuario)
  
  

# area do cadastro
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

# area de cadastro
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