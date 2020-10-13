//calculation pageで計算ボタンを押した時に計算中ですと表示する 
document.addEventListener('DOMContentLoaded', function(){
const check_condition = document.querySelector('#check_condition');
const calculation_now = document.querySelector('#calculation_now');

calculation_now.style.display = "none";
document.querySelector('form').onsubmit = () =>{
    calculation_now.style.display = "block";
    check_condition.style.display = "none";
};
});

