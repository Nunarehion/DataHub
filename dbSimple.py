class Field:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class dbController:
    def __init__(self):
        self.db = {}
        self.transactions = []

    def BEGIN(self):
        self.transactions.append({})

    def SET(self, key, value):
        if self.transactions:
            self.transactions[-1][key] = Field(key, value)
            return
        self.db[key] = Field(key, value)
        # return self.db[key]

    def GET(self, key):
        if self.transactions:
            for transaction in self.transactions:
                if value := transaction.get(key):
                    return value
        return self.db.get(key, "NULL")

    def ROLLBACK(self):
        if self.transactions:
            self.transactions.pop()

    def COMMIT(self):
        if self.transactions:
            if len(self.transactions >= 2):
                self.transactions[-2].update(self.transactions.pop())
            else:
                self.db.update(self.transactions.pop())

    def UNSET(self, key):
            if self.transactions:
            for transaction in self.transactions:
                if value := transaction.get(key):
                    return value
        return self.db.get(key, "NULL")
        self.db.pop(key, None)

    def FINDE(self, value):
        return [key for key in self.db if self.db[key].value == value]

    def COUNTS(self, value):
        return sum(1 for key in self.db if self.db[key].value == value)

    def END(self):
        exit()

    def parseData(self, command: str):
        try:
            (func, *args) = command.split(" ")
            output = self.__getattribute__(func)(*args)
            if output:
                print(output)

        except Exception as e:
            print(e)

    def run(self):
        while True:
            self.parseData(input("> "))


dbController().run()
