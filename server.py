from flask import Flask, jsonify
from flask_cors import CORS
from asyncua import Client
import asyncio

app = Flask(__name__)
CORS(app)

server_endpoint = "opc.tcp://opcuademo.sterfive.com:26543"
node_detail = "ns=1;s=SystemMemoryFree"
PORT = 6969

async def get_opc_data_async():
    async with Client(url=server_endpoint) as client:
        node = client.get_node(node_detail)  # Replace with your specific node ID
        value = await node.get_value()
        return value

@app.route('/get_opc')
def get_opc_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    value = loop.run_until_complete(get_opc_data_async())
    return jsonify({"node_value": value})

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
