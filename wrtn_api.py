import argparse
import httpx
import asyncio
from time import sleep
from icecream import ic

from requests import get, post, put

new_token = ''
    
def make_requests(token, message) -> str:
    global new_token
    if new_token:
        token = new_token
    chat_box_id: str = '665a22664d405cf4ad5da5d4'
    try:
        # Requête 1
        resp = post(
            f"https://william.wow.wrtn.ai/chat/v3/{chat_box_id}/start?platform=web&user=sgassackys@gmail.com&model=claude2.1",
            json={"message": message, "reroll": False, "images": []},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json" 
            }
        )
        # ic(resp.json())
        chat_id = resp.json()["data"]

        # Requête 2
        resp = put(
            f"https://william.wow.wrtn.ai/chat/v3/{chat_box_id}/{chat_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=120
        )

        if resp.json()["result"] != "SUCCESS":
            return
        # ic('Request 2:', resp.json()["result"])
        # Requête 3
        resp = get(
            f"https://william.wow.wrtn.ai/chat/v3/{chat_box_id}/{chat_id}?model=claude2.1&platform=web&user=sgassackys@gmail.com",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=120
        )
        # ic('Request 3:')
        # Requête 4        
        resp = get(
            f"https://api.wrtn.ai/be/api/v2/chat/{chat_box_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=120
        )
        # ic('Request 4:', resp.json()["data"]["messages"][-1][0])

        result: str = resp.json()["data"]["messages"][-1][0]['content']
        return result
    except KeyError as e:
        ic(e)
        ic('The token is invalid or expired. Please provide a valid token.')
        new_token = input('Provide a valid token and press Enter to continue...\n')
        sleep(5)
        return make_requests(token, message)
    except Exception as e:
        ic(e); exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="Bearer token")
    parser.add_argument("message", help="Message content")
    args = parser.parse_args()

    asyncio.run(make_requests(args.token, args.message))
