document.getElementById("action").addEventListener("change", function(){

    var age_elem = document.getElementById("action");
    var s_value = age_elem.options[age_elem.selectedIndex].value;
    var box_elem = document.getElementById("ex_box");

    if(s_value == "delete"){
      box_elem.disabled = false;
    } else{
      box_elem.disabled = true;
    }

    if(s_value == "delall"){
      alert('全レコード削除を選択します');
    }


  }, false);
