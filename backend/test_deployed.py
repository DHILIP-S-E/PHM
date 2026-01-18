"""
Test DEPLOYED backend server
Usage: python test_deployed.py [OPTIONAL_URL]
"""
import requests
import sys
import time

# Default URL (can be overridden by command line argument)
DEFAULT_URL = "http://g0wckoc4sswgsg44gowg88c8.3.110.117.164.sslip.io"

def get_base_url():
    if len(sys.argv) > 1:
        return sys.argv[1].rstrip('/')
    return DEFAULT_URL

BASE_URL = get_base_url()
API_URL = f"{BASE_URL}/api/v1"

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def test_health():
    print_header("1. CHECKING HEALTH ENDPOINT")
    url = f"{BASE_URL}/health"
    print(f"Requesting: {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Health check PASSED")
                return True
            else:
                print("⚠️  Health check returned 200 but status is not 'healthy'")
        else:
            print("❌ Health check FAILED")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
    
    return False

def test_docs():
    print_header("2. CHECKING DOCS (SWAGGER UI)")
    url = f"{BASE_URL}/docs"
    print(f"Requesting: {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Specs/Docs are accessible")
            return True
        else:
            print("❌ Specs/Docs NOT accessible")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
        
    return False

def test_login():
    print_header("3. CHECKING LOGIN (Database Connection)")
    url = f"{API_URL}/auth/login"
    
    # Use a test account that should exist
    payload = {
        "username": "war@gmail.com",
        "password": "12345678" 
    }
    
    print(f"Requesting: {url}")
    print(f"User: {payload['username']}")
    
    try:
        response = requests.post(
            url, 
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login SUCCESSFUL")
            token = response.json().get("access_token")
            print(f"Token received: {token[:20]}...")
            return token
        elif response.status_code == 401:
            print("✅ Server reachable (401 Unauthorized) - Credentials might be wrong, but DB is likely working")
            print(f"Response: {response.json()}")
            return None
        elif response.status_code == 500:
            print("❌ Server Error (500) - Likely Database Connection Issue")
            print(f"Response: {response.text}")
            return None
        else:
            print(f"⚠️  Unexpected Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

if __name__ == "__main__":
    print(f"Targeting Server: {BASE_URL}")
    
    if test_health():
        test_docs()
        test_login()
    else:
        print("\n❌ CRITICAL: Unknown host or server is down.")
        print("Tips:")
        print("1. Check if the URL is correct")
        print("2. If using Coolify/Docker, check logs")
        print("3. Ensure firewall/security groups allow port 80/443")
