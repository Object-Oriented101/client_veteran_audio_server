import torch
from fastapi import FastAPI, WebSocket
import uvicorn
from models import WhisperModel

app = FastAPI()

# Instantiate the model
model = WhisperModel()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive audio data from client
            audio_data = await websocket.receive_bytes()

            # Transcribe and send the result back
            text = model.transcribe(audio_data, use_fp16=torch.cuda.is_available())
            await websocket.send_text(text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8888)