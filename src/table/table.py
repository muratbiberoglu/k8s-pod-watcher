from typing import List

from .row import Row


class Table:
    def __init__(self):
        self.__rows: List[Row] = list()

    def add_row(self, row: Row):
        self.__rows.append(row)

    def to_string(self, indentation: int) -> str:
        max_column_widths = [max(col) for col in zip(*[row.get_length_of_cells() for row in self.__rows])]
        result = ""
        for row in self.__rows:
            result += "\t" * indentation + row.to_string(max_column_widths) + "\n"
        return result
