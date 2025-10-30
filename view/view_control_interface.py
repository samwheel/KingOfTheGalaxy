from src.star import Star

from view.screens import Screen

class ViewControlInterface:
    def __init__(self) -> None:
        self.current_view: Screen|None = None

    def update_views(self, stars: list[Star], player_empire, screen, widgets) -> None:
        pass