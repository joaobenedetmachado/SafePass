import tkinter as tk
from tkinter import ttk, messagebox

def cadastrar():
    usuario = entry_usuario_cadastro.get()
    senha = entry_senha_cadastro.get()
    
    if usuario and senha:
        messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
    else:
        messagebox.showwarning("Cadastro", "Por favor, preencha todos os campos.")

def logar():
    usuario = entry_usuario_login.get()
    senha = entry_senha_login.get()
    
    if usuario == "usuario_exemplo" and senha == "senha_exemplo": 
        messagebox.showinfo("Login", "Login realizado com sucesso!")
    else:
        messagebox.showwarning("Login", "Usuário ou senha incorretos.")

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