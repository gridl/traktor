$(document).ready(function(){
    $('#countries-table').bootstrapTable({
        url: "data/countries.json",
        idField: "iso_code",
        detailView: true,
        showColumns: true,
        undefinedText: 'n/a',
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
            },
            {
                field: "surface_area",
                title: "Area",
                sortable: true,
                visible: false
            },
            {
                field: "forest_area",
                title: "Forest area",
                sortable: true,
                visible: false
            },
            {
                field: "life_expectancy_male",
                title: "Life expectancy (male)",
                sortable: true,
                visible: false
            },
            {
                field: "life_expectancy_female",
                title: "Life expectancy (female)",
                sortable: true,
                visible: false
            },
            {
                field: "population",
                title: "Population",
                sortable: true,
                visible: false
            },
            {
                field: "density",
                title: "Population density",
                sortable: true,
                visible: false
            },
            {
                field: "urban_population",
                title: "Urban population",
                sortable: true,
                visible: false
            },
            {
                field: "population_growth",
                title: "Population growth",
                sortable: true,
                visible: false
            },
            {
                field: "infant_deaths",
                title: "Infant deaths",
                sortable: true,
                visible: false
            },
            {
                field: "inet_users",
                title: "Internet users",
                sortable: true,
                visible: false
            },
            {
                field: "roads_total_network",
                title: "Roads network",
                sortable: true,
                visible: false
            },
            {
                field: "vehicles_per_km_of_road",
                title: "Vehicles per km of road",
                sortable: true,
                visible: false
            },
            {
                field: "control_of_corruption",
                title: "Control of corruption",
                sortable: true,
                visible: false
            },
            {
                field: "military_expenditure",
                title: "Military expenditure",
                sortable: true,
                visible: false
            },
            {
                field: "pc_per_100",
                title: "PCs",
                sortable: true,
                visible: false
            }
        ]
    });
});
