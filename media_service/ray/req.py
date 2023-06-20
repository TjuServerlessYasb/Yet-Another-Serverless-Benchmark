import requests
import json

headers = {
    "Content-Type": "application/json",
    "accept": "application/json",
    }


#req = '{"body":{ "portfolioType":"S&P", "portfolio":"1234"}}'


# req = { "portfolioType":"S&P", "portfolio":"1234"}

req = {"body":{ "portfolioType":"S&P", "portfolio":"1234"}}
resp3 = requests.post("http://10.244.0.158:8000/ms/lastpx", data=json.dumps(req), headers=headers)
print(resp3.text)

review = {"username": "username_68", "password": "password_68", "title": "Alien", "rating": 0, "text": "3M826CsBEDG55LVhkC9N5oiRTlA9CE5J24pnQGQBgLhA3fCqJjS2SyBEPsJEzbvuIqeUHKrc92ot6Z78jWaiLfz8It5RdUOVTNhmOySM4dsIIO7T2d3o0tBpepj3ITQyOTjvegZgJsg3fR69efLEfMOH1CVhjU8Md0eA1CCEMQ2VjO1RdrK1UHCqkTSnO42MP8vFbiYzgE3ImuqFHoXyMz7rpCnNLsVMyyHdeWtc2LnEvak6eN5StXthiETi0sHB"}
resp = {"time": {"compose-review": {"start_time": 1687244587.0820081, "end_time": 1687244587.0820506}}, "body": {"username": "username_68", "password": "password_68", "title": "Alien", "rating": 0, "text": "3M826CsBEDG55LVhkC9N5oiRTlA9CE5J24pnQGQBgLhA3fCqJjS2SyBEPsJEzbvuIqeUHKrc92ot6Z78jWaiLfz8It5RdUOVTNhmOySM4dsIIO7T2d3o0tBpepj3ITQyOTjvegZgJsg3fR69efLEfMOH1CVhjU8Md0eA1CCEMQ2VjO1RdrK1UHCqkTSnO42MP8vFbiYzgE3ImuqFHoXyMz7rpCnNLsVMyyHdeWtc2LnEvak6eN5StXthiETi0sHB"}}


# resp3 = requests.post("http://10.244.0.158:8000/ms/compose_review", data=json.dumps(review), headers=headers)
# print(resp3.text)
#
# resp3 = requests.post("http://10.244.0.158:8000/ms/upload_user_id", data=json.dumps(resp), headers=headers)
# print(resp3.text)
# resp3 = requests.post("http://10.244.0.158:8000/ms/upload_movie_id", data=json.dumps(resp), headers=headers)
# print(resp3.text)
# resp3 = requests.post("http://10.244.0.158:8000/ms/upload_text", data=json.dumps(resp), headers=headers)
# print(resp3.text)
# resp3 = requests.post("http://10.244.0.158:8000/ms/upload_unique_id", data=json.dumps(resp), headers=headers)
# print(resp3.text)


mrreq = ['error finding function upload-movie-id.openfaas-fn-hwh: server returned non-200 status code (404) for function, upload-movie-id, body: ', '{"time": {"mr-upload-unique-id": {"start_time": 1687257263.6203523, "end_time": 1687257263.6204927}}, "body": {"review_id": "6372492463620179"}}', '{"time": {"mr-upload-text": {"start_time": 1687257263.620659, "end_time": 1687257263.620714}, "compose-review": {"start_time": 1687257263.5982065, "end_time": 1687257263.598252}}, "body": {"text": "xGxw0r4hPYM8BUITA3eNr0DeJ597L7loSltMVJzHPRYteTGvY5jxpIQ1r1yrEeFA0omYqErB4dQldaHCNTfzN2kqICV67mTpcDnahm2xVEKvhNzKTUp0vqdNu8zlv2j55bd4gPklRp4cZo9sP5Qkf9YCOFKoMwWkpS7QTFbMLRGC2iHVWsu7Li5x66mRIWWeHYJYtTZPw5fAf4tZw329gBCJVtBbHCvKytTZEYd8QU26rkazp6o50gDKLeLvuCeX"}}', '{"time": {"upload-user-id": {"start_time": 1687257263.6183074, "end_time": 1687257263.632936}}, "body": "No user username_2"}']
resp3 = requests.post("http://10.244.0.158:8000/ms/mr_compose_and_upload_handle", data=json.dumps(mrreq), headers=headers)
print(resp3.text)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
last3req = {"time": {"mr-compose-and-upload": {"start_time": 1687261170.8957996, "end_time": 1687261170.8959844}, "mr-upload-text": {"start_time": 1687261170.8712354, "end_time": 1687261170.871284}, "compose-review": {"start_time": 1687261170.8471284, "end_time": 1687261170.8471708}, "mr-upload-unique-id": {"start_time": 1687261170.8712873, "end_time": 1687261170.871392}, "upload-user-id": {"start_time": 1687261170.8668854, "end_time": 1687261170.8838909}, "upload-movie-id": {"start_time": 1687261170.8649237, "end_time": 1687261170.8838952}}, "body": {"text": "S27CtHJsWYbD77Qo3RqI99NtvcQ6kvwOP2vAzbmJacEDRqJolklAwgCivoKVCSm7HDUvla5LJlYsoxsiV3UkcysMl7i0H8t0dx9Ayp1nFsb0tBWw6pqEjOElKV7wWKbyYymZWdMwVsOt5HnWxw2FZW6yqMOX8me2lAjRMqUIDfAkIOSfD0jPhf47qZVQAXi645mqXLyrPB77ZswVoey5nMH2p8nwgiez6o8hX5DlsZYHW9ipP2VlbuNDh7Blis8V", "review_id": "1972496370871941", "user_id": 537, "movie_id": "22787", "rating": 7, "timestamp": 1687261170895}}

resp3 = requests.post("http://10.244.0.158:8000/ms/store_review_service", data=json.dumps(last3req), headers=headers)
print(resp3.text)
resp3 = requests.post("http://10.244.0.158:8000/ms/upload_user_review", data=json.dumps(last3req), headers=headers)
print(resp3.text)
resp3 = requests.post("http://10.244.0.158:8000/ms/upload_movie_review_handle", data=json.dumps(last3req), headers=headers)
print(resp3.text)