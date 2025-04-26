from conftest import create_admin, create_user, admin_auth_headers


def test_some():
    assert True


def test_create_admin_fixture(create_admin):

    user = create_admin
    assert user.is_superuser == True


def test_create_user_fixture(create_user):

    user = create_user
    assert user.is_superuser == False


def test_access_token_for_admin(admin_auth_headers):
    access_token = admin_auth_headers
    print(f"Access Token: {access_token}")
    assert True
