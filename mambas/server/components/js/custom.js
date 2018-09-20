mambas = {
    showDelete: function() {
        swal({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-success',
            cancelButtonClass: 'btn btn-danger',
            confirmButtonText: 'Yes, delete it!',
            buttonsStyling: false
        }).then(function() {
            swal({
                title: 'Deleted!',
                text: 'Your file has been deleted.',
                type: 'success',
                confirmButtonClass: "btn btn-success",
                buttonsStyling: false
            })
        }).catch(swal.noop)
    }
}