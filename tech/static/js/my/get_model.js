//モデルを選んでいない時はボタンを使えなくする 
document.addEventListener('DOMContentLoaded', function(){
    var model = document.querySelector('#select_model');
    const submit = document.querySelector('#submit');
    model.onchange = function(){
        if (model.value == "none_model"){
            submit.disabled = true;
        }else{
            submit.disabled = false;
        }   
    };
});