@property
class BookNotFoundError(Exception):
	pass

class AlreadyBorrowedError(Exception):
	pass

class book:
    def __init__book (self, isbn, title, author, lend):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.lend = False

    def __str__(self):
        return(
        f"ISBN : {self.isbn}",
        f"제목 : {self.title}"
        f"저자 : {self.author}"
        f"대출여부 : {self.lend}"
        )
   
    def lend(self):
        return self.lend

    def lend(self):
        if self.lend:
            raise AlreadyBorrowedError(f"{self.lend}이미 대출 중인 도서입니다.")
    
        