from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TestCasePath(models.Model):
    typeDict = ((0,u'测试用例文件'),(1,u'码文件'))

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,blank=False)
    filePath = models.FilePathField(path="/usr/testcase",recursive=True)
    type = models.IntegerField(choices=typeDict)
    createTime = models.DateField(auto_now_add=True)
    updateTime = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,default=None)

    class Meta:
        verbose_name = "导入文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name