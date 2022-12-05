import tkinter
import os
from tkinter import *
from tkinter.filedialog import askopenfile

def abrir_logico_1():
    os.system('metodo_logico_1.py')
    ventana_metodos_logicos.destroy()



def abrir_logico_2():
    os.system('metodo_logico_2.py')
    ventana_metodos_logicos.destroy()

def abrir_backtracking_1():
    os.system('enumerative_backtracking.py')
    ventana_metodos_backtracking.destroy()

def abrir_backtracking_2():
    os.system('backtracking_naive.py')
    ventana_metodos_backtracking.destroy()

def abrir_csp_1():
    os.system('csp.py')
    ventana_metodos_csp.destroy()

def abrir_csp_2():
    os.system('annealing.py')
    ventana_metodos_csp.destroy()

def metodos_logico():
    ventana_inicio.destroy()
    global ventana_metodos_logicos
    ventana_metodos_logicos = tkinter.Tk()
    ventana_metodos_logicos.geometry('500x500+700+250')
    ventana_metodos_logicos.title('Metodos Logicos')
    fondo_metodos_logico = tkinter.PhotoImage(file='Menu.png')
    fondo_ub_metodos_logico = tkinter.Label(ventana_metodos_logicos,image=fondo_metodos_logico)
    fondo_ub_metodos_logico.place(x=0,y=0)

    boton_metodo_1 = tkinter.Button(ventana_metodos_logicos, text='Metodo 1',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = abrir_logico_1)
    boton_metodo_1.place(x=200, y=270)

    boton_metodo_2 = tkinter.Button(ventana_metodos_logicos,text='Metodo 2',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = abrir_logico_2)
    boton_metodo_2.place(x=200, y=300)

    ventana_metodos_logicos.mainloop()


def metodos_backtracking():
    ventana_inicio.destroy()
    global ventana_metodos_backtracking
    ventana_metodos_backtracking = tkinter.Tk()
    ventana_metodos_backtracking.geometry('500x500+700+250')
    ventana_metodos_backtracking.title('Metodos Logicos')
    fondo_metodos_logico = tkinter.PhotoImage(file='Menu.png')
    fondo_ub_metodos_logico = tkinter.Label(ventana_metodos_backtracking,image=fondo_metodos_logico)
    fondo_ub_metodos_logico.place(x=0,y=0)

    boton_metodo_1 = tkinter.Button(ventana_metodos_backtracking, text='Metodo 1',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = abrir_backtracking_2)
    boton_metodo_1.place(x=200, y=270)

    boton_metodo_2 = tkinter.Button(ventana_metodos_backtracking,text='Metodo 2',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = abrir_backtracking_1)
    boton_metodo_2.place(x=200, y=300)

    ventana_metodos_backtracking.mainloop()

def metodos_csp():
    ventana_inicio.destroy()
    global ventana_metodos_csp
    ventana_metodos_csp = tkinter.Tk()
    ventana_metodos_csp.geometry('500x500+700+250')
    ventana_metodos_csp.title('Metodos Logicos')
    fondo_metodos_logico = tkinter.PhotoImage(file='Menu.png')
    fondo_ub_metodos_logico = tkinter.Label(ventana_metodos_csp,image=fondo_metodos_logico)
    fondo_ub_metodos_logico.place(x=0,y=0)

    boton_metodo_1 = tkinter.Button(ventana_metodos_csp, text='Metodo 1',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = abrir_csp_1)
    boton_metodo_1.place(x=200, y=270)

    boton_metodo_2 = tkinter.Button(ventana_metodos_csp,text='Metodo 2',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = abrir_csp_2)
    boton_metodo_2.place(x=200, y=300)

    ventana_metodos_csp.mainloop()

def archivo_logico_1():
    ventana_metodos_logicos.destroy()
    global ventana_archivo_logico_1
    ventana_archivo_logico_1 = tkinter.Tk()
    ventana_archivo_logico_1.geometry('500x500+700+250')
    ventana_archivo_logico_1.title('Metodos Logicos')
    fondo_archivo_logico_1 = tkinter.PhotoImage(file='Menu.png')
    fondo_ub_archivo_logico_1 = tkinter.Label(ventana_archivo_logico_1,image=fondo_archivo_logico_1)
    fondo_ub_archivo_logico_1.place(x=0,y=0)
    boton_archivo = tkinter.Button(text='Cargar Archivo',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = cargar_archivo)
    boton_archivo.place(x=225, y=230)

    boton_iniciar = tkinter.Button(text='Iniciar',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = abrir_logico_1)
    boton_iniciar.place(x=225, y=290)

    boton_volver = tkinter.Button(text='Volver',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = inicio)
    boton_volver.place(x=225, y=260)
    ventana_archivo_logico_1.mainloop()

def cargar_archivo():
    buscar = tkinter.filedialog.askopenfilename(initialdir = 'nonogramas')
    fob = open(buscar, 'r')
    global archivo
    archivo = fob.read()



def inicio():
    ventana.destroy()
    global ventana_inicio
    ventana_inicio = tkinter.Tk()
    ventana_inicio.geometry('500x500+700+250')
    ventana_inicio.title('Metodos Logicos')
    fondo_inicio = tkinter.PhotoImage(file='Menu.png')
    fondo_ub_inicio = tkinter.Label(ventana_inicio,image=fondo_inicio)
    fondo_ub_inicio.place(x=0,y=0)

    boton_logica = tkinter.Button(text='Metodos Logicos',
            font='Bodoni',
            cursor='hand2',
            relief='flat',
            bg = '#ffffff',
            highlightbackground='white',
            highlightthickness=2,
            command = metodos_logico)
    boton_logica.place(x=150, y=250)


    boton_csp = tkinter.Button(text='Metodo CSP',
            font='Bodoni',
            cursor='hand2',
            relief='flat',
            bg = '#ffffff',
            highlightbackground='white',
            highlightthickness=2,
            command = metodos_csp
            )
    boton_csp.place(x=150, y=280)

    boton_backtracking = tkinter.Button(text='Metodos Backtracking',
            font='Bodoni',
            cursor='hand2',
            relief='flat',
            bg = '#ffffff',
            highlightbackground='white',
            highlightthickness=2,
            command = metodos_backtracking
            )
    boton_backtracking.place(x=150, y=310)
    ventana_inicio.mainloop()


ventana = tkinter.Tk()
fondo = tkinter.PhotoImage(file='Inicio.png')
label1 = tkinter.Label(ventana, image=fondo)
label1.place(x=0,y=0)
ventana.geometry('500x500+700+250')
ventana.title('Nonogram Solver Menu')
boton_continuar = tkinter.Button(text='Empezar',
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = inicio)

boton_continuar.place(x=390, y=450)
ventana.mainloop()



