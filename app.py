from flask import Flask, request, jsonify

app = Flask(__name__)

# هذا السطر مهم جداً لمنع تشفير الحروف العربية ولإرسالها كنصوص طبيعية
app.config['JSON_AS_ASCII'] = False

messages = []

@app.route("/")
def home():
    return "Server is running 🔥"

@app.route("/send", methods=["POST"])
def send():
    # استخدام force=True يضمن قراءة الـ JSON القادم من الأندرويد مهما كانت الترويسة
    data = request.get_json(force=True)
    
    # حماية السيرفر من التوقف إذا كان الطلب فارغاً
    if not data or "msg" not in data:
        return jsonify({"error": "No message provided"}), 400
        
    messages.append(data["msg"])
    return jsonify({"status": "sent"})

@app.route("/messages")
def get_messages():
    # إرجاع المصفوفة كـ JSON نظامي
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
