import os
import tkinter
from tkinter.filedialog import askopenfile

def cargar_archivo():
    buscar = tkinter.filedialog.askopenfilename(initialdir = '/home/jostos/Escritorio/IA-UNAL-2022-2/Proyecto_Final_IA/nonogramas')
    fob = open(buscar, 'r')
    global archivo
    archivo = fob.read()
    ventana.destroy()


ventana = tkinter.Tk()
fondo = tkinter.PhotoImage(file='Menu.png')
label1 = tkinter.Label(ventana, image=fondo)
label1.place(x=0,y=0)
ventana.geometry('500x500+700+250')
ventana.title('Nonogram Solver: Cargar archivo')
boton_continuar = tkinter.Button(text='Cargar Archivo',        
        font='Bodoni',
        cursor='hand2',
        relief='flat',
        bg = '#ffffff',
        highlightbackground='white',
        highlightthickness=2,
        command = cargar_archivo)
boton_continuar.place(x=175, y=250)
ventana.mainloop()

a = str(archivo)
b = a.split()
rows, cols,temp = [], [], []

count = 0
firstlen = 0
for lst in b:
    elems = lst.split(",")
    if firstlen == 0:
        firstlen = len(elems)
    if len(elems) < firstlen:
        rows.append(elems)
    else:
        temp.append(elems)



for j in range(firstlen):
    k = []
    for i in range(len(temp)):
        k.append(temp[i][j])
    cols.append(k)


for lst in rows:
    while '' in lst:
        lst.remove('')
for lst in cols:
    while '' in lst:
        lst.remove('')

for i in range(len(rows)):
    rows[i] = [int(a) for a in rows[i]]

for i in range(len(cols)):
    cols[i] = [int(a) for a in cols[i]]


