from src.apps.basket.models import Basket


def basket(request):
    return {'basket': Basket(request)}
