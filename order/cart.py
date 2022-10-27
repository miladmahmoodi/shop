from product.models import Product as ProductModel

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = dict()
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity):
        product_pk = str(product.pk)
        if product_pk not in self.cart:
            self.cart[product_pk] = {
                'quantity': 0,
                'price': str(product.price),
            }
        self.cart[product_pk]['quantity'] += quantity
        self.save()

    def __iter__(self):
        pks = self.cart.keys()
        products = ProductModel.objects.filter(
            pk__in=pks,
        )
        for product in products:
            self.cart[str(product.pk)]['product'] = product

        cart_items = self.cart.values()
        for item in cart_items:
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def remove(self, product):
        product_pk = str(product.pk)
        if product_pk in self.cart:
            del self.cart[product_pk]
            self.save()

    def total_cart(self):
        return sum(int(item['total_price']) for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
