import pytest

from funkwhale_api.common import authentication


@pytest.mark.parametrize(
    "setting_value, is_superuser, has_verified_primary_email, expected",
    [
        ("mandatory", False, False, True),
        ("mandatory", False, True, False),
        ("mandatory", True, False, False),
        ("mandatory", True, True, False),
        ("optional", False, False, False),
        ("optional", False, True, False),
        ("optional", True, False, False),
        ("optional", True, True, False),
    ],
)
def test_should_verify_email(
    setting_value,
    is_superuser,
    has_verified_primary_email,
    expected,
    factories,
    settings,
):
    settings.ACCOUNT_EMAIL_VERIFICATION = setting_value
    user = factories["users.User"](is_superuser=is_superuser)
    setattr(user, "has_verified_primary_email", has_verified_primary_email)
    assert authentication.should_verify_email(user) is expected


def test_app_token_authentication(factories, api_request):
    user = factories["users.User"]()
    app = factories["users.Application"](user=user, scope="read write")
    request = api_request.get("/", HTTP_AUTHORIZATION="Bearer {}".format(app.token))

    auth = authentication.ApplicationTokenAuthentication()
    assert auth.authenticate(request)[0] == app.user
    assert request.scopes == ["read", "write"]
