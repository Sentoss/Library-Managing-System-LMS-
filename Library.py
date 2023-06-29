import gi, random, string, json
from datetime import date, timedelta
import pandas as pd
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Add_Book(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add a Book", modal=True)

        self.placementlabel= Gtk.Label(label="Placement")
        self.placement = Gtk.Entry()
        self.ISBNlabel = Gtk.Label(label="ISBN")
        self.ISBN = Gtk.Entry()
        self.copieslabel = Gtk.Label(label="Copies")
        self.copies = Gtk.SpinButton.new_with_range(1, 50,1)
        self.titlelabel = Gtk.Label(label="Title")
        self.title = Gtk.Entry()
        self.authorlabel = Gtk.Label(label="Author")
        self.author = Gtk.Entry()
        self.languagelabel = Gtk.Label(label="Language")
        self.language = Gtk.Entry()
        self.Enter = Gtk.Button.new_with_label("Add Book")

        self.grid = Gtk.Grid()
        self.grid.attach(self.placementlabel, 0, 0, 1, 1)
        self.grid.attach(self.ISBNlabel,      0, 1, 1, 1)
        self.grid.attach(self.copieslabel,    0, 2, 1, 1)
        self.grid.attach(self.titlelabel,     0, 3, 1, 1)
        self.grid.attach(self.authorlabel,    0, 4, 1, 1)
        self.grid.attach(self.languagelabel,  0, 5, 1, 1)
        self.grid.attach(self.placement,      1, 0, 1, 1)
        self.grid.attach(self.ISBN,           1, 1, 1, 1)
        self.grid.attach(self.copies,         1, 2, 1, 1)
        self.grid.attach(self.title,          1, 3, 1, 1)
        self.grid.attach(self.author,         1, 4, 1, 1)
        self.grid.attach(self.language,       1, 5, 1, 1)
        box = self.get_content_area()
        box.add(self.grid)
        self.add_action_widget(self.Enter, Gtk.ResponseType.OK)
        self.show_all()

    def book_values(self):
        vals = [self.placement.get_text(), self.ISBN.get_text(),
                self.title.get_text(), self.author.get_text(), 
                self.language.get_text(), True, self.copies.get_value_as_int()]
        for i in vals:
            if type(i) == str:
                if i == '':
                    raise ValueError("Empty Field")
        self.response(-10)
        return vals


class Add_Member(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add a Member", modal=True)

        self.IDlabel = Gtk.Label(label="ID")
        self.ID = Gtk.Entry()
        self.namelabel = Gtk.Label(label="Name")
        self.name = Gtk.Entry()
        self.numberlabel = Gtk.Label(label="Number")
        self.number = Gtk.Entry()
        self.yearlabel = Gtk.Label(label="Year")
        self.year = Gtk.SpinButton.new_with_range(1, 4, 1)
        self.Enter = Gtk.Button.new_with_label("Add Member")

        self.grid = Gtk.Grid()
        self.grid.attach(self.IDlabel,      0, 0, 1, 1)
        self.grid.attach(self.namelabel,    0, 1, 1, 1)
        self.grid.attach(self.numberlabel,  0, 2, 1, 1)
        self.grid.attach(self.yearlabel,    0, 3, 1, 1)
        self.grid.attach(self.ID,           1, 0, 1, 1)
        self.grid.attach(self.name,         1, 1, 1, 1)
        self.grid.attach(self.number,       1, 2, 1, 1)
        self.grid.attach(self.year,         1, 3, 1, 1)
        box = self.get_content_area()
        box.add(self.grid)
        self.add_action_widget(self.Enter, Gtk.ResponseType.OK)
        self.show_all()

    def member_values(self):
        vals = [self.ID.get_text(), self.name.get_text(),
                self.number.get_text(), self.year.get_value_as_int()]
        for i in vals:
            if type(i) == str:
                if i == '':
                    raise ValueError("Empty Field")
        self.response(-10)
        return vals


class LibraryUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Library Manager")
        self.set_border_width(10)
        #self.maximize()
        self.set_default_size(880, 375)
        
        self.Labelsdict = {'mainstore' : ['Member', 'ID', 'Title', 'Placement', 'ISBN', 'Due Date', 'Copies Left'],
                           'Booksinfo' : ['Placement', 'ISBN', 'Title', 'Author', 'Language', 'Available', 'Copies'],
                           'bSearchfield' : ['Placement', 'ISBN', 'Title', 'Author', 'Language'],
                           'Members' : ['ID', 'Name', 'Phone Number', 'Year'],
                           'mSearchfield' : ['ID', 'Name', 'Phone Number', 'Year']}

        
        self.navigation = Gtk.Notebook()
        self.maintab = Gtk.Grid()
        self.bookstab = Gtk.Grid()
        self.memberstab = Gtk.Grid()
        self.settingstab = Gtk.Grid()
        self.navigation.append_page(self.maintab, Gtk.Label(label="Main"))
        self.navigation.append_page(self.bookstab, Gtk.Label(label="Books"))
        self.navigation.append_page(self.memberstab, Gtk.Label(label="Members"))
        self.navigation.append_page(self.settingstab, Gtk.Label(label="Settings"))
        
        ####### THE MAIN MENU
        
        ### mainsearch = the area that contains the labels and entry boxes for Book Placement and Member ID 
        self.mainsearch = Gtk.Box(spacing=10)
        self.mainsearch.set_hexpand(True)
        self.maintab.attach(self.mainsearch, 0, 0, 1, 1)
        
        ### Memberbox = the container for the member ID label and entry box
        self.memberbox = Gtk.Box(spacing=10)
        self.memberentry = Gtk.Entry()
        self.memberLabel = Gtk.Label(label="Member ID:")
        self.memberbox.pack_start(self.memberLabel, False, False, 0)
        self.memberbox.pack_end(self.memberentry, True, True, 0)

        ### bookbox = the container for the book ID label and entry box
        self.bookbox = Gtk.Box(spacing=10)
        self.bookentry = Gtk.Entry()
        self.bookLabel = Gtk.Label(label="Book Placement:")
        self.bookbox.pack_start(self.bookLabel, False, False, 0)
        self.bookbox.pack_end(self.bookentry, True, True, 0)
        
        # Appending the bookbox and memberbox to the mainsearch area
        self.mainsearch.pack_start(self.memberbox, True, True, 0)
        self.mainsearch.pack_end(self.bookbox, True, True, 0)
        
        #create the data holder (the list store) and the view for said data
        self.mainstore = Gtk.ListStore(str, str, str, str, str, str, int)
        self.mainview = Gtk.TreeView(model=self.mainstore)
        # Wrap the view in a scrolled window
        self.mainscroll = Gtk.ScrolledWindow()
        self.mainscroll.set_propagate_natural_width(True)
        self.mainscroll.set_propagate_natural_height(True)
        self.mainscroll.add(self.mainview)

        self.maintab.attach_next_to(self.mainscroll, self.mainsearch, Gtk.PositionType.BOTTOM, 1, 1)
        
        #the buttons in the main menu, a box for them, and appending them to the maintab right next to the table
        self.mainbuttons = Gtk.Box(orientation=1, spacing=5)
        self.Issuebutton = Gtk.Button.new_with_label("Issue")
        self.Issuebutton.connect("clicked", self.Issue)
        self.Returnbutton = Gtk.Button.new_with_label("Return")
        self.Returnbutton.connect("clicked", self.Return)
        self.mainbuttons.pack_start(self.Issuebutton, False, False, 0)
        self.mainbuttons.pack_start(self.Returnbutton, False, False, 0)
        self.maintab.attach_next_to(self.mainbuttons, self.mainscroll, Gtk.PositionType.RIGHT, 1, 1)
        
        ###### BOOKS MENU
        
        # The Search bar for the books
        self.searchbox = Gtk.Box(spacing=10)
        self.searchbox.set_hexpand(True)
        self.booksearch = Gtk.Entry()
        self.SearchCombo = Gtk.ComboBoxText()
        self.SearchCombo.connect('changed', self.set_search_bcolumn)
        self.searchbox.pack_start(self.booksearch, True, True, 0)
        self.searchbox.pack_end(self.SearchCombo, True, True, 0)
        self.bookstab.attach(self.searchbox, 0, 0, 1, 2)
        
        #create the data holder (the list store) and the view for said data
        self.Booksinfo = Gtk.ListStore(str, str, str, str, str, bool, int)
        self.Bookstable = Gtk.TreeView(model=self.Booksinfo)

        # Wrap the view in a scrolled window
        self.Bookscroll = Gtk.ScrolledWindow()
        self.Bookscroll.add(self.Bookstable)
        self.Bookscroll.set_propagate_natural_width(True)
        self.Bookscroll.set_propagate_natural_height(True)
        self.bookstab.attach_next_to(self.Bookscroll, self.searchbox, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Book's area Buttons
        self.booksbuttons = Gtk.Box(orientation=1, spacing=5)
        self.Removebutton = Gtk.Button.new_with_label("Remove")
        self.Removebutton.connect("clicked", self.Remove_book)
        self.Addbutton = Gtk.Button.new_with_label("Add")
        self.Addbutton.connect("clicked", self.bookadd)
        self.booksbuttons.pack_start(self.Addbutton, False, False, 0)
        self.booksbuttons.pack_start(self.Removebutton, False, False, 0)
        self.bookstab.attach_next_to(self.booksbuttons, self.Bookscroll, Gtk.PositionType.RIGHT, 1, 1)
        
        # MAIN MENU: the settings for the combo box for choosing the book
        # self.bookcombo.set_model(self.Booksinfo)
        # self.booktext = Gtk.CellRendererText()
        # self.bookcombo.pack_start(self.booktext, False)
        # self.bookcombo.add_attribute(self.booktext, "text", 1)

        ######## MEMBERS' MENU
        
        # The Search bar for the Members
        self.msearchbox = Gtk.Box(spacing=10)
        self.msearchbox.set_hexpand(True)
        self.membersearch = Gtk.Entry()
        self.mSearchCombo = Gtk.ComboBoxText()
        self.msearchbox.pack_start(self.membersearch, True, True, 0)
        self.msearchbox.pack_end(self.mSearchCombo, True, True, 0)
        self.memberstab.attach(self.msearchbox, 0, 0, 1, 1)
        self.mSearchCombo.connect('changed', self.set_search_mcolumn)

        #create the data holder (the list store) and the view for said data
        ###### YET TO IMPLEMENT THE FILTER/SEARCH FUNCTION
        self.Membersinfo = Gtk.ListStore(str, str, str, int)
        self.Memberstable = Gtk.TreeView(model=self.Membersinfo)

        # Wrap the view in a scrolled window
        self.Memberscroll = Gtk.ScrolledWindow()
        self.Memberscroll.add(self.Memberstable)
        self.Memberscroll.set_propagate_natural_width(True)
        self.Memberscroll.set_propagate_natural_height(True)
        self.memberstab.attach_next_to(self.Memberscroll, self.msearchbox, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Member's area Buttons
        self.memberbuttons = Gtk.Box(orientation=1, spacing=5)
        self.mRemovebutton = Gtk.Button.new_with_label("Remove")
        self.mRemovebutton.connect("clicked", self.Remove_member)
        self.mAddbutton = Gtk.Button.new_with_label("Add")
        self.mAddbutton.connect("clicked", self.memberadd)
        self.memberbuttons.pack_start(self.mAddbutton, False, False, 0)
        self.memberbuttons.pack_start(self.mRemovebutton, False, False, 0)
        self.memberstab.attach_next_to(self.memberbuttons, self.Memberscroll, Gtk.PositionType.RIGHT, 1, 1)

        # Member's data display
        self.membersdata = Gtk.TextView()
        self.membersdata.get_buffer().set_text("Please select a member to view their data")
        self.membersdata.set_editable(False)
        self.membersdata.set_cursor_visible(False)
        self.membersdata.set_justification(Gtk.Justification.LEFT)
        self.memberstab.attach_next_to(self.membersdata, self.Memberscroll, Gtk.PositionType.BOTTOM, 1, 1)

        # the settings for the combo box for choosing the member in the main menu
        # self.membercombo.set_model(self.Membersinfo) 
        # self.membertext = Gtk.CellRendererText()
        # self.membercombo.pack_start(self.membertext, False)
        # self.membercombo.add_attribute(self.membertext, "text", 0)

        # add the notebook (navigation bar and the pages) to Self/the window object, and set the labels for the tables/views
        self.setLabels()
        self.add(self.navigation)
        # self.populate()
        self.Memberstable.get_selection().connect("changed", self.DisplayData)

        # SEARCH IN BOOKS AND MEMBERS:
        ## Books
        self.Bookstable.set_enable_search(True)
        self.Bookstable.set_search_entry(self.booksearch)
        self.set_search_bcolumn(self.SearchCombo)

        ## Members
        self.Memberstable.set_enable_search(True)
        self.Memberstable.set_search_entry(self.membersearch)
        self.set_search_mcolumn(self.mSearchCombo)
    
        # The auto-completion for the member and book entries!!!

        #member
        self.comember = Gtk.EntryCompletion()
        self.comember.set_model(self.Membersinfo)
        self.comember.set_text_column(0)
        self.memberentry.set_completion(self.comember)
        self.comember.set_inline_selection(True)
        #book
        self.cobook = Gtk.EntryCompletion()
        self.cobook.set_model(self.Booksinfo)
        self.cobook.set_text_column(0)
        self.bookentry.set_completion(self.cobook)
        self.cobook.set_inline_selection(True)


        ## THE SETTINGS MENU
        ## export books
        self.exportButton = Gtk.Button.new_with_label("Export Books")
        self.exportButton.connect("clicked", self.export)
        self.importButton = Gtk.Button.new_with_label("Import Books")
        self.importButton.connect("clicked", self.importbooks)
        self.settingstab.attach(self.exportButton, 0, 0, 1, 1)
        self.settingstab.attach(self.importButton, 0, 1, 1, 1)

        self.importbooks(None)
        self.importMembers()
        self.importMain()
    def setLabels(self):
        renderer = Gtk.CellRendererText()
        
        for z in self.Labelsdict['mainstore']:
            index = self.Labelsdict['mainstore'].index(z)
            column = Gtk.TreeViewColumn(z, renderer, text=index)
            column.set_sort_column_id(index)
            column.set_expand(True)
            #column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            self.mainview.append_column(column)
                
        for z in self.Labelsdict['Booksinfo']:
            index = self.Labelsdict['Booksinfo'].index(z)
            column = Gtk.TreeViewColumn(z, renderer, text=index)
            column.set_expand(True)
            column.set_sort_column_id(index)
            self.Bookstable.append_column(column)
        
        for z in self.Labelsdict['Members']:
            index = self.Labelsdict['Members'].index(z)
            column = Gtk.TreeViewColumn(z, renderer, text=index)
            column.set_expand(True)
            column.set_sort_column_id(index)
            self.Memberstable.append_column(column)
         
        for z in self.Labelsdict['bSearchfield']:
            self.SearchCombo.append_text(z)
            
        for z in self.Labelsdict['mSearchfield']:
            self.mSearchCombo.append_text(z)
        
        self.SearchCombo.set_active(0)
        self.mSearchCombo.set_active(0)
        
    #Updating the search columns after changing the search criteria through the combo boxes
    #For the Books and Members tabs
    def set_search_bcolumn(self, combo):
        self.Bookstable.set_search_column(self.Labelsdict['bSearchfield'].index(self.SearchCombo.get_active_text()))

    def set_search_mcolumn(self, combo):
        self.Memberstable.set_search_column(self.Labelsdict['mSearchfield'].index(self.mSearchCombo.get_active_text()))

    # Return books function
    def Return(self, button, *args):
        if button != None:
            selection = self.mainview.get_selection()
            model, paths = selection.get_selected_rows()
            iter = self.mainstore.get_iter(paths[0])
            item = self.mainstore[iter]

            for i in self.mainstore:
                if item[3] == i[3]:
                    i[6] += 1

            for b in self.Booksinfo:
                if item[3] == b[0] and b[5] == False:
                    b[5] = True
                    break

            self.mainstore.remove(iter)

        else:
            item, iter = args

            for i in self.mainstore:
                if item[3] == i[3]:
                    i[6] += 1

            for b in self.Booksinfo:
                if item[3] == b[0] and b[5] == False:
                    b[5] = True
                    break

            self.mainstore.remove(iter)

    ## Replaced the Entry widgets with combo boxes for ease of use.
    def Issue(self, button):
        memberI = self.memberentry.get_text()
        bookI = self.bookentry.get_text()
        
        for item in self.Booksinfo:
            if bookI == item[0]:
                book = item

        for item in self.Membersinfo:
            if memberI == item[0]:
                member = item  

        if type(book) == str or type(member) == str:
            print("Incorrect Input! They are not in the tables!")
            message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                    buttons=Gtk.ButtonsType.OK, text="Please Enter Correct Information")
            message.run()
            message.destroy()
            return
        if book[5] == False:
            print("Sorry, book is not Available!")
            message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                    buttons=Gtk.ButtonsType.OK, text="Sorry, book is not available!")
            message.run()
            message.destroy()
            return

        copiesleft = book[6]  
        for m in self.mainstore:
            if m[3] == book[0]:
                copiesleft -= 1
                if m[1] == member[0]:
                    print("Member has already borrowed a copy of this book!")
                    message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                    buttons=Gtk.ButtonsType.OK,
                                                    text="Member has already borrowed a copy of this book!")
                    message.run()
                    message.destroy()
                    return

        due_date = date.today() + timedelta(days=14)
        if book[5]:
            copiesleft = copiesleft -1
            self.mainstore.append([member[1], member[0], book[2], book[0], book[1], str(due_date), copiesleft])
            for l in self.mainstore:
                if l[3] == book[0]:
                    l[6] = copiesleft

            if copiesleft == 0:
                book[5] = False

    def Remove_book(self, button):
        confirmation = True
        if confirmation:
            selected = self.Bookstable.get_selection()
            model, paths = selected.get_selected_rows()
            iter = self.Booksinfo.get_iter(paths[0])
            ISBN = self.Booksinfo[iter][0]

            # if you removed/deleted the book, then no one is currently borrowing it....right?
            for x in self.mainstore:
                if x[4] == ISBN:
                    self.mainstore.remove(x.iter)

            self.Booksinfo.remove(iter)

    def Remove_member(self, button):
        selected = self.Memberstable.get_selection()
        model, paths = selected.get_selected_rows()
        for path in paths:
            iter = self.Membersinfo.get_iter(path)
            ID = self.Membersinfo[iter][0]

            for x in self.mainstore:
                if x[1] == ID:
                    self.Return()

            self.Membersinfo.remove(iter)

    ## Fixed. Now it inserts at cursor position.
    def DisplayData(self, event):
        selected = self.Memberstable.get_selection()
        model, paths = selected.get_selected_rows()
        if selected.count_selected_rows() > 0:
            iter = self.Membersinfo.get_iter(paths[0])
            ID = self.Membersinfo[iter][0]
            if len(self.mainstore) > 0:
                self.membersdata.get_buffer().set_text("")
                found = False
                for item in self.mainstore:
                    if item[1] == ID:
                        found = True
                        self.membersdata.get_buffer().insert_at_cursor("Book Title: {}\nBook Placement: {}\nDue Date: {}\n\n".format(
                            item[2], item[3], item[5]))
                    if not found:
                        self.membersdata.get_buffer().set_text("User has no data")

    def bookadd(self, button):
        dialog = Add_Book(self)
        response = -5
        while response == -5:
            response = dialog.run()
            try:
                self.Booksinfo.append(dialog.book_values())
                dialog.destroy()
                break
            except Exception as x:
                if response != -4:
                    message = Gtk.MessageDialog(transient_for=dialog, message_type=Gtk.MessageType.INFO,
                                                buttons=Gtk.ButtonsType.OK, text="Please Enter Correct Information")
                    message.run()
                    message.destroy()
                    print(x)
       
        dialog.destroy()

    def memberadd(self, button):
        dialog = Add_Member(self)
        response = -5
        while response == -5:
            response = dialog.run()
            try:
                self.Membersinfo.append(dialog.member_values())
                dialog.destroy()
                break
            except Exception as x:
                if response != -4:
                    message = Gtk.MessageDialog(transient_for=dialog, message_type=Gtk.MessageType.INFO,
                                                buttons=Gtk.ButtonsType.OK, text="Please Enter Correct Information")
                    message.run()
                    message.destroy()
                    print(x)
       
        dialog.destroy()
        pass
    
    def export(self, button):
        with open("Books_Export.json", 'w', encoding='utf-8') as file:
            data = []
            xdict = {}
            for i in self.Booksinfo:
                for x in range(0, len(list(i))):
                    xdict[self.Labelsdict['Booksinfo'][x]] = list(i)[x]
                data.append(xdict)
                xdict = {}
            json.dump(data, file, indent=4, ensure_ascii=False)

        message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                buttons=Gtk.ButtonsType.OK, text="Export Successful!")
        message.run()
        message.destroy()
    
    def importbooks(self, button):
        if button != None:
            dialog = Gtk.FileChooserDialog(
                title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            )
            filter = Gtk.FileFilter()
            filter.add_mime_type("application/vnd.ms-excel")
            filter.add_mime_type("application/vnd.oasis.opendocument.spreadsheet")
            filter.add_mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            filter.add_mime_type("application/json")
            filter.set_name("xlsx, ods, Json files only")
            dialog.add_filter(filter)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                try:
                    file = dialog.get_filename()
                    extensions = ['.json', '.xlsx', '.ods']
                    item = []
                    for i in range(0, len(extensions)):
                        if extensions[0] in file:
                            with open(file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                for i in data:
                                    item = [i['Placement'], i['ISBN'], i['Title'], i['Author'],
                                                i['Language'], i['Available'], i['Copies']]
                                    self.Booksinfo.append(item)

                            message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                    buttons=Gtk.ButtonsType.OK, text="Import Successful!")
                            message.run()
                            message.destroy()
                            break
                        elif extensions[1] in file:
                            data = pd.read_excel(file)
                            for i in range(0, len(data)):
                                item = list(data.iloc[i])
                                for y in range(0, len(item)):
                                    if type(item[y]) == float:
                                        item[y] = ''
                                    elif type(item[y]) == int and item[y] != item[-1]:
                                        item[y] = str(item[y])
                                self.Booksinfo.append(item)
                            message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                    buttons=Gtk.ButtonsType.OK, text="Import Successful!")
                            message.run()
                            message.destroy()
                            break

                        elif extensions[2] in file:
                            data = pd.read_excel(file, engine='odf')
                            for i in range(0, len(data)):
                                item = list(data.iloc[i])
                                for y in range(0, len(item)):
                                    if type(item[y]) == float:
                                        item[y] = ''
                                    elif type(item[y]) == int and item[y] != item[-1]:
                                        item[y] = str(item[y])
                                self.Booksinfo.append(item)
                            message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                    buttons=Gtk.ButtonsType.OK, text="Import Successful!")
                            message.run()
                            message.destroy()
                            break
                    
                except Exception as x:
                    dialog.destroy()
                    message = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                                    buttons=Gtk.ButtonsType.OK, text="Error! Import Failed!\n{}".format(x))
                    message.run()
                    message.destroy()
                    print(x)
            elif response == Gtk.ResponseType.CANCEL:
                print("Cancel clicked")

            dialog.destroy()

        else:
            try:
                with open('Books.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for i in data:
                        item = [i['Placement'], i['ISBN'], i['Title'], i['Author'],
                                i['Language'], i['Available'], i['Copies']]
                        self.Booksinfo.append(item)
            except FileNotFoundError as x:
                print(type(x), x)
                with open('Books.json', 'w', encoding='utf-8'):
                    pass

    def importMembers(self):
        try:
            with open('Members.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for i in data:
                        item = [i['ID'], i['Name'], i['Phone Number'], i['Year']]
                        self.Membersinfo.append(item)
        except FileNotFoundError as x:
            print(type(x), x)
            with open('Members.json', 'w', encoding='utf-8'):
                pass

    def importMain(self):
        try:
            with open('Dashboard.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for i in data:
                        item = [i['Member'], i['ID'], i['Title'], i['Placement'],
                                i['ISBN'], i['Due Date'], i['Copies Left']]
                        self.mainstore.append(item)

            for i in range(1, len(self.mainstore) + 1):
                iiter = self.mainstore.get_iter(len(self.mainstore) - i)
                item = self.mainstore[iiter]
                exists = False
                if len(self.Membersinfo) > 0:
                    for m in self.Membersinfo:
                        if item[1] == m[0]:
                            exists = True

                    if not exists:
                        self.Return(None, item, iiter)
                else:
                    self.Return(None, item, iiter)
        except FileNotFoundError as x:
            print(type(x), x)
            with open('Dashboard.json', 'w', encoding='utf-8'):
                pass

    def save(self, parent):
        with open('Dashboard.json', 'w', encoding='utf-8') as f:
            data = []
            xdict = {}
            for i in self.mainstore:
                for x in range(0, len(list(i))):
                    xdict[self.Labelsdict['mainstore'][x]] = list(i)[x]
                data.append(xdict)
                xdict = {}
            json.dump(data, f, indent=4, ensure_ascii=False)

        with open('Books.json', 'w', encoding='utf-8') as f:
            data = []
            xdict = {}
            for i in self.Booksinfo:
                for x in range(0, len(list(i))):
                    xdict[self.Labelsdict['Booksinfo'][x]] = list(i)[x]
                data.append(xdict)
                xdict = {}
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        with open('Members.json', 'w', encoding='utf-8') as f:
            data = []
            xdict = {}
            for i in self.Membersinfo:
                for x in range(0, len(list(i))):
                    xdict[self.Labelsdict['Members'][x]] = list(i)[x]
                data.append(xdict)
                xdict = {}
            json.dump(data, f, indent=4, ensure_ascii=False)
        Gtk.main_quit()
window = LibraryUI()
window.connect('destroy', window.save)
window.show_all()
Gtk.main()