import time
from win10toast import ToastNotifier
import struct
import numpy as np
import pyaudio as pa
from tkinter import *
from random import choice
import threading as th
import winsound as ws
from os import startfile

cont = 0
Limite = 0.5
on_of = 0
beep = 0

music_list = ['isolados.wav', 'jhonCena.wav','evilmorty.wav','saidafrente.wav','running.wav']
select_music = choice(music_list)

toaster = ToastNotifier()


##### MEDIDOR VOLUME #####

CHUNK = 2048 * 4
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz

p = pa.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
)


##### GUI para Iniciar #####

root = Tk()
root.title('O Vizinho')
root.iconbitmap('ninja.ico')

# Botoes de instrução

def sinal1():
    ws.Beep(5000, 200)
def sinal2():
    ws.Beep(5000, 1000)
def sinal_reset():
    ws.Beep(3000, 200)
    time.sleep(0.2)
    ws.Beep(3000, 200)
    time.sleep(0.2)
    ws.Beep(3000, 200)

# Funções para os botões principais

def close():
    root.destroy()

def countdown():
    global cont
    now = time.time()
    future = now + 60*20
    dif = int(future - now)
    while dif > 0:
        now = time.time()
        dif = int(future - now)
    ws.Beep(3000, 200)
    time.sleep(0.2)
    ws.Beep(3000, 200)
    time.sleep(0.2)
    ws.Beep(3000, 200)
    if cont > 5:
        cont = 0
        lb_bar1['bg'] = 'green'
        lb_bar2['bg'] = 'green'
        lb_bar3['bg'] = 'green'
    countdown()

def go():
    global cont
    global select_music
    global on_of
    global beep
    on_of = 1
    ##### NOTIFICAÇAO #####


    # Escutando
    while on_of ==1:
        bt_start['text'] = 'Escutando...'
        bt_start['command'] = running
        data = stream.read(CHUNK)
        dataInt = struct.unpack(str(CHUNK) + 'h', data)
        k = np.abs(np.fft.fft(dataInt)) * 2 / (11000 * CHUNK)
        Maximo = max(number for number in k)
        if (Maximo > Limite):  # ValorMaximo sendo o limite de volume escolhido
            print(Maximo, 'valor max')
            print(cont)
            print('--------------')
            cont = cont + 1
            if cont > 5:
                if cont <= 25:
                    lb_bar1['bg'] = 'red'
                    print('aviso 1')
                    if beep == 0:
                        ws.Beep(5000,200)
                        beep = beep + 1
                elif cont <= 45:
                    lb_bar2['bg'] = 'red'
                    print('aviso 2')
                    if beep == 1:
                        ws.Beep(5000, 1000)
                        beep = beep + 1
                else:
                    lb_bar3['bg'] = 'red'
                    toaster.show_toast(
                        "Volume elevado",
                        "Dica: diminua o volume dos fones",
                        icon_path='Volume.ico',
                        duration=5)
                    ws.PlaySound(select_music, ws.SND_FILENAME)
                    select_music = choice(music_list)
                    cont = 0
                    lb_bar1['bg'] = 'green'
                    lb_bar2['bg'] = 'green'
                    lb_bar3['bg'] = 'green'
                    beep = 0
                    time.sleep(5)

def instructions():
    top = Toplevel()
    top.geometry('300x145+560+240')
    top.title('Guia de funcionamento')

    startfile("Instruçoes.txt")

    bt_sinal = Button(top, text = 'Sinal de aviso 1', width=10, bg = '#f0f0f0', command = sinal1)
    bt_sina2 = Button(top, text='Sinal de aviso 2', width=10, bg='#f0f0f0', command=sinal2)
    bt_reset = Button(top, text='Sinal de aviso de reset', width=10, bg='#f0f0f0', command=sinal_reset)
    bt_sinal.pack(fill = X)
    bt_sina2.pack(fill = X)
    bt_reset.pack(fill = X)

def running():
    bt_start['text'] = 'Escutando...'

# root principal

root.geometry('300x138+560+240')  # geometry = ('LarguraxAltura+DistanciaEsquerdaMonitor+DistanciaTopoMonitor')
root['bg'] = '#B0C4DE'

## Threads

x = th.Thread(target=go, daemon=True)           # Medidor do volume
y = th.Thread(target=countdown, daemon=True)    # Timer para reset

## Dentro da root principal

# Botoes

bt_close = Button(root, width = 20, text = 'Fechar', command = close)                           # Botao fechar
bt_start = Button(root, width = 20, text = 'Iniciar', command=lambda:[x.start(),y.start()])     # Botao start
bt_inf = Button(root, width = 20, text = 'Informações', command = instructions)                 # Botao com informação

# Label
lb_bar1 = Label(root, text = '', width=10, bg = 'green')    # Barra de aviso 1
lb_bar2 = Label(root, text = '', width=10, bg = 'green')    # Barra de aviso 2
lb_bar3 = Label(root, text = '', width=10, bg = 'green')    # Barra de aviso 3

# Posição

bt_inf.pack(fill=X)

lb_bar3.pack(fill=X)
lb_bar2.pack(fill=X)
lb_bar1.pack(fill=X)

bt_start.pack(fill=X)

bt_close.pack(fill=X)

root.mainloop()
