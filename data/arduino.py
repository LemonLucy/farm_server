from flask import Flask, request, jsonify
import serial
import time

app = Flask(__name__)

# 아두이노 시리얼 포트 설정 (적합한 포트를 사용하세요)
arduino_port = 'COM3'  # Windows: COM3, Mac/Linux: /dev/ttyUSB0
baud_rate = 9600  # 아두이노의 통신 속도
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

@app.route('/robot/control', methods=['POST'])
def control_robot():
    try:
        # React Native에서 보낸 JSON 데이터를 읽음
        data = request.json
        command = data.get('command', '').strip()

        # 유효한 명령인지 확인
        if command not in ['forward', 'stop', 'backward', 'spray']:
            return jsonify({"status": "error", "message": "Invalid command"}), 400

        # 명령을 아두이노로 전송
        arduino.write(command[0].upper().encode())  # 명령의 첫 글자만 전송 ('F', 'S', 'B', 'P')
        time.sleep(0.1)  # 명령이 처리될 시간을 줌

        return jsonify({"status": "success", "message": f"Command '{command}' sent to Arduino"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
