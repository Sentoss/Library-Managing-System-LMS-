import Book, string, random, Member

def populatebook():
    Books = []
    for x in range(8):
        Books.append(Book.book(random.randint(1000, 9000), random.randint(100, 900),
                      ''.join([random.choice(string.ascii_letters + string.digits)
                               for n in range(10)]), "aaksahsbkhas", "English", True, random.randint(1, 5)))
    return Books

def populatemember():
    Members = []
    for x in range(8):
        Members.append(Member.member(random.randint(100000, 700000),
                                     ''.join([random.choice(string.ascii_letters) for n in range(10)]),
                                     str(random.randint(1000000, 100000000)),
                                     random.randint(1, 5), [], []))
    return Members

