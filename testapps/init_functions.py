from .models import *

def init_status_details():
  status_details=[
    StatusDetail(title="No run"),
    StatusDetail(title="Passed"),
    StatusDetail(title="Faield"),
    StatusDetail(title="Pending"),
    StatusDetail(title="Not test"),
    StatusDetail(title="Blocked")
  ]
  StatusDetail.objects.bulk_create(status_details)

def init_environments():
  environment = [
    Environment(title="Development"),
    Environment(title="Pre-Production (UAT)"),
    Environment(title="Production")
  ]

  Environment.objects.bulk_create(environment)

def init_projects():
  project = [
    Project(title='Major Mobile App', created_by='admin', updated_by='admin')
  ]
  Project.objects.bulk_create(project)

import pandas as pd

def import_sheet():
  number_sheet_read = 0
  path_file = "C:\\Users\\pongpat.cho\\Downloads\\Major Cineplex Project Test Cases.xlsx"
  excel = pd.ExcelFile(path_file)

  sheet_names = excel.sheet_names  

  use_col_map = {
    "module": "A",
    "test_case_id": "D",
    "test_case_desc": "E",
    "test_step": "N",
    "expect_output": "O",
    "remark": "T",
    "test_status": "U",
    "tester": "V",
    "os": "Y"
  }

  usecols = list(use_col_map.values())
  usecols = str(usecols)[1:-1]
  usecols = usecols.replace("'", "")

  excel_sheet = pd.read_excel(excel, header=1, sheet_name=sheet_names[number_sheet_read], usecols=usecols, dtype=str)

  if TestScriptDetail.objects.filter(title=sheet_names[number_sheet_read], project_id=1, environment_id=2).count() == 0:
    test_script_detail = TestScriptDetail(title=sheet_names[number_sheet_read], project_id=1, environment_id=2)
    test_script_detail.save()
    test_script_detail_id = test_script_detail.id
  else:
    test_script_detail_id = TestScriptDetail.objects.filter(title=sheet_names[number_sheet_read], project_id=1, environment_id=2).values('id').latest('id')['id']

  current_test_case_card_id = ""
  for index, row in excel_sheet.iterrows():
    module = row[0]
    code = row[1]
    desc = row[2]
    step = row[3]
    result = row[4]
    remark = row[5]
    status = row[6]
    tester = row[7]
    os = row[8]
    
    if not pd.isna(module) and not pd.isna(code) and pd.isna(desc):
      pass
    elif not pd.isna(module) and pd.isna(code) and pd.isna(desc):
      # test case card
      if TestCaseCard.objects.filter(title=module, test_script_detail_id=test_script_detail_id).count() == 0:
        temp = TestCaseCard(title=module, test_script_detail_id=test_script_detail_id)
        temp.save()
        current_test_case_card_id = temp.id
      else:
        current_test_case_card_id = TestCaseCard.objects.filter(title=module, test_script_detail_id=test_script_detail_id).values('id').latest('id')['id']
    elif not pd.isna(code) and not pd.isna(desc):
      if pd.isna(code):
        code = "-"
      if pd.isna(desc):
        desc = "-"
      if pd.isna(step):
        step = "-"
      if pd.isna(result):
        result = "-"
      if pd.isna(remark):
        remark = "-"
      if pd.isna(status):
        status = "no run"
      
      if pd.isna(module):
        module = "-"
      if ModuleDetail.objects.filter(title=module).count() == 0:
        module = ModuleDetail(title=module)
        module.save()
        module_id = module.id
      else:
        module_id = ModuleDetail.objects.filter(title=module).values('id').latest('id')['id']

      if pd.isna(tester):
        tester = "-"
      if Tester.objects.filter(title=tester).count() == 0:
        temp = Tester(title=tester)
        temp.save()
        tester_id = temp.id
      else:
        tester_id = Tester.objects.filter(title=tester).values('id').latest('id')['id']

      if pd.isna(os):
        os = "-"
      if OsAndDeviceDetail.objects.filter(title=os).count() == 0:
        temp = OsAndDeviceDetail(title=os)
        temp.save()
        os_id = temp.id
      else:
        os_id = OsAndDeviceDetail.objects.filter(title=os).values('id').latest('id')['id']

      status_detail_id = StatusDetail.objects.filter(title__icontains=status).values('id').latest('id')['id']

      test_case_card_detail = TestCaseCardDetail(
        code=code,
        expect_output=result,
        test_step=step,
        remark=remark,
        description=desc,
        module_detail_id=module_id,
        status_detail_id=status_detail_id,
        os_and_device_detail_id=os_id,
        tester_id=tester_id,
        test_case_card_id=current_test_case_card_id
      )
      test_case_card_detail.save()
    
    print(index, "!!!!!!!!!")
