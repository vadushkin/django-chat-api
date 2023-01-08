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
        payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "test message",
        }

        response = self.client.post(self.message_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)

        self.assertEqual(result["message"], "test message")
        self.assertEqual(result["sender"]["id"], self.sender.id)
        self.assertEqual(result["receiver"]["id"], self.receiver.id)
