

class RegisterModeException(Exception):
    def __init__(self, val):
        #self.register_mode = register_mode
        self.val = val
        self.message = f"The given register mode {self.val} must be FR or DB"
        super().__init__(self.message)

    def __str__(self):
        return self.message

class EmptyNewsPageException(Exception):
    def __init__(self, page):
        self.page = page
        self.message = f"This page {self.page} contains no news"
        super().__init__(self.message)
