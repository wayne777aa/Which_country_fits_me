from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於session加密

db_config = {
    'host': '127.0.0.1',
    'user': 'root', # change to your own
    'password': '', # change to your own
    'database': ''
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT country_name FROM countryinfo WHERE iseditable = 1")
        countries = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('modify_cty.html', countries=countries)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "系統錯誤，請稍後再試", 500

#刪除按鈕
@app.route('/delete-country/<string:country_name>')
def delete_country(country_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM countryinfo WHERE country_name = %s", (country_name,))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template("index.html")

#修改按鈕
@app.route('/edit-country-form/<string:country_name>')
def edit_country_form(country_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM countryinfo WHERE country_name = %s", (country_name,))
        country = cursor.fetchone()
        cursor.close()
        conn.close()

        if country:
            return render_template('display.html', country=country)
        else:
            return "找不到該國家數據", 404
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "系統錯誤，請稍後再試", 500

#國家新增提交
@app.route('/save-country', methods=['POST'])
def save_country():
    # 接收表單數據
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

    # 建立資料庫連接並插入數據
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM countryinfo WHERE country_name = %s", (country_name,))
        country = cursor.fetchone()
        
        if country:
            return render_template("error_same_country.html")
        else:
            # 插入數據到 countryinfo
            cursor.execute("""
                INSERT INTO countryinfo (
                    country_name, LandArea, PopulationDensity, ArmedForcesSize, ForestedArea_Percentage,
                    SafetySecurity, Governance, PersonelFreedom, Education, Health, CPI, iseditable
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                country_name, area, population_density, military_size, forest_percentage,
                safety_score, default_governance, civil_liberties, education_score, healthcare_score, cpi, 1  # iseditable 設為 0
            ))

        # 提交更改並關閉連接
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': 'error', 'message': 'Database operation failed'}), 500

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

    # 換成百分比數
    cursor.execute("CREATE TEMPORARY TABLE temp_percentiles AS SELECT country_name, PERCENT_RANK() OVER (ORDER BY LandArea) AS percentile FROM countryinfo")
    conn.commit()
    cursor.execute("UPDATE countryinfo ci JOIN temp_percentiles tp ON ci.country_name = tp.country_name SET ci.LandArea_perc = tp.percentile")
    conn.commit()
    cursor.execute("DROP TEMPORARY TABLE temp_percentiles")
    conn.commit()
    cursor.execute("CREATE TEMPORARY TABLE temp_percentiles AS SELECT country_name, PERCENT_RANK() OVER (ORDER BY PopulationDensity) AS percentile FROM countryinfo")
    conn.commit()
    cursor.execute("UPDATE countryinfo ci JOIN temp_percentiles tp ON ci.country_name = tp.country_name SET ci.PopulationDensity_perc = tp.percentile")
    conn.commit()
    cursor.execute("DROP TEMPORARY TABLE temp_percentiles")
    conn.commit()
    cursor.execute("CREATE TEMPORARY TABLE temp_percentiles AS SELECT country_name, PERCENT_RANK() OVER (ORDER BY ArmedForcesSize) AS percentile FROM countryinfo")
    conn.commit()
    cursor.execute("UPDATE countryinfo ci JOIN temp_percentiles tp ON ci.country_name = tp.country_name SET ci.ArmedForcesSize_perc = tp.percentile")
    conn.commit()
    cursor.execute("DROP TEMPORARY TABLE temp_percentiles")
    conn.commit()
    cursor.execute("CREATE TEMPORARY TABLE temp_percentiles AS SELECT country_name, PERCENT_RANK() OVER (ORDER BY CPI) AS percentile FROM countryinfo")
    conn.commit()
    cursor.execute("UPDATE countryinfo ci JOIN temp_percentiles tp ON ci.country_name = tp.country_name SET ci.CPI_perc = tp.percentile")
    conn.commit()
    cursor.execute("DROP TEMPORARY TABLE temp_percentiles")
    conn.commit()

    # 處理數據的邏輯
    cursor.execute("SELECT C.country_name, C.LandArea_perc * W.countrySize + C.PopulationDensity_perc * W.density + C.ArmedForcesSize_perc * W.army + (C.ForestedArea_Percentage / 100) * W.forest + (C.SafetySecurity / 100) * W.safety + (C.Governance / 100) * W.politicalRights + (C.PersonelFreedom / 100) * W.civilLiberties + (C.Education / 100) * W.education + (C.Health / 100) * W.healthcare + C.CPI_perc * W.economicStatus AS weightedScore FROM countryinfo AS C, weights AS W ORDER BY weightedScore DESC LIMIT 3")

    top_countries = []
    for results in cursor.fetchmany(3):
        top_countries.append(results[0])
        print(results)
    cursor.close()
    conn.close()

    session['top_countries'] = top_countries
    return jsonify({'status': 'success'})

#國家修改提交
@app.route('/update-country', methods=['POST'])
def update_country():
    try:
        # 接收表單數據
        country_name = request.form['country_name']
        land_area = request.form['land_area']
        population_density = request.form['population_density']
        armed_forces_size = request.form['armed_forces_size']
        forested_area_percentage = request.form['forested_area_percentage']
        safety_security = request.form['safety_security']
        governance = request.form['governance']
        personal_freedom = request.form['personal_freedom']
        education = request.form['education']
        health = request.form['health']
        cpi = request.form['cpi']

        # 更新資料庫數據
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE countryinfo
            SET LandArea = %s, PopulationDensity = %s, ArmedForcesSize = %s,
                ForestedArea_Percentage = %s, SafetySecurity = %s, Governance = %s,
                PersonelFreedom = %s, Education = %s, Health = %s, CPI = %s
            WHERE country_name = %s
        """, (land_area, population_density, armed_forces_size, forested_area_percentage,
              safety_security, governance, personal_freedom, education, health, cpi, country_name))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "系統錯誤，請稍後再試", 500

# 結果
@app.route('/result')
def result():
    top_countries = session.get('top_countries', [])
    return render_template('result.html', countries=top_countries)

if __name__ == "__main__":
    app.run(debug=True)
