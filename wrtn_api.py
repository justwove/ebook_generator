import argparse
import httpx
import asyncio

async def make_requests(token, message) -> str:
    chat_box_id: str = '665a22664d405cf4ad5da5d4'
    # Requête 1
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://william.wow.wrtn.ai/chat/v3/{chat_box_id}/start?platform=web&user=sgassackys@gmail.com&model=claude2.1",
            json={"message": message, "reroll": False, "images": []},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json" 
            }
        )
        chat_id = resp.json()["data"]

    # Requête 2
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"https://william.wow.wrtn.ai/chat/v3/{chat_box_id}/{chat_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=120
        )

    if resp.json()["result"] != "SUCCESS":
        return

    # Requête 3
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://william.wow.wrtn.ai/chat/v3/{chat_box_id}/{chat_id}?model=claude2.1&platform=web&user=sgassackys@gmail.com",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=120
        )

    # Requête 4        
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.wrtn.ai/be/api/v2/chat/{chat_box_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=120
        )

    result: str = resp.json()["data"]["messages"][-1][0]['content']
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="Bearer token")
    parser.add_argument("message", help="Message content")
    args = parser.parse_args()

    asyncio.run(make_requests(args.token, args.message))
