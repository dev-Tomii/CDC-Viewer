import tkinter as tk
from tkinter import ttk
from functions import downloadClans, getClans, saveClans
from customclass import AutocompleteCombobox

colors = ['red', 'blue', 'yellow', 'green', 'black', 'white', 'orange', 'purple', 'brown', 'cyan', 'pink', 'teamred', 'teamyellow', 'teamblue', 'teampurple']

treeviewWd = None
clan = None
lider = None
colider = None
seasons = None
color = None
ctGold = None
ctSilver = None
ctBronze = None

# Variables
def loadVars(root):
    global treeviewWd
    global clan
    global lider
    global colider
    global seasons
    global color
    global ctGold
    global ctSilver
    global ctBronze
    clan = tk.StringVar(root)
    lider = tk.StringVar(root)
    colider = tk.StringVar(root)
    seasons = tk.IntVar(root)
    color = tk.StringVar(root)
    ctGold = tk.IntVar(root, value=0)
    ctSilver = tk.IntVar(root, value=0)
    ctBronze = tk.IntVar(root, value=0)

def generateTreeview(root):
    clans = getClans()
    global treeviewWd
    
    # Treeview
    clansFrame = ttk.LabelFrame(root, text='Jogadores', labelanchor='n')
    clansFrame.grid(columnspan=3, row=0, column=0, padx=10, pady=10)
    
    treeview = ttk.Treeview(clansFrame, columns=('lider', 'co-lider', 'seasons', 'ct', 'color'))
    treeviewWd = treeview
    treeview.heading("#0", text="Clã")
    treeview.heading("lider", text="Lider")
    treeview.heading("co-lider", text="Co-Lider")
    treeview.heading("seasons", text="Seasons")
    treeview.heading("ct", text="CTs")
    treeview.heading("color", text="Cor")
    treeview.grid(row=0, column=0, padx=(20,5), pady=20)
    treeview.bind('<ButtonRelease-1>', selectItem)
    
    treeScroll = ttk.Scrollbar(clansFrame, command=treeview.yview, orient=tk.VERTICAL)
    treeScroll.grid(row=0, column=1, pady=10, padx=(0,5), sticky='ns')
    treeview.configure(yscrollcommand=treeScroll.set)
    
    for i in clans:
        treeview.insert("", tk.END, text=i['clan'], values=(i['leader'], i['coleader'], i['seasons'], i['CT'],i['color']))

def generateInfo(root):
    loadVars(root)    
    infoFrame = ttk.LabelFrame(root, text='Informaçao', labelanchor='n')
    infoFrame.grid(row=1, column=0, pady=10, padx=10)

    cla = ttk.Entry(infoFrame, textvariable=clan)
    cla.grid(column=0, row=1, padx=10, pady=(5,10))
    claLabel = ttk.Label(infoFrame, text='Clã', justify=tk.CENTER, width=10)
    claLabel.grid(column=0, row=0, padx=(0, 40), pady=(20, 0))

    leader = ttk.Entry(infoFrame, textvariable=lider)
    leader.grid(column=1, row=1, padx=10, pady=(5,10))
    leaderLabel = ttk.Label(infoFrame, text='Lider', justify=tk.CENTER, width=10)
    leaderLabel.grid(column=1, row=0, padx=(0, 40), pady=(20, 0))

    colid = ttk.Entry(infoFrame, textvariable=colider)
    colid.grid(column=2, row=1, padx=10, pady=(5,10))
    colidLabel = ttk.Label(infoFrame, text='CoLider', justify=tk.CENTER, width=10)
    colidLabel.grid(column=2, row=0, padx=(0, 50), pady=(20, 0))

    seas = ttk.Entry(infoFrame, textvariable=seasons)
    seas.grid(column=0, row=3, padx=10, pady=(5,10))
    seasLabel = ttk.Label(infoFrame, text='Seasons', justify=tk.CENTER, width=10)
    seasLabel.grid(column=0, row=2, padx=(0, 40), pady=(20, 0))
    
    cor = AutocompleteCombobox(infoFrame, textvariable=color, values=colors)
    cor.set_completion_list(colors)
    cor.grid(column=1, row=3, padx=10, pady=(5,10))
    corLabel = ttk.Label(infoFrame, text='Cor', justify=tk.CENTER, width=10)
    corLabel.grid(column=1, row=2, padx=(0, 50), pady=(20, 0))
    
    gold = ttk.Entry(infoFrame, textvariable=ctGold, width=5)
    gold.grid(row=5, column=0, padx=2, pady=(5, 20))
    goldLabel = ttk.Label(infoFrame, text='CT Gold', justify=tk.CENTER, width=10)
    goldLabel.grid(row=4, column=0, padx=(20, 0), pady=(20, 0))
    bronze = ttk.Entry(infoFrame, textvariable=ctSilver, width=5)
    bronze.grid(row=5, column=1, padx=2, pady=(5, 20))
    bronLabel = ttk.Label(infoFrame, text='CT Silver', justify=tk.CENTER, width=10)
    bronLabel.grid(row=4, column=1, padx=(20, 0), pady=(20, 0))
    silver = ttk.Entry(infoFrame, textvariable=ctBronze, width=5)
    silver.grid(row=5, column=2, padx=2, pady=(5, 20))
    silverLabel = ttk.Label(infoFrame, text='CT Bronze', justify=tk.CENTER, width=10)
    silverLabel.grid(row=4, column=2, pady=(20, 0))

def generateButtons(root):
    # Player Buttons
    buttonFrame = ttk.LabelFrame(root, text='Ações do Player', labelanchor='n')
    buttonFrame.grid(row=1, column=1, padx=10, pady=10)

    saveButton = ttk.Button(buttonFrame, text='Salvar', style='Accent.TButton', width=20, command=updateClan)
    saveButton.grid(row=0, column=0, padx=20, pady=20)
    addButton = ttk.Button(buttonFrame, text='Adicionar', style='Accent.TButton', width=20, command=addClan)
    addButton.grid(row=1, column=0, padx=20, pady=20)
    deleteButton = ttk.Button(buttonFrame, text='Eliminar', style='Accent.TButton', width=20, command=deleteClan)
    deleteButton.grid(row=2, column=0, padx=20, pady=20)

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
    clan.set(c['text'])
    lider.set(c['values'][0])
    colider.set(c['values'][1])
    seasons.set(c['values'][2])
    ctGold.set(c['values'][3][0])
    ctSilver.set(c['values'][3][2])
    ctBronze.set(c['values'][3][4])
    color.set(c['values'][4])

def refreshTable():
    treeviewWd.delete(*treeviewWd.get_children())
    clans = getClans()
    for i in clans:
        treeviewWd.insert("", tk.END, text=i['clan'], values=(i['leader'], i['coleader'], i['seasons'], i['CT'],i['color']))
    treeviewWd.update()
    
def clearTable():
    treeviewWd.delete(*treeviewWd.get_children())
    treeviewWd.update()
    with open('./clans.json', 'w') as f:
        f.write('{}')
    
def updateTable():
    downloadClans()
    refreshTable()

def updateClan():
    item = treeviewWd.focus()
    treeviewWd.item(item, text=clan.get(), values=(lider.get(), colider.get(), seasons.get(), f'{ctGold.get()} {ctSilver.get()} {ctBronze.get()}', color.get()))
    treeviewWd.update()
    saveClans(treeviewWd)
    
def addClan():
    cla = {"CT": [int(ctGold.get()), ctSilver.get(), ctBronze.get()], "clan": f"{clan.get()}", "color": f'{color.get()}',"leader": f'{lider.get()}', "seasons": seasons.get(),"coleader": f"{colider.get()}"}
    treeviewWd.insert("", tk.END, text=cla['clan'], values=(cla['leader'], cla['coleader'], cla['seasons'], cla['CT'],cla['color']))
    clans = getClans()
    clans.append(cla)
    saveClans(treeviewWd)
    refreshTable()
    
def deleteClan():
    curItem = treeviewWd.focus()
    items = treeviewWd.get_children()
    i = items.index(curItem)
    treeviewWd.delete(curItem)
    clans = getClans()
    clans.pop(i)
    saveClans(treeviewWd)
    refreshTable()
###

def openClanWindow(root):
    newWindow = tk.Toplevel(root)
    newWindow.iconbitmap('./icon.ico')
    newWindow.title("Clans")
    newWindow.option_add("*tearOff", False)
    newWindow.resizable(False, False)
    generateTreeview(newWindow)
    generateInfo(newWindow)
    generateButtons(newWindow)

