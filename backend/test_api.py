
import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    try:
        # 1. Login
        print("Logging in...")
        resp = requests.post(f"{BASE_URL}/auth/login", data={
            "username": "admin@pharmaec.com",
            "password": "admin123" 
        })
        
        if resp.status_code != 200:
            print(f"❌ Login failed: {resp.status_code} {resp.text}")
            return
            
        token = resp.json()["access_token"]
        print("✅ Login successful")
        
        # 2. Get Unified Masters
        print("Fetching Unified Masters...")
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/unified-masters/all", headers=headers)
        
        if resp.status_code == 200:
            data = resp.json()
            print("✅ Unified Masters fetch successful!")
            print(f"   Categories: {len(data['categories'])}")
            print(f"   Medicine Types: {len(data['medicine_types'])}")
            print(f"   GST Slabs: {len(data['gst_slabs'])}")
        else:
            print(f"❌ Fetch failed: {resp.status_code} {resp.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
