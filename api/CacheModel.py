class  CacheModel:
    
    __instance = None
    model = {}
    
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
    
    def getModel(self, model_name):
        return self.model[model_name]
    
    def addModel(self, model_name, model):
        self.model[model_name] = model
