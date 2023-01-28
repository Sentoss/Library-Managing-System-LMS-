import Member, Book, Populate, gi, random
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#Books = [['Harry Potter', '1351351313'], ['The Ice Dragon', '1351351312'],
        # ['Les Mots et Les Choses', '1351351358'], ['The Order of things', '1351351258'],
         #['The Book Thief', '1351351234']]
        
labels = ['Member', 'ID', 'Title', 'Placement', 'ISBN', 'Due Date', 'Copies Left']
Books = Populate.populatebook()
Members = Populate.populatemember()
Borrowed_Books = []

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
        
        self.Issue()
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
        
        self.Maintab = Gtk.Grid()
        self.Maintab.add(self.dashboard)
        
        self.navigation.append_page(self.Maintab, Gtk.Label(label="Main"))
        
        self.Bookstab = Gtk.Grid()
        self.searchtest = Gtk.Button(label="search")
        
        self.Bookstab.attach(self.booksearch, 0, 0, 2, 2)
        self.Bookstab.attach_next_to(self.Booktable, self.booksearch, Gtk.PositionType.BOTTOM, 2, 2)
        self.Bookstab.attach_next_to(self.SearchCombo, self.booksearch, Gtk.PositionType.RIGHT, 2, 1)
        self.Bookstab.attach_next_to(self.searchtest, self.SearchCombo, Gtk.PositionType.RIGHT, 2, 1)
        self.navigation.append_page(self.Bookstab, Gtk.Label(label="Books"))

        self.searchtest.connect("clicked", self.update)
        self.Memberstab = Gtk.Grid()
        self.navigation.append_page(self.Memberstab, Gtk.Label(label="Members"))

        self.Settingstab = Gtk.Grid()
        self.navigation.append_page(self.Settingstab, Gtk.Label(label="Settings"))
        #self.booksearch.connect('activate', self.)
        self.index = self.SearchCombo.get_active()
    def fillData(self):
        for x in Borrowed_Books:
            self.treeitr = self.mainstore.append(x)
        
        for y in Books:
            self.treeitr = self.Booksinfo.append(y.getInfo())
    
    #a psuedo issuing function for now. Will be later edited to require a variable
    def Issue(self):
        for x in range(len(Members)):
            if random.choice([True, False]):
                randbook = random.choice(Books)
                if randbook.Available == True:
                    Members[x].Active_Books.append(randbook)
                    randbook.Available = False
                    Borrowed_Books.append([Members[x].name, Members[x].ID,
                                           randbook.Title, randbook.Placement,
                                           randbook.ISBN, 'Implement Due Date', randbook.Copies-1])
                 
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
        
    def filterchoice(self, model, iter, data):
        if self.booksearch.get_text() != '':
            if str(model[iter][self.index]) not in self.booksearch.get_text():
                return False
        else:
            return True
        
    #Considering that I'm tired, here's what you have to do wrt the search function and updating the thing
    #you're going to create 2 functions: one which updates when the text changes, and one that updates when
    #the combobox changes. And in both of them (I think) there's an input that gets sent to the 2nd argument  
    #as an argument in that callable function (old error, got fixed), so we take that (which I believei is the
    #the new state of the object (combobox or Entry). You have to use them each in their specific way and
    #then use self.Booksinfo.refilter() inside both, and I believe this should work.
    
window = LibraryManager()
window.connect('destroy', Gtk.main_quit)
window.show_all()
Gtk.main()