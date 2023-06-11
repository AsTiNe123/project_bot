class Person():
    def __init__(self):
        self.name = ''

    def set_data(self, name: str, time_on: list, time_out: list):
        self.name, self.time_on, self.time_out = name, time_on, time_out
        self.score = 0

    def up_score(self):
        self.score +=5
    
    def down_score(self):
        self.score -=5
    
    def task_ignore(self):
        self.score -=1

    def __str__(self):
        return f"пользователь: {self.name} счёт: {self.score}"
    
    def get_score(self):
        return self.score
    
    def change_time(self, time_on, time_out):
        self.time_on, self.time_out = time_on, time_out
    
    def __eq__(self, other):
        return self.name == other
