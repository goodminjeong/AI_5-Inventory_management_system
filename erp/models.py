from django.db import models

# Create your models here.


class Product(models.Model):
    class Meta:
        db_table = "product"
        verbose_name = "상품"

    code = models.CharField(max_length=32, null=False, verbose_name='상품코드')
    name = models.CharField(max_length=32, null=False, verbose_name='상품명')
    description = models.TextField(max_length=256, verbose_name='상품설명')
    price = models.IntegerField(max_length=32, verbose_name='상품가격')
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1, verbose_name='상품사이즈')

    def __str__(self):
        return self.code

    # def save(self, *args, **kwargs):
    #     # 생성될 때 stock quantity를 0으로 초기화 로직
    #     super().save(*args, **kwargs)


class Inbound(Product):
    """
                입고 모델입니다.
                상품, 수량, 입고 날짜, 금액 필드를 작성합니다.
                """
    class Meta:
        db_table = "inbound"
        verbose_name = "입고"

    product = Product()
    name = Product.name
    price = Product.price
    quantity = models.IntegerField(max_length=32, verbose_name='상품수량')
    inbound_date = models.DateTimeField(auto_now_add=True)
