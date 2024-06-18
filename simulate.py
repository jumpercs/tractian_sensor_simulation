import math
import random
import asyncio
import websockets
import json
import time

def simulate_vibration():
    """
    Simula a vibração da máquina em três eixos (X, Y, Z) com uma abordagem combinada.
    Inclui transições suaves, ruído aleatório, eventos esporádicos e padrões cíclicos.
    """
    base_vibration = 50
    t = 0
    event_probability = 0.05  # Probabilidade de evento a cada passo
    event_duration = 0  # Duração do evento atual
    current_event = None

    while True:
        vibrations = {"x": base_vibration, "y": base_vibration, "z": base_vibration}
        
        for axis in vibrations:
            # Estado base de operação
            vibrations[axis] += 20
            noise = random.uniform(-5, 5)  # Ruído aleatório
            vibrations[axis] += noise

        # Simulação de eventos esporádicos
        if event_duration > 0:
            for axis in vibrations:
                if current_event == 'shock':
                    vibrations[axis] += random.uniform(30, 50)
                elif current_event == 'malfunction':
                    vibrations[axis] += random.uniform(60, 100)
            event_duration -= 1
        elif random.random() < event_probability:
            current_event = random.choice(['shock', 'malfunction'])
            event_duration = random.randint(5, 30)  # Duração do evento em passos de tempo
            for axis in vibrations:
                if current_event == 'shock':
                    vibrations[axis] += random.uniform(30, 50)
                elif current_event == 'malfunction':
                    vibrations[axis] += random.uniform(60, 100)

        yield {axis: max(0, vibrations[axis]) for axis in vibrations}
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
