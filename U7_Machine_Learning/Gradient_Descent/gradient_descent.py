import sys


def ax(x, y):
    return 8 * x - 3 * y + 24


def ay(x, y):
    return 4 * (y - 5) - 3 * x


def bx(x, y):
    return 2 * (x - y ** 2)


def by(x, y):
    return 2 * (-2 * x * y + 2 * (y ** 3) + y - 1)


def magnitude(w2):
    return (w2[0] ** 2 + w2[1] ** 2) ** .5


def minimize(x, y, choice):
    if choice == 'A':
        lamb, grad = .1, (ax(x, y), ay(x, y))
        w2 = (lamb * grad[0], lamb * grad[1])
        x -= w2[0]
        y -= w2[1]
        while magnitude(grad) > (10 ** -8):
            print(x, y, magnitude(w2))
            grad = (ax(x, y), ay(x, y))
            w2 = (lamb * grad[0], lamb * grad[1])
            x -= w2[0]
            y -= w2[1]
            print(x, y, magnitude(w2))
        print('Final Location: (' + str(x) + ',', str(y) + ')')
    elif choice == 'B':
        lamb, grad = .1, (bx(x, y), by(x, y))
        w2 = (lamb * grad[0], lamb * grad[1])
        x -= w2[0]
        y -= w2[1]
        while magnitude(w2) > (10 ** -8):
            print(x, y, magnitude(w2))
            grad = (bx(x, y), by(x, y))
            w2 = (lamb * grad[0], lamb * grad[1])
            x -= w2[0]
            y -= w2[1]
            print(x, y, magnitude(w2))
        print('Final Location: (' + str(x) + ',', str(y) + ')')


def inputt():
    user_in = sys.argv[1]
    minimize(0, 0, user_in)


inputt()
