"""
Script kiem thu tu dong toan bo Backend API.
Chay khi server dang bat (uvicorn src.main:app --reload)
"""
import httpx
import asyncio
import json
import sys
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

BASE_URL = "http://localhost:8000"
API = f"{BASE_URL}/api/v1"

TEST_EMAIL = "testuser_auto@xhome.vn"
TEST_PASSWORD = "matkhau123"
TEST_PHONE = "0999888777"

results = []

def log(test_name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append((test_name, passed))
    print(f"  [{status}]  {test_name}")
    if detail and not passed:
        print(f"         -> {detail[:200]}")

async def run_tests():
    async with httpx.AsyncClient(timeout=10) as client:

        # TEST 1
        print("\n[1/6] Health Check...")
        try:
            r = await client.get(f"{BASE_URL}/health")
            log("GET /health", r.status_code == 200, r.text)
        except Exception as e:
            log("GET /health", False, str(e))
            print("\nServer chua chay! Hay chay: uvicorn src.main:app --reload")
            return

        # TEST 2
        print("\n[2/6] Get Properties (ket noi Database)...")
        try:
            r = await client.get(f"{API}/properties?limit=2")
            data = r.json()
            has_items = "items" in data
            log("GET /properties - Status 200", r.status_code == 200, r.text[:200])
            log("GET /properties - Co truong 'items'", has_items)
            if has_items and len(data["items"]) > 0:
                log(f"GET /properties - Tim thay {len(data['items'])} can nha tu DB", True)
            else:
                log("GET /properties - Database tra ve 0 can nha", False, "Chua chay file seed SQL")
        except Exception as e:
            log("GET /properties", False, str(e))

        # TEST 3
        print("\n[3/6] Register...")
        try:
            r = await client.post(f"{API}/auth/register", json={
                "full_name": "Test User Auto",
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD,
                "phone": TEST_PHONE
            })
            if r.status_code == 200:
                user_data = r.json()
                log("POST /auth/register - Tao tai khoan thanh cong", True)
                log(f"POST /auth/register - User ID: {user_data.get('id', 'N/A')}", True)
            elif r.status_code == 400:
                log("POST /auth/register - Email/Phone da ton tai (OK neu da test truoc do)", True, r.text)
            else:
                log("POST /auth/register", False, r.text[:200])
        except Exception as e:
            log("POST /auth/register", False, str(e))

        # TEST 4
        print("\n[4/6] Login & JWT Token...")
        access_token = None
        try:
            r = await client.post(f"{API}/auth/login", data={
                "username": TEST_EMAIL,
                "password": TEST_PASSWORD
            })
            if r.status_code == 200:
                token_data = r.json()
                access_token = token_data.get("access_token")
                log("POST /auth/login - Dang nhap thanh cong", True)
                log(f"POST /auth/login - Nhan duoc JWT Token ({len(access_token)} ky tu)", access_token is not None)
            else:
                log("POST /auth/login", False, r.text[:200])
        except Exception as e:
            log("POST /auth/login", False, str(e))

        # TEST 5
        print("\n[5/6] Bao mat - Goi API khong co Token...")
        try:
            r = await client.get(f"{API}/bookings/my")
            log("GET /bookings/my (khong Token) - Bi chan 401", r.status_code in [401, 403], f"Status: {r.status_code}")
        except Exception as e:
            log("GET /bookings/my (khong Token)", False, str(e))

        # TEST 6
        print("\n[6/6] Dat lich (co Token)...")
        if access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            try:
                r = await client.get(f"{API}/properties?limit=1")
                props = r.json()
                if props.get("items") and len(props["items"]) > 0:
                    property_id = props["items"][0]["id"]

                    r = await client.post(f"{API}/bookings", json={
                        "property_id": property_id,
                        "pax_count": 2,
                        "customer_note": "Test tu dong"
                    }, headers=headers)

                    if r.status_code == 200:
                        booking = r.json()
                        log("POST /bookings - Dat lich thanh cong!", True)
                        log(f"POST /bookings - Ma dat lich: {booking.get('request_code', 'N/A')}", True)
                    else:
                        log("POST /bookings", False, r.text[:300])

                    r = await client.get(f"{API}/bookings/my", headers=headers)
                    if r.status_code == 200:
                        my_bookings = r.json()
                        log(f"GET /bookings/my - Tim thay {len(my_bookings)} lich dat", True)
                    else:
                        log("GET /bookings/my", False, r.text[:200])
                else:
                    log("POST /bookings - Khong co property nao trong DB de test", False)
            except Exception as e:
                log("POST /bookings", False, str(e))
        else:
            log("POST /bookings - Bo qua (khong co Token tu buoc Login)", False)

    # SUMMARY
    print("\n" + "=" * 60)
    passed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"KET QUA: {passed}/{total} tests PASSED")
    if passed == total:
        print("TOAN BO BACKEND HOAT DONG HOAN HAO!")
    else:
        failed = [name for name, p in results if not p]
        print(f"Cac test that bai:")
        for f in failed:
            print(f"  - {f}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_tests())
