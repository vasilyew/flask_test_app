const rowTemplate = '<div class="row"><div class="col-2 col-md-1">{{user_id}}</div><div class="col-10 col-md-4">{{user_name}}</div><div class="col-md-4">{{permissions}}</div>{{buttons}}</div><hr />'
const buttonEditPermissions = '<div class="col-md-1"><input id="edit-{{user_id}}" class="form-control btn btn-success" type="text" value="Edit" /></div>'
const buttonDeleteUser = '<div class="col-md-1"><input id="del-{{user_id}}" class="form-control btn btn-danger" type="text" value="Del" /></div>'

function showUsers(data, status, jqXRP){
    var resultString = '<hr />'
    for(var i in data) {
        var user = data[i]

        var buttonsHtml = ''
        if (isEditor) {
            buttonsHtml += buttonEditPermissions.replace('{{user_id}}', user.id)
        }

        if (isDeleter) {
            buttonsHtml += buttonDeleteUser.replace('{{user_id}}', user.id)
        }

        if (user.id == userId) {
            buttonsHtml = ''
        }

        resultString += rowTemplate
            .replace('{{user_id}}', user.id)
            .replace('{{user_name}}', user.login)
            .replace('{{permissions}}', user.permissions.join(';'))
            .replace('{{buttons}}', buttonsHtml)
    }
    $('#list-user-container').html(resultString)

    for(var i in data) {
        var user = data[i]
        $('#edit-' + user.id).on('click', user, showModalEditUser)
        $('#del-' + user.id).on('click', {user_id: user.id}, deleteUser)
    }
}

function success_update() {
    $('#user-permissions-modal').modal('hide')
    get_users()
}

function updatePermissions(event) {
    var perms = []
    if ($('#checkbox-creator').is(":checked")) {
        perms.push('creator')
    }
    if ($('#checkbox-editor').is(":checked")) {
        perms.push('editor')
    }
    if ($('#checkbox-deleter').is(":checked")) {
        perms.push('deleter')
    }
    $.ajax({
        type: 'PUT',
        url: '/user/' + event.data + '/permissions',
        data: JSON.stringify({permissions: perms.join(';')}),
        success: success_update,
        dataType: 'json',
        contentType: "application/json",
        beforeSend: function(request) {
            request.setRequestHeader('session', localStorage.getItem('session'));
        },
    })
}

function showModalEditUser(event) {
    $('#edit-user-login').text(event.data.login)
    $('#checkbox-creator').prop('checked', event.data.permissions.indexOf('creator') > -1);
    $('#checkbox-editor').prop('checked', event.data.permissions.indexOf('editor') > -1);
    $('#checkbox-deleter').prop('checked', event.data.permissions.indexOf('deleter') > -1);
    $('#update-permissions').unbind()
    $('#update-permissions').on('click', event.data.id, updatePermissions)
    $('#user-permissions-modal').modal('show')
}

function deleteUser(event) {
    $.ajax({
        type: 'DELETE',
        url: '/user/' + event.data.user_id,
        success: get_users,
        beforeSend: function(request) {
            request.setRequestHeader('session', localStorage.getItem('session'))
        },
    })
}

function show_create_user_panel(){
    if (isCreator){
        $('#create-user-container').show()
    }
}

function get_users() {
    $.ajax({
        type: 'GET',
        url: '/user',
        success: showUsers,
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader('session', localStorage.getItem('session'))
        },
    })
}

function set_permissions() {
    var permissions = localStorage.getItem('permissions')
    isCreator = permissions.indexOf('admin') > -1 || permissions.indexOf('creator') > -1
    isEditor = permissions.indexOf('admin') > -1 || permissions.indexOf('editor') > -1
    isDeleter = permissions.indexOf('admin') > -1 || permissions.indexOf('deleter') > -1
}

function set_storage_data(){
    userId = localStorage.getItem('user_id')
    set_permissions()
}

set_storage_data()
show_create_user_panel()
get_users()

function success_add_user() {
    get_users()
    $('#login').val('')
    $('#password').val('')
}

$('#add-user').on('click', function() {
    var login = $('#login').val()
    var password = $('#password').val()
    if (login == '' || password == ''){
        return
    }
    $.ajax({
        type: 'POST',
        url: '/user',
        data: JSON.stringify({login: login, password: password}),
        success: success_add_user,
        contentType: "application/json",
        beforeSend: function(request) {
            request.setRequestHeader('session', localStorage.getItem('session'));
        },
    })
})