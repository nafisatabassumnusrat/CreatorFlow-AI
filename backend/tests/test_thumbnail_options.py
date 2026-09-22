import urllib.request
import json

def test():
    req = urllib.request.Request("http://127.0.0.1:8080/api/videos/demo", data=b"", method="POST")
    demo = json.loads(urllib.request.urlopen(req).read().decode())
    pid = demo["project_id"]
    print("Created demo project:", pid)

    req_thumb = urllib.request.Request(f"http://127.0.0.1:8080/api/videos/{pid}/thumbnail", data=b"", method="POST")
    updated = json.loads(urllib.request.urlopen(req_thumb).read().decode())
    print(f"Total thumbnail options: {len(updated['thumbnail_concepts'])}")
    for c in updated["thumbnail_concepts"]:
        print(f"  Option {c['id']}: '{c['title_text']}' | Score: {c['overall_score']}/10 | Active: {c['is_selected']}")

    # Switch to option 6 ("ZERO TO AGENT IN 5 MIN")
    select_data = json.dumps({"thumbnail_id": "thumb_6"}).encode("utf-8")
    req_sel = urllib.request.Request(
        f"http://127.0.0.1:8080/api/videos/{pid}/select-thumbnail",
        data=select_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    switched = json.loads(urllib.request.urlopen(req_sel).read().decode())
    print("\nSwitched to Option 6:")
    print("Active thumbnail title:", switched["selected_thumbnail"]["title_text"])
    print("Active thumbnail ID:", switched["selected_thumbnail"]["id"])
    assert switched["selected_thumbnail"]["id"] == "thumb_6"
    print("ALL THUMBNAIL OPTIONS TESTS PASSED!")

if __name__ == "__main__":
    test()
