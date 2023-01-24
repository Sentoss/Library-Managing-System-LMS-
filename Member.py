class member():
    def __init__(self, ID: int, name: str, Phone_number: str,
                 year: int, Active_Books: list,
                 Borrowing_History: list):
        self.ID = ID
        self.name = name
        self.Phone_number = Phone_number
        self.year = year
        self.Active_Books = Active_Books
        self.Borrowing_History = Borrowing_History
        #self.Fine_History = Fine_History
# create the variable in the __init__ bracket when you get back to this feature
# delegated the fine function till later, let's just focus on getting the basics down
#     def Fine(self, amount, date):
#       self.Fine_History.append([int(amount), str(date)])

    def Borrow(self, book, issue_date):
        self.Active_Books.append([book, issue_date])
    
    def Return(self, book, return_date):
        for x in self.Active_Books:
            if x[0] == book:
                self.Borrowing_History.append([book, str(self.Active_Books[x][1]),
                                               str(return_date)])
                self.Active_Books.remove(x)
                break
                

