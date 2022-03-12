function success_login(data, status, jqXRP) {
    localStorage.setItem('session', data.session)
    localStorage.setItem('permissions', data.permissions)
    localStorage.setItem('user_id', data.user_id)
    window.location.href = '/users'
}

function error_login(jqXHR, exception) {
    $('#login-error-message').text(jqXHR.responseJSON.error)
    $('#login-error-message').show()
}

$('#submit').on('click', function() {
    $('#login-error-message').hide()
    var login = $('#login').val()
    var password = $('#password').val()
    $.ajax({
        type: 'POST',
        url: '/login',
        data: JSON.stringify({login: login, password: password}),
        success: success_login,
        error: error_login,
        dataType: 'json',
        contentType: "application/json",
    })
})