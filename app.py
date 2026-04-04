from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# قائمة الفواكه المعتمدة تماماً كما في Smali
VALID_FRUITS = ["grape", "lemon", "orange", "apple", "cherry", "watermelon", "strawberry", "mango"]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # استقبال البيانات من التطبيق
        data = request.json
        fruit_occurrences = data.get('occurrences', {})
        fruit_history = data.get('history', [])
        last_round_guesses = data.get('last_round', [])

        # 1. إعطاء وزن مبدئي (1) لكل الفواكه
        prediction_weights = {fruit: 1 for fruit in VALID_FRUITS}

        # 2. استبعاد الكرز والبطيخ بشكل قاطع إذا ظهرا في الجولة السابقة (مطابق تماماً لـ Smali)
        if "cherry" in last_round_guesses and "cherry" in prediction_weights:
            del prediction_weights["cherry"]

        if "watermelon" in last_round_guesses and "watermelon" in prediction_weights:
            del prediction_weights["watermelon"]

        # 3. تطبيق خوارزمية الأوزان بناءً على التكرار
        for fruit, count in fruit_occurrences.items():
            if fruit in prediction_weights:
                if count == 2:
                    prediction_weights[fruit] = 15
                elif count >= 4:
                    prediction_weights[fruit] = 20

        # 4. التدخل الذكي (بنسبة 40% عند وجود 9 إدخالات أو أكثر في التاريخ)
        if len(fruit_history) >= 9:
            if random.randint(0, 99) < 40:
                # يختار عشوائياً بين أقدم إدخالين (Index 0 أو Index 1)
                target_index = 1 if random.choice([True, False]) else 0
                if target_index < len(fruit_history):
                    smart_fruit = fruit_history[target_index]
                    if smart_fruit in prediction_weights:
                        prediction_weights[smart_fruit] = 30

        # 5. حساب النسبة المئوية لأعلى وزن (قاعدة تقليل التخمينات الـ 65%)
        total_weight = sum(prediction_weights.values())
        max_weight = max(prediction_weights.values()) if prediction_weights else 0
        
        max_percentage = 0
        if total_weight > 0:
            max_percentage = (max_weight * 100) // total_weight

        # إذا كانت نسبة سيطرة فاكهة واحدة >= 65%، نكتفي بـ 3 تخمينات فقط لتجنب المخاطرة (كما في المتغير v9)
        target_guesses = 3 if max_percentage >= 65 else 4

        # 6. السحب العشوائي (القرعة) بناءً على الأوزان
        lottery_list = []
        for fruit, weight in prediction_weights.items():
            lottery_list.extend([fruit] * weight)

        # خلط القائمة بشكل عشوائي تماماً
        random.shuffle(lottery_list)

        # 7. استخراج الخانات للتخمين
        final_guesses = []
        for fruit in lottery_list:
            if fruit not in final_guesses:
                final_guesses.append(fruit)
            if len(final_guesses) == target_guesses:
                break

        return jsonify({
            "status": "success", 
            "guesses": final_guesses,
            "target_count": target_guesses,    # تم الإرجاع للتأكيد
            "max_percentage": max_percentage   # لمعرفة نسبة الموثوقية
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # تشغيل السيرفر
    app.run(host='0.0.0.0', port=5000)
