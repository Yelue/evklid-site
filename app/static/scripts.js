/*simple ajax request */
function send_region(element_select){
			document.getElementById('region_choice').value = element_select.value;
			var xhr = new XMLHttpRequest();
			
			xhr.onreadystatechange = function() {
		    if (xhr.readyState == XMLHttpRequest.DONE) {
		        var answer = xhr.responseText;
		        document.getElementById('univer').innerHTML = answer
			    	}
				}
			
			var sel=document.getElementById('select_region').selectedIndex;
		    var options=document.getElementById('select_region').options;

		    var params = 'post_region='+encodeURIComponent(options[sel].value);
			
			xhr.open("POST", '/make_list', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

			

			xhr.send(params);
		}

function send_to_basket(button){
	var xhr = new XMLHttpRequest();
			
			xhr.onreadystatechange = function() {
		    if (xhr.readyState == XMLHttpRequest.DONE) {
		        var answer = xhr.responseText;
		        location.href = location.href;
			    	}
				}
			// alert(document.getElementById('year_choice').value);
			var row = document.getElementById('row_'+button.id);
			var keys = document.getElementById('basket_keys').textContent;
			var text_row = row.textContent;

		    var params = 'text='+encodeURIComponent(text_row)+'&keys_r='+encodeURIComponent(keys);
			
			xhr.open("POST", '/add_to_basket', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

			

			xhr.send(params);

}
function save_data_div(){

	document.getElementById('year_choice').value = document.getElementById('select_year').value;
	// alert(document.getElementById('year_choice').value);
	document.getElementById('region_choice').value = document.getElementById('select_region').value;
}

function save_score(){

	
	var xhr = new XMLHttpRequest();
			
			xhr.onreadystatechange = function() {
		    if (xhr.readyState == XMLHttpRequest.DONE) {
		        var answer = JSON.parse(xhr.responseText);
		       	location.href=location.href;
		       	}
				}

			var subject_name = document.getElementById('subject_name').value;
			var subject_score = document.getElementById('subject_score').value;
			var params = 'subject_name='+encodeURIComponent(subject_name)+'&subject_score='+encodeURIComponent(subject_score);
			
			xhr.open("POST", '/add_to_users_score', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

			

			xhr.send(params);
}
function delete_choice(button){
	var id = button.id;
	var row = document.getElementById('row_'+id);
	var year = document.getElementById('row_'+id+'_td_year').innerHTML;
	var base = document.getElementById('row_'+id+'_td_base').innerHTML;
	var faculty = document.getElementById('row_'+id+'_td_faculty').innerHTML;
	var univer = document.getElementById('row_'+id+'_td_univer').innerHTML;
	var specialty = document.getElementById('row_'+id+'_td_specialty').innerHTML;
	
	var xhr = new XMLHttpRequest();
			
	xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        var answer = xhr.responseText;
        if (answer=='200'){
        	location.href=location.href;
        }
        	
       		}
		}

	var params = 'year='+encodeURIComponent(year)+'&base='+encodeURIComponent(base)+'&faculty='+encodeURIComponent(faculty)+'&univer='+encodeURIComponent(univer)+'&specialty='+encodeURIComponent(specialty);
	
	xhr.open("POST", '/delete_choice', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	

	xhr.send(params);
}
function delete_score(button){
	var id = button.id;
	
	var subject_name = document.getElementById('name_'+id).innerHTML;
	var subject_score = document.getElementById('score_'+id).innerHTML;
	
	var xhr = new XMLHttpRequest();
			
			xhr.onreadystatechange = function() {
		    if (xhr.readyState == XMLHttpRequest.DONE) {
		        var answer = xhr.responseText;
		        if (answer=='200'){
		        	location.href=location.href;
		        }
		        	
		       		}
				}

			var params = 'subject_name='+encodeURIComponent(subject_name)+'&subject_score='+encodeURIComponent(subject_score);
			
			xhr.open("POST", '/delete_score', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

			

			xhr.send(params);	
}
