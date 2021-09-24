class Move:
    pass

class MoveSequence:
    def __init__(self, moves):
        self._moves = moves.split(' ')



class Piece:
    subclasses = {}
    def __new__(cls, *args, **kwargs):
        x = super().__new__(cls)
        return x

    @classmethod
    def register(cls, piece_type):
        def wrapper(subclass):
            cls.subclasses[piece_type] = subclass
        return wrapper
    @classmethod
    def create(cls, piece_type, *args, **kwargs):
        if piece_type not in cls.subclasses:
            raise TypeError("Piece type '{}' is not supported".format(piece_type))
        return cls.subclasses[piece_type](*args, **kwargs)

    @classmethod
    def piece_type(cls, move):
        pass

class OpeningFamily:
    pass


