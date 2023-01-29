import Member, Book, Populate, gi, random
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#Books = [['Harry Potter', '1351351313'], ['The Ice Dragon', '1351351312'],
        # ['Les Mots et Les Choses', '1351351358'], ['The Order of things', '1351351258'],
         #['The Book Thief', '1351351234']]
        
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
        
        #a dict in which each key points to a list that contains all the iters of a store
        self.ItersList = {'mainstore' : [],
                          'Booksinfo' : []}
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
        #self.ReturnButton.connect('clicked', self.Return)
        
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
            self.ItersList['mainstore'].append(treeitr)
        for y in Books:
            treeitr = self.Booksinfo.append(y.getInfo())
            self.ItersList['Booksinfo'].append(treeitr)
    
    # The function to issue books. currently not working. bruh.
    def Issue(self, button):
        Book = None 
        User = None 
        if Book != '' and User != '':
            for x in Books:
                if x.Placement == int(self.BookPentry.get_text()):
                    Book = x
                    break
            for y in Members:
                if int(self.MemberEntry.get_text()) == y.ID:
                    User = y
                    break
            for books in User.Active_Books:
                if Book == books:
                    return False
            
            for i in self.ItersList['Booksinfo']:
                if Book.Placement == self.Booksinfo[i][1]:
                    if Book.Available == False:
                        return False
                    else:
                        Book.Copies = Book.Copies -1
                        if Book.Copies == 0:
                            Book.Available = False
                        Borrowed_Books.append([User.name, User.ID, Book.Title, 
                                              Book.Placement, Book.ISBN, 
                                              'Implement Due Date', Book.Copies])
                
                        User.Active_Books.append(Book)
                        print(User, Borrowed_Books[len(Borrowed_Books)-1])
                        self.ItersList['mainstore'].append(self.mainstore.append(Borrowed_Books[len(Borrowed_Books)-1]))
                        for iter in self.ItersList['mainstore']:
                            if Book.Placement == self.mainstore[iter][3]:
                                self.mainstore[iter][6] = Book.Copies

 
#         for x in range(len(Members)):
#             if random.choice([True, False]):
#                 randbook = random.choice(Books)
#                 if randbook.Available == True:
#                     Members[x].Active_Books.append(randbook)
#                     randbook.Available = False
#                     Borrowed_Books.append([Members[x].name, Members[x].ID,
#                                            randbook.Title, randbook.Placement,
#                                            randbook.ISBN, 'Implement Due Date', randbook.Copies-1])
#                  
#         
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
        if path is not None:
            iter = self.Booksinfo.get_iter(path)
            ISBN = self.Booksinfo[iter][0]
            for x in self.ItersList['mainstore']:
                if ISBN == self.mainstore[x][4]:
                    self.mainstore.remove(x)
                    self.ItersList['mainstore'].remove(x)
                    break
                
            for i in Books:
                if i.ISBN == self.Booksinfo[iter][0]:
                    Books.remove(i)
                    
            self.Booksinfo.remove(iter)
            
window = LibraryManager()
window.connect('destroy', Gtk.main_quit)
window.show_all()
Gtk.main()