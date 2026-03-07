import requests

def check_api_data():
    url = "http://localhost:8000/api/v1/communities/"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            print(f"Total communities returned: {len(data)}")
            for c in data:
                print(f"ID: {c.get('id_community')}, Name: {c.get('name_community')}, Code: {c.get('code')}, Leader: {c.get('leader_name')}")
        else:
            print(f"Error: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error connecting: {e}")

if __name__ == "__main__":
    check_api_data()
