from __future__ import annotations


class PhoneNumber:
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def __cpm__(self, y: PhoneNumber):
        return self.phone_number == y.phone_number


def find_user(phone: PhoneNumber):
    return type(phone)


print(find_user(PhoneNumber(1231)))
