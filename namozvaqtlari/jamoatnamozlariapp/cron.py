import kronos
import random

@kronos.register('0 0 1 * *')
def test():
    print('test')


@kronos.register('0 0 * * *')
def test():
    print('test')