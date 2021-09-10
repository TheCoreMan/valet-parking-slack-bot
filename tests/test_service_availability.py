import requests

service_cloud_url = "https://valet-parking-slack-bot-n2mj5hiwyq-lz.a.run.app" 

def test_cloud_endpoint():
    response = requests.get(service_cloud_url + "/test/healthcheck")
    assert response.ok
    data = response.json()
    assert data["message"] == "I'm alive!"
    assert data["ts"]
