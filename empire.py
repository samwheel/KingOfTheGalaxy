class Empire:
    def __init__(self, name:str = "", emperor_name:str = "") -> None:
        self.__name:str = name
        self.__emperor_name: str = emperor_name
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name:str = "") -> None:
        self.__name = name
    
    @property
    def emperor_name(self) -> str:
        return self.__emperor_name
    
    @emperor_name.setter
    def emperor_name(self, emperor_name:str = "Deathbringer") -> None:
        self.__emperor_name = emperor_name
    
    def __str__(self) -> str:
        return f"Empire {self.name}, Emperor {self.emperor_name}"