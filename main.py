import Member, Book, Populate, gi, random
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

Books = Populate.populatebook()
Members = Populate.populatemember()
Borrowed_Books = []
for x in Members:
    print(x.getInfo())

class LibraryManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Library Manager")
        self.set_border_width(10)
        
        #for now, per the parameters in the population script, we're gonna keep the
        #parameter for objects in this way: that the ISBN and placement are ints
        #it won't be difficult changing them later, but, let's keep it that way to
        #prioritize what's important
        self.Labelsdict = {'mainstore' : ['Member', 'ID', 'Title', 'Placement', 'ISBN', 'Due Date', 'Copies Left'],
                      'Booksinfo' : ['ISBN', 'Placement', 'Title', 'Author', 'Language', 'Available', 'Copies'],
                      'Searchfield' : ['ISBN', 'Placement', 'Title', 'Author', 'Language']}
        
        self.booksearch = Gtk.Entry()
        self.SearchCombo = Gtk.ComboBoxText()
        self.mainstore = Gtk.ListStore(str, int, str, int, int, str, int)
        self.Booksinfo = Gtk.ListStore(int, int, str, str, str, bool, int)
        self.Booksfilter = self.Booksinfo.filter_new()
        self.Booksfilter.set_visible_func(self.filterchoice)
        self.fillData()
        self.dashboard = Gtk.TreeView(model=self.mainstore)
        self.Booktable = Gtk.TreeView(model=self.Booksfilter)
        self.setLabels()
        
        self.navigation = Gtk.Notebook()
        self.add(self.navigation)
        
        #Grids
        self.Maintab = Gtk.Grid()
        self.Maintab.add(self.dashboard)
        self.MainButtonsGrid = Gtk.Grid()
        self.MainEntryGrid = Gtk.Grid()
        
        #Entries
        self.Memberentrylabel = Gtk.Label(label='Member ID')
        self.MemberEntry = Gtk.Entry()
        self.BookPlabel = Gtk.Label(label='Book Placement')
        self.BookPentry = Gtk.Entry()
        self.MainEntryGrid.attach(self.Memberentrylabel, 0, 0, 1, 1)
        self.MainEntryGrid.attach_next_to(self.MemberEntry, self.Memberentrylabel, Gtk.PositionType.RIGHT, 1, 1)
        self.MainEntryGrid.attach(self.BookPlabel, 0, 1, 1, 1)
        self.MainEntryGrid.attach_next_to(self.BookPentry, self.BookPlabel, Gtk.PositionType.RIGHT, 1, 1)
        self.MainEntryGrid.set_row_spacing(20)
        self.MainEntryGrid.set_column_spacing(10)
        
        #Buttons
        self.IssueButton = Gtk.Button(label='Issue')
        self.ReturnButton = Gtk.Button(label='Return')
        self.MainButtonsGrid.attach(self.IssueButton, 0, 0, 1, 1)
        self.MainButtonsGrid.attach_next_to(self.ReturnButton, self.IssueButton, Gtk.PositionType.BOTTOM, 1, 1)
        
        #Assimilation
        self.Maintab.attach_next_to(self.MainButtonsGrid, self.dashboard, Gtk.PositionType.RIGHT, 2, 2)
        self.Maintab.attach_next_to(self.MainEntryGrid, self.dashboard, Gtk.PositionType.TOP, 1, 1)
        self.navigation.append_page(self.Maintab, Gtk.Label(label="Main"))
        
        ##Books Tab UI
        #Grids       
        self.Bookstab = Gtk.Grid()
        self.ButtonGrid = Gtk.Grid()
        self.ContentGrid = Gtk.Grid()
        
        #Buttons
        self.Removebook = Gtk.Button(label='Remove')
        
        #Assimilation
        self.Bookstab.attach(self.ContentGrid, 0, 0, 2, 2)
        self.Bookstab.attach_next_to(self.ButtonGrid, self.ContentGrid, Gtk.PositionType.RIGHT, 1, 1)
        self.ContentGrid.attach(self.booksearch, 0, 0, 2, 2)
        self.ContentGrid.attach_next_to(self.Booktable, self.booksearch, Gtk.PositionType.BOTTOM, 2, 2)
        self.ButtonGrid.attach(self.SearchCombo, 0, 0, 1, 1)
        self.ButtonGrid.attach_next_to(self.Removebook, self.SearchCombo, Gtk.PositionType.BOTTOM, 1, 1)
        self.navigation.append_page(self.Bookstab, Gtk.Label(label="Books"))

        # Members tab UI
        # Grids
        self.Memberstab = Gtk.Grid()
        
        # Assimilation
        self.navigation.append_page(self.Memberstab, Gtk.Label(label="Members"))

        # Settings tab UI
        # Grids
        self.Settingstab = Gtk.Grid()
        
        #Assimilation
        self.navigation.append_page(self.Settingstab, Gtk.Label(label="Settings"))

        # UI-Function connections
        self.booksearch.connect('activate', self.search)
        self.Removebook.connect('clicked', self.removebook)
        self.IssueButton.connect('clicked', self.Issue)
        self.ReturnButton.connect('clicked', self.Return)
        
        
    # Set the labels for all the columns in all trees
    def setLabels(self):
        renderer = Gtk.CellRendererText()
        
        for z in self.Labelsdict['mainstore']:
            column = Gtk.TreeViewColumn(z, renderer, text=self.Labelsdict['mainstore'].index(z))
            self.dashboard.append_column(column)
                
        for z in self.Labelsdict['Booksinfo']:
            column = Gtk.TreeViewColumn(z, renderer, text=self.Labelsdict['Booksinfo'].index(z))
            self.Booktable.append_column(column)
        
        for z in self.Labelsdict['Searchfield']:
            self.SearchCombo.append_text(z)
        
        self.SearchCombo.set_active(1)

    # Fill the trees with the data. somewhat psuedo for now. *somewhat*
    def fillData(self):
        for x in Borrowed_Books:
            treeitr = self.mainstore.append(x)

        for y in Books:
            treeitr = self.Booksinfo.append(y.getInfo())
    
    def raiseLog(self, message):
            self.dialogue = Gtk.MessageDialog( transient_for=self, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text=message)
            self.dialogue.run()
            self.dialogue.destroy()

            
    def Issue(self, button):
        Book = self.BookPentry.get_text() 
        User = self.MemberEntry.get_text()
        
        try:
            for x in Books:
                if x.Placement == int(Book):
                    Book = x
                    break
                
            for y in Members:
                if int(User) == y.ID:
                    User = y
                    break

        except (ValueError, TypeError) as inst:
            self.raiseLog("Please enter correct information!")
            return
        
        if User == self.MemberEntry.get_text() or Book == self.BookPentry.get_text():
            self.raiseLog("Please enter correct information!")
            return
        
        for books in User.Active_Books:
            if Book == books:
                print("User already borrowed the book!")
                return
            
        for i in self.Booksinfo:
            if Book.Placement == i[1]:
                if Book.Available == False:
                    return False
                else:
                    Book.CopiesLeft = Book.CopiesLeft -1
                    if Book.CopiesLeft == 0:
                        Book.Available = False
                    Borrowed_Books.append([User.name, User.ID, Book.Title, 
                                          Book.Placement, Book.ISBN, 
                                          'Implement Due Date', Book.CopiesLeft])
            
                    User.Active_Books.append(Book)
                    self.mainstore.append(Borrowed_Books[len(Borrowed_Books)-1])
                    counter = 0
                    for object in self.mainstore:
                        if Book.Placement == object[3]:
                            object[6] = Book.CopiesLeft
                        

    def Return(self, button):
        selected = self.dashboard.get_selection()
        model, path = selected.get_selected_rows()
        if len(path) != 0:
            iter = self.mainstore.get_iter(path)
            ISBN = self.mainstore[iter][0]
            userID = self.mainstore[iter][1]
            self.mainstore.remove(iter)
            
            for book in Borrowed_Books:
                if book[1] == userID and book[3] == ISBN:
                    Borrowed_Books.remove(book)
                    
            for member in Members:
                if member.ID == userID:
                    user = member
                    break
                
            for z in user.Active_Books:
                if z.ISBN == ISBN:
                    user.Active_Books.remove(z)
                    break
            
        else:
            self.raiseLog('Please choose an item from the list before clicking!')
            return
                            
        
    def filterchoice(self, model, iter, data):
        self.index = self.SearchCombo.get_active()
        if self.booksearch.get_text() != '':
            if str(model[iter][self.index]).__contains__(self.booksearch.get_text()):
                return True
            else:
                return False
        else:
            return True
        
    def search(self, widget):
        self.Booksfilter.refilter()
    
    def removebook(self, button):
        selected = self.Booktable.get_selection()
        model, path = selected.get_selected_rows()
        if len(path) > 0:
            iter = self.Booksinfo.get_iter(path)
            ISBN = self.Booksinfo[iter][0]
            
            for x in self.mainstore:
                if ISBN == x[4]:
                    self.mainstore.remove(x.iter)
                
            for i in Books:
                if i.ISBN == self.Booksinfo[iter][0]:
                    Books.remove(i)
                    break
                
            for m in Members:
                for b in m.Active_Books:
                    if b.ISBN == ISBN:
                        m.Active_Books.remove(b)
                    
            self.Booksinfo.remove(iter)
            
        else:
            self.raiseLog('Please choose an item from the list before clicking!')
            return
        
window = LibraryManager()
window.connect('destroy', Gtk.main_quit)
window.show_all()
Gtk.main()