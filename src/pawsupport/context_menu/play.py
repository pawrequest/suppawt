from context_menu import menus
def foo1(filenames, params):
    print(filenames)
    input()


if __name__ == '__main__':

    fc = menus.FastCommand('Example Fast Command 1', type='FILES', python=foo1)
    fc.compile()

