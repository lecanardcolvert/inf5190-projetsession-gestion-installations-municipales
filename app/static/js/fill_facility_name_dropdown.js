$(document).ready(function() {
  fill_name_dropdown_menu();

  // ===== FILL DROPDOWN MENU - SEARCH BY NAME =====
  function fill_name_dropdown_menu() {
    var name = $("#facility-name").val();
    var method = 'get';
    var url = '/api/v1/installations-noms';

    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          xhr.response.forEach(name => $("#facility-name")
                                           .append('<option value="' + name +
                                                   '">' + name + '</option>'));
        } else {
          console.log(xhr.response);
        }
      }
    };
    xhr.send();
  }
});
