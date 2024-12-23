from flask import Flask, render_template, request, redirect, url_for, jsonify, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于session加密

#測試資料
countries = [
    {
        "id": 1,
        "name": "Country1",
        "area": 100000,
        "population_density": 100,
        "military_size": 5000,
        "alcohol_consumption": 5.0,
        "safety_score": 80,
        "political_rights": 70,
        "civil_liberties": 75,
        "education_score": 85,
        "healthcare_score": 90,
        "cpi": 1000,
    },
    {
        "id": 2,
        "name": "Country2",
        "area": 500000,
        "population_density": 50,
        "military_size": 10000,
        "alcohol_consumption": 2.5,
        "safety_score": 90,
        "political_rights": 80,
        "civil_liberties": 85,
        "education_score": 88,
        "healthcare_score": 92,
        "cpi": 1200,
    },
]

# 首頁
@app.route("/")
def index():
    return render_template("index.html")

# 開始問題
@app.route("/start")
def question():
    return render_template("question.html")

# 新增國家
@app.route('/add-country')
def add_country():
    return render_template('create_cty.html')
# 修改國家
@app.route('/edit-country')
def edit_country():
    return render_template('modify_cty.html')

# 國家修改提交
@app.route('/save-country', methods=['POST'])
def save_country():
    country_name = request.form['country_name']
    area = request.form['area']
    population_density = request.form['population_density']
    military_size = request.form['military_size']
    alcohol_consumption = request.form['alcohol_consumption']
    safety_score = request.form['safety_score']
    political_rights = request.form['political_rights']
    civil_liberties = request.form['civil_liberties']
    education_score = request.form['education_score']
    healthcare_score = request.form['healthcare_score']
    cpi = request.form['cpi']

    # 儲存新國家資料邏輯（可以存到資料庫或列表）
    new_country = {
        "id": len(countries) + 1,  # 根據需求設定 id，這裡假設是自動增長
        "name": country_name,
        "area": area,
        "population_density": population_density,
        "military_size": military_size,
        "alcohol_consumption": alcohol_consumption,
        "safety_score": safety_score,
        "political_rights": political_rights,
        "civil_liberties": civil_liberties,
        "education_score": education_score,
        "healthcare_score": healthcare_score,
        "cpi": cpi,
    }

    countries.append(new_country)  # 把新國家加入到 countries 列表中

    # 可選：重定向到首頁或其他頁面
    return redirect(url_for('index'))


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    print(data)  # 用來檢查接收到的資料
    # 處理數據的邏輯
    top_countries = ['國家1', '國家2', '國家3']
    session['top_countries'] = top_countries
    return jsonify({'status': 'success'})

# 結果
@app.route('/result')
def result():
    top_countries = session.get('top_countries', [])
    return render_template('result.html', countries=top_countries)

if __name__ == "__main__":
    app.run(debug=True)
