from django.db import models

# Create your models here.


class Product(models.Model):
    code = models.CharField(max_length=32, verbose_name='상품코드')
    name = models.CharField(max_length=200, verbose_name='상품명')
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

    def save(self, *args, **kwargs):
        # 생성될 때 stock quantity를 0으로 초기화 로직
        pass
