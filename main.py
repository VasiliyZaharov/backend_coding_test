# КОД РАБОТАЕТ ИСПРАВНО, ВСЕ ВЫВОДИТ В КОНСОЛЬ  
#
# import asyncio
# import ssl
# import websockets
# import json

# # Символы для валютных пар
# symbols = ['btcusdt', 'btcusd', 'ethusdt', 'ethusd', 'trcrub', 'trcusdt', 'ercrub', 'ercusdt']

# async def fetch_trade_data(symbol):
#     url = f'wss://stream.binance.com:9443/ws/{symbol}@trade'
#     async with websockets.connect(url, ssl=ssl.SSLContext()) as ws:
#         while True:
#             response = await ws.recv()
#             tradeData = json.loads(response)

#             formattedData = {
#                 "exchanger": "binance",
#                 "courses": [
#                     {
#                         "direction": symbol.upper(),
#                         "value": round(float(tradeData["p"]), 6)
#                     }
#                 ]
#             }

#             formattedString = json.dumps(formattedData, indent=2)
#             print(formattedString)

# async def main():
#     tasks = [fetch_trade_data(symbol) for symbol in symbols]
#     await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(main())
#
#------------------------------------------------------------------------------------------------
#
import asyncio
import ssl
from fastapi.responses import HTMLResponse, FileResponse
import websockets
import json
from fastapi import FastAPI, WebSocket
from fastapi import Request

app = FastAPI()

# Символы для валютных пар
symbols = ['btcusdt', 'btcrub', 'ethusdt', 'ethrub', 'trcrub', 'trcusdt', 'ercrub', 'ercusdt']

async def fetch_trade_data(symbol, websocket):
    url = f'wss://stream.binance.com:9443/ws/{symbol}@trade'
    async with websockets.connect(url, ssl=ssl.SSLContext()) as ws:
        while True:
            response = await ws.recv()
            tradeData = json.loads(response)

            formattedData = {
                "exchanger": "binance",
                "courses": [
                    {
                        "direction": symbol.upper(),
                        "value": round(float(tradeData["p"]), 6)
                    }
                ]
            }

            formattedString = json.dumps(formattedData, indent=2)
            await websocket.send_text(formattedString)

@app.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    await fetch_trade_data(symbol, websocket)

@app.get("/courses")
async def get_main_page():
    with open("main.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/courses/{symbol}", response_class=HTMLResponse)
async def get_course_page(request: Request, symbol: str):
    file_path = f"currency pair/{symbol}.html"
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




