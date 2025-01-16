import serial
import os

def save_image(data, file_path):
    with open(file_path, 'wb') as f:
        f.write(data)
    print(f"Image saved as {file_path}")

def listen_to_serial(port, baudrate, output_dir):
    image_count = 1
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Listening to {port} at {baudrate} baud...")

        image_data = bytearray()
        capturing = False
        while True:
            line = ser.readline()
            if b"STARTIMAGE" in line:
                print("Start of image detected")
                capturing = True
                image_data = bytearray()
            elif b"ENDIMAGE" in line:
                print("End of image detected")
                capturing = False
                file_path = os.path.join(output_dir, f"image_{image_count}.jpg")
                save_image(image_data, file_path)
                image_count += 1
            elif capturing:
                image_data.extend(line)

    except serial.SerialException as e:
        print(f"Serial exception: {e}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    serial_port = "/dev/tty.usbmodem101"
    baud_rate = 115200
    output_directory = "./data/two"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    listen_to_serial(serial_port, baud_rate, output_directory)
