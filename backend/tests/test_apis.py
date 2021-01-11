import requests


url = "http://127.0.0.1:8000/apis/88bvchvnsj7/back"
#ip_adress_params = {"ip_adress": "kaFKX"}
#verify_backend_func = requests.post(url, params=ip_adress_params)
data = {
   "scraping_date": "q",
   "header_hash": "a",
   "new_header": "a",
   "source": "a",
   "public_date": "a",
}

data_all = [data] * 2
verify_backend_func = requests.post(url, json=data_all)
print(verify_backend_func.json())
