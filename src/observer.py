class Observer:
    def update(self) -> None:
        raise NotImplementedError("Subclasses must override this method")

class Subject:
    def __init__(self) -> None:
        self.__observer_list: list[Observer] = []

    def add_observer(self, observer:Observer) -> None:
        self.__observer_list.append(observer)
    
    def remove_observer(self, observer:Observer) -> None:
        self.__observer_list.remove(observer)
    
    def update_observers(self) -> None:
        for observer in self.__observer_list:
            observer.update()