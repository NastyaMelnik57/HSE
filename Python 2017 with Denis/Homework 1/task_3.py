class UniqObject:

    __instance = None
    
    def __init__(self):
        if self.__instance is not None: #если существует уже экземпляр, то выдаем ошибку
            raise 'The object already exists'
    
    @classmethod
    def create_object(cls):
        if cls.__instance is None:
            cls.__instance = UniqObject()
        return cls.__instance

object1 = UniqObject.create_object() #можно просто вызвать UniqObject()
object2 = UniqObject.create_object()
print(id(object1), id(object2))
