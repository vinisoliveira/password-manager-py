from sqlite3.dbapi2 import Cursor
import PySimpleGUI as sg
import sqlite3
from PySimpleGUI.PySimpleGUI import Button, Popup, WIN_CLOSED

sg.theme('random')
master_pass = '123'

#CONEXÃO COM O BANCO DE DADOS
conn = sqlite3.connect('Password.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
''')

#EXIBIR OS SERVIÇOS NA LISTBOX
def read_task():
    cursor.execute('''SELECT service FROM users''')
    data = cursor.fetchall()
    conn.commit()
    return data

#FUNÇÃO PARA INSERIR OS DADOS NO BANCO DE DADOS
def insert_password(service, user, password):
    cursor.execute(f'''
            INSERT INTO users (service, username, password)
            VALUES ('{service}', '{user}', '{password}')
    ''')
    conn.commit()

#FUNÇÃO QUE DELETA UM SERVIÇO
def delete(x):
    cursor.execute('''
        DELETE FROM users WHERE service = ?''', x)
    conn.commit()

#VOU TENTAR ENCAIXAR ESSA FUNÇÃO PARA QUE O USUÁRIO CONSIGA RECUPERAR UMA SENHA
def show_services():
    cursor.execute('''
            SELECT service, username, password FROM users;
    ''')
    for service, user, password in cursor.fetchall():
        print(service, user, password)

#TELA INICIAL DO PROGRAMA(ENTRADA DA SENHA)
def front():
    flayout = [
        [sg.Text('Digite sua senha:')],
        [sg.Input('', key= '-PASS-'), sg.Button('Entrar'), sg.Button('Sair')],
        [sg.Text('Tema'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')]
    ]

    window = sg.Window('Passwords Manager', flayout, size=(500, 100),
    element_justification= ('center'))
    button, values = window.Read()
    if values['-PASS-'] != master_pass and button == 'Entrar':
        sg.popup_error('Senha Incorreta')
        window.close()
        front()
    elif values['-PASS-'] == master_pass and button == 'Entrar':
        window.close()
        layout()
    elif button == 'Sair':
        window.close(); del window
        
 #TELA DE INTERAÇÃO COM O PROGRAMA(REGISTRO E EXCLUSÃO DE DADOS)
def layout():
    sg.theme('values.["-THEME-"]')
    service = read_task()
    layout = [
        [sg.Text('Serviço '), sg.Input('', size = (25,1), key = '-SERVICE-')],
        [sg.Text('Usúario'), sg.Input('', size = (25,1), key = '-USER-')],
        [sg.Text('Senha  '), sg.Input('', size = (25,1), key = '-PASSWORD-')],
        [sg.Button('Enviar')],
        [sg.Text('═────────────◇────────────═')],
        [sg.Text('Serviços salvos')],
        [sg.Listbox(service , size = (32,15), key = '-BOX-')],
        [sg.Button('Deletar'), sg.Button('Recuperar'),sg.Text('\t'),sg.Button('Sair')]

    ]

    window = sg.Window('Password Manager', layout, finalize= True)
    while True:
        button, values = window.Read(timeout=100)
        if button == 'Enviar':
            service = values['-SERVICE-']
            user = values['-USER-']
            password = values['-PASSWORD-']
            if service and user and password != '':
                insert_password(service, user, password)

            service = read_task()

            window.find_element('-SERVICE-').Update('')
            window.find_element('-USER-').Update('')
            window.find_element('-PASSWORD-').Update('')
            window.find_element('-BOX-').Update(service)
        
        if button == 'Recuperar':
            show_services()
            

        if button == 'Deletar':
             #AINDA PRECISA FAZER COM QUE ESSA MENSAGEM DE CONFIRMAÇÃO FUNCIONE COMO DEVERIA   
            sg.popup_yes_no('Tem Certeza?') #ESTOU PROCURANDO NA DOCUMENTAÇÃO DO PSG COMO FAZER ISSO 
            try:
                if service:
                    x = values['-BOX-'][0]
                    delete(x)
                    service = read_task()
                    window.find_element('-BOX-').Update(service)
            except IndexError:
                Popup('Nenhum serviço selecionado')

        if button == 'Sair' or button == sg.WIN_CLOSED:
           break


front()