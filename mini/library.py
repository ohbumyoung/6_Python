from models import PrintedBook, EBook, BookNotFoundError

class library:
    
    def __init__(self):
        self.books = {}
    
    def createPrintedBook(self, isbn, title, author, keep) :
       
        printedBook = PrintedBook(isbn, title, author, keep)
        self.books[isbn] = printedBook

    
    def createEBook(self, isbn, title, author, fileFormat, fileMB) :
        ebook = EBook(isbn, title, author, fileFormat, fileMB)
        self.books[isbn] = ebook
    
    
    def readBook(self, isbn = None) :
        if isbn is None:
            for book in self.books.values():
                print(book)
        else:
            if isbn in self.books:
                print(self.books[isbn])
            else:
                raise BookNotFoundError(f"ISBN '{isbn}'에 해당하는 도서가 없습니다.")    
    
    
    def updatePrintedBook(self, isbn, title=None, author=None, keep=None):
        if isbn not in self.books:
            raise BookNotFoundError(f"ISBN '{isbn}'에 해당하는 도서가 없습니다.")
        
        book = self.books[isbn]
        if title: 
            book.title = title
        if author: 
            book.author = author
        if keep: 
            book.keep = keep 

    def updateEBook(self, isbn, title=None, author=None, fileFormat=None, fileMB=None):
        if isbn not in self.books:
            raise BookNotFoundError(f"ISBN '{isbn}'에 해당하는 도서가 없습니다.")
            
        book = self.books[isbn]
        if title: 
            book.title = title
        if author: 
            book.author = author
        if fileFormat: 
            book.fileFormat = fileFormat  
        if fileMB: 
            book.fileMB = fileMB
    
    
    
    def deleteBook(self, isbn):
        if isbn in self.books :
            del self.books[isbn]
            print(f"isbn : {isbn} 도서가 삭제되었습니다.")
        else :
            raise BookNotFoundError(f"존재하지 않는 ISBN입니다: {isbn}")

    def borrow(self, isbn):
        if isbn not in self.books:
            raise BookNotFoundError(
            f"ISBN '{isbn}'에 해당하는 도서가 없습니다."
        )

        book = self.books[isbn]
        book.borrow()
        print(f"'{book.title}' 도서를 대출했습니다.")

    def possiblebook(self):
        for book in self.books.values():
            if book.LoanStatus == False:
                print(book)

    def readAuthors(self):
        ERGauthors = set()

        for book in self.books.values():
            ERGauthors.add(book.author)

        for author in ERGauthors:
            print(author)


    