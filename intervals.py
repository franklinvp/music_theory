from typing import Union
import notes

class Interval:
    def __init__(self, value: float):
        double_value = 2*value
        if double_value == float(int(double_value)):
            self.value = value
        else:
            raise ValueError('Twice the value must be an integer.')

    def __repr__(self) -> str:
        _ = self.value
        _r = int(_).__repr__() if abs(_) >= 1 else '-' if _ < 0 else ''
        return _r + ('½' if _ % 1 else '')
    
    def __mult__(self, factor: int):
        self.value *= factor
        return self

    __rmult__ = __mult__

    def __add__(self, value: Union[int, notes.note]):
        if isinstance(value, int):
            self.value += value
            return self
        elif isinstance(value, notes.note):
            return notes._add_interval(value, self)
        else:
            raise ValueError(f'Note expected but {type(value)} input.')

    __radd__ = __add__
