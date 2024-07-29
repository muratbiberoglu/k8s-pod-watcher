from typing import List

from src.util.modifiers import Modifiers


class Row:
    __default_modifier = Modifiers.DIMMED
    __table_cell_separator = "  "

    def __init__(self, cells: List[str], modifiers: List = None):
        self.__cells = cells
        self.__modifiers = modifiers

        if not self.__modifiers:
            self.__modifiers = [Row.__default_modifier] * len(self.__cells)
        if len(self.__modifiers) < len(self.__cells):
            self.__modifiers.extend([Row.__default_modifier] * (len(self.__cells) - len(self.__modifiers)))

    def to_string(self, max_column_widths: List[int]):
        modified_cell_list = list()
        for i, cell in enumerate(self.__cells):
            modified_cell_list.append(self.__modifiers[i] + cell.ljust(max_column_widths[i]) + Modifiers.NORMAL)
        return Row.__table_cell_separator.join(modified_cell_list)

    def get_length_of_cells(self) -> List[int]:
        return list(map(len, self.__cells))
