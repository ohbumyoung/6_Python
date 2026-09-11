# main.py

from models import PrintedBook, EBook
from library import Library
from models import BookNotFoundError, AlreadyBorrowedError


def main():

    library = Library()

    while True:

        print("\n==============================")
        print("        도서 관리 프로그램")
        print("==============================")
        print("1. 일반 도서 등록")
        print("2. 전자책 등록")
        print("3. 전체 도서 목록")
        print("4. 대출 가능한 도서 검색")
        print("5. 저자 목록 보기")
        print("6. 도서 대출")
        print("7. 도서 반납")
        print("8. 도서 삭제")
        print("0. 프로그램 종료")
        print("==============================")

        choice = input("메뉴를 선택하세요: ")

        # 1. 일반 도서 등록
        if choice == "1":

            print("\n[일반 도서 등록]")

            isbn = input("ISBN: ")
            title = input("제목: ")
            author = input("저자: ")
            location = input("책 보관 위치: ")

            book = PrintedBook(
                isbn,
                title,
                author,
                location
            )

            library.add_book(book)

            print("일반 도서가 등록되었습니다.")

        # 2. 전자책 등록
        elif choice == "2":

            print("\n[전자책 등록]")

            isbn = input("ISBN: ")
            title = input("제목: ")
            author = input("저자: ")
            file_format = input("파일 포맷: ")

            while True:

                try:
                    file_size = float(input("파일 용량(MB): "))
                    break

                except ValueError:
                    print("파일 용량은 숫자로 입력해주세요.")

            book = EBook(
                isbn,
                title,
                author,
                file_format,
                file_size
            )

            library.add_book(book)

            print("전자책이 등록되었습니다.")

        # 3. 전체 도서 목록
        elif choice == "3":

            library.list_books()

        # 4. 대출 가능한 도서
        elif choice == "4":

            library.list_available_books()

        # 5. 저자 목록
        elif choice == "5":

            library.list_authors()

        # 6. 대출
        elif choice == "6":

            isbn = input("대출할 도서의 ISBN: ")

            try:
                library.borrow_book(isbn)

            except BookNotFoundError as e:
                print(f"오류: {e}")

            except AlreadyBorrowedError as e:
                print(f"오류: {e}")

        # 7. 반납
        elif choice == "7":

            isbn = input("반납할 도서의 ISBN: ")

            try:
                library.return_book(isbn)

            except BookNotFoundError as e:
                print(f"오류: {e}")

        # 8. 삭제
        elif choice == "8":

            isbn = input("삭제할 도서의 ISBN: ")

            try:
                library.delete_book(isbn)

            except BookNotFoundError as e:
                print(f"오류: {e}")

        # 0. 종료
        elif choice == "0":

            print("프로그램을 종료합니다.")
            break

        # 잘못된 메뉴
        else:

            print("잘못된 메뉴입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()