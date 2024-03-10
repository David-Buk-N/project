var addButtonElements = document.querySelectorAll("#addButton");
addButtonElements.forEach(function(element) {
    element.addEventListener("click", function() {
        //redirect to the "add" page
        window.location.href = "add-content.html";
    });
});