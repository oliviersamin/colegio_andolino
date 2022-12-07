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

function hideShowPrice() {
    const price = document.getElementById('id_price')
    const value = price.options[price.selectedIndex].value
    const month = document.getElementById('id_price_per_month')
    const day = document.getElementById('id_price_per_day')

  if (value == 'daily_price') {
    month.style.display = 'none'
    month.previousElementSibling.style.display = 'none'
    day.style.display = 'block'
    day.previousElementSibling.style.display = 'block'
  }
  else if(value == 'monthly_price') {
    month.style.display = 'block'
    month.previousElementSibling.style.display = 'block'
    day.style.display = 'none'
    day.previousElementSibling.style.display = 'none'
  }

}

function hideShowDate() {
  const dateField = document.getElementById('id_date')
  const all_year = document.getElementById('id_is_all_year')
  const value = all_year.options[all_year.selectedIndex].value
  const days = document.getElementById('id_days_hour')

  if (value == 'true'){
    dateField.style.display = 'none'
    dateField.previousElementSibling.style.display = 'none'
    dateField.nextElementSibling.style.display = 'none'
    days.style.display = 'block'
    days.previousElementSibling.style.display = 'block'
    days.nextElementSibling.style.display = 'block'
  }
  else {
    dateField.style.display = 'block'
    dateField.previousElementSibling.style.display = 'block'
    dateField.nextElementSibling.style.display = 'block'
    days.style.display = 'none'
    days.previousElementSibling.style.display = 'none'
    days.nextElementSibling.style.display = 'none'
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

  else if (document.URL.includes('create-my-activity')) {
    hideShowDate()
    hideShowPrice()
    const dateField = document.getElementById('id_date')
    const daysField = document.getElementById('id_days_hour')
    const all_year = document.getElementById('id_is_all_year')
    const price = document.getElementById('id_price')
    all_year.addEventListener('click', hideShowDate)
    price.addEventListener('click', hideShowPrice)
  }
}
