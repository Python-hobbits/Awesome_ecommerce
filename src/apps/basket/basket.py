from decimal import Decimal
from django.conf import settings
from src.apps.inventory.models import Product


class Basket(object):
    """
    The Basket class is used to manage a user's shopping basket.
    """

    def __init__(self, request):
        """
        The Basket instance is associated with the user's session, allowing
        the management of items in the basket.
        If no basket exists in the session, a new one is created.
        """
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)

        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):
        """
        This method allows adding a product to the basket, specifying the quantity.
        If the product is already in the basket, you can choose to update its
        quantity using the update_quantity parameter.
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {"quantity": 0, "price": str(product.price)}
        if update_quantity:
            self.basket[product_id]["quantity"] = quantity
        else:
            self.basket[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """
        This method updates the user's session with the current
        basket data and marks the session as modified.
        """
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True

    def remove(self, product):
        """
        Removes a product from the basket.
        If the specified product is in the basket, it is removed,
        and the changes are saved to the session.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        """
        This method iterates through the items in the basket, fetching product information
        and calculating total prices for each item. It yields the item as a dictionary
        with product details.
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.basket[str(product.id)]["product"] = product

        for item in self.basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Returns the total number of items in the basket.
        """
        return sum(item["quantity"] for item in self.basket.values())

    def get_total_price(self):
        """
        Returns the total price of all items in the basket.
        """
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.basket.values())

    def clear(self):
        """
        Clears the basket by removing all items.
        """
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True

    def get_quantity(self, product):
        """
        Returns the quantity of a specific product in the basket.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            return self.basket[product_id]["quantity"]
        return 0
