import Member, Book, Populate, sys, gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#Books = [['Harry Potter', '1351351313'], ['The Ice Dragon', '1351351312'],
        # ['Les Mots et Les Choses', '1351351358'], ['The Order of things', '1351351258'],
         #['The Book Thief', '1351351234']]

Books = Populate.populate()
Harry = Member.member(2200, "Harry", "0111258070", 3, [], [])

class LibraryManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Library Manager")
        
        self.button = Gtk.Button(label="print Books")
        self.button.connect("clicked", self.printbooks)
        self.add(self.button)
        
    def printbooks(self, widget):
        for i in Books:
            print(i.getInfo())

window = LibraryManager()
window.connect('destroy', Gtk.main_quit)
window.show_all()
Gtk.main()