class SmartContract:
    def __init__(self):
        self.allowed_categories = {}

    def set_allowed_category(self, recipient, category):
        if recipient not in self.allowed_categories:
            self.allowed_categories[recipient] = []
        self.allowed_categories[recipient].append(category)

    def validate_transaction(self, transaction):
        recipient = transaction['recipient']
        category = transaction['category']
        if recipient in self.allowed_categories:
            return category in self.allowed_categories[recipient]
        return False
