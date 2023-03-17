/*Loading indicator on button*/
function showLoadingText() {
    document.getElementById("login-submit").value = "Loading ...";
}

function showOriginalText(originalButtonText){
    document.getElementById("login-submit").value = originalButtonText;
}

/* Set edit opening hours modal content dynamically based on the users' choice */
function openHoursModal(id, day_abbr, day, location_value){

    $('#'+id).before('<div id="'+id+'-placeholder"></div>').detach().appendTo('body').removeClass('hide');

    document.getElementById("day_abb").value = day_abbr;
    document.getElementById("day_string").innerHTML = day;

    document.getElementById("fe_open").value = location_value['Hours'][day_abbr]['Open'];
    document.getElementById("fe_close").value = location_value['Hours'][day_abbr]['Close'];
    document.getElementById("rx_open").value = location_value['RXHours'][day_abbr]['Open'];
    document.getElementById("rx_close").value = location_value['RXHours'][day_abbr]['Close'];
}

/*Remove feedback box and message on click on any element on the page*/
window.addEventListener("click", function(event) {
    alert_box = document.getElementById("alert-box");
    if(alert_box){
        alert_box.remove();
    }
    sessionStorage.removeItem('_flashes');
});

/* Menu */
function sortMenuAlphabetical(ul) {
    var ul = document.getElementById(ul);

    Array.from(ul.getElementsByTagName("LI"))
        .sort((a, b) => a.textContent.localeCompare(b.textContent))
        .forEach(li => ul.appendChild(li));
    }


function filterMenuList() {
    var input, filter, ul, li, i, txtValue;

    input = document.getElementById("filter_keyword_input");
    filter = input.value.toUpperCase();
    ul = document.getElementById("rootSidebar");
    li = ul.getElementsByTagName("li");

    for (i = 0; i < li.length; i++) {
        store_element = li[i].getElementsByTagName("a")[0].getElementsByClassName("store_location")[0];
        txtValue = store_element.textContent || store_element.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function highlightSelectedMenuListElement(selected_id){
    var ul, li, i, txtValue;

    ul = document.getElementById("rootSidebar");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {

        store_element = li[i].getElementsByTagName("a")[0].getElementsByClassName("store_location")[0];
        txtValue = store_element.textContent || store_element.innerText;

        if (txtValue.toUpperCase().indexOf(selected_id) > -1){    
            li[i].classList.add("sidebar__item--selected");

        } else {
            li[i].classList.remove("sidebar__item--selected");
        }
    }
}

//Toogle for store details
function show_details() {
    var more_info_accordion = document.getElementById("more_info_accordion")

    if (more_info_accordion.classList.contains("active")){
        more_info_accordion.classList.remove("active");
    } else {
        more_info_accordion.classList.add("active");
    }
}

/* Loading of location information */
function updateLocationContent(location_id) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {   
        if (xmlhttp.status == 200) {

            document.getElementById("location_content").innerHTML = xmlhttp.response;
        }
        else {
            console.log(xmlhttp.status);
            console.log('Error was returned');
        }
        }
    };
    url = "/location/"+location_id;
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    xmlhttp.onload = () => {
        document.getElementById("more_info_accordion").addEventListener('click', show_details, false);
    }
}

