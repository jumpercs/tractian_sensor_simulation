import math
import random
import asyncio
import websockets
import json
import time

def simulate_vibration():
    """
    Simula a vibração da máquina com uma abordagem combinada.
    Inclui transições suaves, ruído aleatório, eventos esporádicos e padrões cíclicos.
    """
    base_vibration = 50
    t = 0
    event_probability = 0.01  # Probabilidade de evento a cada passo

    while True:
        # Estado base de operação
        vibration = base_vibration + 20 * math.sin(0.05 * t)  # Oscilação cíclica
        noise = random.uniform(-5, 5)  # Ruído aleatório

        # Simulação de eventos esporádicos
        if random.random() < event_probability:
            event_type = random.choice(['shock', 'malfunction'])
            if event_type == 'shock':
                vibration += random.uniform(30, 50)
            elif event_type == 'malfunction':
                vibration += random.uniform(60, 100)

        # Adiciona ruído aleatório
        vibration += noise

        yield max(0, vibration)
        t += 1

async def send_vibration_data():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        vibration_generator = simulate_vibration()
        while True:
            try:
                vibration_data = {
                    "timestamp": time.time(),
                    "vibration": next(vibration_generator)
                }
                await websocket.send(json.dumps(vibration_data))
                await asyncio.sleep(1)  # Enviar dados a cada 1 segundo
            except websockets.ConnectionClosed:
                print("Connection closed, retrying...")
                await asyncio.sleep(1)
                await send_vibration_data()
            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(send_vibration_data())
