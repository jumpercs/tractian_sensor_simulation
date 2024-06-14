import random
import json
import time
import asyncio
import websockets

def simulate_vibration():
    """
    Simula a vibração da máquina de acordo com o estado:
    0: máquina desligada
    10-100: máquina funcionando
    >100: máquina com problemas
    """
    # Definindo as fases da simulação
    phases = [    # máquina desligada
        (90, 100, 15),  # máquina funcionando
        (100, 130, 10), # máquina com problemas
    ]

    while True:
        for min_val, max_val, duration in phases:
            for _ in range(duration):
                yield random.uniform(min_val, max_val)



async def send_vibration_data():
    global actualTime
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        vibration_generator = simulate_vibration()
        while True:
            # Gerar dados de vibração sintéticos
            vibration_data = {
                #timestamp + 5 minutos do anterior
                "timestamp": time.time(),
                "vibration": next(vibration_generator)
            }
            actualTime = vibration_data["timestamp"]
            await websocket.send(json.dumps(vibration_data))
            await asyncio.sleep(0.1)  # Enviar dados a cada 5 minutos

asyncio.run(send_vibration_data())
