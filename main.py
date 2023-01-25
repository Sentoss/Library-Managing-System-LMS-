import Member, Book, Populate, sys, gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#Books = [['Harry Potter', '1351351313'], ['The Ice Dragon', '1351351312'],
        # ['Les Mots et Les Choses', '1351351358'], ['The Order of things', '1351351258'],
         #['The Book Thief', '1351351234']]
        
labels = ['ISBN', 'Placement', 'Title', 'Author', 'Language', 'Available', 'Copies']
Books = Populate.populate()
Harry = Member.member(2200, "Harry", "0111258070", 3, [], [])

class LibraryManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Library Manager")
        self.set_border_width(10)
        
        #for now, per the parameters in the population script, we're gonna keep the
        #parameter for objects in this way: that the ISBN and placement are ints
        #it won't be difficult changing them later, but, let's keep it that way to
        #prioritize what's important
        self.store = Gtk.ListStore(int, int, str, str, str, bool, int)
        self.fillData(Books)
        self.dashboard = Gtk.TreeView(model=self.store)
        
        for i in range(len(labels)):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(labels[i], renderer, text=i)
            self.dashboard.append_column(column)
            
            
#         self.title = Gtk.CellRendererText()
#         #self.author = Gtk.CellRendererText()
# 
#         self.column.pack_start(self.title, True)
#         #self.column.pack_start(self.author, True)
# 
#         self.column.add_attribute(self.title, "text", 0)
#         #self.column.add_attribute(self.author, "text", 1)
# 
#         self.dashboard.append_column(self.column)


        self.navigation = Gtk.Notebook()
        self.add(self.navigation)
        
        self.Maintab = Gtk.Grid()
        self.Maintab.add(self.dashboard)
        self.navigation.append_page(self.Maintab, Gtk.Label(label="Main"))
        
        self.Bookstab = Gtk.Grid()
        self.navigation.append_page(self.Bookstab, Gtk.Label(label="Books"))

        self.Memberstab = Gtk.Grid()
        self.navigation.append_page(self.Memberstab, Gtk.Label(label="Members"))

        self.Settingstab = Gtk.Grid()
        self.navigation.append_page(self.Settingstab, Gtk.Label(label="Settings"))
    
    def fillData(self, source):
        #self.appended = []
        for x in range(len(source)):
            self.treeitr = self.store.append([source[x].getInfo()[0], source[x].getInfo()[1],
                              source[x].getInfo()[2], source[x].getInfo()[3],
                              source[x].getInfo()[4], source[x].getInfo()[5],
                              source[x].getInfo()[6]])
            
#             self.appended.append(self.treeitr)
#         for x in range(len(self.appended)):
#             print(self.store[self.appended[x]][:])
# ^ tests

window = LibraryManager()
window.connect('destroy', Gtk.main_quit)
window.show_all()
Gtk.main()