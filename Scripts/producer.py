import hid
import asyncio
import websockets
import json
import time

# Define the vendor and product ID
VENDOR_ID = 0x04D8
PRODUCT_ID = 0x033F
REPORT_SIZE = 24  # Adjust this value based on your device's report size

async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(message)
    except Exception as e:
        print(e)
        raise('Connection got closed..trying again')
    
async def send_messages(websocket, data=None):
    try:
        if data is not None:
            await websocket.send(json.dumps(data))
    except Exception as e:          
        raise('Connection got closed..trying again')

async def print_frames(websocket,device):    
    device.open(VENDOR_ID, PRODUCT_ID)
    print(f"Connected to the device: {device}")
    # Set non-blocking mode
    device.set_nonblocking(1)
    tag_state = {}
    while True:        
        # Read data from the device
        data = device.read(REPORT_SIZE)
        if data:
            hex_data = [f"{byte:02X}" for byte in data]
            tag_id = ''.join(hex_data[10:22])
            current_time = time.time()     
            if tag_id not in tag_state.keys():
                tag_state[tag_id] = {'EPC':tag_id,'last_detection':current_time,'status':False}
                await send_messages(websocket,data={'client': 'producer', 'action': 'stream','frame': tag_state[tag_id]})
            else:
                if current_time - tag_state[tag_id]['last_detection'] < 2:                    
                    tag_state[tag_id]['last_detection'] = current_time
                else:
                    tag_state[tag_id]['status']  = not tag_state[tag_id]['status']
                    tag_state[tag_id]['last_detection'] = current_time
                    await send_messages(websocket,data={'client': 'producer', 'action': 'stream','frame': tag_state[tag_id]})
        await asyncio.sleep(1)    
        


async def main():
    device = hid.device()
    print(device)
    while True:    
        try:
            async with websockets.connect(f"ws://localhost:8000/ws/hid_detection/producer/") as websocket:                                
                await websocket.send(json.dumps({'client': 'producer','action': 'connection'}))
                await asyncio.gather(await print_frames(websocket,device),receive_messages(websocket))
        except Exception as e:
            print('here',e)
            device.close()
            await asyncio.sleep(5)                
            continue
    
    

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
