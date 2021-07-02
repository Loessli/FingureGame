import requests


if __name__ == '__main__':
    data ={
        "user": "zhuqi"
    }
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    response = requests.post(url="http://127.0.0.1:51233/search/", json=data, headers=headers)
