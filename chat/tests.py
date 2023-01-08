from rest_framework.test import APITestCase


class TestMessage(APITestCase):
    message_url = "/chat/message"

    def setUp(self):
        from users.models import CustomUser, UserProfile

        self.sender = CustomUser.objects._create_user("sender", "sender123")
        UserProfile.objects.create(
            first_name="sender", last_name="sender", user=self.sender, caption="sender", about="sender")

        self.receiver = CustomUser.objects._create_user("receiver", "receiver123")
        UserProfile.objects.create(
            first_name="receiver", last_name="receiver", user=self.receiver, caption="receiver", about="receiver")

        self.client.force_authenticate(user=self.sender)

    def test_post_message(self):
        test_payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "test message",
        }

        response = self.client.post(self.message_url, data=test_payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)

        self.assertEqual(result["message"], "test message")
        self.assertEqual(result["sender"]["id"], self.sender.id)
        self.assertEqual(result["receiver"]["id"], self.receiver.id)

    def test_update_message(self):
        test_payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "test message",
        }

        self.client.post(self.message_url, data=test_payload)

        test_payload = {
            "message": "test message updated",
            "is_read": True
        }
        response = self.client.patch(
            self.message_url + "/1", data=test_payload)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"], "test message updated")
        self.assertEqual(result["is_read"], True)

    def test_delete_message(self):
        test_payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "test message",

        }
        self.client.post(self.message_url, data=test_payload)

        response = self.client.delete(
            self.message_url + "/1", data=test_payload)

        self.assertEqual(response.status_code, 204)

    def test_get_message(self):
        response = self.client.get(
            self.message_url + f"?user_id={self.receiver.id}")
        self.assertEqual(response.status_code, 200)
