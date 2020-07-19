function get_timestamp(){
  let current_date = new Date();
  let date = current_date.getDate();
  let month = current_date.getMonth()+1;
  let year = current_date.getFullYear();
  let hours = current_date.getHours();
  let minutes = current_date.getMinutes();
  let sec = current_date.getSeconds();
  let mili = current_date.getUTCMilliseconds();

  if(date < 10){
    date = "0" + date.toString();
  }

  if(month < 10){
    month = "0" + month.toString();
  }

  if(hours < 10){
    hours = "0" + hours.toString();
  }

  if(minutes < 10){
    minutes = "0" + minutes.toString();
  }

  if(sec < 10){
    sec = "0" + sec.toString();
  }

  let time_stamp = year + "-" + month + "-" + date + " " + hours + ":" + minutes + ":" + sec + "." + mili;
  return time_stamp;
}

function append_test_case_card_detail_to_element(access_to, uuid){
  row = '<div class="container">';
  
  row += '<div class="row">';
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid);
  row += '<h7><b>Module</b></h7>';
  row += '<select id="module_choose{0}" name="module_choose" class="form-control wrapper" style="width: 100%;"></select>'.f(uuid);
  row += '<script>$("#module_choose{0}").html($("#module_detail_options").html());</script>'.f(uuid);
  row += '<script>make_select_searchable("#module_choose{0}");</script>'.f(uuid);
  row += '<input placeholder="type something.." class="form-control wrapper" class="form-control wrapper" id="new_module_choose{0}" name="new_module_choose" value="" type="text" hidden/>'.f(uuid);
  row += '<script>$("#module_choose{0}").on("change.select2 change", function(e){ if($("#module_choose{0}").val() == "-1"){ $("#new_module_choose{0}").prop("hidden", false); } else{$("#new_module_choose{0}").prop("hidden", true); $("#new_module_choose{0}").val("");}});</script>'.f(uuid);
  row += '<script>\
  if($("#module_choose{0}").val() == "-1"){ \
    $("#new_module_choose{0}").prop("hidden", false); \
  } \
  else{ \
    $("#new_module_choose{0}").prop("hidden", true); \
    $("#new_module_choose{0}").val(""); \
  } \
</script>'.f(uuid);
  row += '</div>';
  row += '</div>';

  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid);
  row += '<h7><b>Test Case Code</b></h7>'
  row += '<input placeholder="type something.." class="form-control wrapper" id="test_case_code{0}" name="test_case_code" style="width: 100%;" value="" type="text"/>'.f(uuid);
  row += '</div>';
  row += '</div>';
  row += '</div>';

  row += '<div class="row">';
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid);
  row += '<h7><b>Test Description</b></h7>'
  row += '<textarea placeholder="type something.." class="form-control wrapper" id="test_case_desc{0}" name="test_case_desc" style="width: 100%;" value="" type="text" oninput="show_all_textarea(this);"></textarea>'.f(uuid);
  row += '<script>show_all_textarea("#test_case_desc{0}");</script>'.f(uuid);
  row += '</div>';
  row += '</div>';
  row += '</div>';

  row += '<div class="row">';
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid);
  row += '<h7><b>Expected Result</b></h7>';
  row += '<textarea placeholder="type something.." class="form-control wrapper" id="test_case_output{0}" name="test_case_output" style="width: 100%;" value="" type="text" oninput="show_all_textarea(this);"></textarea>'.f(uuid);
  row += '<script>show_all_textarea("#test_case_output{0}");</script>'.f(uuid);
  row += '</div>';
  row += '</div>';
  row += '</div>';

  row += '<div class="row">';
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid);
  row += '<h7><b>Test Steps</b></h7>';
  row += '<textarea placeholder="type something.." class="form-control wrapper" id="test_case_step{0}" name="test_case_step" style="width: 100%;" value="" type="text" oninput="show_all_textarea(this);"></textarea>'.f(uuid);
  row += '</div>';
  row += '</div>';
  row += '</div>';

  row += '<div class="row">';
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid);
  row += '<h7><b>Remark</b></h7>';
  row += '<textarea placeholder="type something.." class="form-control wrapper" id="test_case_remark{0}" name="test_case_remark" style="width: 100%;" value="" type="text" oninput="show_all_textarea(this);"></textarea>'.f(uuid);
  row += '</div>';
  row += '</div>';
  row += '</div>';

  row += '<div class="row">'
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid);
  row += '<h7><b>Test Status</b></h7>';
  row += '<select id="status_detail_choose{0}" name="status_detail_choose" class="form-control wrapper" style="width: 100%;"></select>'.f(uuid);
  row += '<script>$("#status_detail_choose{0}").html($("#status_detail_options").html());</script>'.f(uuid);
  row += '</div>';
  row += '</div>';

  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid); 
  row += '<h7><b>Last Updated</b></h7>';
  row += '<input class="form-control wrapper" id="last_update_time{0}" name="last_update_time" class="form-control wrapper" style="width: 100%; display: inline-block;" readonly/>'.f(uuid);
  row += '<script>$(".{0}").on("change", function(e){ $("#last_update_time{0}").val(get_timestamp); });</script>'.f(uuid);
  row += '<script>set_value("#last_update_time{0}", get_timestamp);</script>'.f(uuid);
  row += '</div>';
  row += '</div>';
  
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid); 
  row += '<h7><b>Tester</b></h7>';
  row += '<input class="form-control wrapper" id="tester{0}" class="form-control wrapper" style="width: 100%;" readonly/>'.f(uuid);
  row += '<h7><b>Device/OS</b></h7>';
  row += '<input class="form-control wrapper" id="os_and_device_detail{0}" class="form-control wrapper" style="width: 100%;" readonly/>'.f(uuid);
  row += '</div>';
  row += '</div>';
  row += '</div>';

  row += '<div class="row">';
  row += '<div class="col">';
  row += '<div class="{0}">'.f(uuid); 
  row += '<h7><b>Attachments</b></h7>';
  row += '<i class="fas fa-plus-circle" style="margin-left: 7px; cursor: pointer; color: green;" onclick="add_file_input({0}, {1});"></i>'.f("'#attach_file_container{0}'".f(uuid), "'attach_file{0}'".f(uuid));
  row += '<div id="attach_file_container{0}">'.f(uuid);
  row += '</div>';
  row += '</div>';
  row += '</div>';
  row += '</div>';

  row += '<div class="row">';
  row += '<div class="col" style="text-align: center; margin-top:10px;">';
  row += '<input id="test_case_card_detail_id{0}" name="test_case_card_detail_id" type="text" value="{0}" hidden>'.f(uuid);
  row += '<button id="delete_item_btn{0}" onclick="copy_input_delete_id_to_div(\{1}\, \{2}\); $(this).parent().parent().parent().remove();" hidden></button>'.f(uuid, "'{0}_delete_ids'".f(access_to), "'#test_case_card_detail_id{0}'".f(uuid));
  row += '<button type="button" class="btn btn-danger btn-sm" style="width: 60%;" onclick="delete_confirm_plug_element_onclick({0})"><b>Remove</b></button>'.f("'#delete_item_btn{0}'".f(uuid));
  row += '<hr>';
  row += '</div>';
  row += '</div>';

  row += '</div>';
  $(access_to).append(row);
}

function copy_input_delete_id_to_div(element, input_delete_id){
  let text = "<input type='text' name='delete_ids' value='{0}' hidden>".f($(input_delete_id).val());
  $(element).append(text);
}

function copy_input_delete_img_id_to_div(element, value){
  let text = "<input type='text' name='delete_img_ids' value='{0}' hidden>".f(value);
  $(element).append(text);
}

function copy_option_inner_html_by_value_to_element(element_datalist, value_search, to_element){
  let text = $(element_datalist + ' option[value="' + value_search + '"]').html();
  $(to_element).val(text);
}

// trigger other element that hidden to run function
function delete_confirm_plug_element_onclick(access_to){
  $("#delete_confirm_modal").modal('show');
  $('#delete_confirm_btn').click(function(){ $(access_to).click(); });
}

function set_value(element_id, value){
  $(element_id).val(value);
}

function set_select2_val(element_id, value){
  $(element_id).val(value).trigger('change.select2');
}

function show_all_textarea(element){
  var scroll_height = $(element).get(0).scrollHeight;
	$(element).css('height', scroll_height + 'px');
}

function read_url_preview_img(input, preview_id) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $(preview_id).attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
  }
  else{
    $(preview_id).attr('src', '');
  }
}

function add_file_input(div_id, name){
  text = '<div style="margin-top: 10px;">';
  text += '<img src="" style="height: 128px; width: 128px;"/>';
  text += '<input type="file" name="{0}" onchange="check_file_size(this, $(this).parent().find({2})); read_url_preview_img(this, $(this).parent().find({1}))" accept="image/*">'.f(name, "'img'", "'span'");
  text += '<span style="color: red;"></span>';
  text += '<i class="fas fa-minus-circle" style="color: red; cursor: pointer;" onclick="delete_confirm_plug_element_onclick($(this).parent().find({0}));"></i>'.f("'button'");
  text += '<button type="button" onclick="$(this).parent().remove();" hidden></button>';
  text += '</div>';

  $(div_id).append(text);
}

function read_url_preview_img(input_element, preview_element) {
  if (input_element.files && input_element.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $(preview_element).attr('src', e.target.result);
    }
    reader.readAsDataURL(input_element.files[0]);
  }
  else{
    $(preview_element).attr('src', '');
  }
}

function check_file_size(element, p_status_show_element){
  const kb = 512;
  if(element.files[0].size >= (kb * 1024)){
    $(element).val('');
    $(p_status_show_element).text("Size must not over {0} KB. ".f(kb));
  }
  else{
    $(p_status_show_element).text("");
  }
}