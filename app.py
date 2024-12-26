from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於session加密

db_config = {
    'host': 'localhost',
    'user': 'root', # change to your own
    'password': 'localhost', # change to your own
    'database': 'countries'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

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
    forest_percentage = request.form['forest_percentage']
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
        "forest_percentage": forest_percentage,
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

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE weights")
    conn.commit()
    cursor.execute("INSERT INTO weights (countrySize, density, army, forest, safety, politicalRights, civilLiberties, education, healthcare, economicStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (data["countrySize"], data["density"], data["army"], data["forest"], data["safety"], data["politicalRights"], data["civilLiberties"], data["education"], data["healthcare"], data["economicStatus"]))
    conn.commit()

    # 處理數據的邏輯
    cursor.execute("SELECT C.country_name, (C.LandArea / 1454000) * W.countrySize + (C.PopulationDensity / 26337) * W.density + (C.ArmedForcesSize / 1359000) * W.army + (C.ForestedArea_Percentage) * W.forest + (C.SafetySecurity / 100) * W.safety + (C.Governance / 100) * W.politicalRights + (C.PersonelFreedom / 100) * W.civilLiberties + (C.Education) * W.education + (C.Health / 100) * W.healthcare + (C.CPI / 4583.71) * W.economicStatus AS weightedScore FROM countryinfo AS C, weights AS W ORDER BY weightedScore DESC LIMIT 3")
    
    top_countries = []
    for results in cursor.fetchmany(3):
        top_countries.append(results[0])
        print(results)
    cursor.close()
    conn.close()

    session['top_countries'] = top_countries
    return jsonify({'status': 'success'})

# 結果
@app.route('/result')
def result():
    top_countries = session.get('top_countries', [])
    return render_template('result.html', countries=top_countries)

if __name__ == "__main__":
    app.run(debug=True)