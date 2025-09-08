class Empire:
    def __init__(self, name:str = "", emperor_name:str = "") -> None:
        self.name:str = name
        self.emperor_name: str = emperor_name
    
    def __str__(self) -> str:
        return f"Empire {self.name}, Emperor {self.emperor_name}"