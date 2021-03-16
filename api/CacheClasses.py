import json

class  CacheClasses:
    
    __instance = None
    classes = []
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if CacheClasses.__instance == None:
            CacheClasses()
        return CacheClasses.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if CacheClasses.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            classes = []
            classes80 = []
            with open('./api/params.json', 'rb') as f:
                params = json.load(f)
                classes = params['classes'][:numClass]
                classes80 = params['classes_80']
            CacheClasses.__instance = self
    
    def getClasses(self):
        return self.classes
    
    def getClasses80(self):
        return self.classes80
