from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_del = models.BooleanField(default=False, verbose_name='是否注销')

    class Meta:
        # 设定该类为抽象类,不迁移
        abstract = True
