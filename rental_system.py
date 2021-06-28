from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import re
import mysql.connector
from tkinter import ttk
import datetime
from datetime import timedelta, date

#database connection
database = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd= "richardjr041501mysql",
    database = "book_rental"
)
#database object
cursor = database.cursor()

#global var, purpose is to preserve val of the variable for later use, like edit function
orig_bookid = ''
orig_customerid = ''
book_count = 0
total_rental_cost = 0
cart = []
item_cost = []
num_rented_book = 0

def frame_destroy():
    frame.destroy()

def frame_update():
    global frame
    frame = Frame(root, bg="#2f2f2d")
    frame.config(bd=1, relief=SOLID)

def table_destroy():
    table.destroy()

def table_update():
    global table
    table = ttk.Treeview(frame, height=12)

def check_ID(key):
    pattern = re.compile(r'\d\d\d\d-\d\d\d\d')
    res = re.fullmatch(pattern, key)
    if res:
        return True
    else:
        return False

def delete_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button):
    delete_query = "DELETE FROM customer WHERE CustomerID = %s"
    delete_query_referenced = "DELETE FROM rents WHERE CustomerID = %s"
    del_prompt = messagebox.askyesno("Delete student data", "Are you sure to delete it?") 
    if del_prompt:
        del_data = table.selection()[0] #deletes selected data in treeview
        table.delete(del_data)

        cursor.execute(delete_query_referenced, (customer_id_entry.get(),))# try
        database.commit()
        cursor.execute(delete_query, (customer_id_entry.get(),))
        database.commit()
      

        customer_id_entry.delete(0, END)
        name_entry.delete(0, END)
        phonenum_entry.delete(0, END)
        address_entry.delete(0, END)
        val_id_entry.delete(0, END) 
        photo_entry.delete(0, END)
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showinfo("Deleted Data", "Data is/are deleted!")

def delete_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button):
    delete_query = "DELETE FROM book WHERE BookID = %s"
    delete_query_rents = "DELETE FROM rents WHERE BookID = %s"
    delete_query_genre = "DELETE FROM genre WHERE BookID = %s"
    delete_query_author = "DELETE FROM author WHERE BookID = %s"
    
    del_prompt = messagebox.askyesno("Delete data", "Are you sure to delete it?") 
    if del_prompt:

        cursor.execute(delete_query_rents, (book_id_entry.get(),))
        database.commit()

        cursor.execute(delete_query_genre, (book_id_entry.get(),))
        database.commit()

        cursor.execute(delete_query_author, (book_id_entry.get(),))
        database.commit()

        cursor.execute(delete_query, (book_id_entry.get(),))
        database.commit()

        del_data = table.selection()[0] #deletes selected data in treeview
        table.delete(del_data)
        book_id_entry.delete(0, END)
        title_entry.delete(0, END)
        publisher_entry.delete(0, END)
        isbn_entry.delete(0, END)
        yearpub_entry.delete(0, END) 
        bookcost_entry.delete(0, END)
        avlb_entry.delete(0, END)
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showinfo("Deleted Data", "Data is/are deleted!")

def edit_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button, orig_customerid):
    edit_prompt = messagebox.askyesno("Edit data", "Are you sure to make these changes?")
    if edit_prompt:
        try:
            query = "UPDATE customer SET CustomerID = %s, Name = %s, PhoneNumber = %s, Address = %s, ValidID = %s, Photo = %s WHERE CustomerID = %s"
            query_param = (customer_id_entry.get(), name_entry.get(), phonenum_entry.get(), address_entry.get(), val_id_entry.get(), photo_entry.get(), orig_customerid)
            cursor.execute(query, query_param)
            database.commit()
            #changes values in the table, where the values are from the entries provided
            selected = table.focus()
            values = table.item(selected, text = "", values=(customer_id_entry.get(), name_entry.get(), phonenum_entry.get(), address_entry.get(), val_id_entry.get(), photo_entry.get()))
            customer_id_entry.delete(0, END)
            name_entry.delete(0, END)
            phonenum_entry.delete(0, END)
            address_entry.delete(0, END)
            val_id_entry.delete(0, END) 
            photo_entry.delete(0, END)
            
            del_button["state"] = DISABLED
            edit_button["state"] = DISABLED
        except:
            messagebox.showerror("Error", "Customer ID {} is already taken. Please provide unique CustomerID".format(customer_id_entry.get()))

def edit_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button, orig_bookid):
    edit_prompt = messagebox.askyesno("Edit data", "Are you sure to make these changes?")
    if edit_prompt:
        try:
            query = "UPDATE book SET BookID = %s, Title = %s, Publisher = %s, ISBN = %s, YearPublished = %s, BookCost = %s, Availability = %s WHERE BookID = %s"
            query_param = (book_id_entry.get(), title_entry.get(), publisher_entry.get(), isbn_entry.get(), yearpub_entry.get(), bookcost_entry.get(), avlb_entry.get(), orig_bookid)
            cursor.execute(query, query_param)
            database.commit()
            #changes values in the table, where the values are from the entries provided
            selected = table.focus()
            values = table.item(selected, text = "", values=(book_id_entry.get(), title_entry.get(), publisher_entry.get(), isbn_entry.get(), yearpub_entry.get(), bookcost_entry.get(), avlb_entry.get()))
            book_id_entry.delete(0, END)
            title_entry.delete(0, END)
            publisher_entry.delete(0, END)
            isbn_entry.delete(0, END)
            yearpub_entry.delete(0, END) 
            bookcost_entry.delete(0, END)
            avlb_entry.delete(0, END)
            
            del_button["state"] = DISABLED
            edit_button["state"] = DISABLED
        except:
            messagebox.showerror("Error", "Book ID {} is already taken. Please provide unique Book ID or book is not available of the moment.".format(book_id_entry.get()))

def select_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button):
    try:
        book_id_entry.delete(0, END)
        title_entry.delete(0, END)
        publisher_entry.delete(0, END)
        isbn_entry.delete(0, END)
        yearpub_entry.delete(0, END) 
        bookcost_entry.delete(0, END)
        avlb_entry.delete(0, END)
    except:
        messagebox.showerror("Select Data", "No data was selected!")
    try:
        selected = table.focus()
        values = table.item(selected, "values")
        del_button["state"] = NORMAL
        edit_button["state"] = NORMAL
        book_id_entry.insert(0, values[0])
        title_entry.insert(0, values[1])
        publisher_entry.insert(0, values[2])
        isbn_entry.insert(0, values[3])
        yearpub_entry.insert(0, values[4])
        bookcost_entry.insert(0, values[5])
        avlb_entry.insert(0, values[6])
        global orig_bookid
        orig_bookid = values[0]
    except:
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showerror("Select Data", "No data was selected!")

def select_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button):
    try:
        customer_id_entry.delete(0, END)
        name_entry.delete(0, END)
        phonenum_entry.delete(0, END)
        address_entry.delete(0, END)
        val_id_entry.delete(0, END) 
        photo_entry.delete(0, END)
    except:
        messagebox.showerror("Select Data", "No data was selected!")
    try:
        selected = table.focus()
        values = table.item(selected, "values")
        del_button["state"] = NORMAL
        edit_button["state"] = NORMAL
        customer_id_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        phonenum_entry.insert(0, values[2])
        address_entry.insert(0, values[3])
        val_id_entry.insert(0, values[4])
        photo_entry.insert(0, values[5])
        global orig_customerid
        orig_customerid = values[0]
    except:
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showerror("Select Data", "No data was selected!")

def search_customer(search_entry):
    try:
        table_destroy()
        table_update()
    except:
        pass
    
    #define columns of the table
    table ["columns"] = ("Customer ID", "Name", "Phone Number", "Address", "Valid ID", "Photo")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Customer ID", width = 95, anchor = CENTER, stretch = NO)
    table.column("Name", width = 290, anchor = CENTER)
    table.column("Phone Number", width = 135, anchor = CENTER)
    table.column("Address", width = 195, anchor = CENTER)
    table.column("Valid ID", width = 180, anchor = CENTER)
    table.column("Photo",  width = 180, anchor = CENTER)
    #table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Customer ID", text = "Customer ID", anchor = CENTER )
    table.heading("Name", text = "Full Name", anchor = CENTER )
    table.heading("Phone Number", text = "Phone Number", anchor = CENTER )
    table.heading("Address", text = "Address", anchor = CENTER )
    table.heading("Valid ID", text = "Valid ID", anchor = CENTER)
    table.heading("Photo", text = "Photo",  anchor = CENTER)
    # table.heading("Availability", text = "Availability",  anchor = CENTER)
    
    count = 0
    search_query = "SELECT * FROM customer WHERE CustomerID LIKE %s or Name LIKE %s or PhoneNumber LIKE %s or Address LIKE %s"
    data = (search_entry.get(), search_entry.get(), search_entry.get(),search_entry.get(),)
    search_entry.delete(0,END)
    cursor.execute(search_query, data)

    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for customer in cursor:
        if count%2==0:
            table.insert(parent = '', index='end', iid = count, values = (customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]), tags=("odd",))
        else:
            table.insert(parent = '', index='end', iid = count, values = (customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]), tags=("even",))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=6)

def display_customers():
    try:
        frame_destroy()
        table_destroy()
    except:
        pass
    frame_update()  
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="nw", pady = 20, padx = 50)
    
     
    customer_title = Label(frame, text= "Customers", background = "#2f2f2d", font = ("Open Sans", 20, "bold"), fg="white" )
    customer_title.grid(row=0, column=0, sticky=NSEW, columnspan = 6, pady=10, padx=(30,0))

    search_entry = Entry(frame, width = 20, fg = "Black", font= ("Open Sans", 10, "bold"))
    search_entry.grid(row=1, column=4, sticky=E, pady = 5, padx =(20, 15))

    search_button = Button(frame, text = "Seacrh", font= ("Open Sans", 10, "bold"), padx = 20, fg = "White", background = "royal blue", command= lambda: search_customer(search_entry))
    search_button.grid(row=1, column=5, sticky=W, pady = 5, padx = (0,15))
    
    #define columns of the table
    table ["columns"] = ("Customer ID", "Name", "Phone Number", "Address", "Valid ID", "Photo")

    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Customer ID", width = 95, anchor = CENTER, stretch = NO)
    table.column("Name", width = 290, anchor = CENTER)
    table.column("Phone Number", width = 135, anchor = CENTER)
    table.column("Address", width = 195, anchor = CENTER)
    table.column("Valid ID", width = 180, anchor = CENTER)
    table.column("Photo",  width = 180, anchor = CENTER)
    #table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Customer ID", text = "Customer ID", anchor = CENTER )
    table.heading("Name", text = "Full Name", anchor = CENTER )
    table.heading("Phone Number", text = "Phone Number", anchor = CENTER )
    table.heading("Address", text = "Address", anchor = CENTER )
    table.heading("Valid ID", text = "Valid ID", anchor = CENTER)
    table.heading("Photo", text = "Photo",  anchor = CENTER)
    # table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    display_customer_query = "SELECT * FROM customer"
    cursor.execute(display_customer_query)
    
    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for customer_details in cursor:
        if count%2==0:
            table.insert(parent = '', index='end', iid = count, values = (customer_details[0], customer_details[1], customer_details[2], customer_details[3], customer_details[4], customer_details[5]), tags=("odd",))
        else:
             table.insert(parent = '', index='end', iid = count, values = (customer_details[0], customer_details[1], customer_details[2], customer_details[3], customer_details[4], customer_details[5]), tags=("even",))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=6)

    #entry boxes for update book info
    header = ["Customer ID", "Full Name", "Phone Number", "Address", "Valid ID", "Photo"]
    for item in range(6):

        if item == 1:
            e = Entry(frame, width=20, font=('Helvetica',8, "bold"), justify = CENTER)
            e.grid(row=8, column=item,sticky = NSEW) 
            e.insert(END, header[item])
            e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
        else:
            if item == 1:
                e = Entry(frame, width=10, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=8, column=item, sticky = NSEW, padx = 5) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
            else:
                e = Entry(frame, width=12, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=8, column=item, sticky = NSEW) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    # entry for update inputs
    customer_id_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    customer_id_entry.grid(row = 9, column = 0, sticky = NSEW)

    name_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    name_entry.grid(row = 9, column = 1, sticky = NSEW)

    phonenum_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    phonenum_entry.grid(row = 9, column = 2, sticky = NSEW)

    address_entry = Entry(frame, width=15, font=('Helvetica',8), justify = CENTER)
    address_entry.grid(row = 9, column = 3, sticky = NSEW)

    val_id_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    val_id_entry.grid(row = 9, column = 4, sticky = NSEW)

    photo_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    photo_entry.grid(row = 9, column = 5, sticky = NSEW)

    # avlb_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    # avlb_entry.grid(row = 7, column = 6, sticky = NSEW)

    edit_button = Button(frame, text="Edit", padx =33, pady = 10, state = "disabled",  borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command= lambda: edit_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button, orig_customerid))
    edit_button.grid(row=10, column=2, pady = 5, padx = (0,30), sticky=E)

    del_button = Button(frame, text="Delete", padx =25, pady = 10, state = "disabled",  borderwidth = "2", bg='#e64e4e', fg = "white", font=("Open Sans", 8, "bold"), command= lambda: delete_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button))
    del_button.grid(row=10, column=4, pady = 5, sticky=W, padx = (15,100))

    select_button = Button(frame, text="Select Data", padx =25, pady = 10, borderwidth = "2", bg='#B99976', fg = "black", font=("Open Sans", 8, "bold"), command=lambda: select_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button))
    select_button.grid(row=10, column=3 , pady = 5, sticky=N, padx = (15,30))
    
def search_book(search_entry):
    try:
        table_destroy()
        table_update()
    except:
        pass

    #define columns of the table
    table ["columns"] = ("Book ID", "Title", "Publisher", "ISBN", "Year Published", "Book Cost", "Availability")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Book ID", width = 95, anchor = CENTER, stretch = NO)
    table.column("Title", width = 290, anchor = CENTER)
    table.column("Publisher", width = 135, anchor = CENTER)
    table.column("ISBN", width = 155, anchor = CENTER)
    table.column("Year Published", width = 130, anchor = CENTER)
    table.column("Book Cost",  width = 110, anchor = CENTER)
    table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Book ID", text = "Book ID", anchor = CENTER )
    table.heading("Title", text = "Title", anchor = CENTER )
    table.heading("Publisher", text = "Publisher", anchor = CENTER )
    table.heading("ISBN", text = "ISBN", anchor = CENTER )
    table.heading("Year Published", text = "Year Published", anchor = CENTER)
    table.heading("Book Cost", text = "Book Cost",  anchor = CENTER)
    table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    search_query = "SELECT * FROM book WHERE BookID LIKE %s or Title LIKE %s or Publisher LIKE %s or ISBN LIKE %s or YearPublished LIKE %s or BookCost LIKE %s or Availability LIKE %s"
    data = (search_entry.get(), search_entry.get(), search_entry.get(),search_entry.get(), search_entry.get(), search_entry.get(), search_entry.get(),)
    search_entry.delete(0,END)
    cursor.execute(search_query, data)

    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for book in cursor:
        if count&2==0:
            table.insert(parent = '', index='end', iid = count, values = (book[0], book[1], book[2], book[3], book[4], book[5], book[6]), tags = ("odd",))
        else:
            table.insert(parent = '', index='end', iid = count, values = (book[0], book[1], book[2], book[3], book[4], book[5], book[6]), tags = ("even",))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=7)

def display_custmer_billing():
    pass
    

#pending, to be solve later (least prioritized)
def display_by_ISBN(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, select_button, delete_button, edit_button ):
    try:
        table_destroy()
    except:
        pass

    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="nw", pady = 20, padx = 80)


    book_title = Label(frame, text= "Books", background = "#2f2f2d", font = ("Open Sans", 20, "bold"), fg="white" )
    book_title.grid(row=0, column=0, sticky=NSEW, columnspan = 6, pady=10, padx=(100,0))

    search_entry = Entry(frame, width = 20, fg = "Black", font= ("Open Sans", 10, "bold"))
    search_entry.grid(row=1, column=5, sticky=E, pady = 5)

    search_button = Button(frame, text = "Seacrh", font= ("Open Sans", 10, "bold"), padx = 20, fg = "White", background = "royal blue", command= lambda: search_book(search_entry))
    search_button.grid(row=1, column=6, sticky=W, pady = 5, padx = (15,0))

    #define columns of the table
    table ["columns"] = ("Title", "Publisher", "ISBN", "Year Published", "Book Cost", "Available Copies")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Title", width = 230, anchor = CENTER, stretch = NO)
    table.column("Publisher", width = 170, anchor = CENTER)
    table.column("ISBN", width = 170, anchor = CENTER)
    table.column("Year Published", width = 140, anchor = CENTER)
    table.column("Book Cost",  width = 140, anchor = CENTER)
    table.column("Available Copies",  width = 180, anchor = CENTER)
    #create headings
    table.heading("0")
    table.heading("Title", text = "Title", anchor = CENTER )
    table.heading("Publisher", text = "Publisher", anchor = CENTER )
    table.heading("ISBN", text = "ISBN", anchor = CENTER )
    table.heading("Year Published", text = "Year Published", anchor = CENTER)
    table.heading("Book Cost", text = "Book Cost",  anchor = CENTER)
    table.heading("Available Copies", text = "Available Copies",  anchor = CENTER)

    table.grid(row=2, column=0, rowspan=6, columnspan=7)
    
    count = 0
    display_book_query = "SELECT book.Title, book.Publisher, book.ISBN, book.YearPublished book.BookCost FROM book"
    cursor.execute(display_book_query)

    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for book_item in cursor:
        if count%2==0:
            table.insert(parent = '', index='end', iid = count, values = (book_item[0], book_item[1], book_item[2], book_item[3], book_item[4]), tags=("odd",))
        else:
            table.insert(parent = '', index='end', iid = count, values = (book_item[0], book_item[1], book_item[2], book_item[3], book_item[4]), tags=("even",))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=7)

    book_id_entry["state"] = DISABLED
    title_entry["state"] = DISABLED
    publisher_entry["state"] = DISABLED
    isbn_entry["state"] = DISABLED
    yearpub_entry["state"] = DISABLED
    bookcost_entry["state"] = DISABLED
    avlb_entry["state"] = DISABLED
    select_button["state"] = DISABLED
    edit_button["state"] = DISABLED
    del_button["state"] = DISABLED
    

def display_books():
    try:
        frame_destroy()
        table_destroy()
    except:
        pass
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="nw", pady = 20, padx = 80)
    
    book_title = Label(frame, text= "Books", background = "#2f2f2d", font = ("Open Sans", 20, "bold"), fg="white" )
    book_title.grid(row=0, column=0, sticky=NSEW, columnspan = 6, pady=10, padx=(100,0))

    search_entry = Entry(frame, width = 20, fg = "Black", font= ("Open Sans", 10, "bold"))
    search_entry.grid(row=1, column=5, sticky=E, pady = 5)

    search_button = Button(frame, text = "Seacrh", font= ("Open Sans", 10, "bold"), padx = 20, fg = "White", background = "royal blue", command= lambda: search_book(search_entry))
    search_button.grid(row=1, column=6, sticky=W, pady = 5, padx = (15,0))

    by_book_id_button = Button(frame, text = "By Book ID", font= ("Open Sans", 10, "bold"), padx = 10, fg = "White", background = "#2f2f2d", command= display_books)
    by_book_id_button.grid(row=1, column=0, sticky=W, pady = 5, padx = (15,0))

    by_isbn_button = Button(frame, text = "By Isbn", font= ("Open Sans", 10, "bold"), padx = 15, fg = "White", background = "#2f2f2d", command= lambda: display_by_ISBN(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, select_button, del_button, edit_button ))
    by_isbn_button.grid(row=1, column=1, sticky=W, pady = 5, padx = (15,0))


    #define columns of the table
    table ["columns"] = ("Book ID", "Title", "Publisher", "ISBN", "Year Published", "Book Cost", "Availability")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Book ID", width = 95, anchor = CENTER, stretch = NO)
    table.column("Title", width = 290, anchor = CENTER)
    table.column("Publisher", width = 135, anchor = CENTER)
    table.column("ISBN", width = 155, anchor = CENTER)
    table.column("Year Published", width = 130, anchor = CENTER)
    table.column("Book Cost",  width = 110, anchor = CENTER)
    table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Book ID", text = "Book ID", anchor = CENTER )
    table.heading("Title", text = "Title", anchor = CENTER )
    table.heading("Publisher", text = "Publisher", anchor = CENTER )
    table.heading("ISBN", text = "ISBN", anchor = CENTER )
    table.heading("Year Published", text = "Year Published", anchor = CENTER)
    table.heading("Book Cost", text = "Book Cost",  anchor = CENTER)
    table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    display_book_query = "SELECT * FROM book"
    cursor.execute(display_book_query)

    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for book_item in cursor:
        if count%2==0:
            table.insert(parent = '', index='end', iid = count, values = (book_item[0], book_item[1], book_item[2], book_item[3], book_item[4], book_item[5], book_item[6]), tags=("odd",))
        else:
            table.insert(parent = '', index='end', iid = count, values = (book_item[0], book_item[1], book_item[2], book_item[3], book_item[4], book_item[5], book_item[6]), tags=("even",))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=7)

    #entry boxes for update book info
    header = ["Book ID", "Title", "Publisher", "ISBN", "Year Published", "Book Cost", "Availability"]
    for item in range(7):

        if item == 1:
            e = Entry(frame, width=20, font=('Helvetica',8, "bold"), justify = CENTER)
            e.grid(row=8, column=item,sticky = NSEW) 
            e.insert(END, header[item])
            e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
        else:
            if item == 1:
                e = Entry(frame, width=10, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=8, column=item, sticky = NSEW, padx = 5) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
            else:
                e = Entry(frame, width=12, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=8, column=item, sticky = NSEW) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    # entry for update inputs
    book_id_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    book_id_entry.grid(row = 9, column = 0, sticky = NSEW)

    title_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    title_entry.grid(row = 9, column = 1, sticky = NSEW)

    publisher_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    publisher_entry.grid(row = 9, column = 2, sticky = NSEW)

    isbn_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    isbn_entry.grid(row = 9, column = 3, sticky = NSEW)

    yearpub_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    yearpub_entry.grid(row = 9, column = 4, sticky = NSEW)

    bookcost_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    bookcost_entry.grid(row = 9, column = 5, sticky = NSEW)

    avlb_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    avlb_entry.grid(row = 9, column = 6, sticky = NSEW)

    edit_button = Button(frame, text="Edit", padx =33, pady = 10, state = "disabled",  borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command=lambda: edit_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button, orig_bookid))
    edit_button.grid(row=10, column=2, pady = 5, padx = 40, sticky=W)

    del_button = Button(frame, text="Delete", padx =25, pady = 10, state = "disabled",  borderwidth = "2", bg='#e64e4e', fg = "white", font=("Open Sans", 8, "bold"), command=lambda: delete_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button))
    del_button.grid(row=10, column=4, pady = 5, sticky=E, padx = 15)

    select_button = Button(frame, text="Select Data", padx =25, pady = 10, borderwidth = "2", bg='#B99976', fg = "black", font=("Open Sans", 8, "bold"), command=lambda: select_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button))
    select_button.grid(row=10, column=3 , pady = 5, sticky=W, padx = (15,15))

    table.grid(row=2, column=0, rowspan=6, columnspan=7)



def login(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry, return_rentals_button):
    try:
        frame_destroy()
        frame_update()
        frame.grid(row=1, column=1, rowspan = 6, columnspan=6, sticky=NW, pady = 50, padx=270)
    except:
        pass
    try:
        # frame_update()
        # frame.grid(row=1, column=1, rowspan = 6, columnspan=6, sticky=NW, pady = 50, padx=270)

        login_title = Label(frame, text="Log In", background = "#2f2f2d", fg = "white", font = ("Open Sans", 20, "bold"))
        login_title.grid(row=0, column=1, sticky = W)
        username_lbl = Label(frame, text = "Username", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        username_lbl.grid(row=1, column=0, sticky = W,pady=(20,10), padx = 20)
        username_entry = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        username_entry.grid(row=2, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        password_lbl = Label(frame,text= "Password", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        password_lbl.grid(row=3, column=0, sticky = W, pady=(20,10), padx = 20)
        password_entry = Entry(frame, show="*", font=('Helvetica',14, "bold"), width=50)
        password_entry.grid(row=4, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        def getdata():
            try:
                users  = []
                query = "SELECT Role FROM user WHERE username = %s AND password = %s"
                data = (username_entry.get(), password_entry.get())
                cursor.execute(query,data)
                for user in cursor:
                    users.append(user)

                if len(users) != 0:
                    display_book_button ["state"] = NORMAL
                    add_book_button ["state"] = NORMAL
                    display_customer_button ["state"] = NORMAL
                    display_rentals_button ["state"] = NORMAL
                    rent_button ["state"] = NORMAL
                    search_button ["state"] = NORMAL
                    return_rentals_button ["state"] = NORMAL
                    role_entry.insert(END, users[0])
                    role_entry.config(state="disabled", disabledbackground = "#403b35", disabledforeground = "white") 
                    messagebox.showinfo("Successful", "Successfully log in!")
                    frame_destroy()
                else:
                    messagebox.showerror("Error", "Incorrect username or password")
            except:
                messagebox.showerror("Error", "Incorrect username or password")

        login_button = Button(frame, text="Log in", background = "royal blue", fg = "white", font = ("Open Sans", 14, "bold"), padx = 15, pady = 10, command = getdata)
        login_button.grid(row=5, column=1, sticky = W, pady = (30,10), padx = 20)
        ask_signin = Label(frame, text="Don't have an account?", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10, "bold"))
        ask_signin.grid(row=6, column=1, sticky=W, pady = (20,0))
        signin_button = Button(frame, text="Sign in", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10, "bold"), borderwidth = 0, command = lambda: signin(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry, return_rentals_button))
        signin_button.grid(row=7, column=1, sticky = W, pady = (5,20), padx= 50)

    except:
        messagebox.showerror("Error", "Incorrect username or password")

def signin(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry, return_rentals_button):
    try:
        frame_destroy()
        frame_update()
        frame.grid(row=1, column=1, rowspan = 9, columnspan=6, sticky=NW, pady = 50, padx=270)
    except:
        pass

    try:
        signin_title = Label(frame, text="Sign In", background = "#2f2f2d", fg = "white", font = ("Open Sans", 20, "bold"))
        signin_title.grid(row=0, column=1, sticky = W)
        username_lbl = Label(frame, text = "Username", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        username_lbl.grid(row=1, column=0, sticky = W,pady=(20,10), padx = 20)
        username_entry = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        username_entry.grid(row=2, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        password_lbl = Label(frame,text= "Password", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        password_lbl.grid(row=3, column=0, sticky = W, pady=(20,10), padx = 20)
        password_entry = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        password_entry.grid(row=4, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        role_lbl = Label(frame,text= "Role", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        role_lbl.grid(row=5, column=0, sticky = W, pady=(20,10), padx = 20)
        # role_ent = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        # role_ent.grid(row=6, column = 0, columnspan = 3, sticky = NSEW, padx = 20)
        
        # copy this, change entry to dropdown
        roles = ["Select Role", "Administrator", "Clerk"]
        role_ent = ttk.Combobox(frame, values = roles)
        role_ent.grid(row=6, column=0, columnspan= 3, sticky="nsew", padx =20)
        role_ent.current(0) #initially set combobox to Select Course
        #role_ent.grid(row=6, column=1, padx=(0,20), pady=20)

        def getdata():
            try:
                user_data = []
                if username_entry.get() != "" and password_entry.get() != "" and role_ent.get() != "" and role_ent.get() != "Select Role":
                    user_data = [username_entry.get(), password_entry.get(), role_ent.get().capitalize()] #role is always upper for uniformity when displayed
                    query = "INSERT INTO user VALUES (%s,%s,%s)"
                    data = (user_data[0], user_data[1], user_data[2]) 
                    cursor.execute(query,data)
                    database.commit()
                    display_book_button ["state"] = NORMAL
                    add_book_button ["state"] = NORMAL
                    display_customer_button ["state"] = NORMAL
                    display_rentals_button ["state"] = NORMAL
                    rent_button ["state"] = NORMAL
                    search_button ["state"] = NORMAL
                    return_rentals_button ["state"] = NORMAL
                    role_entry.insert(END, user_data[2])
                    role_entry.config(state="disabled", disabledbackground = "#403b35", disabledforeground = "white") 
                    messagebox.showinfo("Successful", "Successfully signed in!")
                    frame_destroy()
                else:
                    messagebox.showerror("Error", "Incorrect username or password or role.")
            except:
                messagebox.showerror("Error", "Incorrect username or password or role.")

        signin_button = Button(frame, text="Sign in", background = "royal blue", fg = "white", font = ("Open Sans", 14, "bold"), padx = 15, pady = 10, command = getdata)
        signin_button.grid(row=7, column=1, sticky = W, pady = (30,10), padx = 20)
        ask_login = Label(frame, text="Already have an account?", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10, "bold"))
        ask_login.grid(row=8, column=1, sticky=W, pady = (20,0))
        login_button = Button(frame, text="Log in", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10, "bold"), borderwidth = 0, command = lambda: login(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry, return_rentals_button))
        login_button.grid(row=9, column=1, sticky = W, pady = (5,20), padx= 50)

    except:
        pass

def add_book_inventory():
    try: #destroys existing frames from other display
        frame_destroy()
        table_destroy()
    except:
        pass
    
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 19, columnspan=6, sticky=NW, pady = 40, padx=430)

    book_details_title = Label(frame, text="Book Details", background = "#2f2f2d", fg = "white", font = ("Open Sans", 18, "bold"))
    book_details_title.grid(row=0, column=0, sticky = N, columnspan =3)

    book_id_lbl = Label(frame, text = "Book ID", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    book_id_lbl.grid(row=1, column=0, sticky = W,pady=(10,2), padx = 20)
    book_id_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    book_id_entry.grid(row=2, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    title_lbl = Label(frame,text= "Title", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    title_lbl.grid(row=3, column=0, sticky = W, pady=(10,2), padx = 20)
    title_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    title_entry.grid(row=4, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    publisher_lbl = Label(frame,text= "Publisher", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    publisher_lbl.grid(row=5, column=0, sticky = W, pady=(10,2), padx = 20)
    publisher_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    publisher_entry.grid(row=6, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    isbn_lbl = Label(frame,text= "ISBN", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    isbn_lbl.grid(row=7, column=0, sticky = W, pady=(10,2), padx = 20)
    isbn_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    isbn_entry.grid(row=8, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    yearpub_lbl = Label(frame,text= "Year Published (YYYY-MM-DD)", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    yearpub_lbl.grid(row=9, column=0, sticky = W, pady=(10,2), padx = 20)
    yearpub_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    yearpub_entry.grid(row=10, column = 0, columnspan = 3, sticky = NSEW, padx = 20)
    
    bookcost_lbl = Label(frame,text= "Rental Price or Book Cost", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    bookcost_lbl.grid(row=11, column=0, sticky = W, pady=(10,2), padx = 20)
    bookcost_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    bookcost_entry.grid(row=12, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    genre_lbl = Label(frame,text= "Genre (e.g romance,comedy)", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    genre_lbl.grid(row=13, column=0, sticky = W, pady=(10,2), padx = 20)
    genre_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    genre_entry.grid(row=14, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    author_fname_lbl = Label(frame,text= "Author First Name", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    author_fname_lbl.grid(row=15, column=0, sticky = W, pady=(10,2), padx = 20)
    author_fname_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    author_fname_entry.grid(row=16, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    author_lname_lbl = Label(frame,text= "Author Last Name", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10))
    author_lname_lbl.grid(row=17, column=0, sticky = W, pady=(10,2), padx = 20)
    author_lname_entry = Entry(frame, font=('Helvetica',10, "bold"), width=50)
    author_lname_entry.grid(row=18, column = 0, columnspan = 3, sticky = NSEW, padx = 20)
    
    def getdata():
        #try:
        run = True
        #b_details refers to single valued-simple attributes 
        b_details = [book_id_entry.get(),title_entry.get(),publisher_entry.get(),isbn_entry.get(),yearpub_entry.get(),bookcost_entry.get(), "Available", author_fname_entry.get(), author_lname_entry.get()] #once added, its availability will set to available
        genre_val = genre_entry.get().split(",")
        
        for item in b_details:
            if item == None or item == "":
                messagebox.showerror('Incomplete Data', "Data is incomplete, complete data first to proceed.")
                run = False
                break
        if run:
            query = "INSERT INTO book VALUES (%s,%s,%s,%s,%s,%s,%s)"
            data = (b_details[0], b_details[1],b_details[2], b_details[3], b_details[4], b_details[5], b_details[6]) 
            cursor.execute(query,data)
            database.commit()

            #query to insert val for genre table
            query_genre = "INSERT INTO genre VALUES (%s,%s)"
            #loop on the values of the genre val
            for data in genre_val:
                cursor.execute(query_genre, (book_id_entry.get(),data))
                database.commit()
            query_author = "INSERT INTO author VALUES (%s, %s,%s)"
            cursor.execute(query_author, (book_id_entry.get(),author_fname_entry.get(), author_lname_entry.get()))
            database.commit()

            book_id_entry.delete(0,END)
            title_entry.delete(0,END)
            publisher_entry.delete(0,END)
            isbn_entry.delete(0,END)
            yearpub_entry.delete(0,END)
            bookcost_entry.delete(0,END)
            genre_entry.delete(0,END) 
            author_fname_entry.delete(0,END)
            author_lname_entry.delete(0,END)
            messagebox.showinfo("Successful", "Successfully added the book in the inventory!")
            # else:
            #     messagebox.showerror("Error", "Incorrect input. Please try again!")
        # except:
            # messagebox.showerror("Error", "Incorrect input. Please try again!")

    add_button = Button(frame, text="Enter", background = "royal blue", fg = "white", font = ("Open Sans", 12, "bold"), padx = 15, pady = 10, command = getdata)
    add_button.grid(row=19, column=0 , sticky = N, columnspan =3, pady=(20,5))

def add_customer_details():
    try: #destroys existing frames from other display
        frame_destroy()
        table_destroy()
    except:
        pass
    
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 13, columnspan=6, sticky=NW, pady = 60, padx=370)

    customer_details_title = Label(frame, text="Customer Details", background = "#2f2f2d", fg = "white", font = ("Open Sans", 20, "bold"))
    customer_details_title.grid(row=0, column=0, sticky = N, columnspan =3)

    customer_id_lbl = Label(frame, text = "Customer ID", background = "#2f2f2d", fg = "white", font = ("Open Sans", 11))
    customer_id_lbl.grid(row=1, column=0, sticky = W,pady=(15,5), padx = 20)
    customer_id_entry = Entry(frame, font=('Helvetica',11, "bold"), width=50)
    customer_id_entry.grid(row=2, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    name_lbl = Label(frame,text= "Full Name", background = "#2f2f2d", fg = "white", font = ("Open Sans", 11))
    name_lbl.grid(row=3, column=0, sticky = W, pady=(15,5), padx = 20)
    name_entry = Entry(frame, font=('Helvetica',11, "bold"), width=50)
    name_entry.grid(row=4, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    phonenum_lbl = Label(frame,text= "Phone Number", background = "#2f2f2d", fg = "white", font = ("Open Sans", 11))
    phonenum_lbl.grid(row=5, column=0, sticky = W, pady=(15,5), padx = 20)
    phonenum_entry = Entry(frame, font=('Helvetica',11, "bold"), width=50)
    phonenum_entry.grid(row=6, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    address_lbl = Label(frame,text= "Address", background = "#2f2f2d", fg = "white", font = ("Open Sans", 11))
    address_lbl.grid(row=7, column=0, sticky = W, pady=(15,5), padx = 20)
    address_entry = Entry(frame, font=('Helvetica',11, "bold"), width=50)
    address_entry.grid(row=8, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    val_id_lbl = Label(frame,text= "Valid ID (file path)", background = "#2f2f2d", fg = "white", font = ("Open Sans", 11))
    val_id_lbl.grid(row=9, column=0, sticky = W, pady=(15,5), padx = 20)
    val_id_entry = Entry(frame, font=('Helvetica',11, "bold"), width=50)
    val_id_entry.grid(row=10, column = 0, columnspan = 3, sticky = NSEW, padx = 20)
    
    photo_lbl = Label(frame,text= "Photo (file path)", background = "#2f2f2d", fg = "white", font = ("Open Sans", 11))
    photo_lbl.grid(row=11, column=0, sticky = W, pady=(15,5), padx = 20)
    photo_entry = Entry(frame, font=('Helvetica',11, "bold"), width=50)
    photo_entry.grid(row=12, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

    def getdata():
        #try:
        run = True
        user_details = [customer_id_entry.get(),name_entry.get(),phonenum_entry.get(),address_entry.get(),val_id_entry.get(),photo_entry.get()]
        for item in user_details:
            if item == None or item == "":
                messagebox.showerror('Incomplete Data', "Data is incomplete, complete data first to proceed.")
                run = False
                break
        if run:
            query = "INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s)"
            data = (user_details[0], user_details[1],user_details[2], user_details[3], user_details[4], user_details[5]) 
            cursor.execute(query,data)
            database.commit()
            messagebox.showinfo("Added", "Customer Details Added!")
            frame_destroy()
            rent_book(user_details[0], user_details[1]) #values (customerID, customerName)
        else:
            messagebox.showerror("Error", "Incorrect input. Please try again!")
        #except:
            
            #messagebox.showerror("Error", "Incorrect input. Please try again!")

    add_button = Button(frame, text="Enter", background = "royal blue", fg = "white", font = ("Open Sans", 12, "bold"), padx = 15, pady = 10, command = getdata)
    add_button.grid(row=13, column=0 , sticky = N, columnspan =3, pady=20)

def customer_type():
    try: #destroys existing frames from other display
        frame_destroy()
        table_destroy()
    except:
        pass

    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="NW", pady = 170, padx = 340)

    customer_type = Label(frame, text="Type of Customer", background = "#2f2f2d", fg = "white", font = ("Open Sans", 20, "bold"))
    customer_type.grid(row=0, column=0, sticky = NSEW, columnspan =2)

    #allows the user to choose, if new_customer add customer details first, else proceed to the rental.
    new_customer_button = Button(frame, text="New Customer", background = "royal blue", fg = "white", font = ("Open Sans", 14, "bold"), padx =20, pady = 30, command = add_customer_details)
    new_customer_button.grid(row=1, column=0, padx = (50,30), pady = 50)
    old_customer_button = Button(frame, text="Old Customer", background = "#EEEEEE", fg = "black", font = ("Open Sans", 14, "bold"), padx =20, pady = 30, command = pick_customer_to_rent)
    old_customer_button.grid(row=1, column=1, padx = (30,50), pady = 50)

def rent_book(customer_id, name):
    try: #destroys existing frames from other display
        frame_destroy()
        table_destroy()
    except:
        pass
    
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="NW", pady = 50, padx = 50)

    rent_title = Label(frame, text= "Select Book for Rent", background = "#2f2f2d", font = ("Open Sans", 14, "bold"), fg="white" )
    rent_title.grid(row=0, column=0, sticky=NSEW, columnspan = 6, pady=10)

    customer_id_lbl = Label(frame, text= "Customer ID: ", background = "#2f2f2d", font = ("Open Sans", 10, "bold"), fg="white" )
    customer_id_lbl.grid(row=1, column=0, padx = (5,0), sticky= W)

    name_lbl =  Label(frame, text= "Customer Name: ", background = "#2f2f2d", font = ("Open Sans", 10, "bold"), fg="white" )
    name_lbl.grid(row=2, column=0, padx = (5,0), sticky = W)

    customer_idnum_entry = Entry(frame, width=10,fg='white', font=('Open Sans',10, 'bold'), borderwidth=1, background="#2f2f2d")
    customer_idnum_entry.grid(row=1, column=1, sticky= NSEW)

    customer_name_entry = Entry(frame, width=10,fg='white', font=('Open Sans',10, 'bold'), borderwidth=1, background="#2f2f2d")
    customer_name_entry.grid(row=2, column=1, sticky= NSEW)
   
    book_count_lbl = Label(frame, text= "Book Count Added on Cart:", background = "#2f2f2d", font = ("Open Sans", 10, "bold"), fg="white" )
    book_count_lbl.grid(row=1, column=4, padx=(10,0))

    book_count_entry = Entry(frame, width=15,fg='white', font=('Open Sans',10, 'bold'), borderwidth=1, background="#2f2f2d")
    book_count_entry.grid(row=1, column=5, padx=(2,10))
    
    total_cost_lbl = Label(frame, text= "Total Cost:", background = "#2f2f2d", font = ("Open Sans", 10, "bold"), fg="white" )
    total_cost_lbl.grid(row=2, column=4, padx=(10,0))

    total_cost_entry = Entry(frame, width=15,fg='white', font=('Open Sans',10, 'bold'), borderwidth=1, background="#2f2f2d")
    total_cost_entry.grid(row=2, column=5, padx=(2,10))
    
    customer_idnum_entry.insert(END, customer_id)
    customer_name_entry.insert(END, name)

    customer_idnum_entry.config(state="disabled", disabledbackground = "#2f2f2d", disabledforeground = "white")
    customer_name_entry.config(state="disabled", disabledbackground = "#2f2f2d", disabledforeground = "white")
    book_count_entry.config(state="disabled", disabledbackground = "#2f2f2d", disabledforeground = "white")
    total_cost_entry.config(state="disabled", disabledbackground = "#2f2f2d", disabledforeground = "white")

    #define columns of the table
    table ["columns"] = ("Book ID", "Title", "Publisher", "ISBN", "Year Published", "Book Cost", "Availability")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Book ID", width = 95, anchor = CENTER, stretch = NO)
    table.column("Title", width = 290, anchor = CENTER)
    table.column("Publisher", width = 135, anchor = CENTER)
    table.column("ISBN", width = 155, anchor = CENTER)
    table.column("Year Published", width = 130, anchor = CENTER)
    table.column("Book Cost",  width = 110, anchor = CENTER)
    table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Book ID", text = "Book ID", anchor = CENTER )
    table.heading("Title", text = "Title", anchor = CENTER )
    table.heading("Publisher", text = "Publisher", anchor = CENTER )
    table.heading("ISBN", text = "ISBN", anchor = CENTER )
    table.heading("Year Published", text = "Year Published", anchor = CENTER)
    table.heading("Book Cost", text = "Book Cost",  anchor = CENTER)
    table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    display_book_query = "SELECT * FROM book"
    cursor.execute(display_book_query)

    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for book_item in cursor:
        if count % 2 == 0:
            table.insert(parent = '', index='end', iid = count, values = (book_item[0], book_item[1], book_item[2], book_item[3], book_item[4], book_item[5], book_item[6]), tags=("odd",))
        else:
            table.insert(parent = '', index='end', iid = count, values = (book_item[0], book_item[1], book_item[2], book_item[3], book_item[4], book_item[5], book_item[6]), tags=("even",))
        count += 1

    table.grid(row=3, column=0, rowspan=6, columnspan=6)

    add_button = Button(frame, text="Add", background = "royal blue", fg = "white", font = ("Open Sans", 12, "bold"), padx = 32, pady = 10, command = lambda: add_to_cart(book_count_entry, total_cost_entry))
    add_button.grid(row=9, column=2 , sticky = E, pady=20)

    rent_button = Button(frame, text="Rent", background = "#4de375", fg = "white", font = ("Open Sans", 12, "bold"), padx = 30, pady = 10, command = lambda: rent_books_in_cart(customer_id, name))
    rent_button.grid(row=9, column=3 , sticky = N, pady=20)

    remove_button = Button(frame, text="Remove", background = "#e64e4e", fg = "white", font = ("Open Sans", 12, "bold"), padx = 15, pady = 10, command = lambda: remove_from_cart(book_count_entry, total_cost_entry))
    remove_button.grid(row=9, column=4 , sticky = W, pady=20)

    
def add_to_cart(book_count_entry, total_cost_entry): 
    selected = table.focus()
    values = table.item(selected, "values")
    
    global  book_count
    global total_rental_cost
    global item_cost
    if book_count == 5:
        messagebox.showinfo("Exceed Maximum", "Maximum of 5 books to be rented at a time!")
        return
    if values[6].upper() == "AVAILABLE":
        for item in cart:
            if item == values[0]:
                messagebox.showinfo("Already in Cart", "Item is already on the cart")   #to be fixed
                return
        #changes availability to added once
        added_item = table.item(selected, text = "", values=(values[0], values[1], values[2], values[3], values[4], values[5], "Added"))
        cart.append(values[0])
        item_cost.append(values[5])
        total_rental_cost += int(values[5])
        book_count += 1
        book_count_entry ["state"] = NORMAL
        total_cost_entry ["state"] = NORMAL
        book_count_entry.delete(0, END)
        book_count_entry.insert(END, book_count)
        total_cost_entry.delete(0, END)
        total_cost_entry.insert(END, total_rental_cost)
        book_count_entry ["state"] = DISABLED
        total_cost_entry ["state"] = DISABLED
        #print(cart) #for debugging purposes
    else:
        messagebox.showinfo("Not Available", "Book is not available!")
        
def remove_from_cart(book_count_entry, total_cost_entry):
    selected = table.focus()
    values = table.item(selected, "values")
    global  book_count
    global total_rental_cost
    global item_cost
    if book_count == 0:
        messagebox.showinfo("No item", "No book/s added on the cart!")
        return
    else:
        temp = 0
        for val in cart:
            if values[0] == val:
                removed_item = table.item(selected, text = "", values=(values[0], values[1], values[2], values[3], values[4], values[5], "Available"))
                book_count -= 1
                item_cost.remove(values[5])
                total_rental_cost -= int(values[5])
                cart.remove(val)
                book_count_entry ["state"] = NORMAL
                total_cost_entry["state"] = NORMAL
                book_count_entry.delete(0, END)
                book_count_entry.insert(END, book_count)
                total_cost_entry.delete(0, END)
                total_cost_entry.insert(END, total_rental_cost)
                book_count_entry ["state"] = DISABLED
                total_cost_entry["state"] = DISABLED
                messagebox.showinfo("Removed", "Book ID {} removed in the cart".format(values[0]))
                temp += 1
                break
        if temp == 0:
            messagebox.showinfo("Not in the cart", "Book ID {} not in the cart!".format(values[0]))
       #print(cart) #for debugging purposes

def rent_books_in_cart(customer_id, name):
    global cart
    global total_rental_cost
    global item_cost
    global book_count
    global num_rented_book
    date_today = date.today()
    start_date = date_today.strftime("%Y-%m-%d")
    due_date = date.today() + timedelta(days=5)
    prompt = messagebox.askyesno("Confirm", "Are you sure?")
    
    if prompt:
        if len(cart) == 0 or total_rental_cost == 0:
            messagebox.showinfo("No item in the cart", "No book/books in the cart!")
            return
        cursor.execute("SELECT ReturnStatus FROM rents WHERE CustomerID=%s",(customer_id,))

        for status in cursor:
            if status[0] == "Not yet returned":
                num_rented_book += 1

        if num_rented_book + len(cart) >= 5:
            messagebox.showinfo("Maximum", "Exceed number of books rented!")
            num_rented_book = 0
            return

        query_avlb = "UPDATE book SET Availability = %s WHERE BookID = %s"
        for item in cart: #elements in the cart are the book id of the book rented
            cursor.execute(query_avlb, ("Not Available",item))
            database.commit()
       
        query_rental = "INSERT INTO rents VALUES (%s,%s,%s,%s,%s,%s,%s)"
        for bookid, cost in zip(cart,item_cost):
            cursor.execute(query_rental, (customer_id, bookid, start_date, due_date,None,"Not yet returned",cost))
            database.commit()
        messagebox.showinfo("Successful", "Customer ID: {}\nNumber of Books rented: {}\nTotalcost: {}".format(customer_id,book_count,total_rental_cost))
        cart = []
        total_rental_cost = 0
        item_cost = []
        book_count = 0
        frame_destroy()

def search_customer_to_rent(search_entry):
    try:
        table_destroy()
        table_update()
    except:
        pass

    
     #define columns of the table
    table ["columns"] = ("Customer ID", "Name", "Phone Number", "Address", "Valid ID", "Photo")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Customer ID", width = 95, anchor = CENTER, stretch = NO)
    table.column("Name", width = 290, anchor = CENTER)
    table.column("Phone Number", width = 135, anchor = CENTER)
    table.column("Address", width = 195, anchor = CENTER)
    table.column("Valid ID", width = 180, anchor = CENTER)
    table.column("Photo",  width = 180, anchor = CENTER)
    #table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Customer ID", text = "Customer ID", anchor = CENTER )
    table.heading("Name", text = "Full Name", anchor = CENTER )
    table.heading("Phone Number", text = "Phone Number", anchor = CENTER )
    table.heading("Address", text = "Address", anchor = CENTER )
    table.heading("Valid ID", text = "Valid ID", anchor = CENTER)
    table.heading("Photo", text = "Photo",  anchor = CENTER)
    # table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    search_query = "SELECT * FROM customer WHERE CustomerID LIKE %s or Name LIKE %s or PhoneNumber LIKE %s or Address LIKE %s"
    data = (search_entry.get(), search_entry.get(), search_entry.get(), search_entry.get(),)
    search_entry.delete(0,END)
    cursor.execute(search_query, data)

    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")
    
    for customer in cursor:
        if count % 2 == 0:
            table.insert(parent = '', index='end', iid = count, values = (customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]), tags=("odd",))
        else:
             table.insert(parent = '', index='end', iid = count, values = (customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]), tags=("even",))
        count += 1

    table.grid(row=2, column=0, rowspan=6, columnspan=7)

def pick_customer_to_rent():
    try: #destroys existing frames from other display
        frame_destroy()
        table_destroy()
    except:
        pass
    
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="NW", pady = 20, padx = 50)

    select_customer_title = Label(frame, text= "Select Customer to Rent", background = "#2f2f2d", font = ("Open Sans", 14, "bold"), fg="white" )
    select_customer_title.grid(row=0, column=0, sticky=NSEW, columnspan = 6, pady=10, padx=(155,0))

    search_entry = Entry(frame, width = 20, fg = "Black", font= ("Open Sans", 10, "bold"))
    search_entry.grid(row=1, column=5, sticky=E, pady = 5, padx = (770,5))

    search_button = Button(frame, text = "Seacrh", font= ("Open Sans", 10, "bold"), padx = 20, fg = "White", background = "royal blue", command= lambda: search_customer_to_rent(search_entry))
    search_button.grid(row=1, column=6, sticky=E, pady = 5, padx = (0,15))

     #define columns of the table
    table ["columns"] = ("Customer ID", "Name", "Phone Number", "Address", "Valid ID", "Photo")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Customer ID", width = 95, anchor = CENTER, stretch = NO)
    table.column("Name", width = 290, anchor = CENTER)
    table.column("Phone Number", width = 135, anchor = CENTER)
    table.column("Address", width = 195, anchor = CENTER)
    table.column("Valid ID", width = 180, anchor = CENTER)
    table.column("Photo",  width = 180, anchor = CENTER)
    #table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Customer ID", text = "Customer ID", anchor = CENTER )
    table.heading("Name", text = "Full Name", anchor = CENTER )
    table.heading("Phone Number", text = "Phone Number", anchor = CENTER )
    table.heading("Address", text = "Address", anchor = CENTER )
    table.heading("Valid ID", text = "Valid ID", anchor = CENTER)
    table.heading("Photo", text = "Photo",  anchor = CENTER)
    # table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    display_customer_query = "SELECT * FROM customer"
    cursor.execute(display_customer_query)
    
    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for customer_details in cursor:
        if count % 2 == 0:
            table.insert(parent = '', index='end', iid = count, values = (customer_details[0], customer_details[1], customer_details[2], customer_details[3], customer_details[4], customer_details[5]), tags = ("odd",))
        else:
             table.insert(parent = '', index='end', iid = count, values = (customer_details[0], customer_details[1], customer_details[2], customer_details[3], customer_details[4], customer_details[5]), tags = ("even",))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=7)

    def get_data():
        global num_rented_book
        selected = table.focus()
        values = table.item(selected, "values")
        cursor.execute("SELECT ReturnStatus FROM rents WHERE CustomerID=%s",(values[0],))

        for status in cursor:
            if status[0] == "Not yet returned":
                num_rented_book += 1

        if num_rented_book + len(cart) >= 5:
            messagebox.showinfo("Maximum", "Exceed number of books rented!")
            num_rented_book = 0
            return
        num_rented_book = 0
        rent_book(values[0], values[1])

    enter_button = Button(frame, text="Enter", background = "royal blue", fg = "white", font = ("Open Sans", 12, "bold"), padx = 30, pady = 10, command = get_data)
    enter_button.grid(row=9, column=0 , sticky = N, pady=20, columnspan = 6, padx = (150, 0))

def search_rentals(search_entry):
    try:
        table_destroy()
        table_update()
    except:
        pass

    #define columns of the table
    table ["columns"] = ("Customer ID", "Customer Name", "Book ID", "Start Date", "Due Date", "Return Date", "Return Status", "Cost")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Customer ID", width = 120, anchor = CENTER, stretch = NO)
    table.column("Customer Name", width = 175, anchor = CENTER, stretch = NO)
    table.column("Book ID", width =120, anchor = CENTER)
    table.column("Start Date", width = 140, anchor = CENTER)
    table.column("Due Date", width = 140, anchor = CENTER)
    table.column("Return Date", width = 140, anchor = CENTER)
    table.column("Return Status", width = 140, anchor = CENTER)
    table.column("Cost",  width = 80, anchor = CENTER)
    #table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Customer ID", text = "Customer ID", anchor = CENTER )
    table.heading("Customer Name", text = "Customer Name", anchor = CENTER )
    table.heading("Book ID", text = "Book ID", anchor = CENTER )
    table.heading("Start Date", text = "Start Date", anchor = CENTER )
    table.heading("Due Date", text = "Due Date", anchor = CENTER )
    table.heading("Return Date", text = "Return Date", anchor = CENTER)
    table.heading("Return Status", text = "Return Status",  anchor = CENTER)
    table.heading("Cost", text = "Cost",  anchor = CENTER)
    # table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    search_query= "SELECT rents.CustomerID, customer.Name, rents.BookID, rents.StartDate, rents.DueDate, rents.ReturnDate, rents.ReturnStatus, rents.PaymentCost FROM book_rental.rents INNER JOIN customer ON rents.CustomerID = customer.CustomerID WHERE rents.CustomerID LIKE %s or customer.Name LIKE %s or rents.BookID LIKE %s"
    data = (search_entry.get(), search_entry.get(), search_entry.get(),)
    search_entry.delete(0,END)
    cursor.execute(search_query, data)
    
    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")

    for rents_col in cursor:
        if count % 2 == 0:
            table.insert(parent = '', index='end', iid = count, values = (rents_col[0],rents_col[1],rents_col[2], rents_col[3], rents_col[4], rents_col[5], rents_col[6], rents_col[7]), tags=("odd",))
        else:
            table.insert(parent = '', index='end', iid = count, values = (rents_col[0],rents_col[1],rents_col[2], rents_col[3], rents_col[4], rents_col[5], rents_col[6], rents_col[7]), tags=("even",))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=7)

def display_rentals():
    try: #destroys existing frames from other display
        frame_destroy()
        table_destroy()
    except:
        pass
    
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="NW", pady = 20, padx = 50)

    rentals_title = Label(frame, text= "Book Rentals", background = "#2f2f2d", font = ("Open Sans", 18, "bold"), fg="white" )
    rentals_title.grid(row=0, column=0, sticky=N, columnspan = 6, pady=10, padx = (140, 0))

    search_button = Button(frame, text= "Search",  background = "royal blue", font = ("Open Sans", 10, "bold"), fg="white", padx = 20, command = lambda: search_rentals(search_entry))
    search_button.grid(row=1, column=6, sticky = E, pady=5, padx = (0,15))

    search_entry = Entry(frame, width=20,fg='black', font=('Open Sans',10, 'bold'), borderwidth=1, background="white")
    search_entry.grid(row=1, column=5, sticky=E, padx = (750,5), pady=5)

    #define columns of the table
    table ["columns"] = ("Customer ID", "Customer Name", "Book ID", "Start Date", "Due Date", "Return Date", "Return Status", "Cost")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Customer ID", width = 120, anchor = CENTER, stretch = NO)
    table.column("Customer Name", width = 175, anchor = CENTER, stretch = NO)
    table.column("Book ID", width =120, anchor = CENTER)
    table.column("Start Date", width = 140, anchor = CENTER)
    table.column("Due Date", width = 140, anchor = CENTER)
    table.column("Return Date", width = 140, anchor = CENTER)
    table.column("Return Status", width = 140, anchor = CENTER)
    table.column("Cost",  width = 80, anchor = CENTER)
    #table.column("Availability",  width = 115, anchor = CENTER)

    #create headings
    table.heading("0")
    table.heading("Customer ID", text = "Customer ID", anchor = CENTER )
    table.heading("Customer Name", text = "Customer Name", anchor = CENTER )
    table.heading("Book ID", text = "Book ID", anchor = CENTER )
    table.heading("Start Date", text = "Start Date", anchor = CENTER )
    table.heading("Due Date", text = "Due Date", anchor = CENTER )
    table.heading("Return Date", text = "Return Date", anchor = CENTER)
    table.heading("Return Status", text = "Return Status",  anchor = CENTER)
    table.heading("Cost", text = "Cost",  anchor = CENTER)
    # table.heading("Availability", text = "Availability",  anchor = CENTER)

    count = 0
    display_rents_query = "SELECT rents.CustomerID, customer.Name, rents.BookID, rents.StartDate, rents.DueDate, rents.ReturnDate, rents.ReturnStatus, rents.PaymentCost FROM book_rental.rents INNER JOIN customer ON rents.CustomerID = customer.CustomerID"
    cursor.execute(display_rents_query)

    table.tag_configure('even', background = "#2f2f2d")
    table.tag_configure('odd', background = "#2b2a27")
    for rents_col in cursor:
        if count %2 == 0:
            table.insert(parent = '', index='end', iid = count, values = (rents_col[0],rents_col[1],rents_col[2], rents_col[3], rents_col[4], rents_col[5], rents_col[6], rents_col[7]), tags = ("odd", ))
        else:
            table.insert(parent = '', index='end', iid = count, values = (rents_col[0],rents_col[1],rents_col[2], rents_col[3], rents_col[4], rents_col[5], rents_col[6], rents_col[7]), tags = ("even", ))
        count += 1
    table.grid(row=2, column=0, rowspan=6, columnspan=7)

    def return_rent():
        selected = table.focus()
        values = table.item(selected, "values")
        if values[6] == "Returned":
            messagebox.showinfo("Invalid", "Book is already returned!")
            return
        else:
            date_today = date.today()
            cur_date = date_today.strftime("%Y-%m-%d") #once returned button is clickied, the return date is the current date
            #query to update the rent table, specifically the return status column
            query_update_return_status = "UPDATE rents SET  ReturnDate = %s, ReturnStatus = %s WHERE CustomerID = %s and BookID = %s"
            data = (cur_date, "Returned",  values[0], values[2],)
            cursor.execute(query_update_return_status, data)
            database.commit()
            #query to update the availability of the book to "Available" in the book table
            query_update_book_avlb = "UPDATE book SET Availability = %s WHERE BookID = %s"
            data = ("Available", values[2],)
            cursor.execute(query_update_book_avlb, data)
            database.commit()

            #replace values in the table once book is returned
            new_val = table.item(selected, text = "", values=(values[0], values[1], values[2], values[3], values[4], cur_date, "Returned", values[7]))

            messagebox.showinfo("Returned", "Book ID {} is now returned! by {} - {} .".format(values[2], values[0],values[1]))

    return_button = Button(frame, text="Return", background = "royal blue", fg = "white", font = ("Open Sans", 12, "bold"), padx = 30, pady = 10, command = return_rent)
    return_button.grid(row=8, column=0, sticky = N, pady=(10,5), padx = (150,0), columnspan = 6)

root = Tk()
root.title("Book Rental System")
root.geometry("1440x730")
root.configure(bg="#EEEEEE")

#UI for main layout
#use image coffee.jpg as root background
bg = ImageTk.PhotoImage(Image.open("images/bookstore.jpg"))
bg_lbl = Label(root, image = bg )
bg_lbl.grid(row=1, column=1, sticky=NSEW)

#frames, 
sidebar = LabelFrame(root, bg = "#2f2f2d", borderwidth = 2)
header = LabelFrame(root, bg= "#403b35", borderwidth = 1.5)
frame = Frame(root, bg="#F0F0F0", borderwidth=1.5)          #destroyed after every function
frame.config(bd=1, relief=SOLID)

#grid bar
sidebar.grid(row=1, column=0, sticky="ns", rowspan = 5)
header.grid(row=0, column=0, columnspan=6, sticky = "we")

#sidebar contents
title_home = Button(header, text='Book Rental System', font=("Open Sans", 17, "bold"), bg="#403b35", fg="white", padx = 30, pady=20, borderwidth = 0, command = frame_destroy)
title_home.grid(row=0, column = 0, columnspan=4)

#button icons

#buttons in the sidebar
display_book_button = Button(sidebar, text="Display\nBooks",  padx = 30, bg='#2f2f2d', fg = "white", font=("Open Sans", 14), borderwidth = 0, command = display_books) 
add_book_button = Button(sidebar, text="Add Books\nin the Inventory",  bg='#2f2f2d', fg = "white",padx = 30,font=("Open Sans", 14), borderwidth = 0, command= add_book_inventory)
display_customer_button = Button(sidebar, text="Display\nCustomer",  bg='#2f2f2d', fg = "white", padx = 30,font=("Open Sans", 14), borderwidth = 0, command= display_customers)
display_rentals_button =  Button(sidebar, text="Billing",  bg='#2f2f2d', fg = "white", padx = 30,font=("Open Sans", 14), borderwidth = 0, command= None)
rent_book_button =  Button(sidebar, text="Rent",  bg='#2f2f2d', fg = "white", padx = 30,font=("Open Sans", 14), borderwidth = 0, command=customer_type)
return_rentals_button = Button(sidebar, text="Return\nRentals",  bg='#2f2f2d', fg = "white", padx = 30,font=("Open Sans", 14), borderwidth = 0, command=display_rentals)

rent_book_button.grid(row=0, column=0, pady=20)
return_rentals_button.grid(row=1, column=0,pady=20)
display_customer_button.grid(row=2, column=0,  pady = 20)
display_book_button.grid(row=3, column=0, pady = 20)
display_rentals_button.grid(row=4, column=0, pady=20)
add_book_button.grid(row=5, column=0,  pady = 20)

#search button
search_button = Button(header, text="Search", bg='royalblue1',fg="white", padx = 20, font=("Open Sans", 10, "bold"), borderwidth = 0, command = None)
search_entry = Entry(header, width=20,fg='black', font=('Open Sans',12, 'bold'), borderwidth="2")

search_entry.grid(row=0, column=4, padx=(600,0))
search_button.grid(row=0, column=5,padx=(5,0))

#role label and entry
role_lbl = Label(header, text = "User:", fg='white', font=('Open Sans',10, 'bold'), borderwidth=0, background="#403b35")
role_lbl.grid(row=0, column=6, padx= (10,2))
role_entry = Entry(header, width=20,fg='white', font=('Open Sans',10, 'bold'), borderwidth=0, background="#403b35")
role_entry.grid(row=0, column=7, padx= (0,2))

#initally state of these buttons are disabled until user succesfully log in
display_book_button ["state"] = DISABLED
add_book_button ["state"] = DISABLED
display_customer_button ["state"] = DISABLED
display_rentals_button ["state"] = DISABLED
rent_book_button ["state"] = DISABLED
return_rentals_button ["state"] = DISABLED 
search_button ["state"] = DISABLED 

#initialize table and map its style
table = ttk.Treeview(frame, height = 12)

#table style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background = "#2f2f2d", rowheight = 30, fieldbackground="#2f2f2d")
style.configure("Treeview",font=("Montserrat", 12), foreground = "white")
style.configure("Treeview.Heading",font=("Montserrat", 12),  background = "#2f2f2d", foreground = "white")
style.map("Treeview", background=[("selected", "#403b35")])
style.map("Treeview", foreground=[("selected", "white")])

login(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_book_button, search_button, role_entry, return_rentals_button)

root.mainloop()