class Recipe:
    def __init__(self, id, ingredients, procedure):
        self.id = id
        self.ingredients = ingredients
        self.procedure = procedure
    
    def toDBCollection(self):
        return {
            "_id": self.id,
            "ingredients": self.ingredients,
            "procedure": self.procedure
        }