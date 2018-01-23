'''Полиморфизм функции in_programme позволяет по дефолтку считать,
что классические произведения включены в программу
, а рок - нет. Но для классов Шопен и Coj in_programme имеет другие реализации
(включать только с 4 курса и только на факультете русского рока соответственно'''



class Play:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self._name
    
class Classic(Play):
    def __init__(self, name):
        super().__init__(name)
        
    def in_programme(self):
        return True
        
class Shopen(Classic):
    def __init__(self, name):
        super().__init__(name)

    def in_programme(self, course):
        if course < 4:
            return False
        else:
            return True
    
class Mozart(Classic):
    def __init__(self, name):
        super().__init__(name)

class Rock(Play):
    def __init__(self, name):
        super().__init__(name)

    def in_programme(self):
        return False

class Coj(Rock):
    def __init__(self, name):
        super().__init__(name)
    def in_programme(self, faculty):
        if faculty == 'Russian Rock':
            return True
        else:
            return False
        
class Dilan(Rock):
    def __init__(self, name):
        super().__init__(name)

play1 = Mozart('Don Juan')
print(play1.in_programme())
play2 = Shopen('Vals')
print(play2.in_programme(4))
