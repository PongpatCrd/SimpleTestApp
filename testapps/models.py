from django.db import models
from django.utils.timezone import now
from django.conf import settings

# Create your models here.
class Environment(models.Model):
  id         = models.AutoField(primary_key=True)
  title      = models.CharField(max_length=100)
  created_at = models.DateTimeField(default=now, editable=False)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'environments'

class Project(models.Model):
  id         = models.AutoField(primary_key=True)
  title      = models.CharField(max_length=255, null=False, blank=False)
  created_at = models.DateTimeField(default=now, editable=False)
  updated_at = models.DateTimeField(auto_now=True)
  created_by = models.CharField(max_length=50, null=False, blank=False, default="system")
  updated_by = models.CharField(max_length=50, null=False, blank=False, default="system")
  
  class Meta:
    db_table = 'projects'

class StatusDetail(models.Model):
  id         = models.AutoField(primary_key=True)
  title      = models.CharField(max_length=50, null=False, blank=False)
  created_at = models.DateTimeField(default=now, editable=False)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'status_details'

class ModuleDetail(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100, null=False, blank=False)
  created_at = models.DateTimeField(default=now, editable=False)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'module_details'

class OsAndDeviceDetail(models.Model):
  id    = models.AutoField(primary_key=True)
  title = models.CharField(max_length=125)
  created_at = models.DateTimeField(default=now, editable=False)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'os_and_device_details'

class TestScriptDetail(models.Model):
  id          = models.AutoField(primary_key=True)
  title       = models.CharField(max_length=255, null=False, blank=False)
  created_at  = models.DateTimeField(default=now, editable=False)
  updated_at  = models.DateTimeField(auto_now=True)
  project     = models.ForeignKey(Project, on_delete=models.CASCADE)
  environment = models.ForeignKey(Environment, on_delete=models.CASCADE)

  class Meta:
    db_table = 'test_script_details'

class Tester(models.Model):
  id         = models.AutoField(primary_key=True)
  title      = models.CharField(max_length=60)
  created_at = models.DateTimeField(default=now, editable=False)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'testers'

class TestCaseCard(models.Model):
  id                 = models.AutoField(primary_key=True)
  title              = models.CharField(max_length=150, null=False, blank=False)
  created_at         = models.DateTimeField(default=now, editable=False)
  updated_at         = models.DateTimeField(auto_now=True)
  test_script_detail = models.ForeignKey(TestScriptDetail, on_delete=models.CASCADE)

  class Meta:
    db_table = 'test_case_card'

class TestCaseCardDetail(models.Model):
  id                      = models.AutoField(primary_key=True)
  code                    = models.CharField(max_length=255, null=False, blank=True)
  expect_output           = models.TextField(null=True, blank=True)
  test_step               = models.TextField(null=True, blank=True)
  remark                  = models.TextField(null=True, blank=True)
  description             = models.TextField(null=True, blank=True)
  module_detail           = models.ForeignKey(ModuleDetail, on_delete=models.CASCADE, null=True)
  status_detail           = models.ForeignKey(StatusDetail, on_delete=models.CASCADE, null=True)
  os_and_device_detail    = models.ForeignKey(OsAndDeviceDetail, on_delete=models.SET_NULL, null=True)
  tester                  = models.ForeignKey(Tester, on_delete=models.SET_NULL, null=True)
  test_case_card          = models.ForeignKey(TestCaseCard, on_delete=models.CASCADE)
  created_at              = models.DateTimeField(default=now, editable=False)
  updated_at              = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = 'test_case_card_detail'

class TestCaseCardDetailImg(models.Model):
  id = models.AutoField(primary_key=True)
  photo = models.ImageField(upload_to="attachments/%Y/%m/%d/")
  test_case_card_detail = models.ForeignKey(TestCaseCardDetail, on_delete=models.CASCADE)

  class Meta:
    db_table = 'test_case_card_detail_img'