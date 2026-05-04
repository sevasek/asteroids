import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_DEFAULT_FONT_SIZE


class MenuElement:
    def __init__(self, text, y_offset=0, font_size=None, color="white"):
        self.text = text
        self.y_offset = y_offset
        self.font_size = font_size or MENU_DEFAULT_FONT_SIZE
        self.color = color


class Menu:
    def __init__(self):
        self.elements = []
        self._font_cache = {}

    def _get_font(self, size):
        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.SysFont(None, size)
        return self._font_cache[size]

    def add(self, element: MenuElement):
        self.elements.append(element)

    def remove(self, text: str):
        self.elements = [e for e in self.elements if e.text != text]

    def clear(self):
        self.elements.clear()

    def draw(self, screen):
        screen.fill("black")

        for element in self.elements:
            font = self._get_font(element.font_size)
            text_surface = font.render(element.text, True, element.color)
            rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + element.y_offset))
            screen.blit(text_surface, rect)

        pygame.display.flip()