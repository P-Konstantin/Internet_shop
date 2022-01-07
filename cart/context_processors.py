from .cart import Cart


def cart(request):
    '''Контектстный процессор - функция Python,
    принимающая объект запроса request и возвращающая словарь,
    который будет добавлен в контекст запроса.'''
    return {'cart': Cart(request)}


