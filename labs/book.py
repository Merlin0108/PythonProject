class Book:
    def __init__(self, title, author, pages, cover_path):
        self.title = title
        self.author = author
        self.pages = pages
        self.cover_path = cover_path

    def get_info(self):
        return f"Название: {self.title}\nАвтор: {self.author}\nСтраниц: {self.pages}"