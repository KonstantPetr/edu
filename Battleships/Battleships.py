from random import randint
from random import choice


# logic

class Board:

    def __init__(self, hid=False, size=6):
        self.hid = hid  # скрывать ли расстановку кораблей на доске, фолс для своей доски, тру для доски врага
        self.size = size  # размер поля
        self.count = 0  # счётчик уничтоженных кораблей
        self.field = [['O'] * size for _ in range(size)]  # собственно игровое поле
        self.busy = []  # занятость клеток
        self.ships = []  # корабли

    def __str__(self):  # отображение поля
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'

        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hid:
            res = res.replace('■', 'O')

        return res

    def add_ship(self, ship):  # добавляет корабль

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()

        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):  # обводит контур корабля
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and (cur not in self.busy):
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def out(self, d):  # для объекта класса Dot возвращает тру если точка выходит за поле, фолс - если не выходит
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):  # производит попытку выстрела
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shoot(d):
                ship.hp -= 1
                self.field[d.x][d.y] = 'X'
                if ship.hp == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Ship demolished!')
                    return False
                else:
                    print('Ship hit!')
                    return True

        self.field[d.x][d.y] = '.'
        print('Miss!')
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Ship:

    def __init__(self, length, bow, direction):
        self.length = length  # длина корабля
        self.bow = bow  # точка, где находится нос корабля
        self.direction = direction  # направление корабля, вертикальное или горизонтельное
        self.hp = length  # оставшиеся жизни

    @property
    def dots(self):
        ship_dots = []

        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.direction == 'vert':
                cur_x += i
            if self.direction == 'hor':
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shoot(self, shot):
        return shot in self.dots


class Dot:

    def __init__(self, x, y):
        self.x = x  # координата точки по оси x
        self.y = y  # координата точки по оси y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


# frontend

class Game:

    def __init__(self, size=6):
        self.size = size
        u_board = self.random_board()
        c_board = self.random_board()
        c_board.hid = True
        self.user = User(u_board, c_board)
        self.ai = AI(c_board, u_board)

    def greet(self):  # приветствие и правила игры
        print('         Hi friend!          \n'
              ' Welcome to Battleship Game! \n'
              '  To make a turn enter: x y  \n'
              '           x - row           \n'
              '          y - column         \n')

    def random_board(self):
        board = None

        while board is None:
            board = self.try_board()

        return board

    def try_board(self):
        lengths = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0

        for l in lengths:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), choice(['vert', 'hor']))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()

        return board

    def loop(self):  # метод с самим игровым циклом
        num = 0
        while True:
            print('-'*30)
            print('User board:')
            print(self.user.my_board)
            print('-'*30)
            print('AI board:')
            print(self.ai.my_board)
            print('-'*30)
            if num % 2 == 0:
                print('User turn!')
                repeat = self.user.move()
            else:
                print('AI turn!')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.my_board.defeat():
                print('-'*30)
                print('User win!')
                break

            if self.user.my_board.defeat():
                print('-'*30)
                print('AI win!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


class Player:

    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):

        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class User(Player):

    def ask(self):
        while True:
            cords = input('Your turn:\n').split()

            if len(cords) != 2:
                print('Enter TWO numbers separated by space!')
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print('You have to enter DIGITS, not anything else!')
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class AI(Player):

    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Computer turn: {d.x + 1} {d.y + 1}')
        return d


# exceptions

class BoardException(Exception):
    pass


class BoardOutException(BoardException):

    def __str__(self):
        return "You're trying to shoot outside the game board!"


class BoardUsedException(BoardException):

    def __str__(self):
        return 'You already shot this cell!'


class BoardWrongShipException(BoardException):
    pass


game = Game()
game.start()
