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

    showChart: function(elem, mode="epoch") {
        elem.empty();
        var id = elem.attr("id");
        var data = JSON.parse(elem.data("data").replace(new RegExp("'", "g"), '"'));
        var key = elem.data("key");
        var parseTime = mode == "time";
        Morris.Area({
            element: id,
            data: data,
            xkey: mode,
            ykeys: [key],
            labels: [key],
            parseTime: parseTime,
            pointSize: 0,
            fillOpacity: 0,
            behaveLikeLine: true,
            gridLineColor: "#e0e0e0",
            lineWidth: 3,
            hideHover: "auto",
            lineColors: ["#00bcd4", "#9c27b0", "#f44336", "#ff9800", "#4caf50"],
            resize: true,
            hoverCallback: function (index, options, content, row) {
                return "Epoch " + content;
              }
        });
    }
};

$(function() {
    "use strict";

    // TODO: Move into mambas Object
    $(".clickable-row").click(function(event) {
        var elem = $(event.target);
        if(elem.parents("button").length < 1 && !elem.is("button") &&
           elem.parents("a").length < 1 && !elem.is("a")) {
            window.location = $(this).data("href");
        }
    });

    $(".btn-toggle").click(function(event) {
        var cb = $(this).find("input:checkbox");
        cb.trigger("click");
        var state = cb.is(":checked");
        var icons = $(this).find(".icons");
        if(state) {
            icons.addClass("checked");
        } else {
            icons.removeClass("checked");
        }
    });

    $(".chart-toggle").click(function(event) {
        var idElem = $(this).data("chart-id");
        var elem = $("#" + idElem);
        var checked = $(this).is(":checked");
        if(checked) {
            mambas.showChart(elem, "time");
        }
        else {
            mambas.showChart(elem);
        }
    });

    $(".chart").each(function() {
        mambas.showChart($(this));
    });

    $(".chart").hideShow().on("visibilityChanged", function(event, visibility) {
        if(visibility == "shown") {
            mambas.showChart($(this));
        }
    });  
});