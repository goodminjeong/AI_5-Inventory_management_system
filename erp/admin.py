from django.contrib import admin
from .models import Product, Inbound, Outbound

# Register your models here.
admin.site.register(Product)  # 이 코드가 나의 Product 모델을 Admin에 추가 해 줍니다
admin.site.register(Inbound)
admin.site.register(Outbound)
