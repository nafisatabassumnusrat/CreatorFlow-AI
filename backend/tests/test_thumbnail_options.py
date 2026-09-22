from fastapi.testclient import TestClient
from backend.main import app

def test_thumbnail_options_flow():
    client = TestClient(app)
    
    # Create demo project
    res_demo = client.post("/api/videos/demo")
    assert res_demo.status_code == 200
    demo = res_demo.json()
    pid = demo["project_id"]
    assert pid is not None

    # Generate / retrieve thumbnails
    res_thumb = client.post(f"/api/videos/{pid}/thumbnail")
    assert res_thumb.status_code == 200
    updated = res_thumb.json()
    assert len(updated.get("thumbnail_concepts", [])) >= 1

    # Select thumbnail option
    first_thumb_id = updated["thumbnail_concepts"][0]["id"]
    res_sel = client.post(
        f"/api/videos/{pid}/select-thumbnail",
        json={"thumbnail_id": first_thumb_id}
    )
    assert res_sel.status_code == 200
    switched = res_sel.json()
    assert switched["selected_thumbnail"]["id"] == first_thumb_id
