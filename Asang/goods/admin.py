from django.contrib import admin

# Register your models here.
from goods.models import CategoryModel, UnitModel, GoodsSPUModel, GoodsSKUModel, GalleryModel, BannerModel, \
    ActivityModel, ZoneModel

admin.site.register(CategoryModel)
admin.site.register(UnitModel)
admin.site.register(GoodsSPUModel)
admin.site.register(GoodsSKUModel)
admin.site.register(GalleryModel)
admin.site.register(BannerModel)
admin.site.register(ActivityModel)
admin.site.register(ZoneModel)
