import wit

access_token = '5LWLMABHXZMOT53DHSZKP63LLHIZU7MC'
wit.init()

response = wit.voice_query_auto(access_token)
print('Response: {}'.format(response))
wit.close()