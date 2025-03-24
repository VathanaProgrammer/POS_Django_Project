$(document).ready(function () {
    const sidebar = $('#sidebar');
    const humburger = $('#humburger');

    // Click hamburger to open sidebar
    humburger.on('click', function (e) {
        e.preventDefault();
        e.stopPropagation(); // Stop bubbling to document click
        sidebar.addClass('show');
    });

    // Prevent clicks inside sidebar from closing it
    sidebar.on('click', function (e) {
        e.stopPropagation();
    });

    // Click outside sidebar closes it
    $(document).on('click', function () {
        if (sidebar.hasClass('show')) {
            sidebar.removeClass('show');
        }
    });
    function showAlert(title, icon, text, showCancel = false, confirmText = "OK", cancelText = "Cancel") {
        return Swal.fire({
            title: title,
            icon: icon,
            text: text,
            showCancelButton: showCancel,
            confirmButtonText: confirmText,
            cancelButtonText: cancelText
        });
    }
    $('#dropdownBtn').click(function (e) {
        e.stopPropagation(); // prevent bubbling to document
        $('#dropdownMenu').toggleClass('show');
        $('#dropdownIcon').toggleClass('rotate');
    });

    // Close dropdown if clicked outside
    $(document).click(function (e) {
        if (!$(e.target).closest('.custom-dropdown').length) {
            $('#dropdownMenu').removeClass('show');
            $('#dropdownIcon').removeClass('rotate');
        }
    });
    $('#new_pro_or_cate').click(function (e) {
        e.stopPropagation(); // prevent bubbling to document
        $('#dropdownmenu_new').toggleClass('show');
        $('#dropdownIcon_new').toggleClass('rotate');
    });

        // Close dropdown if clicked outside
        $(document).click(function (e) {
            if (!$(e.target).closest('.custom-dropdown').length) {
                $('#dropdownmenu_new').removeClass('show');
                $('#dropdownIcon_new').removeClass('rotate');
            }
        });

        $('#dropdownBtn_in_add_proForm').click(function (e) {
            e.stopPropagation(); // prevent bubbling to document
            $('#dropdownMenu_in_add_proForm').toggleClass('show');
            $('#dropdownIcon_in_add_proForm').toggleClass('rotate');
        });

                // Close dropdown if clicked outside
                $(document).click(function (e) {
                    if (!$(e.target).closest('.custom-dropdown').length) {
                        $('#dropdownMenu_in_add_proForm').removeClass('show');
                        $('#dropdownIcon_in_add_proForm').removeClass('rotate');
                    }
                });

                $('#new_pro_click').click(function() {
                    $('#add_product').toggleClass('show_add_pro_form');
                });
                
                $('#add_cancel').on('click', function() {
                    $('#add_product').removeClass('show_add_pro_form');
                    if(isProduct_update){
                        isProduct_update = false;
                    }
                    console.log('after click cancel product: '+ isProduct_update)
                });
                
                $("#new_cate_click").on('click', function() {
                    $('#add_category').toggleClass('show_add_pro_form');
                });
                
                $('#add_cate_cancel').on('click', function() {
                    $('#add_category').removeClass('show_add_pro_form');
                });
                
                // Prevent form submission when clicking on the dropdown button
$('#dropdownBtn_in_add_proForm').click(function(event) {
    event.preventDefault();  // Prevent form submission
    $('#dropdownMenu_in_add_proForm').toggle();  // Toggle the dropdown menu visibility
});

$("#categoriess").on('click', function() {
    $('#category').toggleClass('show_add_pro_form');
});
   
});