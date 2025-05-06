from copy import deepcopy

class dbController:
    def __init__(self):
        self.db = {}
        self.transactions = []

    def BEGIN(self):
        new_transaction = deepcopy(self.db)
        if self.transactions:
            new_transaction = deepcopy(self.transactions[-1])
        self.transactions.append(new_transaction)

    def SET(self, key, value):
        if self.transactions:
            self.transactions[-1][key] = value
        else:
            self.db[key] = value

    def GET(self, key):
        if self.transactions:
            return self.transactions[-1].get(key, "NULL")
        return self.db.get(key, "NULL")

    def ROLLBACK(self):
        if self.transactions:
            self.transactions.pop()

    def COMMIT(self):
        if self.transactions:
            last_transaction = self.transactions.pop()
            if self.transactions:
                self.transactions[-1] = last_transaction
            else:
                self.db = last_transaction

    def UNSET(self, key):
        if self.transactions:
            self.transactions[-1].pop(key, None)
        else:
            self.db.pop(key, None)
            
    def FIND(self, value):
        if self.transactions:
            return [key for key in self.transactions[-1] if self.transactions[-1][key] == value]
        return [key for key in self.db if self.db[key] == value]
    
    def COUNTS(self, value):
        if self.transactions:
            return sum(1 for key in self.transactions[-1] if self.transactions[-1][key] == value)
        return sum(1 for key in self.db if self.db[key] == value)
    
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
