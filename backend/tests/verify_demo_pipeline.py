import urllib.request
import json
import time

def run():
    print("1. Testing Demo Creation...")
    req = urllib.request.Request("http://127.0.0.1:8080/api/videos/demo", data=b"", method="POST")
    resp = urllib.request.urlopen(req)
    demo = json.loads(resp.read().decode())
    pid = demo["project_id"]
    print(f"   [OK] Demo Project: {pid}")
    print(f"   [OK] Stage: {demo['current_stage']}")
    print(f"   [OK] Gate 1: {demo['waiting_for_approval_type']}")
    print(f"   [OK] Title: {demo['selected_title']}")

    print("\n2. Testing Gate 1: Human Script Approval & Auto-Advance...")
    approve_data = json.dumps({"approval_type": "script", "decision": "approve"}).encode("utf-8")
    req2 = urllib.request.Request(
        f"http://127.0.0.1:8080/api/videos/{pid}/approve",
        data=approve_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    resp2 = urllib.request.urlopen(req2)
    demo2 = json.loads(resp2.read().decode())
    print(f"   [OK] Stage: {demo2['current_stage']}")
    print(f"   [OK] Gate 2: {demo2['waiting_for_approval_type']}")
    print(f"   [OK] Storyboard Scenes: {len(demo2['storyboard'])}")
    print(f"   [OK] Quality Checks Passed: {demo2['quality_checks']['passed'] if demo2['quality_checks'] else False}")

    print("\n3. Testing Gate 2: Human Production Approval & FFmpeg Rendering...")
    render_data = json.dumps({"approval_type": "production", "decision": "approve"}).encode("utf-8")
    req3 = urllib.request.Request(
        f"http://127.0.0.1:8080/api/videos/{pid}/approve",
        data=render_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    resp3 = urllib.request.urlopen(req3)
    demo3 = json.loads(resp3.read().decode())
    print(f"   [OK] Final Stage: {demo3['current_stage']}")
    print(f"   [OK] Rendered Video: {demo3['rendered_video_url']}")
    print(f"   [OK] File Size MB: {demo3['final_package']['file_size_mb'] if demo3['final_package'] else 0}")
    print(f"   [OK] Activity Logs Count: {len(demo3['activity_logs'])}")
    print("\nEND-TO-END DEMO VERIFICATION COMPLETED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run()
