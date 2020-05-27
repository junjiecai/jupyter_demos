from typing import NewType

PhoneNumber = NewType('PhoneNumber', int)


def find_user(phone: PhoneNumber):
    return type(phone)


print(find_user(PhoneNumber(12322)))  # 注意：不要和Class的初始化混淆
