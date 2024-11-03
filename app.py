from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# グローバル変数
current_problem = ""
current_answer = 0  # ユーザー用の正解の答えを保持する変数
cpu_problem = ""    # CPU用の問題
cpu_answer = 0      # CPU用の正解
cpu_last_answer = 0 # CPUが最後に解答した答え
correct_answers = 0
cpu_correct_answers = 0  # CPUの正解数を保持する変数
end_time = 0  # タイマーの終了時間

def generate_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return f"{num1} + {num2}", num1 + num2  # 問題のテキストと正解を返す

@app.route('/', methods=['GET', 'POST'])
def home():
    global current_problem, current_answer, cpu_problem, cpu_answer, cpu_last_answer
    global correct_answers, cpu_correct_answers, end_time

    if request.method == 'POST':
        if 'reset' in request.form:  # リセットボタンが押された場合
            correct_answers = 0
            cpu_correct_answers = 0  # CPUの正解数もリセット
            current_problem, current_answer = generate_problem()  # ユーザー用の新しい問題と正解を取得
            cpu_problem, cpu_answer = generate_problem()  # CPU用の新しい問題と正解を取得
            end_time = time.time() + 10  # 10秒のタイマーをリセット
        else:
            answer = request.form['answer']

            # ユーザーの正解チェック
            if answer.isdigit() and int(answer) == current_answer:
                correct_answers += 1

            # 新しい問題を生成
            current_problem, current_answer = generate_problem()

        return render_template('index.html', problem=current_problem, user_result=correct_answers, cpu_problem=cpu_problem, cpu_result=cpu_correct_answers, end_time=end_time, cpu_last_answer=cpu_last_answer)

    # 初回アクセス時の問題生成
    current_problem, current_answer = generate_problem()  # ユーザー用の新しい問題と正解を取得
    cpu_problem, cpu_answer = generate_problem()  # CPU用の新しい問題と正解を取得
    end_time = time.time() + 10  # 最初のタイマー設定
    return render_template('index.html', problem=current_problem, user_result=correct_answers, cpu_problem=cpu_problem, cpu_result=cpu_correct_answers, end_time=end_time, cpu_last_answer=cpu_last_answer)

@app.route('/cpu_calculation', methods=['GET'])
def cpu_calculation():
    global cpu_problem, cpu_answer, cpu_correct_answers, cpu_last_answer, end_time
    remaining_time = end_time - time.time()

    # タイマーが切れている場合はCPUの計算を停止
    if remaining_time <= 0:
        return jsonify({'cpu_problem': cpu_problem, 'cpu_result': cpu_correct_answers, 'cpu_last_answer': cpu_last_answer, 'cpu_active': False})

    # CPUが80％の確率で正解する
    if random.random() < 0.8:
        cpu_correct_answers += 1
        cpu_last_answer = cpu_answer  # CPUが正解した場合の答えを保存

    # 新しい問題を生成
    cpu_problem, cpu_answer = generate_problem()
    return jsonify({'cpu_problem': cpu_problem, 'cpu_result': cpu_correct_answers, 'cpu_last_answer': cpu_last_answer, 'cpu_active': True})

@app.route('/timer', methods=['GET'])
def timer():
    global end_time
    remaining_time = max(0, end_time - time.time())
    return jsonify({'remaining_time': remaining_time})

if __name__ == "__main__":
    app.run(debug=True)