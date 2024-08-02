import tkinter as tk
from tkinter import ttk
from functions import downloadLegends, getLegends, saveLegends
from customclass import AutocompleteCombobox

treeviewWd = None
lenda = None
thumbnail = None

# Variables
def loadVars(root):
    global treeviewWd
    global lenda
    global thumbnail
    lenda = tk.StringVar(root)
    thumbnail = tk.StringVar(root)

def generateTreeview(root):
    lendas = sorted(getLegends(), key=lambda x: x['legend_name_key'])
    global treeviewWd
    
    # Treeview
    clansFrame = ttk.LabelFrame(root, text='Lendas', labelanchor='n')
    clansFrame.grid(columnspan=3, row=0, column=0, padx=10, pady=10)
    
    treeview = ttk.Treeview(clansFrame, columns=('thumbnail'))
    treeviewWd = treeview
    treeview.heading("#0", text="Lenda")
    treeview.heading("thumbnail", text="Thumbnail")
    treeview.column("thumbnail", stretch=tk.YES, width=600)
    
    treeview.grid(row=0, column=0, padx=(20,5), pady=20)
    treeview.bind('<ButtonRelease-1>', selectItem)
    
    treeScroll = ttk.Scrollbar(clansFrame, command=treeview.yview, orient=tk.VERTICAL)
    treeScroll.grid(row=0, column=1, pady=10, padx=(0,5), sticky='ns')
    treeview.configure(yscrollcommand=treeScroll.set)
    
    for i in lendas:
        treeview.insert("", tk.END, text=i['legend_name_key'], values=(i['thumbnail']))

def generateInfo(root):
    loadVars(root)    
    infoFrame = ttk.LabelFrame(root, text='Informaçao', labelanchor='n')
    infoFrame.grid(row=1, column=0, pady=10, padx=10)

    legend = ttk.Entry(infoFrame, textvariable=lenda, width=50)
    legend.grid(column=0, row=1, padx=10, pady=5)
    LendaLabel = ttk.Label(infoFrame, text='Lenda', justify=tk.LEFT, width=30)
    LendaLabel.grid(column=0, row=0, padx=(0, 50), pady=(10, 0))

    thumb = ttk.Entry(infoFrame, textvariable=thumbnail, width=50)
    thumb.grid(columnspan=2 ,column=0, row=3, padx=10, pady=(5,10))
    thumbLabel = ttk.Label(infoFrame, text='Thumbnail URL', justify=tk.LEFT, width=30)
    thumbLabel.grid(columnspan=2, column=0, row=2, padx=(0, 50), pady=(5, 0))


def generateButtons(root):
    # Legend Buttons
    buttonFrame = ttk.LabelFrame(root, text='Ações da Lenda', labelanchor='n')
    buttonFrame.grid(row=1, column=1, padx=10, pady=10)

    saveButton = ttk.Button(buttonFrame, text='Salvar', style='Accent.TButton', width=20, command=updateLegend)
    saveButton.grid(row=0, column=0, padx=20, pady=(10,5))
    addButton = ttk.Button(buttonFrame, text='Adicionar', style='Accent.TButton', width=20, command=addLegend)
    addButton.grid(row=1, column=0, padx=20, pady=5)
    deleteButton = ttk.Button(buttonFrame, text='Eliminar', style='Accent.TButton', width=20, command=deleteLegend)
    deleteButton.grid(row=2, column=0, padx=20, pady=(5, 10))

    # Buttons
    dbFrame = ttk.LabelFrame(root, text='Ações da DB', labelanchor='n')
    dbFrame.grid(row=1, column=2, padx=10, pady=10)

    resetButton = ttk.Button(dbFrame, text='Reset', width=20, command=clearTable)
    resetButton.grid(row=2, column=0, padx=20, pady=10)
    updateButton = ttk.Button(dbFrame, text='Atualizar', width=20, command=updateTable)
    updateButton.grid(row=3, column=0, padx=20, pady=(10, 20))

# Functions
def selectItem(e):
    curItem = treeviewWd.focus()
    c = treeviewWd.item(curItem)
    lenda.set(c['text'])
    thumbnail.set(c['values'][0])

def refreshTable():
    treeviewWd.delete(*treeviewWd.get_children())
    clans = getLegends()
    for i in clans:
        treeviewWd.insert("", tk.END, text=i['legend_name_key'], values=(i['thumbnail']))
    treeviewWd.update()
    
def clearTable():
    treeviewWd.delete(*treeviewWd.get_children())
    treeviewWd.update()
    with open('./legends.json', 'w') as f:
        f.write('{}')
    
def updateTable():
    downloadLegends()
    refreshTable()

def updateLegend():
    item = treeviewWd.focus()
    treeviewWd.item(item, text=lenda.get(), values=(thumbnail.get()))
    treeviewWd.update()
    saveLegends(treeviewWd)
    
def addLegend():
    legend = {"thumbnail": thumbnail.get(), "legend_name_key": lenda.get()}
    treeviewWd.insert("", tk.END, text=legend['legend_name_key'], values=(legend['thumbnail']))
    lendas = getLegends()
    lendas.append(legend)
    saveLegends(treeviewWd)
    refreshTable()
    
def deleteLegend():
    curItem = treeviewWd.focus()
    items = treeviewWd.get_children()
    i = items.index(curItem)
    treeviewWd.delete(curItem)
    lendas = getLegends()
    lendas.pop(i)
    saveLegends(treeviewWd)
    refreshTable()
###

def openLegendWindow(root):
    newWindow = tk.Toplevel(root)
    newWindow.iconbitmap('./icon.ico')
    newWindow.title("Legends")
    newWindow.option_add("*tearOff", False)
    newWindow.resizable(False, False)
    generateTreeview(newWindow)
    generateInfo(newWindow)
    generateButtons(newWindow)

