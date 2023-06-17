from receiver import To_Google, To_Yandex

class Sender():
    @staticmethod
    def send(address, phone_numbers: list, message):
        result_list = []
        for number in phone_numbers:
            if address == "Google":
                recepient = To_Google()
            elif address == "Yandex":
                recepient = To_Yandex()
            result = [recepient.response(number, message).status_code, number]
            result_list.append(result)
        return result_list