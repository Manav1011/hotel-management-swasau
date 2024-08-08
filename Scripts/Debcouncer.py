import hid
import time

    
VENDOR_ID = 0x04D8
PRODUCT_ID = 0x033F
REPORT_SIZE = 24  # Adjust this value based on your device's report size
device = hid.device()
tag_state = {}
device.open(VENDOR_ID, PRODUCT_ID)
print(f"Connected to the device: {device}")
device.set_nonblocking(1)

while True:
        # Read data from the device
        data = device.read(REPORT_SIZE)
        if data:
            hex_data = [f"{byte:02X}" for byte in data]
            tag_id = ''.join(hex_data[10:22])
            current_time = time.time()
            if tag_id not in tag_state.keys():
                tag_state[tag_id] = {'last_detection':current_time,'status':False}
                print(tag_state[tag_id])
            else:
                if current_time - tag_state[tag_id]['last_detection'] < 2:
                    print("Debouncing period still now crossed No sending")
                    tag_state[tag_id]['last_detection'] = current_time
                else:
                    tag_state[tag_id]['status']  = not tag_state[tag_id]['status']
                    tag_state[tag_id]['last_detection'] = current_time
                    print(tag_state[tag_id])
                     

            