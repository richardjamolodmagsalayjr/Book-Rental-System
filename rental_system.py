from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import re
import mysql.connector
from tkinter import ttk

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
    del_prompt = messagebox.askyesno("Delete student data", "Are you sure to delete it?") 
    if del_prompt:
        del_data = table.selection()[0] #deletes selected data in treeview
        table.delete(del_data)
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
    del_prompt = messagebox.askyesno("Delete data", "Are you sure to delete it?") 
    if del_prompt:
        del_data = table.selection()[0] #deletes selected data in treeview
        table.delete(del_data)
        cursor.execute(delete_query, (book_id_entry.get(),))
        database.commit()
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
            values = table.item(selected, text = "", values=(customer_id_entry.get(), name_entry.get(), phonenum_entry.get(), address_entry.get(), val_id_entry.get()))
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
            messagebox.showerror("Error", "Book ID {} is already taken. Please provide unique Book ID".format(book_id_entry.get()))

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

def display_customers():
    try:
        frame_destroy()
        table_destroy()
    except:
        pass
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=7, sticky="nw", pady = 50, padx = 80)
    
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
    for customer_details in cursor:
        table.insert(parent = '', index='end', iid = count, values = (customer_details[0], customer_details[1], customer_details[2], customer_details[3], customer_details[4], customer_details[5]))
        count += 1
    table.grid(row=0, column=0, rowspan=6, columnspan=7)

    #entry boxes for update book info
    header = ["Customer ID", "Full Name", "Phone Number", "Address", "Valid ID", "Photo"]
    for item in range(6):

        if item == 1:
            e = Entry(frame, width=20, font=('Helvetica',8, "bold"), justify = CENTER)
            e.grid(row=6, column=item,sticky = NSEW) 
            e.insert(END, header[item])
            e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
        else:
            if item == 1:
                e = Entry(frame, width=10, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW, padx = 5) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
            else:
                e = Entry(frame, width=12, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    # entry for update inputs
    customer_id_entry = Entry(frame, width=20, font=('Helvetica',8), justify = CENTER)
    customer_id_entry.grid(row = 7, column = 0, sticky = NSEW)

    name_entry = Entry(frame, width=30, font=('Helvetica',8), justify = CENTER)
    name_entry.grid(row = 7, column = 1, sticky = NSEW)

    phonenum_entry = Entry(frame, width=20, font=('Helvetica',8), justify = CENTER)
    phonenum_entry.grid(row = 7, column = 2, sticky = NSEW)

    address_entry = Entry(frame, width=35, font=('Helvetica',8), justify = CENTER)
    address_entry.grid(row = 7, column = 3, sticky = NSEW)

    val_id_entry = Entry(frame, width=35, font=('Helvetica',8), justify = CENTER)
    val_id_entry.grid(row = 7, column = 4, sticky = NSEW)

    photo_entry = Entry(frame, width=35, font=('Helvetica',8), justify = CENTER)
    photo_entry.grid(row = 7, column = 5, sticky = NSEW)

    # avlb_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    # avlb_entry.grid(row = 7, column = 6, sticky = NSEW)

    edit_button = Button(frame, text="Edit", padx =33, pady = 10, state = "disabled",  borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command= lambda: edit_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button, orig_customerid))
    edit_button.grid(row=8, column=2, pady = 5, padx = 15, sticky=E)

    del_button = Button(frame, text="Delete", padx =25, pady = 10, state = "disabled",  borderwidth = "2", bg='#e64e4e', fg = "white", font=("Open Sans", 8, "bold"), command= lambda: delete_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button, orig_customerid))
    del_button.grid(row=8, column=4, pady = 5, sticky=W, padx = 15)

    select_button = Button(frame, text="Select Data", padx =25, pady = 10, borderwidth = "2", bg='#B99976', fg = "black", font=("Open Sans", 8, "bold"), command=lambda: select_customer(customer_id_entry, name_entry, phonenum_entry, address_entry, val_id_entry, photo_entry, del_button, edit_button))
    select_button.grid(row=8, column=3 , pady = 5, sticky=N, padx = 15)

def display_books():
    try:
        frame_destroy()
        table_destroy()
    except:
        pass
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="nw", pady = 50, padx = 80)
    
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
    for book_item in cursor:
        table.insert(parent = '', index='end', iid = count, values = (book_item[0], book_item[1], book_item[2], book_item[3], book_item[4], book_item[5], book_item[6]))
        count += 1
    table.grid(row=0, column=0, rowspan=6, columnspan=7)

    #entry boxes for update book info
    header = ["Book ID", "Title", "Publisher", "ISBN", "Year Published", "Book Cost", "Availability"]
    for item in range(7):

        if item == 1:
            e = Entry(frame, width=20, font=('Helvetica',8, "bold"), justify = CENTER)
            e.grid(row=6, column=item,sticky = NSEW) 
            e.insert(END, header[item])
            e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
        else:
            if item == 1:
                e = Entry(frame, width=10, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW, padx = 5) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
            else:
                e = Entry(frame, width=12, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    # entry for update inputs
    book_id_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    book_id_entry.grid(row = 7, column = 0, sticky = NSEW)

    title_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    title_entry.grid(row = 7, column = 1, sticky = NSEW)

    publisher_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    publisher_entry.grid(row = 7, column = 2, sticky = NSEW)

    isbn_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    isbn_entry.grid(row = 7, column = 3, sticky = NSEW)

    yearpub_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    yearpub_entry.grid(row = 7, column = 4, sticky = NSEW)

    bookcost_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    bookcost_entry.grid(row = 7, column = 5, sticky = NSEW)

    avlb_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    avlb_entry.grid(row = 7, column = 6, sticky = NSEW)

    edit_button = Button(frame, text="Edit", padx =33, pady = 10, state = "disabled",  borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command=lambda: edit_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button, orig_bookid))
    edit_button.grid(row=8, column=2, pady = 5, padx = 15, sticky=W)

    del_button = Button(frame, text="Delete", padx =25, pady = 10, state = "disabled",  borderwidth = "2", bg='#e64e4e', fg = "white", font=("Open Sans", 8, "bold"), command=lambda: delete_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button, orig_bookid))
    del_button.grid(row=8, column=4, pady = 5, sticky=W, padx = 15)

    select_button = Button(frame, text="Select Data", padx =25, pady = 10, borderwidth = "2", bg='#B99976', fg = "black", font=("Open Sans", 8, "bold"), command=lambda: select_book(book_id_entry, title_entry, publisher_entry, isbn_entry, yearpub_entry, bookcost_entry, avlb_entry, del_button, edit_button))
    select_button.grid(row=8, column=3 , pady = 5, sticky=W, padx = 15)

def login(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry):
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
        username_lbl.grid(row=1, column=0, sticky = W,pady=20, padx = 20)
        username_entry = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        username_entry.grid(row=2, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        password_lbl = Label(frame,text= "Password", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        password_lbl.grid(row=3, column=0, sticky = W, pady=20, padx = 20)
        password_entry = Entry(frame, font=('Helvetica',14, "bold"), width=50)
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
        signin_button = Button(frame, text="Sign in", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10, "bold"), borderwidth = 0, command = lambda: signin(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry))
        signin_button.grid(row=7, column=1, sticky = W, pady = (5,20), padx= 50)

    except:
        messagebox.showerror("Error", "Incorrect username or password")

def signin(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry):
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
        username_lbl.grid(row=1, column=0, sticky = W,pady=20, padx = 20)
        username_entry = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        username_entry.grid(row=2, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        password_lbl = Label(frame,text= "Password", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        password_lbl.grid(row=3, column=0, sticky = W, pady=20, padx = 20)
        password_entry = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        password_entry.grid(row=4, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        role_lbl = Label(frame,text= "Role", background = "#2f2f2d", fg = "white", font = ("Open Sans", 14))
        role_lbl.grid(row=5, column=0, sticky = W, pady=20, padx = 20)
        role_ent = Entry(frame, font=('Helvetica',14, "bold"), width=50)
        role_ent.grid(row=6, column = 0, columnspan = 3, sticky = NSEW, padx = 20)

        def getdata():
            try:
                user_data = []
                if username_entry.get() != "" and password_entry.get() != "" and role_ent.get() != "":
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
        login_button = Button(frame, text="Log in", background = "#2f2f2d", fg = "white", font = ("Open Sans", 10, "bold"), borderwidth = 0, command = lambda: login(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry))
        login_button.grid(row=9, column=1, sticky = W, pady = (5,20), padx= 50)

    except:
        pass

def rent():
    try: #destroys existing frames from other display
        frame_destroy()
        table_destroy()
    except:
        pass

    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="nw", pady = 50, padx = 80)

    new_customer_button = Button(frame, )

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
display_book_button = Button(sidebar, text="Display\nBooks",  padx = 30, bg='#2f2f2d', fg = "white", font=("Open Sans", 12), borderwidth = 0, command = display_books) 
add_book_button = Button(sidebar, text="Add Books\nin the Inventory",  bg='#2f2f2d', fg = "white",padx = 30,font=("Open Sans", 12), borderwidth = 0, command=None)
display_customer_button = Button(sidebar, text="Display\nCustomer",  bg='#2f2f2d', fg = "white", padx = 30,font=("Open Sans", 12), borderwidth = 0, command= display_customers)
display_rentals_button =  Button(sidebar, text="Display\nRentals",  bg='#2f2f2d', fg = "white", padx = 30,font=("Open Sans", 12), borderwidth = 0, command=None)
rent_button =  Button(sidebar, text="Rent",  bg='#2f2f2d', fg = "white", padx = 30,font=("Open Sans", 12), borderwidth = 0, command=None)
display_book_button.grid(row=0, column=0, pady = 20)
add_book_button.grid(row=1, column=0,  pady = 20)
display_customer_button.grid(row=2, column=0,  pady = 20)
display_rentals_button.grid(row=3, column=0, pady=20)
rent_button.grid(row=4, column=0, pady=20)


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
rent_button ["state"] = DISABLED
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

login(display_book_button, add_book_button, display_customer_button, display_rentals_button, rent_button, search_button, role_entry)

root.mainloop()