from django.conf import settings
from electronicAccessories.models import Electronic

class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket


    def save(self):
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True

    def add(self, product, count=1, update_count=False):
        product_pk = str(product.pk)

        if product_pk not in self.basket:
            self.basket[product_pk] = {
                'count_product': 0,
                'price_product': str(product.price)
            }

        if update_count:
            self.basket[product_pk]['count_product'] = count
        else:
            self.basket[product_pk]['count_product'] += count

        self.save()

    def remove(self, product):
        product_pk = str(product.pk)

        if product_pk in self.basket:
            del self.basket[product_pk]
            self.save()

    def get_total_price(self):
        return sum(float(item['price_product']) * int(item['count_product']) for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True

    def __len__(self):
        return sum(int(item['count_product']) for item in self.basket.values())

    def __iter__(self):
        list_product_pk = self.basket.keys()

        list_product_obj = Electronic.objects.filter(pk__in=list_product_pk)

        basket = self.basket.copy()

        for product_obj in list_product_obj:
            basket[str(product_obj.pk)]['laptop'] = product_obj
        for item in basket.values():
            item['total_price'] = float(item['price_product']) * int(item['count_product'])
            yield item