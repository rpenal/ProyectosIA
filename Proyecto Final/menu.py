import tkinter 
import os
from tkinter import *
from tkinter.filedialog import askopenfile

def abrir_logico_1():
    os.system('python3 /home/jostos/Escritorio/IA-UNAL-2022-2/Proyecto_Final_IA/m_logico.py')
    ventana.destroy()

def abrir_logico_2():
    os.system('python3 /home/jostos/Escritorio/IA-UNAL-2022-2/Proyecto_Final_IA/metodo_logico/Metodo_2/nonogram_solver.py')




def metodos_logico():
    ventana.destroy()
    global ventana_metodos_logicos
    ventana_metodos_logicos = tkinter.Tk()
    ventana_metodos_logicos.geometry('500x500+400+80')
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
        command = archivo_logico_1)
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

def archivo_logico_1():
    ventana_metodos_logicos.destroy()
    ventana_archivo_logico_1 = tkinter.Tk()
    ventana_archivo_logico_1.geometry('500x500+400+80')
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
    ventana_archivo_logico_1.mainloop()

def cargar_archivo():
    buscar = tkinter.filedialog.askopenfilename(initialdir = '/home/jostos/Escritorio/IA-UNAL-2022-2/Proyecto_Final_IA/nonogramas')
    fob = open(buscar, 'r')
    global archivo
    archivo = fob.read()

ventana = tkinter.Tk()
fondo = tkinter.PhotoImage(file='Menu.png')
label1 = tkinter.Label(ventana, image=fondo)
label1.place(x=0,y=0)
ventana.geometry('500x500+400+80')
ventana.title('Nonogram Solver Menu')





boton_logica = tkinter.Button(text='CSP',        
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = metodos_logico)
boton_logica.place(x=225, y=280)

ventana.mainloop()

