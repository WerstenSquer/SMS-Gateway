from receiver import To_Google, To_Yandex

class Sender():
    @staticmethod
    def send(address, phone_number, message):
        if address == "Google":
            recepient = To_Google()
        elif address == "Yandex":
            recepient = To_Yandex()
        return [recepient.response(phone_number, message).status_code,
                recepient.response(phone_number, message).url]