mambas = {
    deleteSession: function(session_name) {
        swal({
            title: 'Are you sure?',
            html: "The Session <b>" + session_name + "</b> will be deleted permanently. You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-success',
            cancelButtonClass: 'btn',
            confirmButtonText: 'Yes, delete it!',
            buttonsStyling: false
        }).then(
            function() {
                swal({
                    title: 'Deleted!',
                    text: 'Your file has been deleted.',
                    type: 'success',
                    confirmButtonClass: "btn btn-success",
                    buttonsStyling: false
                })
            },
            function() {
            }
        ).catch(swal.noop)
    },

    createProject: function() {
        swal({
            title: 'Create a new project',
            html: '<div class="form-group">' +
                '<input id="input-field" type="text" class="form-control" placeholder="Enter a project name" />' +
                '</div>',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-success',
            cancelButtonClass: 'btn',
            confirmButtonText: 'Create',
            buttonsStyling: false
        }).then(function(result) {
            swal({
                type: 'success',
                html: 'You entered: <strong>' +
                    $('#input-field').val() +
                    '</strong>',
                confirmButtonClass: 'btn btn-success',
                buttonsStyling: false
            })
        }).catch(swal.noop)
    }
}