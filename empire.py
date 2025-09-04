class Empire:

    def init(self, name:str = "") -> None:
        self.__name:str = name
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name:str = "") -> None:
        self.__name = name