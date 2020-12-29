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

def insert_password(service, user, password):
    cursor.execute(f'''
            INSERT INTO users (service, username, password)
            VALUES ('{service}', '{user}', {password})
    ''')
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
        window.exit()
        
def layout():
    layout = [
        [sg.Text('Serviço '), sg.Input('', size = (25,1), key = '-SERVICE-')],
        [sg.Text('Usúario'), sg.Input('', size = (25,1), key = '-USER-')],
        [sg.Text('Senha  '), sg.Input('', size = (25,1), key = '-PASSWORD-')],
        [sg.Button('Enviar')],
        [sg.Text('═────────────◇────────────═')],
        [sg.Text('Serviços salvos')],
        [sg.Listbox('SERVIÇOS', size = (32,15), key = '-BOX-')],
        [sg.Button('Sair')]
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

            window.find_element('-SERVICE-').Update('')
            window.find_element('-USER-').Update('')
            window.find_element('-PASSWORD-').Update('')
        if button == 'Sair':
            window.exit()
        if WIN_CLOSED:
            break

front()