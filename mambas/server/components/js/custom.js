mambas = {
    createProject: function() {
        swal({
            title: "Create a new Project",
            html: "<div class='form-group'>" +
                "<input id='input-create-project' type='text' class='form-control' placeholder='Enter a project name' />" +
                "</div>",
            showCancelButton: true,
            confirmButtonClass: "btn btn-primary",
            cancelButtonClass: "btn",
            confirmButtonText: "Create",
            buttonsStyling: false
        }).then((result) => {
            if (result.value) {
                var projectName = $("#input-create-project").val()
                var json = JSON.stringify({"name": projectName});
                $.post("/projects", json).done((data) => {
                    swal({
                        title: "Created",
                        html: "The Project <b>" + projectName + "</b> was created.",
                        type: "success",
                        confirmButtonClass: "btn",
                        buttonsStyling: false
                    }).then(() => {
                        var url = "/projects/" + data.id.toString() + "/dashboard";
                        window.location.href = url;
                    });
                }).fail(() => {
                    swal({
                        title: "Error",
                        html: "The Project <b>" + projectName + "</b> could not be created.",
                        type: "error",
                        confirmButtonClass: "btn",
                        buttonsStyling: false
                    });
                });
            }
        });
    },

    displayToken: function(token) {
        swal({
            title: "Token",
            html: "<div class='form-group'>" +
                "<input type='text' class='form-control text-center' value='" + token + "' readonly /><br>" +
                "<p class='text-muted'>Need help? </p>" +
                "</div>",
            type: "info",
            confirmButtonClass: "btn",
            buttonsStyling: false
        });
    },

    deleteSession: function(sessionName, idProject, idSession) {
        swal({
            title: "Are you sure?",
            html: "The Session <b>" + sessionName + "</b> will be deleted permanently. You won't be able to revert this!",
            type: "warning",
            showCancelButton: true,
            confirmButtonClass: "btn btn-warning",
            cancelButtonClass: "btn",
            confirmButtonText: "Delete",
            buttonsStyling: false
        }).then((result) => {
            if(result.value) {
                var url = "/projects/" + idProject + "/sessions/" + idSession;
                $.ajax({
                    url: url,
                    type: "DELETE"
                }).done(() => {
                    swal({
                        title: "Deleted",
                        html: "The session <b>" + sessionName + "</b> was deleted.",
                        type: "success",
                        confirmButtonClass: "btn",
                        buttonsStyling: false
                    }).then(() => {
                        window.location.href = "/";
                    });
                }).fail(() => {
                    swal({
                        title: "Error",
                        html: "The session <b>" + sessionName + "</b> could not be deleted.",
                        type: "error",
                        confirmButtonClass: "btn",
                        buttonsStyling: false
                    });
                });
            }
        });
    },

    deleteProject: function(projectName, idProject) {
        swal({
            title: "Are you sure?",
            html: "The Project <b>" + projectName + "</b> will be deleted permanently. You won't be able to revert this!",
            type: "warning",
            showCancelButton: true,
            confirmButtonClass: "btn btn-warning",
            cancelButtonClass: "btn",
            confirmButtonText: "Delete",
            buttonsStyling: false
        }).then((result) => {
            if(result.value) {
                var url = "/projects/" + idProject;
                $.ajax({
                    url: url,
                    type: "DELETE"
                }).done(() => {
                    swal({
                        title: "Deleted",
                        html: "The Project <b>" + projectName + "</b> was deleted.",
                        type: "success",
                        confirmButtonClass: "btn",
                        buttonsStyling: false
                    }).then(() => {
                        window.location.href = "/";
                    });
                }).fail(() => {
                    swal({
                        title: "Error",
                        html: "The Project <b>" + projectName + "</b> could not be deleted.",
                        type: "error",
                        confirmButtonClass: "btn",
                        buttonsStyling: false
                    });
                });
            }
        });
    },

    setChart: function(idElement, data, key) {
        if(!idElement in graphs) {
            var graph = Morris.Area({
                element: idElement,
                xkey: "epoch",
                ykeys: [key],
                parseTime: false,
                pointSize: 3,
                fillOpacity: 0,
                pointStrokeColors: ["#4680ff"],
                behaveLikeLine: true,
                gridLineColor: "#e0e0e0",
                lineWidth: 3,
                hideHover: "auto",
                lineColors: ["#4680ff"],
                resize: true
            });

            graphs[idElement] = graph;
        }

        graphs[idElement].setData(data);
    }
};

$(function() {
    "use strict";

    var graphs = {};

    $(".clickable-row").click(function(event) {
        var elem = $(event.target);
        if(elem.parents("button").length < 1 && !elem.is("button") &&
           elem.parents("a").length < 1 && !elem.is("a")) {
            window.location = $(this).data("href");
        }
    });
});