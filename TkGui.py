import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import Main

def addcard(*args):
    tree.insert('', 'end', 'new')
    tree.focus('new')
    tree.selection_set('new')
    cardname.set("")
    setname.set("")
    cardquantity.set('0')

def savecard(*args):
    if tree.focus()=='new':
        tree.delete('new')
        newcard = Main.CardDB(name.get(), mtgset.get(), [Main.Color.G], quantity.get())
        Main.addtoDB(newcard)
        Main.saveDB()
        tree.insert('', 'end', newcard.getDBid(), text=newcard.name, values = (newcard.set,quantity.get(),newcard.price))
        Main.checkpic(newcard.getDBid())
        tree.selection_set(newcard.getDBid())
    else:
        tree.set(tree.selection()[0], 'quantity', cardquantity.get())
        Main.DB[tree.selection()[0]].quantity = cardquantity.get()
        Main.saveDB()

def delete(*args):
    if tree.selection()[0] != 'new': del Main.DB[tree.selection()[0]]
    Main.saveDB()
    tree.delete(tree.selection()[0])

def changepic(picname):
    loadedimg = ImageTk.PhotoImage(Image.open('CardImages/'+picname+'.jpg').resize((450, 640)))
    cardimage['image'] = loadedimg
    cardimage.image = loadedimg



def changefocus():
    if tree.focus()=='new':
        changepic('Back')
        return None
    cardname.set(Main.DB[tree.selection()[0]].name)
    setname.set(Main.DB[tree.selection()[0]].set)
    cardquantity.set(Main.DB[tree.selection()[0]].quantity)
    changepic(tree.selection()[0])
    if tree.exists('new'): tree.delete('new')

def getDB():
    tree.delete(*tree.get_children())
    Main.DB = Main.readDB()
    for item in Main.DB:
        card = Main.DB[item]
        tree.insert('', 'end', item, text=card.name, values = (card.set,card.quantity,card.price))
        Main.checkpic(item)


#This creates the main window of an application
window = tk.Tk()
window.title("MTGPricer")
window.geometry("1200x800")
window.configure(background='white')
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0,weight=1)
window.grid()

#This loads cardimage
path = "CardImages/back.jpg"
loadedimg = ImageTk.PhotoImage(Image.open(path).resize((450,640)))

#This creates Entry vars
cardname = StringVar()
cardquantity = StringVar()
setname = StringVar()

#This creates treeview
tree = ttk.Treeview(window, columns=('set', 'quantity', 'price'))
tree.column('set', width=100, anchor='center')
tree.heading('set', text='Set')
tree.column('quantity', width=100, anchor='center')
tree.heading('quantity', text='Quantity')
tree.column('price', width=100, anchor='center')
tree.heading('price', text='Price')
tree.bind("<<TreeviewSelect>>", lambda e: changefocus())


imagebuttons = ttk.Frame(window)

cardimage = ttk.Label(imagebuttons)
cardimage['image'] = loadedimg

update = ttk.Button(imagebuttons, text='Update', command=savecard)
delete = ttk.Button(imagebuttons, text='Delete', command=delete)
add = ttk.Button(imagebuttons, text='Add', command=addcard)

carddata = ttk.Frame(window, width=200, height=100)
carddata['borderwidth'] = 2
carddata['relief'] = 'sunken'
namelabel = ttk.Label(carddata, text = "Name:")
name = ttk.Entry(carddata, textvariable=cardname)
mtgsetlabel = ttk.Label(carddata, text = "Set:")
mtgset = ttk.Entry(carddata, textvariable=setname)
quantitylabel = ttk.Label(carddata, text = "Quantity:")
quantity = Spinbox(carddata, from_=0.0, to=100.0, textvariable=cardquantity)





tree.grid(column=0, row=0, sticky=(N,S,E,W), padx=5, pady=5)

imagebuttons.grid(column=1, row=0, sticky=(N,W,E,S), padx=5, pady=5)

cardimage.grid(column=0, row=0, sticky=(E,W))
update.grid(column=0, row=1, pady=5)
delete.grid(column=0, row=2, pady=5)
add.grid(column=0, row=3, pady=5)

carddata.grid(column=2, row=0, sticky=(N,W,E,S), padx=5, pady=5)

namelabel.grid(column=0, row=0, sticky=(N,W,E,S), padx=5, pady=5)
name.grid(column=0, row=1, sticky=(N,W,E,S), padx=5)
mtgsetlabel.grid(column=0, row=2, sticky=(N,W,E,S), padx=5, pady=5)
mtgset.grid(column=0, row=3, sticky=(N,W,E,S), padx=5)
quantitylabel.grid(column=0, row=4, sticky=(N,W,E,S), padx=5, pady=5)
quantity.grid(column=0, row=5, sticky=(N,W,E,S), padx=5)


#Start the GUI
getDB()
window.mainloop()