import copy
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any


class Color:
    WHITE = "white"
    BLACK = "black"

    @staticmethod
    def opposite(color: str) -> str:
        return Color.BLACK if color == Color.WHITE else Color.WHITE


class Position:

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return f"Position({self.row}, {self.col})"

    def is_valid(self) -> bool:
        return 0 <= self.row < 8 and 0 <= self.col < 8

    def to_chess_notation(self) -> str:
        file = chr(ord('a') + self.col)
        rank = 8 - self.row
        return f"{file}{rank}"

    @staticmethod
    def from_chess_notation(notation: str) -> 'Position':
        col = ord(notation[0]) - ord('a')
        row = 8 - int(notation[1])
        return Position(row, col)


class Piece(ABC):

    def __init__(self, color: str, position: Position):
        self.color = color
        self.position = position
        self.has_moved = False

    @abstractmethod
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        pass

    def copy(self) -> 'Piece':
        return copy.copy(self)

    def __repr__(self):
        return f"{self.color}_{self.get_symbol()}"


class King(Piece):
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if new_pos.is_valid():
                piece_at = board.get_piece_at(new_pos)
                if piece_at is None or piece_at.color != self.color:
                    moves.append(new_pos)
        return moves

    def get_symbol(self) -> str:
        return 'K' if self.color == Color.WHITE else 'k'


class Queen(Piece):
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            for step in range(1, 8):
                new_pos = Position(self.position.row + dr * step, self.position.col + dc * step)
                if not new_pos.is_valid():
                    break
                piece = board.get_piece_at(new_pos)
                if piece is None:
                    moves.append(new_pos)
                else:
                    if piece.color != self.color:
                        moves.append(new_pos)
                    break
        return moves

    def get_symbol(self) -> str:
        return 'Q' if self.color == Color.WHITE else 'q'


class Rook(Piece):
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            for step in range(1, 8):
                new_pos = Position(self.position.row + dr * step, self.position.col + dc * step)
                if not new_pos.is_valid():
                    break
                piece = board.get_piece_at(new_pos)
                if piece is None:
                    moves.append(new_pos)
                else:
                    if piece.color != self.color:
                        moves.append(new_pos)
                    break
        return moves

    def get_symbol(self) -> str:
        return 'R' if self.color == Color.WHITE else 'r'


class Bishop(Piece):
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for step in range(1, 8):
                new_pos = Position(self.position.row + dr * step, self.position.col + dc * step)
                if not new_pos.is_valid():
                    break
                piece = board.get_piece_at(new_pos)
                if piece is None:
                    moves.append(new_pos)
                else:
                    if piece.color != self.color:
                        moves.append(new_pos)
                    break
        return moves

    def get_symbol(self) -> str:
        return 'B' if self.color == Color.WHITE else 'b'


class Knight(Piece):
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in jumps:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if new_pos.is_valid():
                piece = board.get_piece_at(new_pos)
                if piece is None or piece.color != self.color:
                    moves.append(new_pos)
        return moves

    def get_symbol(self) -> str:
        return 'N' if self.color == Color.WHITE else 'n'


class Pawn(Piece):
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1

        one_step = Position(self.position.row + direction, self.position.col)
        if one_step.is_valid() and board.get_piece_at(one_step) is None:
            moves.append(one_step)

            two_step = Position(self.position.row + 2 * direction, self.position.col)
            if self.position.row == start_row and board.get_piece_at(two_step) is None:
                moves.append(two_step)

        for dc in [-1, 1]:
            capture_pos = Position(self.position.row + direction, self.position.col + dc)
            if capture_pos.is_valid():
                piece = board.get_piece_at(capture_pos)
                if piece and piece.color != self.color:
                    moves.append(capture_pos)

        return moves

    def get_symbol(self) -> str:
        return 'P' if self.color == Color.WHITE else 'p'


class Griffin(Piece):

    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            first = Position(self.position.row + dr, self.position.col + dc)
            if not first.is_valid():
                continue
            piece_first = board.get_piece_at(first)
            second = Position(self.position.row + 2 * dr, self.position.col + 2 * dc)
            if second.is_valid():
                piece_second = board.get_piece_at(second)
                if piece_first is not None:
                    if piece_second is None or piece_second.color != self.color:
                        moves.append(second)
                else:
                    moves.append(first)
        return moves

    def get_symbol(self) -> str:
        return 'G' if self.color == Color.WHITE else 'g'


class Jumper(Piece):

    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dr, dc in directions:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if new_pos.is_valid():
                piece = board.get_piece_at(new_pos)
                if piece is None or piece.color != self.color:
                    moves.append(new_pos)
        return moves

    def get_symbol(self) -> str:
        return 'J' if self.color == Color.WHITE else 'j'


class Wizard(Piece):

    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        knight_jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_jumps:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if new_pos.is_valid():
                piece = board.get_piece_at(new_pos)
                if piece is None or piece.color != self.color:
                    moves.append(new_pos)
        diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diag:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if new_pos.is_valid():
                piece = board.get_piece_at(new_pos)
                if piece is None or piece.color != self.color:
                    moves.append(new_pos)
        return moves

    def get_symbol(self) -> str:
        return 'W' if self.color == Color.WHITE else 'w'


class Move:
    def __init__(self, piece: Piece, from_pos: Position, to_pos: Position,
                 captured_piece: Optional[Piece] = None,
                 promotion_piece_type: Optional[str] = None,
                 is_en_passant: bool = False,
                 en_passant_target: Optional[Position] = None):
        self.piece = piece
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.captured_piece = captured_piece
        self.promotion_piece_type = promotion_piece_type
        self.is_en_passant = is_en_passant
        self.en_passant_target = en_passant_target

    def __repr__(self):
        return f"{self.piece} {self.from_pos.to_chess_notation()} -> {self.to_pos.to_chess_notation()}"


class Board:
    def __init__(self, use_new_pieces: bool = False, new_pieces_positions: dict = None):

        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = Color.WHITE
        self.move_history: List[Move] = []
        self.en_passant_target: Optional[Position] = None
        self.use_new_pieces = use_new_pieces
        self._init_board(use_new_pieces, new_pieces_positions or {})

    def _init_board(self, use_new: bool, new_positions: dict):
        for col in range(8):
            self.set_piece_at(Position(6, col), Pawn(Color.WHITE, Position(6, col)))
            self.set_piece_at(Position(1, col), Pawn(Color.BLACK, Position(1, col)))
        back_row_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for row, color, row_idx in [(7, Color.WHITE, 7), (0, Color.BLACK, 0)]:
            for col in range(8):
                pos = Position(row_idx, col)
                pos_notation = pos.to_chess_notation()
                if use_new and pos_notation in new_positions:
                    piece_type = new_positions[pos_notation]
                    if piece_type == 'Griffin':
                        piece = Griffin(color, pos)
                    elif piece_type == 'Jumper':
                        piece = Jumper(color, pos)
                    elif piece_type == 'Wizard':
                        piece = Wizard(color, pos)
                    else:
                        piece = back_row_pieces[col](color, pos)
                else:
                    piece = back_row_pieces[col](color, pos)
                self.set_piece_at(pos, piece)

    def set_piece_at(self, pos: Position, piece: Optional[Piece]):
        self.grid[pos.row][pos.col] = piece
        if piece:
            piece.position = pos

    def get_piece_at(self, pos: Position) -> Optional[Piece]:
        if pos.is_valid():
            return self.grid[pos.row][pos.col]
        return None

    def is_valid_move(self, move: Move, check_check: bool = True) -> bool:
        piece = move.piece
        if piece is None or piece.color != self.current_turn:
            return False

        if move.to_pos == move.from_pos:
            return False

        possible = piece.get_possible_moves(self)
        if move.to_pos not in possible:
            return False

        if isinstance(piece, Pawn) and move.to_pos == self.en_passant_target:
            move.is_en_passant = True
            direction = -1 if piece.color == Color.WHITE else 1
            captured_pos = Position(move.to_pos.row - direction, move.to_pos.col)
            move.captured_piece = self.get_piece_at(captured_pos)
            if move.captured_piece and move.captured_piece.color != piece.color:
                pass
            else:
                return False
        else:
            target_piece = self.get_piece_at(move.to_pos)
            if target_piece and target_piece.color == piece.color:
                return False
            move.captured_piece = target_piece
        if isinstance(piece, Pawn):
            last_rank = 0 if piece.color == Color.WHITE else 7
            if move.to_pos.row == last_rank:
                if move.promotion_piece_type is None:
                    return False
            else:
                if move.promotion_piece_type:
                    return False

        if check_check:
            temp_board = self.simulate_move(move)
            if temp_board.is_king_in_check(self.current_turn):
                return False
        return True

    def simulate_move(self, move: Move) -> 'Board':
        new_board = copy.deepcopy(self)
        piece = new_board.get_piece_at(move.from_pos)
        if not piece:
            raise ValueError("ÐÐµÑ ÑÐ¸Ð³ÑÑÑ Ð½Ð° ÑÑÐ°ÑÑÐ¾Ð²Ð¾Ð¹ Ð¿Ð¾Ð·Ð¸ÑÐ¸Ð¸")

        new_board.set_piece_at(move.from_pos, None)
        if move.is_en_passant and move.captured_piece:
            new_board.set_piece_at(move.captured_piece.position, None)

        new_board.set_piece_at(move.to_pos, piece)
        piece.position = move.to_pos

        if isinstance(piece, Pawn) and move.promotion_piece_type:
            piece_type_map = {
                'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight
            }
            new_piece_class = piece_type_map.get(move.promotion_piece_type)
            if new_piece_class:
                new_piece = new_piece_class(piece.color, move.to_pos)
                new_board.set_piece_at(move.to_pos, new_piece)

        new_board.en_passant_target = None
        if isinstance(piece, Pawn) and abs(move.to_pos.row - move.from_pos.row) == 2:
            mid_row = (move.from_pos.row + move.to_pos.row) // 2
            new_board.en_passant_target = Position(mid_row, move.to_pos.col)

        return new_board

    def make_move(self, move: Move) -> bool:
        if not self.is_valid_move(move):
            return False
        self.move_history.append(move)
        self.set_piece_at(move.from_pos, None)
        if move.is_en_passant and move.captured_piece:
            self.set_piece_at(move.captured_piece.position, None)

        piece = move.piece
        self.set_piece_at(move.to_pos, piece)
        piece.position = move.to_pos
        piece.has_moved = True
        if isinstance(piece, Pawn) and move.promotion_piece_type:
            piece_type_map = {'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}
            new_piece_class = piece_type_map.get(move.promotion_piece_type)
            if new_piece_class:
                new_piece = new_piece_class(piece.color, move.to_pos)
                self.set_piece_at(move.to_pos, new_piece)
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(move.to_pos.row - move.from_pos.row) == 2:
            mid_row = (move.from_pos.row + move.to_pos.row) // 2
            self.en_passant_target = Position(mid_row, move.to_pos.col)

        self.current_turn = Color.opposite(self.current_turn)
        return True

    def undo_move(self) -> bool:
        if not self.move_history:
            return False
        last_move = self.move_history.pop()

        piece = last_move.piece
        self.set_piece_at(last_move.from_pos, piece)
        piece.position = last_move.from_pos
        piece.has_moved = False

        self.set_piece_at(last_move.to_pos, None)

        if last_move.captured_piece:
            self.set_piece_at(last_move.captured_piece.position, last_move.captured_piece)

        self.current_turn = Color.opposite(self.current_turn)
        return True

    def undo_moves(self, count: int) -> int:
        undone = 0
        for _ in range(count):
            if not self.undo_move():
                break
            undone += 1
        return undone

    def is_king_in_check(self, color: str) -> bool:
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(Position(row, col))
                if piece and piece.color == color and isinstance(piece, King):
                    king_pos = Position(row, col)
                    break
            if king_pos:
                break
        if not king_pos:
            return False

        opponent_color = Color.opposite(color)
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(Position(row, col))
                if piece and piece.color == opponent_color:
                    moves = piece.get_possible_moves(self)
                    if king_pos in moves:
                        return True
        return False

    def is_checkmate(self) -> bool:
        if not self.is_king_in_check(self.current_turn):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(Position(row, col))
                if piece and piece.color == self.current_turn:
                    for move_to in piece.get_possible_moves(self):
                        move = Move(piece, piece.position, move_to)
                        if self.is_valid_move(move, check_check=True):
                            return False
        return True

    def display(self):
        print("  a b c d e f g h")
        for row in range(8):
            print(8 - row, end=" ")
            for col in range(8):
                piece = self.get_piece_at(Position(row, col))
                if piece:
                    print(piece.get_symbol(), end=" ")
                else:
                    print(".", end=" ")
            print(8 - row)
        print("  a b c d e f g h\n")


class CheckersPiece(Piece):

    def __init__(self, color: str, position: Position, is_king: bool = False):
        super().__init__(color, position)
        self.is_king = is_king

    def get_possible_moves(self, board: 'Board') -> List[Position]:
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        if not self.is_king:
            for dc in [-1, 1]:
                new_pos = Position(self.position.row + direction, self.position.col + dc)
                if new_pos.is_valid() and board.get_piece_at(new_pos) is None:
                    moves.append(new_pos)
            for dc in [-1, 1]:
                mid_pos = Position(self.position.row + direction, self.position.col + dc)
                if mid_pos.is_valid():
                    mid_piece = board.get_piece_at(mid_pos)
                    if mid_piece and mid_piece.color != self.color:
                        land_pos = Position(self.position.row + 2 * direction, self.position.col + 2 * dc)
                        if land_pos.is_valid() and board.get_piece_at(land_pos) is None:
                            moves.append(land_pos)
        else:
            dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in dirs:
                for step in range(1, 8):
                    new_pos = Position(self.position.row + dr * step, self.position.col + dc * step)
                    if not new_pos.is_valid():
                        break
                    piece = board.get_piece_at(new_pos)
                    if piece is None:
                        moves.append(new_pos)
                    else:
                        if piece.color != self.color:
                            moves.append(new_pos)
                        break
        return moves

    def get_symbol(self) -> str:
        if self.color == Color.WHITE:
            return 'W' if not self.is_king else 'WK'
        else:
            return 'B' if not self.is_king else 'BK'


class CheckersBoard(Board):
    def _init_board(self, use_new: bool = False, new_positions: dict = None):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.set_piece_at(Position(row, col), CheckersPiece(Color.BLACK, Position(row, col)))
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.set_piece_at(Position(row, col), CheckersPiece(Color.WHITE, Position(row, col)))
        self.current_turn = Color.WHITE
        self.move_history = []

    def is_valid_move(self, move: Move, check_check: bool = True) -> bool:
        piece = move.piece
        if not piece or piece.color != self.current_turn:
            return False
        if move.to_pos not in piece.get_possible_moves(self):
            return False
        target = self.get_piece_at(move.to_pos)
        if target and target.color == piece.color:
            return False
        dr = move.to_pos.row - move.from_pos.row
        dc = move.to_pos.col - move.from_pos.col
        if abs(dr) == 2 and abs(dc) == 2:
            mid_row = (move.from_pos.row + move.to_pos.row) // 2
            mid_col = (move.from_pos.col + move.to_pos.col) // 2
            mid_piece = self.get_piece_at(Position(mid_row, mid_col))
            if not mid_piece or mid_piece.color == piece.color:
                return False
            move.captured_piece = mid_piece
        return True

    def make_move(self, move: Move) -> bool:
        if not self.is_valid_move(move):
            return False
        self.move_history.append(move)

        self.set_piece_at(move.from_pos, None)
        if move.captured_piece:
            self.set_piece_at(move.captured_piece.position, None)

        piece = move.piece
        self.set_piece_at(move.to_pos, piece)
        piece.position = move.to_pos

        if (piece.color == Color.WHITE and move.to_pos.row == 0) or (
                piece.color == Color.BLACK and move.to_pos.row == 7):
            if not piece.is_king:
                piece.is_king = True

        self.current_turn = Color.opposite(self.current_turn)
        return True

    def display(self):
        print("  a b c d e f g h  (Ð¨Ð°ÑÐºÐ¸)")
        for row in range(8):
            print(8 - row, end=" ")
            for col in range(8):
                piece = self.get_piece_at(Position(row, col))
                if piece:
                    sym = piece.get_symbol()
                    print(sym[0] if len(sym) == 1 else sym[0], end=" ")
                else:
                    print(".", end=" ")
            print(8 - row)
        print("  a b c d e f g h\n")


class Game:
    def __init__(self):
        self.board = None
        self.mode = None

    def start(self):
        print("ÐÐ¾Ð±ÑÐ¾ Ð¿Ð¾Ð¶Ð°Ð»Ð¾Ð²Ð°ÑÑ Ð² Ð¸Ð³ÑÑ!")
        print("ÐÑÐ±ÐµÑÐ¸ÑÐµ ÑÐµÐ¶Ð¸Ð¼:")
        print("1. ÐÐ»Ð°ÑÑÐ¸ÑÐµÑÐºÐ¸Ðµ ÑÐ°ÑÐ¼Ð°ÑÑ")
        print("2. Ð¨Ð°ÑÐ¼Ð°ÑÑ Ñ Ð½Ð¾Ð²ÑÐ¼Ð¸ ÑÐ¸Ð³ÑÑÐ°Ð¼Ð¸ (ÐÑÐ¸ÑÑÐ¸Ð½, ÐÑÑÐ³ÑÐ½, ÐÐ¾Ð»ÑÐµÐ±Ð½Ð¸Ðº)")
        print("3. Ð¨Ð°ÑÐºÐ¸")
        choice = input("ÐÐ°Ñ Ð²ÑÐ±Ð¾Ñ (1/2/3): ").strip()

        if choice == '1':
            self.mode = 'chess'
            self.board = Board(use_new_pieces=False)
        elif choice == '2':
            self.mode = 'chess_new'
            print("ÐÐ²ÐµÐ´Ð¸ÑÐµ Ð¿Ð¾Ð·Ð¸ÑÐ¸Ð¸ Ð´Ð»Ñ Ð½Ð¾Ð²ÑÑ ÑÐ¸Ð³ÑÑ Ð² ÑÐ¾ÑÐ¼Ð°ÑÐµ: ÐºÐ»ÐµÑÐºÐ° ÑÐ¸Ð¿")
            print("Ð¢Ð¸Ð¿Ñ: Griffin, Jumper, Wizard. ÐÑÐ¸Ð¼ÐµÑ: a1 Griffin c8 Jumper")
            positions_input = input("ÐÐ¾Ð·Ð¸ÑÐ¸Ð¸: ").strip()
            new_positions = {}
            tokens = positions_input.split()
            for i in range(0, len(tokens), 2):
                if i + 1 < len(tokens):
                    pos_str = tokens[i]
                    piece_type = tokens[i + 1]
                    if piece_type in ['Griffin', 'Jumper', 'Wizard']:
                        try:
                            pos = Position.from_chess_notation(pos_str)
                            new_positions[pos_str] = piece_type
                        except:
                            print(f"ÐÐµÐ²ÐµÑÐ½Ð°Ñ Ð¿Ð¾Ð·Ð¸ÑÐ¸Ñ {pos_str}, Ð¿ÑÐ¾Ð¿ÑÑÐºÐ°ÐµÐ¼")
            self.board = Board(use_new_pieces=True, new_pieces_positions=new_positions)
        elif choice == '3':
            self.mode = 'checkers'
            self.board = CheckersBoard()
        else:
            print("ÐÐµÐ²ÐµÑÐ½ÑÐ¹ Ð²ÑÐ±Ð¾Ñ, Ð·Ð°Ð¿ÑÑÐºÐ°Ñ ÐºÐ»Ð°ÑÑÐ¸ÑÐµÑÐºÐ¸Ðµ ÑÐ°ÑÐ¼Ð°ÑÑ")
            self.mode = 'chess'
            self.board = Board()

        self.game_loop()

    def game_loop(self):
        while True:
            self.board.display()
            if self.board.is_checkmate() and self.mode != 'checkers':
                print(f"ÐÐ°Ñ! ÐÐ¾Ð±ÐµÐ´Ð¸Ð» {Color.opposite(self.board.current_turn)}")
                break

            print(f"Ð¥Ð¾Ð´ {'Ð±ÐµÐ»ÑÑ' if self.board.current_turn == Color.WHITE else 'ÑÐµÑÐ½ÑÑ'}")
            cmd = input("ÐÐ²ÐµÐ´Ð¸ÑÐµ ÑÐ¾Ð´ (Ð½Ð°Ð¿ÑÐ¸Ð¼ÐµÑ 'e2 e4') Ð¸Ð»Ð¸ 'undo' Ð´Ð»Ñ Ð¾ÑÐºÐ°ÑÐ°, 'undo N', 'exit': ").strip()

            if cmd.lower() == 'exit':
                break
            if cmd.lower().startswith('undo'):
                parts = cmd.split()
                count = 1
                if len(parts) > 1:
                    try:
                        count = int(parts[1])
                    except:
                        count = 1
                self.board.undo_moves(count)
                print(f"ÐÑÐºÐ°Ñ Ð½Ð° {count} ÑÐ¾Ð´(Ð¾Ð²)")
                continue

            try:
                from_str, to_str = cmd.split()
                from_pos = Position.from_chess_notation(from_str)
                to_pos = Position.from_chess_notation(to_str)
                piece = self.board.get_piece_at(from_pos)
                if not piece:
                    print("ÐÐ° ÑÑÐ¾Ð¹ ÐºÐ»ÐµÑÐºÐµ Ð½ÐµÑ ÑÐ¸Ð³ÑÑÑ!")
                    continue

                promotion = None
                if isinstance(piece, Pawn) and (to_pos.row == 0 or to_pos.row == 7):
                    prom = input("ÐÑÐµÐ²ÑÐ°ÑÐ¸ÑÑ Ð¿ÐµÑÐºÑ Ð² (Q/R/B/N): ").upper()
                    if prom in ['Q', 'R', 'B', 'N']:
                        promotion = prom
                    else:
                        promotion = 'Q'

                move = Move(piece, from_pos, to_pos, promotion_piece_type=promotion)
                if self.board.make_move(move):
                    print("Ð¥Ð¾Ð´ Ð²ÑÐ¿Ð¾Ð»Ð½ÐµÐ½")
                else:
                    print("ÐÐµÐ´Ð¾Ð¿ÑÑÑÐ¸Ð¼ÑÐ¹ ÑÐ¾Ð´!")
            except Exception as e:
                print(f"ÐÑÐ¸Ð±ÐºÐ° Ð²Ð²Ð¾Ð´Ð°: {e}")


if __name__ == "__main__":
    game = Game()
    game.start()
