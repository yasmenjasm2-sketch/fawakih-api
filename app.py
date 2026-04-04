from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# قائمة الفواكه المعتمدة
VALID_FRUITS = ["grape", "lemon", "orange", "apple", "cherry", "watermelon", "strawberry", "mango"]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # استقبال البيانات من التطبيق
        data = request.json
        fruit_occurrences = data.get('occurrences', {})
        fruit_history = data.get('history', [])
        last_round_guesses = data.get('last_round', [])

        # إعطاء وزن مبدئي (1) لكل الفواكه
        prediction_weights = {fruit: 1 for fruit in VALID_FRUITS}

        # 1. استبعاد الكرز والبطيخ بنسبة 50% بناءً على الجولة السابقة
        if "cherry" in last_round_guesses:
            is_ai_confident = fruit_occurrences.get("cherry", 0) >= 2
            if not is_ai_confident and random.randint(0, 99) < 50:
                prediction_weights.pop("cherry", None)

        if "watermelon" in last_round_guesses:
            is_ai_confident = fruit_occurrences.get("watermelon", 0) >= 2
            if not is_ai_confident and random.randint(0, 99) < 50:
                prediction_weights.pop("watermelon", None)

        # 2. تطبيق خوارزمية الذكاء الاصطناعي (الأوزان)
        for fruit, count in fruit_occurrences.items():
            if fruit in prediction_weights:
                if count == 2:
                    prediction_weights[fruit] = 15
                elif count >= 4:
                    prediction_weights[fruit] = 20

        # 3. التدخل الذكي (بنسبة 40% عند تجاوز 9 إدخالات)
        if len(fruit_history) >= 9:
            if random.randint(0, 99) < 40:
                target_index = 1 if random.choice([True, False]) else 2
                if target_index < len(fruit_history):
                    smart_fruit = fruit_history[target_index]
                    if smart_fruit in prediction_weights:
                        prediction_weights[smart_fruit] = 30

        # 4. السحب العشوائي (القرعة) بناءً على الأوزان
        lottery_list = []
        for fruit, weight in prediction_weights.items():
            lottery_list.extend([fruit] * weight)

        random.shuffle(lottery_list)

        # استخراج 4 خانات للتخمين
        final_guesses = []
        for fruit in lottery_list:
            if fruit not in final_guesses:
                final_guesses.append(fruit)
            if len(final_guesses) == 4:
                break

        return jsonify({"status": "success", "guesses": final_guesses})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
