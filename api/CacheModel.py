class  CacheModel:
    
    __instance = None
    model = None
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if CacheModel.__instance == None:
            CacheModel()
        return CacheModel.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if CacheModel.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CacheModel.__instance = self
    
    def getModel(self):
        return self.model
    
    def setModel(self, model):
        self.model = model
