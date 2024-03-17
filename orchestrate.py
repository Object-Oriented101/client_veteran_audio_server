import uvicorn
from fastapi import FastAPI, WebSocket
import websockets
import asyncio

app = FastAPI()

WHISPER_SERVER_WS_URL = "ws://localhost:8888/ws"

@app.websocket("/client_ws")
async def websocket_endpoint_client(websocket: WebSocket):
    await websocket.accept()
    async with websockets.connect(WHISPER_SERVER_WS_URL) as whisper_websocket:
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
            await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Adjust port as necessary
