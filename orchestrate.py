import uvicorn
from fastapi import FastAPI, WebSocket
import websockets
import asyncio

app = FastAPI()

WHISPER_SERVER_WS_URL = "ws://0.0.0.0:8000/ws"

@app.websocket("/ws")
async def websocket_endpoint_client(websocket: WebSocket):
    await websocket.accept()
    whisper_websocket = await websockets.connect(WHISPER_SERVER_WS_URL)
    try:
        while True:
            # Receive audio data from the client
            audio_data = await websocket.receive_bytes()

            # Send audio data to the Whisper server
            await whisper_websocket.send(audio_data)

            # Receive transcription from the Whisper server
            text = await whisper_websocket.recv()

            # Send transcription back to the client
            await websocket.send_text(text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure the Whisper server connection is closed when done
        await whisper_websocket.close()
        await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8888)  # Adjust port as necessary
