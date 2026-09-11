class BookNotFoundError(Exception):
    pass

class AlreadyBorrowedError(Exception):
    pass

class Book:

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.LoanStatus = False
    
    def borrow(self):

        if self.LoanStatus:
            raise AlreadyBorrowedError(
                f"'{self.title}'은(는) 이미 대출 중입니다."
            )

        self.LoanStatus = True

    
    def return_book(self):
        self.LoanStatus = False

    
    def get_status(self):
        if self.LoanStatus:
            return "대출 중"
        else:
            return "대출 가능"

    
    def __str__(self):
        return (
            f"ISBN: {self.isbn}, "
            f"제목: {self.title}, "
            f"작가: {self.author}, "
            f"대출여부: {self.get_status()}"
        )



class PrintedBook(Book):

    def __init__(self, isbn, title, author, keep):
        super().__init__(isbn, title, author)

        self.keep = keep

    def __str__(self):
        return (
            f"[일반 도서] "
            f"ISBN: {self.isbn}, "
            f"제목: {self.title}, "
            f"작가: {self.author}, "
            f"대출여부: {self.get_status()}, "
            f"보관 위치: {self.keep}"
        )

class EBook(Book):

    def __init__(self, isbn, title, author, fileFormat, fileMB):
        super().__init__(isbn, title, author)

        self.fileFormat = fileFormat
        self.fileMB = fileMB

    def __str__(self):
        return (
            f"[전자책] "
            f"ISBN: {self.isbn}, "
            f"제목: {self.title}, "
            f"작가: {self.author}, "
            f"대출여부: {self.get_status()}, "
            f"파일 포맷: {self.fileFormat}, "
            f"파일 용량: {self.fileMB}"
        )