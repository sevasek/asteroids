import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_DEFAULT_FONT_SIZE, MENU_SECTION_PADDING, MENU_ELEMENT_PADDING


class MenuElement:
    def __init__(self, text, font_size=None, color="white", x_offset=None):
        self.text = text
        self.font_size = font_size or MENU_DEFAULT_FONT_SIZE
        self.color = color
        self.x_offset = x_offset  # None = center, number = offset from center


class MenuSection:
    def __init__(self):
        self.elements = []
        self.padding = MENU_ELEMENT_PADDING

    def add(self, element: MenuElement):
        self.elements.append(element)

    def clear(self):
        self.elements.clear()

    def get_height(self, font_getter):
        if not self.elements:
            return 0
        total_height = 0
        i = 0
        while i < len(self.elements):
            h1 = font_getter(self.elements[i].font_size).render(self.elements[i].text, True, self.elements[i].color).get_height()
            if i + 1 < len(self.elements):
                h2 = font_getter(self.elements[i+1].font_size).render(self.elements[i+1].text, True, self.elements[i+1].color).get_height()
                total_height += max(h1, h2)
            else:
                total_height += h1
            i += 2
        total_height += ((len(self.elements) // 2) - 1) * self.padding if len(self.elements) > 2 else 0
        return total_height


class Menu:
    def __init__(self):
        self.top = MenuSection()
        self.middle = MenuSection()
        self.bottom = MenuSection()
        self._font_cache = {}

    def _get_font(self, size):
        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.SysFont(None, size)
        return self._font_cache[size]

    def add_to_top(self, element: MenuElement):
        self.top.add(element)

    def add_to_middle(self, element: MenuElement):
        self.middle.add(element)

    def add_to_bottom(self, element: MenuElement):
        self.bottom.add(element)

    def clear_all(self):
        self.top.clear()
        self.middle.clear()
        self.bottom.clear()

    def draw(self, screen, starfield=None, middle_pairs=False):
        screen.fill("black")
        if starfield:
            starfield.draw(screen)

        font_getter = self._get_font

        top_height = self.top.get_height(font_getter)
        middle_height = self.middle.get_height(font_getter)
        bottom_height = self.bottom.get_height(font_getter)

        total_section_padding = MENU_SECTION_PADDING * 2
        available_height = SCREEN_HEIGHT - top_height - middle_height - bottom_height - total_section_padding
        middle_start_y = SCREEN_HEIGHT // 2 - middle_height // 2

        y = MENU_SECTION_PADDING
        self._draw_section(screen, self.top, y, font_getter)
        y += top_height + MENU_SECTION_PADDING

        y = middle_start_y
        if middle_pairs:
            self._draw_section_pairs(screen, self.middle, y, font_getter)
        else:
            self._draw_section(screen, self.middle, y, font_getter)
        y += middle_height + MENU_SECTION_PADDING

        y = SCREEN_HEIGHT - MENU_SECTION_PADDING - bottom_height
        self._draw_section_down(screen, self.bottom, y, font_getter)

        pygame.display.flip()

    def _draw_section(self, screen, section: MenuSection, start_y: int, font_getter):
        y = start_y
        for element in section.elements:
            font = font_getter(element.font_size)
            text_surface = font.render(element.text, True, element.color)
            if element.x_offset is not None:
                x = SCREEN_WIDTH // 2 + element.x_offset
                rect = text_surface.get_rect(center=(x, y + text_surface.get_height() // 2))
            else:
                rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y + text_surface.get_height() // 2))
            screen.blit(text_surface, rect)
            y += text_surface.get_height() + section.padding

    def _draw_section_down(self, screen, section: MenuSection, start_y: int, font_getter):
        y = start_y
        for element in section.elements:
            font = font_getter(element.font_size)
            text_surface = font.render(element.text, True, element.color)
            if element.x_offset is not None:
                x = SCREEN_WIDTH // 2 + element.x_offset
                rect = text_surface.get_rect(center=(x, y + text_surface.get_height() // 2))
            else:
                rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y + text_surface.get_height() // 2))
            screen.blit(text_surface, rect)
            y += text_surface.get_height() + section.padding

    def _draw_section_pairs(self, screen, section: MenuSection, start_y: int, font_getter):
        y = start_y
        i = 0
        while i < len(section.elements):
            element1 = section.elements[i]
            font1 = font_getter(element1.font_size)
            text1 = font1.render(element1.text, True, element1.color)
            height1 = text1.get_height()

            row_height = height1

            if i + 1 < len(section.elements):
                element2 = section.elements[i + 1]
                font2 = font_getter(element2.font_size)
                text2 = font2.render(element2.text, True, element2.color)
                height2 = text2.get_height()
                row_height = max(height1, height2)

            center_y = y + row_height // 2

            if element1.x_offset is not None:
                x1 = SCREEN_WIDTH // 2 + element1.x_offset
            else:
                x1 = SCREEN_WIDTH // 2
            rect1 = text1.get_rect(center=(x1, center_y))
            screen.blit(text1, rect1)

            if i + 1 < len(section.elements):
                element2 = section.elements[i + 1]
                font2 = font_getter(element2.font_size)
                text2 = font2.render(element2.text, True, element2.color)

                if element2.x_offset is not None:
                    x2 = SCREEN_WIDTH // 2 + element2.x_offset
                else:
                    x2 = SCREEN_WIDTH // 2
                rect2 = text2.get_rect(center=(x2, center_y))
                screen.blit(text2, rect2)

            y += row_height + section.padding
            i += 2