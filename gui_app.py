# gui_app.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QCheckBox, QMessageBox, QInputDialog, QGroupBox, QFormLayout
)
from book_library import Book, EBook, Library, BookNotAvailableError

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.setWindowTitle("📘 Library Management System")
        self.setGeometry(200, 100, 700, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ---- Form Section ----
        form_group = QGroupBox("Add New Book")
        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.size_input = QLineEdit()
        self.ebook_checkbox = QCheckBox("Is eBook?")

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Author:", self.author_input)
        form_layout.addRow("ISBN:", self.isbn_input)
        form_layout.addRow(self.ebook_checkbox)
        form_layout.addRow("Download Size (MB):", self.size_input)

        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_book)

        form_layout.addRow(self.add_button)
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # ---- Action Buttons ----
        action_layout = QHBoxLayout()
        self.lend_button = QPushButton("Lend Book")
        self.lend_button.clicked.connect(self.lend_book)
        self.return_button = QPushButton("Return Book")
        self.return_button.clicked.connect(self.return_book)
        self.remove_button = QPushButton("Remove Book")
        self.remove_button.clicked.connect(self.remove_book)
        self.view_author_button = QPushButton("View Books by Author")
        self.view_author_button.clicked.connect(self.view_books_by_author)

        for btn in [self.lend_button, self.return_button, self.remove_button, self.view_author_button]:
            action_layout.addWidget(btn)

        main_layout.addLayout(action_layout)

        # ---- List Display ----
        main_layout.addWidget(QLabel("📗 Available Books:"))
        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        self.setLayout(main_layout)
        self.update_book_list()

    # ===== Logic Methods =====

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        size = self.size_input.text()
        is_ebook = self.ebook_checkbox.isChecked()

        if not title or not author or not isbn:
            self.show_error("Title, Author, and ISBN are required.")
            return

        if is_ebook and not size:
            self.show_error("Download size is required for eBooks.")
            return

        book = EBook(title, author, isbn, size) if is_ebook else Book(title, author, isbn)
        self.library.add_book(book)
        self.show_info(f"Book '{title}' added.")
        self.clear_inputs()
        self.update_book_list()

    def lend_book(self):
        isbn, ok = QInputDialog.getText(self, "Lend Book", "Enter ISBN:")
        if ok and isbn:
            try:
                self.library.lend_book(isbn)
                self.show_info("Book lent successfully.")
            except BookNotAvailableError as e:
                self.show_error(str(e))
            self.update_book_list()

    def return_book(self):
        isbn, ok = QInputDialog.getText(self, "Return Book", "Enter ISBN:")
        if ok and isbn:
            try:
                self.library.return_book(isbn)
                self.show_info("Book returned successfully.")
            except BookNotAvailableError as e:
                self.show_error(str(e))
            self.update_book_list()

    def remove_book(self):
        isbn, ok = QInputDialog.getText(self, "Remove Book", "Enter ISBN:")
        if ok and isbn:
            self.library.remove_book(isbn)
            self.show_info("Book removed.")
            self.update_book_list()

    def view_books_by_author(self):
        author, ok = QInputDialog.getText(self, "Search by Author", "Enter author name:")
        if ok and author:
            books = list(self.library.books_by_author(author))
            self.list_widget.clear()
            if books:
                self.list_widget.addItem(f"Books by {author}:")
                for book in books:
                    self.list_widget.addItem(str(book))
            else:
                self.show_info("No books found by this author.")

    def update_book_list(self):
        self.list_widget.clear()
        self.list_widget.addItem("Available Books:")
        for book in self.library:
            self.list_widget.addItem(str(book))

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.size_input.clear()
        self.ebook_checkbox.setChecked(False)

    # ===== Utility Methods =====
    def show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)

    def show_info(self, msg):
        QMessageBox.information(self, "Info", msg)

# ===== App Entry Point =====

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LibraryApp()
    win.show()
    sys.exit(app.exec_())
