from src.apps.basket.basket import Basket


def basket(request):
    return {"basket": Basket(request)}
