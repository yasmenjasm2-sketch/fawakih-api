import os
import signal
# لا تنسَ إضافة هذه المكتبات في أعلى الملف بجانب مكتباتك الحالية

@app.route('/shutdown', methods=['POST', 'GET'])
def shutdown():
    try:
        # إرسال إشارة لإنهاء عملية السيرفر (PID)
        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({"status": "success", "message": "تم إرسال أمر إيقاف السيرفر بنجاح"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
