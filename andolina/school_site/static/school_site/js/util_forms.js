// get the children variable from django context varaible
const data = document.currentScript.dataset;
const children = data.children;

function hideShowUsers() {
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

function hideShowParentList() {
  const parents_checkbox = document.getElementById("id_is_partner_already_created")
  const firstName = document.getElementById('id_first_name')
  const lastName = document.getElementById('id_last_name')
  const parentsList = document.getElementById('id_user')
  if (parents_checkbox.checked) {
      firstName.style.display = 'none'
      firstName.previousElementSibling.style.display = 'none'
      lastName.style.display = 'none'
      lastName.previousElementSibling.style.display = 'none'
      parentsList.style.display = 'block'
      parentsList.previousElementSibling.style.display = 'block'
    }
    else {
      firstName.style.display = 'block'
      firstName.previousElementSibling.style.display = 'block'
      lastName.style.display = 'block'
      lastName.previousElementSibling.style.display = 'block'
      parentsList.style.display = 'none'
      parentsList.previousElementSibling.style.display = 'none'

  }


}

// to be executed when the whole page is loaded
window.onload = function initialize_form(){
  if (document.URL.includes('my-bills')) {
    hideShowUsers()
    const wholeYear = document.getElementById("id_whole_actual_school_year");
    wholeYear.addEventListener("click", hideShowYearAndMonth);
  }
  else if (document.URL.includes('add-partner')){
    hideShowParentList()
    const parents_checkbox = document.getElementById("id_is_partner_already_created");
    parents_checkbox.addEventListener("click", hideShowParentList);
  }
}
