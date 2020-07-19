from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from testapps.models import *
from testapps.controllers import *

# Create your views here.
def index(request):
  projects = Project.objects.values()
  environments = Environment.objects.values()

  context = {
    'projects'    : projects,
    'environments': environments
  }
  return render(request, 'testapps/index.html', context)

def index_test_script_detail_select_html(request):
  if request.method == "GET":
    project_id = request.GET.get('project_selector')
    env_id = request.GET.get('environment_selector')
  else:
    project_id = request.POST.get('project_selector')
    env_id = request.POST.get('environment_selector')
  
  test_script_details = TestScriptDetail.objects.filter(project_id=project_id, environment_id=env_id).all()
  context = {
    'test_script_details'   : test_script_details
  }
  index_test_script_detail_select_html = render_to_string('testapps/index_test_script_detail_select.html', context, request=request)

  response = {
    'index_test_script_detail_select_html': index_test_script_detail_select_html
  }
  return JsonResponse(response)

def index_test_script_detail_select_on_selected(request):
  project_id = request.POST.get('project_selector')
  env_id = request.POST.get('environment_selector')
  test_script_detail_id = request.POST.get('test_script_detail_choose')
  new_test_script_title = request.POST.get('new_test_script_detail_choose')

  test_script_detail = TestScriptDetail.objects.filter(title=new_test_script_title, project=project_id, environment=env_id).values()
  if len(test_script_detail) > 0:
    test_script_detail = test_script_detail[0]
    
  if test_script_detail_id == "-1":
    if len(test_script_detail) == 0:
      try:
        with transaction.atomic():
          project = Project.objects.get(id=project_id)
          environment = Environment.objects.get(id=env_id)
        
          test_script_detail = TestScriptDetail(title=new_test_script_title, project=project, environment=environment)
          test_script_detail.save()
          test_script_detail_id = test_script_detail.id
      except:
        pass
    else:
      test_script_detail_id = test_script_detail['id']
  
  test_script_details = TestScriptDetail.objects.filter(project_id=project_id, environment_id=env_id).all()
  context = {
    'current_test_script_detail_id': test_script_detail_id,
    'test_script_details'   : test_script_details
  }
  index_test_script_detail_select_html = render_to_string('testapps/index_test_script_detail_select.html', context, request=request)
  
  module_details = ModuleDetail.objects.values()
  status_details = StatusDetail.objects.values()
  os_and_device_details = OsAndDeviceDetail.objects.values()
  testers = Tester.objects.values()

  test_details = get_test_details(test_script_detail_id)
  context = {
    'current_test_script_detail_id': test_script_detail_id,
    'module_details'               : module_details,
    'status_details'               : status_details,
    'os_and_device_details'        : os_and_device_details,
    'testers'                      : testers,
    'test_details'                 : test_details
  }
  test_case_card_html = render_to_string('testapps/test_case_cards.html', context, request=request)

  response = {
    'index_test_script_detail_select_html': index_test_script_detail_select_html,
    'test_case_card_html': test_case_card_html
  }
  return JsonResponse(response)

def test_case_card_html(request):
  if request.method == "GET":
    test_script_detail_id = request.GET.get('test_script_detail_choose')
  else:
    test_script_detail_id = request.POST.get('test_script_detail_choose')
  if not test_script_detail_id:
    if request.method == "GET":
      test_script_detail_id = request.GET.get('test_script_detail_id')
    else:
      test_script_detail_id = request.POST.get('test_script_detail_id')

  module_details = ModuleDetail.objects.values()
  status_details = StatusDetail.objects.values()
  os_and_device_details = OsAndDeviceDetail.objects.values()
  testers = Tester.objects.values()

  test_details = get_test_details(test_script_detail_id)
  context = {
    'current_test_script_detail_id': test_script_detail_id,
    'module_details'               : module_details,
    'status_details'               : status_details,
    'os_and_device_details'        : os_and_device_details,
    'testers'                      : testers,
    'test_details'                 : test_details
  }
  test_case_card_html = render_to_string('testapps/test_case_cards.html', context, request=request)
  response = {
    'test_case_card_html': test_case_card_html
  }
  return JsonResponse(response)

def update_test_case_card_details(request):
  '''
  see parameter need at test_case_cards.html in $("#test_case_card_form{{ forloop.counter }}").on('submit', function(e){
  '''
  datas = request.POST

  # delete test_case_card_detail
  delete_ids = datas.getlist('delete_ids')
  if delete_ids:
    delete_test_case_card_detail_by_ids(delete_ids)

  # delete_test_case_card_detail_img
  delete_img_ids = datas.getlist('delete_img_ids')
  if delete_img_ids:
    delete_test_case_card_detail_img_by_ids(delete_img_ids)

  # collect new text
  collect_text(request)
  
  # update test_case_card_detail
  update_test_case_card_detail(request)
  
  # insert new test_case_card_detail
  insert_test_case_card_detail(request)

  response = test_case_card_html(request)
  return response

def create_test_case_card(request):
  test_case_card_title = request.POST.get('test_case_card_title')
  test_script_detail_id = request.POST.get('test_script_detail_id')

  try:
    with transaction.atomic():
      if test_case_card_title and test_script_detail_id:
        test_case_card = TestCaseCard(title=test_case_card_title, test_script_detail_id=test_script_detail_id)
        test_case_card.save()
  except:
    pass

  response = test_case_card_html(request)
  return response

def delete_test_case_card(request):
  test_case_card_id = request.POST.get('test_case_card_id')
  try:
    with transaction.atomic():
      TestCaseCard.objects.get(id=test_case_card_id).delete()
  except:
    pass

  return JsonResponse({})  

def delete_test_script_detail(request):
  test_script_detail_id = request.POST.get('test_script_detail_choose')
  try:
    with transaction.atomic():
      TestScriptDetail.objects.get(id=test_script_detail_id).delete()
  except:
    pass
    
  response = index_test_script_detail_select_html(request)
  return response

from io import StringIO

def export_test_case_card(request):
  test_case_card_ids = request.POST.getlist('test_case_card_id')
  html_str = export_test_case_card_html_str(test_case_card_ids)

  f = StringIO()
  f.write(html_str)
  f.seek(0)
  f_name = gen_file_name()

  response = HttpResponse(f.read(), content_type="application/force-download")
  response['Content-Disposition'] = 'inline; filename={}'.format(f_name)
  return response