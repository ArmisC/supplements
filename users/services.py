import uuid

from users.models import User


def get_anonymous_id(request):
    if not request.session.session_key:
        request.session.create()

    if 'anon_id' not in request.session:
        request.session['anon_id'] = str(uuid.uuid4())

    return request.session['anon_id']


def create_anonymous_user(request):
    ai = get_anonymous_id(request)
    user, created = User.objects.get_or_create(
        email=ai,
        defaults={
            "role": "I",
            "password": ai,
            "logged_in": True,
        }
    )
    print('------------------')
    print(user, created, user.logged_in)
    print('------------------')
    return user
