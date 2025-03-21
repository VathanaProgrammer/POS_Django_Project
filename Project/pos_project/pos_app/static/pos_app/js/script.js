$(document).ready(function(){
    let sidebar = $('#sidebar');
    const humburger = $('#humburger');
    humburger.click(function(e){
        e.preventDefault(); // <-- Important!

        console.log('Clicked!');
        sidebar.addClass('show');
    })
})