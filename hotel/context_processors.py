
def common_variables(request):
    return {'logged_in': request.session.get('logged_in', False),
            'access_type':request.session.get('access_type'),
            'user_id':request.session.get('user_id')}
