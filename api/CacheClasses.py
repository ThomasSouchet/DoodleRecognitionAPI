import json

class  CacheClasses:
    
    __instance = None
    params = {}
    
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
            with open('./api/params.json', 'rb') as f:
                self.params = json.load(f)
            CacheClasses.__instance = self
    
    def getClasses(self, numClass):
        return self.params['classes'][:numClass]
    
    def getClasses80(self):
        return self.params['classes_80']
    
    def getAnimalsClasses(self):
        return self.params['classes_animals']
    
    def getFoodClasses(self):
        return self.params['classes_food']

    def getTransportClasses(self):
        return self.params['classes_transport']

    def getObjectClasses(self):
        return self.params['classes_object']
