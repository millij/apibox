(function(){
    var fileInput = document.querySelector(".file-input"),
        uploadBtn = document.querySelector(".upload"),
        actualFileInp = document.querySelector(".actual"),
        uploadForm = document.querySelector("#uploadForm");

    fileInput.addEventListener("click", function(){
        actualFileInp.click();
    });
     uploadBtn.addEventListener("click", function(){
        if(fileInput.value){
             uploadForm.submit();
        }
    });

     actualFileInp.addEventListener("change", function(){
        var filePath = actualFileInp.value;
        fileInput.value = filePath.match(/[^\/\\]+$/);
    });
})();