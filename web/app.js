$(document).ready(function(){
    $('#countries-table').bootstrapTable({
        url: "data/countries.json",
        idField: "iso_code",
        detailView: true,
        classes: "table table-no-bordered",
        search: true,
        detailFormatter: function(index, row) {
            return '<div class="row"><div class="col-md-6"><img src="' + row['flag_big'] + '" /></div>'
                 + '<div class="col-md-6"><img src="' + row['map'] + '"/></div></div>'
        },
        columns: [
            {
                field: "position",
                title: "HDI",
                titleTooltip: "Position in Human Development Index",
                width: 16,
                sortable: true,
                cellStyle: "index",
                order: "asc"
            },
            {
                field: "flag_small",
                title: "Flag",
                formatter: function(value, row, index) {return '<img src="' + value + '"/>'},
                width: 32
            },
            {
                field: "name",
                title: "Name",
                formatter: function(value, row, index) {return '<a href="' + row['wiki'] + '">' + value + '</a>'}
            },
            {
                field: "iso_code",
                title: "ISO code"
            },
            {
                field: "languages",
                title: "Languages",
                formatter: function(value, row, index) {return value.join(", ")},
            }
        ]
    });
});
