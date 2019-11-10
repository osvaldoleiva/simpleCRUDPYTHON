from tkinter import *
from tkinter import ttk
import sqlite3

class Product:
    
    db_name='database.db'
  
    def __init__(self,window):
        self.wind = window
        self.wind.title('Product aplication')
        #creating a frame container
        frame = LabelFrame(self.wind, text = "Registrar un nuevo producto")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name imput
        Label(frame, text="Name: ").grid(row = 1,column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column=1)

        # Price imput
        Label(frame, text="Price: ").grid(row =2, column=0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Button add product
        ttk.Button(frame, text = "Save product", command=self.addProduct).grid(row = 3, columnspan= 2, sticky = W + E)

        # OutPut messages
        self.message = Label(text ='', fg = 'red')
        self.message.grid(row = 3, column= 0, columnspan =2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height= 10, columns =2)
        self.tree.grid(row=4, column = 0, columnspan= 2)
        self.tree.heading('#0', text="Name: ", anchor= CENTER)
        self.tree.heading('#1', text="Price: ", anchor= CENTER)

        ttk.Button(text='DELETE', command=self.deleteProduct).grid(row=5, column=0, sticky= W + E)
        ttk.Button(text='UPDATE', command=self.editProduct).grid(row=5, column=1, sticky= W + E)
        
        #Fedding table
        self.getProduct()
      
    def runQuery(self, query, parametros =() ):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resulset = cursor.execute(query,parametros)
            conn.commit()
        return resulset

    def getProduct(self):
        #recorro y elimino datos de  la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.runQuery(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[1],values = row[2])

    def validation(self):
        return len(self.name.get()) !=0 and len(self.price.get()) !=0
    def addProduct(self):
        if(self.validation):
          queryInsert='INSERT INTO product VALUES(NULL, ?, ?)'
          parametres = (self.name.get(), self.price.get())
          self.runQuery(queryInsert,parametres)
          print("Datos guardados")
          self.getProduct()
          self.message['text'] = 'Product {} added successfully'.format(self.name.get())
          self.name.delete(0, END)
          self.price.delete(0, END)
        else:
            print("error")
    def deleteProduct(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text']= 'Select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text'][0]
        query = 'DELETE FROM product WHERE name = ?'
        self.runQuery(query,(name,))
        self.message['text']= 'Record {} deleted successfuly'.format(name)
        self.getProduct()
        
    def editProduct(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text']= 'Select a record'
            return
        name = self.tree.item(self.tree.selection())['text']
        oldPrice = self.tree.item(self.tree.selection())['values'][0]
        self.editWind = Toplevel()
        self.editWind.title='Edit Wind'

        # Old name
        Label(self.editWind, text='Old name: ').grid(row = 0, column = 1)
        Entry(self.editWind, textvariable = StringVar(self.editWind, value = name), state = 'readonly').grid(
            row = 0, column=2)
        # new Name
        Label(self.editWind, text='New name').grid(row = 1, column = 1)
        new_name=Entry(self.editWind)
        new_name.grid(row = 1, column= 2)
        # Old price
        Label(self.editWind, text='Old price: ').grid(row = 2, column = 1)
        Entry(self.editWind, textvariable = StringVar(self.editWind, value = oldPrice), state = 'readonly').grid(
            row = 2, column=2)
        # new price
        Label(self.editWind, text='New price').grid(row = 3, column = 1)
        new_price=Entry(self.editWind)
        new_price.grid(row = 3, column= 2)

        Button(self.editWind, text='Update', command = lambda: self.edit_records(new_name.get(),
                    name,new_price.get(),oldPrice)).grid(row=4, column=2, sticky=W)
    
    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price =  ? WHERE name = ? AND price = ?'
        parameters = (new_name,new_price,name,old_price)
        self.runQuery(query,parameters)
        self.editWind.destroy()
        self.message['text']='Record {} update successfuly'.format(name)
            
if __name__ == "__main__":
    window = Tk()
    aplication = Product(window)
    window.mainloop()
    
    