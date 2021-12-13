$(document).ready(function() {
  // ===== SUBSCRIBE FORM =====
  $("#subscribe-form").submit(function(event) {
    var form = $(this);
    var url = form.attr("action");
    var method = form.attr("method");

    event.preventDefault();
    $("#subscribe-submit").prop('disabled', true);

    var form_json = form.serializeJSON();
    var form_json_string = JSON.stringify(form_json);

    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 201) {
          window.location.href = 'subscribe-success';
        } else {
          console.log(xhr.response.error);
          $("#subscribe-error").text(xhr.response.error);
          $("#subscribe-error").show();
        }
      }
    };
    xhr.send(form_json_string);

    $("#subscribe-submit").prop('disabled', false);
  });

  // ===== CHANGE SEARCH MODE =====
  $('#select-mode-borough').change(function() {
    $("#search-name-div").hide();
    $("#search-borough-div").show();
  });
  $('#select-mode-name').change(function() {
    $("#search-borough-div").hide();
    $("#search-name-div").show();
  });

  // ===== FACILITY SEARCH FORM - SEARCH BY NAME =====
  $("#search-name-form").submit(function(event) {
    var form = $(this);
    var method = form.attr("method");
    var name = $("#facility-name").val();
    var url = form.attr("action") + '?nom=' + name;

    event.preventDefault();
    $("#submit-search-name").prop('disabled', true);

    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          $("#search-error").hide();
          fill_search_results(xhr.response);
          $("#submit-search-name").prop('disabled', false);
        } else {
          console.log(xhr.response);
          $("#search-error")
              .text("Une erreur est survenue. Veuillez réessayer.");
          $("#search-error").show();
        }
      }
    };
    xhr.send();
  });

  // ===== FACILITY SEARCH FORM - SEARCH BY BOROUGH =====
  $("#search-borough-form").submit(function(event) {
    var form = $(this);
    var method = form.attr("method");
    var borough = $("#borough-name").val();
    var url = form.attr("action") + '?arrondissement=' + borough;

    event.preventDefault();
    $("#submit-search-borough").prop('disabled', true);

    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          $("#search-error").hide();
          fill_search_results(xhr.response);
          $("#submit-search-borough").prop('disabled', false);
        } else {
          console.log(xhr.response);
          $("#search-error")
              .text("Une erreur est survenue. Veuillez réessayer.");
          $("#search-error").show();
        }
      }
    };
    xhr.send();
  });

  // ===== FACILITY SEARCH FORM - FILL RESULTS =====
  function fill_search_results(json_response) {
    if ($.fn.dataTable.isDataTable('#slides-table')) {
      $('#slides-table').dataTable().fnClearTable();
      if (json_response.glissades.length > 0) {
        $('#slides-table').dataTable().fnAddData(json_response.glissades);
      }
    } else {
      var table = $('#slides-table').DataTable({
        language :
            {url : "//cdn.datatables.net/plug-ins/1.11.3/i18n/fr_fr.json"},
        data : json_response.glissades,
        columns : [
          {data : 'id'},
          {data : 'nom'},
          {data : 'arrondissement.nom'},
          {data : 'ouvert'},
          {data : 'deblaye'},
          {data : 'condition'},
          {
            data : null,
            sortable : false,
            render : function(data, type, full) {
              return '<button onclick=edit() class="btn btn-info btn-sm"' +
                     full[0] + '>' +
                     'Edit' +
                     '</button>';
            }
          },
          {
            data : null,
            sortable : false,
            render : function(data, type, full) {
              return '<button onclick=deleteData("glissades",' + data["id"] +
                     ') class="btn btn-danger btn-sm"' +
                     '>' +
                     'Supprimer' +
                     '</button>';
            }
          },
        ]
      });
    }

    // Fill aquatic installations table
    if ($.fn.dataTable.isDataTable('#aquatic_installations-table')) {
      $('#aquatic_installations-table').dataTable().fnClearTable();
      if (json_response.installations_aquatiques.length > 0) {
        $('#aquatic_installations-table')
            .dataTable()
            .fnAddData(json_response.installations_aquatiques);
      }
    } else {
      $('#aquatic_installations-table').DataTable({
        language :
            {url : "//cdn.datatables.net/plug-ins/1.11.3/i18n/fr_fr.json"},
        data : json_response.installations_aquatiques,
        columns : [
          {data : 'id'},
          {data : 'nom'},
          {data : 'arrondissement.nom'},
          {data : 'type'},
          {data : 'adresse'},
          {data : 'propriete'},
          {data : 'gestion'},
          {data : 'equipement'},
          {
            data : null,
            sortable : false,
            render : function(data, type, full) {
              return '<button onclick=edit() class="btn btn-info btn-sm"' +
                     full[0] + '>' +
                     'Edit' +
                     '</button>';
            }
          },
          {
            data : null,
            sortable : false,
            render : function(data, type, full) {
              return '<button onclick=deleteData("aquatics",' + data["id"] +
                     ') class="btn btn-danger btn-sm"' +
                     '>' +
                     'Supprimer' +
                     '</button>';
            }
          },

        ]
      });
    }

    // Fill ice rinks table
    if ($.fn.dataTable.isDataTable('#ice_rinks-table')) {
      $('#ice_rinks-table').dataTable().fnClearTable();
      if (json_response.patinoires.length > 0) {
        $('#ice_rinks-table').dataTable().fnAddData(json_response.patinoires);
      }
    } else {
      $('#ice_rinks-table').DataTable({
        language :
            {url : "//cdn.datatables.net/plug-ins/1.11.3/i18n/fr_fr.json"},
        data : json_response.patinoires,
        columns : [
          {data : 'id'},
          {data : 'nom'},
          {data : 'arrondissement.nom'},
          {data : 'date_heure'},
          {data : 'ouvert'},
          {data : 'deblaye'},
          {data : 'arrose'},
          {data : 'resurface'},
          {
            data : null,
            sortable : false,
            render : function(data, type, full) {
              return '<button onclick=edit() class="btn btn-info btn-sm"' +
                     full[0] + '>' +
                     'Edit' +
                     '</button>';
            }
          },
          {
            data : null,
            sortable : false,
            render : function(data, type, full) {
              return '<button onclick=deleteData("ice-rinks",' + data["id"] +
                     ') class="btn btn-danger btn-sm"' +
                     '>' +
                     'Supprimer' +
                     '</button>';
            }
          },

        ]
      });
    }
  }
});

function edit() { alert("Bonjour"); }
function deleteData(type, id) {
  var jqxhr = $.ajax({
    type : 'DELETE',
    url : "/api/v1/installations/" + type + "/" + id,
  });
  jqxhr.done(function(data) { alert("La suppression a réussi"); });
  jqxhr.fail(function(jqXHR) { alert("La suppression a échouée"); });
}
