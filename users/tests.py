from rest_framework.test import APITestCase

from .views import get_random, get_access_token, get_refresh_token


class TestGenericFunctions(APITestCase):
    def test_get_random(self):
        # guinea pigs
        test_x = get_random(10)
        test_y = get_random(10)
        test_j = get_random(20)

        # if testX is not null
        self.assertTrue(test_x)
        self.assertTrue(test_y)
        self.assertTrue(test_j)

        # check the length of test cases
        self.assertEqual(len(test_x), 10)
        self.assertEqual(len(test_y), 10)
        self.assertEqual(len(test_j), 20)

        # check if test_x == test_y
        self.assertNotEqual(test_x, test_y)

    def test_get_access_token(self):
        # test test_payload :|
        test_payload = {
            'id': 1
        }

        # get back out test token and go to check
        test_token = get_access_token(test_payload)

        # check if test_token is null
        self.assertTrue(test_token)

    def test_get_refresh_token(self):
        # get back out test token and go to check
        test_token = get_refresh_token()

        # check if test_token is null
        self.assertTrue(test_token)


class TestAuthentication(APITestCase):
    login_url = "/user/login/"
    register_url = "/user/register/"
    refresh_url = "/user/refresh/"

    def test_register(self):
        # test case
        test_payload = {
            "username": "Oak",
            "password": "loading",
            "email": "oak@gmail.com"
        }
        # response from server
        response = self.client.post(
            self.register_url,
            data=test_payload
        )

        # check if we get 201
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        # test case
        test_payload = {
            "username": "Titmouse",
            "password": "cool",
            "email": "titmouse@gmail.com"
        }

        # test register
        self.client.post(self.register_url, data=test_payload)

        # test login
        response = self.client.post(self.login_url, data=test_payload)
        result = response.json()

        # check if we get 200
        self.assertEqual(response.status_code, 200)

        # check if we get tokens
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        # test case
        test_payload = {
            "username": "Larch",
            "password": "awesome",
            "email": "larch@gmail.com"
        }

        # test register
        self.client.post(self.register_url, data=test_payload)

        # test login
        response = self.client.post(self.login_url, data=test_payload)
        refresh = response.json()["refresh"]

        # check if we get a refresh token
        response = self.client.post(
            self.refresh_url,
            data={"refresh": refresh}
        )
        result = response.json()

        # check if we get 200
        self.assertEqual(response.status_code, 200)

        # check if we get tokens
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])
