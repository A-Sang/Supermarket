from django.contrib import admin

# Register your models here.
from goods.models import CategoryModel, UnitModel, GoodsSPUModel, GoodsSKUModel, GalleryModel

admin.site.register(CategoryModel)
admin.site.register(UnitModel)
admin.site.register(GoodsSPUModel)
admin.site.register(GoodsSKUModel)
admin.site.register(GalleryModel)
