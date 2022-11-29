// get the children variable from django context varaible
const data = document.currentScript.dataset;
const children = data.children;

function hideShowUsers() {
  console.log('inside hideShowUsers')
  const users = document.getElementById("id_users")
  if (parseInt(children) == 1) {
    console.log('only one child')
    for(let item of users) {
      if(item.value == 'children') {
        users.removeChild(item)
      }
      else if(item.value == 'each_child') {
        users.removeChild(item)
      }
    }
  }
  else if (parseInt(children) > 1) {
    for(let item of users) {
      if(item.value == 'child') {
        users.removeChild(item)
      }
    }
  }
  else{
        console.log('no child')
  }
}

function hideShowYearAndMonth() {
  const wholeYear = document.getElementById("id_whole_actual_school_year")
  const year = document.getElementById("id_year")
  const month = document.getElementById("id_month")
  if (wholeYear.checked) {
    year.style.display = 'none'
    year.previousElementSibling.style.display = 'none'
    month.style.display = 'none'
    month.previousElementSibling.style.display = 'none'

  }
  else {
    year.style.display = 'block'
    year.previousElementSibling.style.display = 'block'
    month.style.display = 'block'
    month.previousElementSibling.style.display = 'block'

  }
}

// to be executed when the whole page is loaded
window.onload = function initialize_form(){
  hideShowUsers()
  const wholeYear = document.getElementById("id_whole_actual_school_year");
  wholeYear.addEventListener("click", hideShowYearAndMonth);
}
