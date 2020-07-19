from django.db import transaction
from datetime import datetime
from testapps.models import *
from django.forms.models import model_to_dict

import base64

def get_test_details(test_script_detail_id):
  test_status_is_complete = ['Passed']
  test_details = []
  status_test_is_complete = StatusDetail.objects.filter(title__in=test_status_is_complete).values_list('id', flat=True)
  test_case_cards = TestCaseCard.objects.filter(test_script_detail_id=test_script_detail_id).all()

  test_case_card_detail_img = TestCaseCardDetailImg.objects.all().order_by('test_case_card_detail_id', 'id')
  test_case_card_detail_imgs_dict = {}
  for detail in test_case_card_detail_img:
    try:
      test_case_card_detail_imgs_dict[detail.test_case_card_detail.id].append(detail)
    except:
      test_case_card_detail_imgs_dict[detail.test_case_card_detail.id] = [detail]

  test_details = []
  for test_case_card in test_case_cards:
    temp = {
      'test_case_card_id'            : test_case_card.id,
      'test_case_title'              : test_case_card.title,
      'test_case_card_details'       : [],
      'n_test_cases_passed'          : 0
    }
    test_case_card_details = test_case_card.testcasecarddetail_set.values()
    for test_case_card_detail in test_case_card_details:
      test_case_card_detail['updated_at'] = test_case_card_detail['updated_at'].strftime('%Y-%m-%d %H:%M:%S.%f')

      try:
        test_case_card_detail['test_case_card_detail_imgs'] = test_case_card_detail_imgs_dict[test_case_card_detail['id']]
      except:
        test_case_card_detail['test_case_card_detail_imgs'] = []

      temp['test_case_card_details'].append(test_case_card_detail)
      if test_case_card_detail['status_detail_id'] in status_test_is_complete:
        temp['n_test_cases_passed'] += 1
    test_details.append(temp)

  return test_details

def get_export_test_details(test_case_card_ids):
  test_case_cards = TestCaseCard.objects.filter(id__in=test_case_card_ids).all()

  test_details = []
  for test_case_card in test_case_cards:
    temp = {
      'test_case_card_id'            : test_case_card.id,
      'test_case_title'              : test_case_card.title,
      'test_case_card_details'       : []
    }
    test_case_card_details = test_case_card.testcasecarddetail_set.all()
    for test_case_card_detail in test_case_card_details:
      temp_test_case_card_detail = {
        'code': test_case_card_detail.code,
        'module_detail_title': test_case_card_detail.module_detail.title,
        'remark': test_case_card_detail.remark,
        'status_detail_title': test_case_card_detail.status_detail.title,
        'tester_title': test_case_card_detail.tester.title,
        'os_and_device_detail_title': test_case_card_detail.os_and_device_detail.title,
        'updated_at': test_case_card_detail.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
      }

      temp['test_case_card_details'].append(temp_test_case_card_detail)
    test_details.append(temp)

  return test_details

def delete_test_case_card_detail_by_ids(arr_id):
  try:
    with transaction.atomic():
      TestCaseCardDetail.objects.filter(id__in=arr_id).delete()
    complete = True
    msg = ''
  except:
    complete = False
    msg = 'Error delete_test_case_card_detail_by_ids.'
  
  result = {
    'complete': complete,
    'msg': msg
  }
  return result

def delete_test_case_card_detail_img_by_ids(arr_id):
  try:
    with transaction.atomic():
      TestCaseCardDetailImg.objects.filter(id__in=arr_id).delete()
    complete = True
    msg = ''
  except:
    complete = False
    msg = 'Error delete_test_case_card_detail_img_by_ids.'
  
  result = {
    'complete': complete,
    'msg': msg
  }
  return result

def collect_text(request):
  module_ids = request.POST.getlist('module_choose')
  new_module_titles = request.POST.getlist('new_module_choose')
  tester_id = request.POST.get('tester_choose')
  new_tester_choose = request.POST.get('new_tester_choose')
  os_and_device_detail_id = request.POST.get('os_and_device_detail_choose')
  new_os_and_device_detail_choose = request.POST.get('new_os_and_device_detail_choose')

  db_module_detail_ids = ModuleDetail.objects.values_list('id', flat=True)
  for i in range(len(module_ids)):
    id = int(module_ids[i])
    if id not in db_module_detail_ids and ModuleDetail.objects.filter(title=new_module_titles[i]).values().count() == 0:
      ModuleDetail(title=new_module_titles[i]).save()
  
  db_tester_ids = Tester.objects.values_list('id', flat=True)
  id = int(tester_id)
  if id not in db_tester_ids and Tester.objects.filter(title=new_tester_choose).values().count() == 0:
    Tester(title=new_tester_choose).save()

  db_os_and_device_detail_ids = OsAndDeviceDetail.objects.values_list('id', flat=True)
  id = int(os_and_device_detail_id)
  if id not in db_os_and_device_detail_ids and OsAndDeviceDetail.objects.filter(title=new_os_and_device_detail_choose).values().count() == 0:
    OsAndDeviceDetail(title=new_os_and_device_detail_choose).save()
  return

def update_test_case_card_detail(request):
  module_ids = request.POST.getlist('module_choose')
  new_module_titles = request.POST.getlist('new_module_choose')
  test_case_codes = request.POST.getlist('test_case_code')
  test_case_descs = request.POST.getlist('test_case_desc')
  test_case_steps = request.POST.getlist('test_case_step')
  test_case_outputs = request.POST.getlist('test_case_output')
  test_case_remarks = request.POST.getlist('test_case_remark')
  status_detail_ids = request.POST.getlist('status_detail_choose')
  last_update_times = request.POST.getlist('last_update_time')
  test_case_card_detail_ids = request.POST.getlist('test_case_card_detail_id')

  tester_id = request.POST.get('tester_choose')
  new_tester_choose = request.POST.get('new_tester_choose')
  os_and_device_detail_id = request.POST.get('os_and_device_detail_choose')
  new_os_and_device_detail_choose = request.POST.get('new_os_and_device_detail_choose')
  test_case_card_id = request.POST.get('test_case_card_id')

  db_test_case_card_details_ids = TestCaseCardDetail.objects.values_list('id', flat=True)
  new_test_case_card_detail_imgs = []
  for i in range(len(test_case_card_detail_ids)):
    try:
      id = int(test_case_card_detail_ids[i])    
    except:
      id = test_case_card_detail_ids[i]
    
    if id in db_test_case_card_details_ids:
      obj = TestCaseCardDetail.objects.get(id=id)
      last_update_time = datetime.strptime(last_update_times[i], '%Y-%m-%d %H:%M:%S.%f')

      if obj.updated_at.strftime('%Y-%m-%d %H:%M:%S') < last_update_time.strftime('%Y-%m-%d %H:%M:%S'):
        obj.code = test_case_codes[i]
        obj.expect_output = test_case_outputs[i]
        obj.test_step = test_case_steps[i]
        obj.remark = test_case_remarks[i]
        obj.description = test_case_descs[i]

        if module_ids[i] == "-1":
          module_id = ModuleDetail.objects.get(title=new_module_titles[i]).id
        else:
          module_id = module_ids[i]
        obj.module_detail_id = module_id

        obj.status_detail_id = int(status_detail_ids[i])
        
        if os_and_device_detail_id == "-1":
          os_and_device_detail_id = OsAndDeviceDetail.objects.get(title=new_os_and_device_detail_choose).id
        obj.os_and_device_detail_id = int(os_and_device_detail_id)
        
        if tester_id == "-1":
          tester_id = Tester.objects.get(title=new_tester_choose).id
        obj.tester_id = tester_id
        obj.updated_at = last_update_times[i]
        
        obj.save()

        test_case_card_detail_id = obj.id
        
        if test_case_card_detail_id:
          input_name = "attach_file" + test_case_card_detail_ids[i]
          imgs = request.FILES.getlist(input_name)
          for img in imgs:
            if img.size <= (512*1024):
              new_test_case_card_detail_imgs.append(
                TestCaseCardDetailImg(photo=img, test_case_card_detail_id=test_case_card_detail_id)
              ) 
      else:
        pass
    else:
      pass
  try:
    with transaction.atomic():
      TestCaseCardDetailImg.objects.bulk_create(new_test_case_card_detail_imgs)
  except:
    pass
  return

def insert_test_case_card_detail(request):
  module_ids = request.POST.getlist('module_choose')
  new_module_titles = request.POST.getlist('new_module_choose')
  test_case_codes = request.POST.getlist('test_case_code')
  test_case_descs = request.POST.getlist('test_case_desc')
  test_case_steps = request.POST.getlist('test_case_step')
  test_case_outputs = request.POST.getlist('test_case_output')
  test_case_remarks = request.POST.getlist('test_case_remark')
  status_detail_ids = request.POST.getlist('status_detail_choose')
  last_update_times = request.POST.getlist('last_update_time')
  test_case_card_detail_ids = request.POST.getlist('test_case_card_detail_id')
  

  tester_id = request.POST.get('tester_choose')
  new_tester_choose = request.POST.get('new_tester_choose')
  os_and_device_detail_id = request.POST.get('os_and_device_detail_choose')
  new_os_and_device_detail_choose = request.POST.get('new_os_and_device_detail_choose')
  test_case_card_id = request.POST.get('test_case_card_id')

  all_keys = request.POST.keys()
  
  db_test_case_card_detail_ids = list(TestCaseCardDetail.objects.values_list('id', flat=True).order_by('id'))
  new_test_case_card_detail_imgs = []
  for i in range(len(test_case_card_detail_ids)):
    try:
      id = int(test_case_card_detail_ids[i])
    except:
      id = test_case_card_detail_ids[i]

    if id not in db_test_case_card_detail_ids:
      new_record = True
    elif id <= db_test_case_card_detail_ids[-1]:
      new_record = False
    else:
      new_record = True

    if new_record:
      code = test_case_codes[i]
      expect_output = test_case_outputs[i]
      test_case_step = test_case_steps[i]
      remark = test_case_remarks[i]
      description = test_case_descs[i]
      
      if module_ids[i] == "-1":
        module_id = ModuleDetail.objects.get(title=new_module_titles[i]).id
      else:
        module_id = module_ids[i]
      module_detail_id = module_id
      
      status_detail_id = int(status_detail_ids[i])
      
      if os_and_device_detail_id == "-1":
        os_and_device_detail_id = OsAndDeviceDetail.objects.get(title=new_os_and_device_detail_choose).id
      os_and_device_detail_id = int(os_and_device_detail_id)
      
      if tester_id == "-1":
        tester_id = Tester.objects.get(title=new_tester_choose).id
      tester_id = int(tester_id)
      
      test_case_card_detail = TestCaseCardDetail(
        code                    = code,
        expect_output           = expect_output,
        test_step               = test_case_step,
        remark                  = remark,
        description             = description,
        module_detail_id        = module_detail_id,
        status_detail_id        = status_detail_id,
        os_and_device_detail_id = os_and_device_detail_id,
        tester_id               = tester_id,
        test_case_card_id       = test_case_card_id,
        updated_at              = last_update_times[i]
      )

      try:
        with transaction.atomic():
          test_case_card_detail.save()
          test_case_card_detail_id = test_case_card_detail.id
      except:
        test_case_card_detail_id = ""
      
      if test_case_card_detail_id:
        input_name = "attach_file" + test_case_card_detail_ids[i]
        imgs = request.FILES.getlist(input_name)
        for img in imgs:
          if img.size <= (512*1024):
            new_test_case_card_detail_imgs.append(
              TestCaseCardDetailImg(photo=img, test_case_card_detail_id=test_case_card_detail_id)
            ) 
  try:
    with transaction.atomic():
      TestCaseCardDetailImg.objects.bulk_create(new_test_case_card_detail_imgs)
  except:
    pass
  return

def export_test_case_card_html_str(test_case_card_ids):
  test_case_cards = TestCaseCard.objects.filter(id__in=test_case_card_ids).all()
  html_str = ""
  for test_case_card in test_case_cards:
    html_str += "<h3>Test Script: {}</h3>".format(test_case_card.test_script_detail.title)
    html_str += "<h4>Test Case: {}</h4>".format(test_case_card.title)
    for test_case_card_detail in test_case_card.testcasecarddetail_set.all():
      temp_html = ""
      temp_html += """
        <h7><b>Module:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Test Code:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Test Description:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Remark:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Test Status:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Last Updated:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Tester:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Device/OS:</b> <span style="font-weight:normal; color: red;">{}</span></h7><br>
        <h7><b>Attachments</b></h7><br>
      """.format(
        test_case_card_detail.module_detail.title,
        test_case_card_detail.code,
        test_case_card_detail.description,
        test_case_card_detail.remark,
        test_case_card_detail.status_detail.title,
        test_case_card_detail.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        test_case_card_detail.tester.title,
        test_case_card_detail.os_and_device_detail.title
      )
      
      for test_case_card_detail_img in test_case_card_detail.testcasecarddetailimg_set.all():
        path = "." + test_case_card_detail_img.photo.url
        data_uri = base64.b64encode(open(path, 'rb').read()).decode('ascii')
  
        temp_html += "<img src='data:image/png;base64,{}' style='max-width: 512px; max-height: 512px;'><br><br>".format(data_uri)
      temp_html += "<hr style='width=90%;'>"
      html_str += temp_html
  return html_str

def gen_file_name():
  timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
  file_name = "STA_export_{}.html".format(timestamp)
  return file_name