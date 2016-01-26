import wit


def ask_wit(message):
    access_token = 'PWKWIJSS4XX3EJDMC6AHHI6N7VQ5JJXW'
    wit.init()
    # response = wit.voice_query_auto(access_token)

    response = wit.text_query(message, access_token)
    wit.close()
    return 'Response: {}'.format(response)
