import asyncio
import websockets
import json
import httpx

async def handler(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            print(f"Received data: {data}")
            store_data(data)
            # Check each vibration component individually
            vibration = data["vibration"]
            if vibration["x"] > 100 or vibration["y"] > 100 or vibration["z"] > 100:
                print("Alert: High vibration detected!")
                await send_notification()
        except json.JSONDecodeError:
            print("Received invalid JSON")
        except Exception as e:
            print(f"An error occurred: {e}")

async def send_notification():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:5000/send-notification",
            json={
                "device_token": "efZ9LlpuRHKM1gH0saKnSZ:APA91bH0NvuHAiLLhGkeD5PR_1wJ4mENU26jC3zsVTfr6sRQ3k5LcSRt1ZH8uBDURYFpGMe7XjuhoB8WHy1Hf4QkasLgegjUGL_AFbXpQWDj-Gs3RY92FbjL8qdtio3x11J3a07VHLGx",
                "title": "High vibration detected",
                "message": "High vibration detected in the machine"
            }
        )
        print(f"Notification response: {response.status_code}")

def store_data(data):
    try:
        print(f"Storing data: {data}")
        with open("data.json", "a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"An error occurred while storing data: {e}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())
