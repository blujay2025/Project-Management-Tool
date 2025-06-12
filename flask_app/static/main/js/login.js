// Handles credential checking for login
let count     = 0
const login_credentials = function checkCredentials() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var data_dict = {'email': email, 'password': password}

    jQuery.ajax({
        url: "/processlogin",
        data: data_dict,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.success == 1) {
                window.location.href = "/projects";
              } else {
                count = count + 1;
                document.getElementById('count').innerText = count;
              }
            }
    });
}

const login_button = document.getElementById('login-button');
login_button.addEventListener('click', login_credentials);