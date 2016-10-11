import json


def test_count(client):
    res = client.open('/cheese/pairs?count=2')
    assert res.status_code == 200
    data = json.loads(res.data.decode())
    assert len(data) == 2
