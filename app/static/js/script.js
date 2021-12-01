$(document).ready(function() {
    $("#search-installations-form").submit(function(event) {
        var form = $(this);
        var url = form.attr("action");

        event.preventDefault();
        $("#search-installations-submit").prop('disabled', true);
        validate_form(url, 'get', form.serialize());
        $("#search-installations-submit").prop('disabled', false);
    });
});

async function validate_form(url, type, data) {
    let result;

    try {
        result = await $.ajax({
            url: url,
            type: type,
            data: data,
            dataType: "json",
            success: function(response) {

                // Fill slides table
                if ($.fn.dataTable.isDataTable('#slides-table')) {
                    $('#slides-table').dataTable().fnClearTable();
                    if (response.glissades.length > 0) {
                        console.log(response.glissades);
                        $('#slides-table').dataTable().fnAddData(response.glissades);
                    }
                } else {
                    $('#slides-table').DataTable({
                        language: {
                            url: "//cdn.datatables.net/plug-ins/1.11.3/i18n/fr_fr.json"
                        },
                        data: response.glissades,
                        columns: [
                            { data: 'id' },
                            { data: 'nom' },
                            { data: 'arrondissement.nom' },
                            { data: 'ouvert' },
                            { data: 'deblaye' },
                            { data: 'condition' }
                        ]
                    });
                }

                // Fill aquatic installations table
                if ($.fn.dataTable.isDataTable('#aquatic_installations-table')) {
                    $('#aquatic_installations-table').dataTable().fnClearTable();
                    if (response.installations_aquatiques.length > 0) {
                        $('#aquatic_installations-table').dataTable().fnAddData(response.installations_aquatiques);
                    }
                } else {
                    $('#aquatic_installations-table').DataTable({
                        language: {
                            url: "//cdn.datatables.net/plug-ins/1.11.3/i18n/fr_fr.json"
                        },
                        data: response.installations_aquatiques,
                        columns: [
                            { data: 'id' },
                            { data: 'nom' },
                            { data: 'arrondissement.nom' },
                            { data: 'type' },
                            { data: 'adresse' },
                            { data: 'propriete' },
                            { data: 'gestion' },
                            { data: 'equipement' }
                        ]
                    });
                }

                // Fill ice rinks table
                if ($.fn.dataTable.isDataTable('#ice_rinks-table')) {
                    $('#ice_rinks-table').dataTable().fnClearTable();
                    if (response.patinoires.length > 0) {
                        $('#ice_rinks-table').dataTable().fnAddData(response.patinoires);
                    }
                } else {
                    $('#ice_rinks-table').DataTable({
                        language: {
                            url: "//cdn.datatables.net/plug-ins/1.11.3/i18n/fr_fr.json"
                        },
                        data: response.patinoires,
                        columns: [
                            { data: 'id' },
                            { data: 'nom' },
                            { data: 'arrondissement.nom' },
                            { data: 'date_heure' },
                            { data: 'ouvert' },
                            { data: 'deblaye' },
                            { data: 'arrose' },
                            { data: 'resurface' }
                        ]
                    });
                }

            },
            error: function(xhr, status, error){
                var errorMessage = xhr.status + ': ' + xhr.statusText
                alert('Erreur : ' + errorMessage);
            }
        });
        return result;
    } catch (error) {
        console.error(error);
    }
}