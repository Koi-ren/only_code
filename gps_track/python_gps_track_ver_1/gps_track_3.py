from flask import Flask, render_template, jsonify
import serial
import time

app = Flask(__name__)

# Serial 통신 설정
serial_port = 'COM6'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/coordinates')
def get_coordinates():
    coordinates = []
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("Lat:"):
            try:
                latitude = float(line.split()[1]) / 10000000.0
                longitude = float(line.split()[3]) / 10000000.0
                altitude = float(line.split()[5])
                coordinates.append({'latitude': latitude, 'longitude': longitude, 'altitude': altitude})
            except ValueError:
                print("Invalid data format:", line)
        if len(coordinates) >= 2:
            break
    return jsonify({'coordinates': coordinates})

if __name__ == '__main__':
    app.run(debug=True)
