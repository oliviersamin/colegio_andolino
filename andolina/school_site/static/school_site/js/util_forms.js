
console.log('inside javascript file...');
// var test = JSON.parse("{{ children|escapejs }}");
// var test = '{{ context }}'
const data = document.currentScript.dataset;
const children = data.children;
console.log('TEST = ', children)


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

window.onload = function initialize_form(){
  const wholeYear = document.getElementById("id_whole_actual_school_year");
  wholeYear.addEventListener("click", hideShowYearAndMonth);
}
