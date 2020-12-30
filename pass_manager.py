from sqlite3.dbapi2 import Cursor
import PySimpleGUI as sg
import sqlite3
from PySimpleGUI.PySimpleGUI import Button, Popup, WIN_CLOSED

sg.theme('random')
master_pass = '123'

conn = sqlite3.connect('Password.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
''')

def read_task():
    cursor.execute('''SELECT service FROM users''')
    data = cursor.fetchall()
    conn.commit()
    return data

def insert_password(service, user, password):
    cursor.execute(f'''
            INSERT INTO users (service, username, password)
            VALUES ('{service}', '{user}', '{password}')
    ''')
    conn.commit()

def delete(x):
    cursor.execute('''
        DELETE FROM users WHERE service = ?''', x)
    conn.commit()

def show_services():
    cursor.execute('''
            SELECT service FROM users;
    ''')
    for service, user, password in cursor.fetchall():
        print(service, user, password)

def front():
    flayout = [
        [sg.Text('Digite sua senha:')],
        [sg.Input('', key= '-PASS-'), sg.Button('Entrar'), sg.Button('Sair')]
    ]

    window = sg.Window('Passwords Manager', flayout, size=(500, 100),
    element_justification= ('center'))
    button, values = window.Read()
    if values['-PASS-'] != master_pass and button == 'Entrar':
        sg.Popup('Senha Incorreta')
        window.close()
        front()
    elif values['-PASS-'] == master_pass and button == 'Entrar':
        window.close()
        layout()
    elif button == 'Sair':
        window.close(); del window
        
def layout():
    service = read_task()
    layout = [
        [sg.Text('Serviço '), sg.Input('', size = (25,1), key = '-SERVICE-')],
        [sg.Text('Usúario'), sg.Input('', size = (25,1), key = '-USER-')],
        [sg.Text('Senha  '), sg.Input('', size = (25,1), key = '-PASSWORD-')],
        [sg.Button('Enviar')],
        [sg.Text('═────────────◇────────────═')],
        [sg.Text('Serviços salvos')],
        [sg.Listbox(service , size = (32,15), key = '-BOX-')],
        [sg.Button('Deletar'), sg.Text('\t  \t'),sg.Button('Sair')]
    ]

    window = sg.Window('Password Manager', layout, finalize= True)
    while True:
        button, values = window.Read()
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

        if button == 'Deletar':
            try:
                if service:
                    x = values['-BOX-'][0]
                    delete(x)
                    service = read_task()
                    window.find_element('-BOX-').Update(service)
            except IndexError:
                Popup('Nenhum serviço selecionado')

        if button == 'Sair':
            break
        if button == sg.WIN_CLOSED:
            break
        

front()