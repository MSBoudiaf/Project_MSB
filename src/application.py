
from abc import ABC, abstractmethod

class Application (ABC):
    @abstractmethod
    def app_launch (self):...

    @abstractmethod
    def app_main_menu (self):...

    @abstractmethod
    def app_quit (self):...