'''
КОД РАБОТАЕТ ИСПРАВНО, ТОЛЬКО ВЫВОДИТ ВСЕ ДАННЫЕ ИЗ 
wss://stream.binance.com:9443/ws/{symbol}@trade В КОНСОЛЬ С УЧЕТОМ НУЖНЫХ ВАЛЮТНЫХ ПАР
'''
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
import logging
from fastapi.responses import HTMLResponse, FileResponse
import websockets
import json
from fastapi import FastAPI, WebSocket
from fastapi import Request

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

symbols = ['btcusdt', 'btcrub', 'ethusdt', 'ethrub', 'trcrub', 'trcusdt', 'ercrub', 'ercusdt']

websocket_connections = {}

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

critical_handler = logging.FileHandler('critical.log')
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(critical_handler)

error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(error_handler)

warning_handler = logging.FileHandler('warning.log')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(warning_handler)

info_handler = logging.FileHandler('info.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(info_handler)

class DebugHandler(logging.Handler):
    def emit(self, record):
        if record.levelno == logging.DEBUG:
            print("Custom Debug:", self.format(record))

debug_handler = DebugHandler()
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(debug_handler)

async def fetch_trade_data(symbol):
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
            
            if symbol in websocket_connections:
                for websocket in websocket_connections[symbol]:
                    await websocket.send_text(formattedString)

            await asyncio.sleep(5)

@app.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()

    if symbol not in websocket_connections:
        websocket_connections[symbol] = []

    websocket_connections[symbol].append(websocket)

    await fetch_trade_data(symbol)

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







