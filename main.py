import tkinter as tk
from tkinter import ttk
from customclass import AutocompleteCombobox
import sv_ttk

from functions import getPlayers, savePlayer, verifyDB, downloadPlayers, getClansValues, getLegendsValues
from clans import openClanWindow
from lendas import openLegendWindow
verifyDB()

ranks = ['Lider', 'Co-Lider', 'Membro']

root = tk.Tk()
root.iconbitmap('./icon.ico')
root.title("CDC Viewer")
root.option_add("*tearOff", False)
root.resizable(False, False)
sv_ttk.set_theme('dark')

# Variables
name = tk.StringVar()
cost = tk.IntVar()
clan = tk.StringVar()
rank = tk.StringVar()
legend = tk.StringVar()

# Functions
players = getPlayers()['jogadores']

def updateValues():
    cla.configure(values=getClansValues())
    lenda.configure(values=getLegendsValues())
    
def clearTable():
    treeview.delete(*treeview.get_children())
    treeview.update()
    with open('./players.json', 'w') as f:
        f.write('{}')
    
def refreshTable():
    treeview.delete(*treeview.get_children())
    players = getPlayers()['jogadores']
    for i in players:
        treeview.insert("", tk.END, text=i['nome'], values=(i['custo'], i['clan'], i['hierarquia'], i['lenda']))
    treeview.update()
        
def selectItem(e):
    curItem = treeview.focus()
    p = treeview.item(curItem)
    name.set(p['text'])
    cost.set(p['values'][0])
    clan.set(p['values'][1])
    rank.set(p['values'][2])
    legend.set(p['values'][3])
    
def updatePlayer():
    item = treeview.focus()
    treeview.item(item, text=name.get(), values=(cost.get(), clan.get(), rank.get(), legend.get()))
    treeview.update()
    savePlayer(treeview)
    refreshTable()
    
def addPlayer():
    player = {"nome": name.get(), "hierarquia": rank.get(), "custo": cost.get(), "clan": clan.get(), "lenda": legend.get()}
    treeview.insert("", tk.END, text=player['nome'], values=(player['custo'], player['clan'], player['hierarquia'], player['lenda']))
    players = getPlayers()['jogadores']
    players.append(player)
    savePlayer(treeview)
    refreshTable()
    
def deletePlayer():
    curItem = treeview.focus()
    items = treeview.get_children()
    i = items.index(curItem)
    treeview.delete(curItem)
    players = getPlayers()['jogadores']
    players.pop(i)
    savePlayer(treeview)
    refreshTable()
    
def updateTable():
    downloadPlayers()
    updateValues()
    refreshTable()

# Treeview
playersFrame = ttk.LabelFrame(root, text='Jogadores', labelanchor='n')
playersFrame.grid(columnspan=3, row=0, column=0, padx=10, pady=10)

treeview = ttk.Treeview(playersFrame, columns=('cost', 'clan', 'rank', 'legend'))
treeview.heading("#0", text="Nome")
treeview.heading("cost", text="Custo")
treeview.heading("clan", text="Clan")
treeview.heading("rank", text="Hierarquia")
treeview.heading("legend", text="Lenda")

treeview.bind('<ButtonRelease-1>', selectItem)

for i in players:
    treeview.insert("", tk.END, text=i['nome'], values=(i['custo'], i['clan'], i['hierarquia'], i['lenda']))
treeview.grid(row=0, column=0, padx=(10, 0), pady=10)
treeScroll = ttk.Scrollbar(playersFrame, command=treeview.yview, orient=tk.VERTICAL)
treeScroll.grid(row=0, column=1, pady=10, padx=5, sticky='ns')
treeview.configure(yscrollcommand=treeScroll.set)

#Player Info
infoFrame = ttk.LabelFrame(root, text='Informaçao', labelanchor='n')
infoFrame.grid(row=1, column=0, pady=10, padx=10)

nome = ttk.Entry(infoFrame, textvariable=name)
nome.grid(column=0, row=1, padx=(20,5), pady=5)
nomeLabel = ttk.Label(infoFrame, text='Nome', justify=tk.LEFT, width=20)
nomeLabel.grid(column=0, row=0, padx=(20,5), pady=(10, 0))

custo = ttk.Entry(infoFrame, textvariable=cost)
custo.grid(column=1, row=1, padx=(5,20), pady=5)
custoLabel = ttk.Label(infoFrame, text='Custo', justify=tk.LEFT, width=20)
custoLabel.grid(column=1, row=0, padx=(5,10), pady=(10, 0))

cla = AutocompleteCombobox(infoFrame, textvariable=clan, width=16, values=getClansValues())
cla.set_completion_list(getClansValues())
cla.grid(column=0, row=3, padx=(20,5), pady=5)
claLabel = ttk.Label(infoFrame, text='Clã', justify=tk.LEFT, width=20)
claLabel.grid(column=0, row=2, padx=(10,5), pady=(5, 0))

hierarquia = AutocompleteCombobox(infoFrame, textvariable=rank, width=16, values=ranks)
hierarquia.set_completion_list(ranks)
hierarquia.grid(column=1, row=3, padx=(5,20), pady=5)
hierarquiaLabel = ttk.Label(infoFrame, text='Hierarquia', justify=tk.LEFT, width=20)
hierarquiaLabel.grid(column=1, row=2, padx=(5,10), pady=(5, 0))

lenda = AutocompleteCombobox(infoFrame, textvariable=legend, width=16, values=getLegendsValues())
lenda.set_completion_list(getLegendsValues())
lenda.grid(columnspan=2, column=0, row=5, padx=20, pady=(5, 20))
lendaLabel = ttk.Label(infoFrame, text='Lenda', justify=tk.LEFT, width=20)
lendaLabel.grid(columnspan=2, column=0, row=4, padx=5, pady=(5, 0))

# Player Buttons
buttonFrame = ttk.LabelFrame(root, text='Ações do Player', labelanchor='n')
buttonFrame.grid(row=1, column=1, padx=10, pady=10)

saveButton = ttk.Button(buttonFrame, text='Salvar', style='Accent.TButton', width=20, command=updatePlayer)
saveButton.grid(row=0, column=0, padx=20, pady=20)
saveButton = ttk.Button(buttonFrame, text='Adicionar', style='Accent.TButton', width=20, command=addPlayer)
saveButton.grid(row=1, column=0, padx=20, pady=20)
deleteButton = ttk.Button(buttonFrame, text='Eliminar', style='Accent.TButton', width=20, command=deletePlayer)
deleteButton.grid(row=2, column=0, padx=20, pady=20)

# Buttons
dbFrame = ttk.LabelFrame(root, text='Ações da DB', labelanchor='n')
dbFrame.grid(row=1, column=2, padx=10, pady=10)

clanButton = ttk.Button(dbFrame, text='Clas', width=20, command= lambda x=root: openClanWindow(x))
clanButton.grid(row=0, column=0, padx=20, pady=(20, 10))
legendsButton = ttk.Button(dbFrame, text='Lendas', width=20, command= lambda x=root: openLegendWindow(x))
legendsButton.grid(row=1, column=0, padx=20, pady=10)
resetButton = ttk.Button(dbFrame, text='Clear', width=20, command=clearTable)
resetButton.grid(row=2, column=0, padx=20, pady=10)
updateButton = ttk.Button(dbFrame, text='Atualizar', width=20, command=updateTable)
updateButton.grid(row=3, column=0, padx=20, pady=(10, 20))

root.mainloop()