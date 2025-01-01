from immo.models import User

def user_context(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        return {'logged_in_user': user}
    return {}