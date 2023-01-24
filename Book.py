class book():
    def __init__(self, ISBN, Placement, Title, Author, Language, Available, Copies):
        self.ISBN = ISBN
        self.Placement = Placement
        self.Title = Title
        self.Author = Author
        self.Language = Language
        self.Available = Available
        self.Copies = Copies
    Series = None
    
    def getInfo(self):
        return self.ISBN, self.Placement, self.Title, self.Author, self.Language, self.Available, self.Copies