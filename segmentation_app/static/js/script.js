$(document).ready(function() {
    // Show filename when file is selected
    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
        
        // Show image preview
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $("#image-preview").attr("src", e.target.result);
                $(".preview-container").removeClass("d-none");
            }
            reader.readAsDataURL(file);
        }
    });
    
    // Show spinner when form is submitted
    $("#upload-form").on("submit", function() {
        $("#spinner").removeClass("d-none");
        $(this).find("button[type='submit']").prop("disabled", true);
    });
});