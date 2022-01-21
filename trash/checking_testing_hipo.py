import sys


def check_a(var):
    if var is True:
        print('Is True\n')
        # print('check', (sys.exc_info()[0] is None), sys.exc_info())
        raise Exception(('comment', 'Тут жопа'))
    else:
        print('Is False\n')

        var = 1 / 0


def catch(fn, par):
    try:
        fn(par)
    except Exception as rr:
        ex0 = sys.exc_info()[0]
        ex1 = sys.exc_info()[1]
        ex2 = sys.exc_info()[2]
        print('args[0]', ex0.args, type(ex0.args), type(ex0))
        print('args[1]', ex1.args, type(ex1.args))
        print('[2]', ex2, type(ex2))
        print('check_catch', sys.exc_info())
        print()

        if ex0 == Exception:
            print('\n\nYES!!!\n\n')


catch(check_a, True)
catch(check_a, False)
