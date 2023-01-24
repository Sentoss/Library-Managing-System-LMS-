import Book, string, random

def populate():
    Books = []
    for x in range(8):
        Books.append(Book.book(random.randint(1000, 9000), random.randint(100, 900),
                      ''.join([random.choice(string.ascii_letters + string.digits)
                               for n in range(10)]), "aaksahsbkhas", "English", True, 1))
    return Books