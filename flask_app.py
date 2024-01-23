from flask import Flask
from flask import render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    job = db.Column(db.Text)
    age = db.Column(db.Integer)
    hometown = db.Column(db.Text)
    cur_city = db.Column(db.Text)
    curtown_long = db.Column(db.Text)
    languages = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    ans1 = db.Column(db.Text)
    ans2 = db.Column(db.Text)
    ans3 = db.Column(db.Text)
    ans4 = db.Column(db.Text)
    ans5 = db.Column(db.Text)
    ans6 = db.Column(db.Text)
    ans7 = db.Column(db.Text)
    ans8 = db.Column(db.Text)
    ans9 = db.Column(db.Text)
    ans10 = db.Column(db.Text)
    ans11 = db.Column(db.Text)


with app.app_context():
    db.create_all()


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')


@app.route('/process')
def process():
    if not request.args:
        return redirect(url_for('questionnaire'))
    gender = request.args.get('gender')
    job = request.args.get('profession')
    age = request.args.get('age')
    hometown = request.args.get('hometown')
    cur_city = request.args.get('currenttown')
    curtown_long = request.args.get('curtow')
    languages = request.args.get('languages')
    user = User(
        gender=gender,
        job=job,
        age=age,
        hometown=hometown,
        cur_city=cur_city,
        curtown_long=curtown_long,
        languages=languages
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    ans1 = request.args.get('cotcheese')
    ans2 = request.args.get('beet')
    ans3 = request.args.get('turnon')
    ans4 = request.args.get('disp')
    ans5 = request.args.get('blind')
    ans6 = request.args.get('sorrel')
    ans7 = request.args.get('catalogue')
    ans8 = request.args.get('graph')
    ans9 = request.args.get('obl')
    ans10 = request.args.get('shoe')
    ans11 = request.args.get('dancer')
    info = {
        'gender': gender,
        'job': job,
        'age': age,
        'hometown': hometown,
        'cur_city': cur_city,
        'curtown_long': curtown_long,
        'languages': languages,
        'ans1': ans1,
        'ans2': ans2,
        'ans3': ans3,
        'ans4': ans4,
        'ans5': ans5,
        'ans6': ans6,
        'ans7': ans7,
        'ans8': ans8,
        'ans9': ans9,
        'ans10': ans10,
        'ans11': ans11
    }
    answer = Answers(
        id=user.id,
        ans1=ans1,
        ans2=ans2,
        ans3=ans3,
        ans4=ans4,
        ans5=ans5,
        ans6=ans6,
        ans7=ans7,
        ans8=ans8,
        ans9=ans9,
        ans10=ans10,
        ans11=ans11
    )
    db.session.add(answer)
    db.session.commit()
    return render_template('process.html', info=info)


@app.route('/statistics')
def statistics():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    all_info['females'] = dict(db.session.query(
        User.gender, func.count(User.gender)).group_by(User.gender).all()
                               )['Женщина']
    all_info['males'] = dict(db.session.query(
        User.gender, func.count(User.gender)).group_by(User.gender).all()
                             )['Мужчина']
    all_info['jobs'] = dict(db.session.query(
        User.job, func.count(User.job)).group_by(User.job).all())
    if None in all_info['jobs'].keys():
        del all_info['jobs'][None]
    all_info['hometowns'] = dict(db.session.query(
        User.hometown, func.count(User.hometown)).group_by(User.hometown).all())
    if None in all_info['hometowns'].keys():
        del all_info['hometowns'][None]
    all_info['curcity'] = dict(db.session.query(
        User.cur_city, func.count(User.cur_city)
    ).group_by(User.cur_city).all())
    if None in all_info['curcity'].keys():
        del all_info['curcity'][None]
    all_info['ages'] = dict(db.session.query(
        User.age, func.count(User.age)
    ).group_by(User.age).all())
    if None in all_info['ages'].keys():
        del all_info['ages'][None]
    all_languages = db.session.query(User.languages).all()
    all_langs = {}
    for lang in all_languages:
        lang = str(lang)
        lang = lang.replace('(', '')
        lang = lang.replace(')', '')
        lang = lang.replace(' ', '')
        lang = lang.replace("'", '')
        lang = lang[:-1]
        lang = lang.lower()
        lang = lang.split(',')
        for la in lang:
            if la not in all_langs:
                all_langs[la] = 1
            else:
                all_langs[la] += 1
    all_info['languages'] = all_langs
    if None in all_info['languages'].keys():
        del all_info['languages'][None]
    all_info['Творог'] = dict(
        db.session.query(Answers.ans1, func.count(Answers.ans1)).group_by(Answers.ans1).all())
    if None in all_info['Творог'].keys():
        del all_info['Творог'][None]
    if 'твОрог' not in all_info['Творог'].keys():
        all_info['Творог']['твОрог'] = 0
    if 'творОг' not in all_info['Творог'].keys():
        all_info['Творог']['творОг'] = 0
    all_info['Свекла'] = dict(
        db.session.query(Answers.ans2, func.count(Answers.ans2)).group_by(Answers.ans2).all())
    if None in all_info['Свекла'].keys():
        del all_info['Свекла'][None]
    if 'свЕкла' not in all_info['Свекла'].keys():
        all_info['Свекла']['свЕкла'] = 0
    if 'свеклА' not in all_info['Свекла'].keys():
        all_info['Свекла']['свеклА'] = 0
    all_info['Включит'] = dict(
        db.session.query(Answers.ans3, func.count(Answers.ans3)).group_by(Answers.ans3).all())
    if None in all_info['Включит'].keys():
        del all_info['Включит'][None]
    if 'вклЮчит' not in all_info['Включит'].keys():
        all_info['Включит']['вклЮчит'] = 0
    if 'включИт' not in all_info['Включит'].keys():
        all_info['Включит']['включИт'] = 0
    all_info['Диспансер'] = dict(
        db.session.query(Answers.ans4, func.count(Answers.ans4)).group_by(Answers.ans4).all())
    if None in all_info['Диспансер'].keys():
        del all_info['Диспансер'][None]
    if 'диспАнсер' not in all_info['Диспансер'].keys():
        all_info['Диспансер']['диспАнсер'] = 0
    if 'диспансЕр' not in all_info['Диспансер'].keys():
        all_info['Диспансер']['диспансЕр'] = 0
    all_info['Жалюзи'] = dict(
        db.session.query(Answers.ans5, func.count(Answers.ans5)).group_by(Answers.ans5).all())
    if None in all_info['Жалюзи'].keys():
        del all_info['Жалюзи'][None]
    if 'жАлюзи' not in all_info['Жалюзи'].keys():
        all_info['Жалюзи']['жАлюзи'] = 0
    if 'жалюзИ' not in all_info['Жалюзи'].keys():
        all_info['Жалюзи']['жалюзИ'] = 0
    all_info['Щавель'] = dict(
        db.session.query(Answers.ans6, func.count(Answers.ans6)).group_by(Answers.ans6).all())
    if None in all_info['Щавель'].keys():
        del all_info['Щавель'][None]
    if 'щАвель' not in all_info['Щавель'].keys():
        all_info['Щавель']['щАвель'] = 0
    if 'щавЕль' not in all_info['Щавель'].keys():
        all_info['Щавель']['щавЕль'] = 0
    all_info['Каталог'] = dict(
        db.session.query(Answers.ans7, func.count(Answers.ans7)).group_by(Answers.ans7).all())
    if None in all_info['Каталог'].keys():
        del all_info['Каталог'][None]
    if 'катАлог' not in all_info['Каталог'].keys():
        all_info['Каталог']['катАлог'] = 0
    if 'каталОг' not in all_info['Каталог'].keys():
        all_info['Каталог']['каталОг'] = 0
    all_info['Граффити'] = dict(
        db.session.query(Answers.ans8, func.count(Answers.ans8)).group_by(Answers.ans8).all())
    if None in all_info['Граффити'].keys():
        del all_info['Граффити'][None]
    if 'грАффити' not in all_info['Граффити'].keys():
        all_info['Граффити']['грАффити'] = 0
    if 'граффИти' not in all_info['Граффити'].keys():
        all_info['Граффити']['граффИти'] = 0
    all_info['Облегчить'] = dict(
        db.session.query(Answers.ans9, func.count(Answers.ans9)).group_by(Answers.ans9).all())
    if None in all_info['Облегчить'].keys():
        del all_info['Облегчить'][None]
    if 'облЕгчить' not in all_info['Облегчить'].keys():
        all_info['Облегчить']['облЕгчить'] = 0
    if 'облегчИть' not in all_info['Облегчить'].keys():
        all_info['Облегчить']['облегчИть'] = 0
    all_info['Туфля'] = dict(
        db.session.query(Answers.ans10, func.count(Answers.ans10)).group_by(Answers.ans10).all())
    if None in all_info['Туфля'].keys():
        del all_info['Туфля'][None]
    if 'тУфля' not in all_info['Туфля'].keys():
        all_info['Туфля']['тУфля'] = 0
    if 'туфлЯ' not in all_info['Туфля'].keys():
        all_info['Туфля']['туфлЯ'] = 0
    all_info['Танцовщица'] = dict(
        db.session.query(Answers.ans11, func.count(Answers.ans11)).group_by(Answers.ans11).all())
    if None in all_info['Танцовщица'].keys():
        del all_info['Танцовщица'][None]
    if 'танцОвщица' not in all_info['Танцовщица'].keys():
        all_info['Танцовщица']['танцОвщица'] = 0
    if 'танцовщИца' not in all_info['Танцовщица'].keys():
        all_info['Танцовщица']['танцовщИца'] = 0

    labels = ['Женщины', 'Мужчины']
    counts = [all_info['females'], all_info['males']]
    fig, ax = plt.subplots()
    ax.set_title('Распределение женщин и мужчин, прошедших опрос')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/genders.png')
    plt.clf()
    plt.close()

    jobs = all_info['jobs'].keys()
    numbers = all_info['jobs'].values()
    plt.bar(jobs, numbers, color='#FF7F50')
    plt.xlabel('Профессия')
    plt.ylabel('Количество человек')
    plt.title('Распределение опрошенных по профессиям')
    plt.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/jobs.png')
    plt.clf()
    plt.close()

    ages = all_info['ages'].keys()
    nums = all_info['ages'].values()
    plt.bar(ages, nums, color='#FF7F50')
    plt.xlabel('Возраст')
    plt.ylabel('Количество человек')
    plt.title('Распределение опрошенных по возрасту')
    plt.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/ages.png')
    plt.clf()
    plt.close()

    langs = all_info['languages'].keys()
    numbs = all_info['languages'].values()
    plt.bar(langs, numbs, color='#DE3163')
    plt.xlabel('Язык')
    plt.ylabel('Количество человек')
    plt.title('Распределение опрошенных по знанию языков')
    plt.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/languages.png')
    plt.clf()
    plt.close()

    hometowns = all_info['hometowns'].keys()
    nus = all_info['hometowns'].values()
    plt.bar(hometowns, nus, color='#FF7F50')
    plt.xlabel('Родной город')
    plt.ylabel('Количество человек из города')
    plt.title('Распределение опрошенных по родным городам')
    plt.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/hometowns.png')
    plt.clf()
    plt.close()

    curcity = all_info['curcity'].keys()
    nu = all_info['curcity'].values()
    plt.bar(curcity, nu, color='#DE3163')
    plt.xlabel('Город')
    plt.ylabel('Количество человек из города')
    plt.title('Распределение опрошенных по городам')
    plt.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/curcity.png')
    plt.clf()
    plt.close()

    labels = ['твОрог', 'творОг']
    counts = [all_info['Творог']['твОрог'], all_info['Творог']['творОг']]
    fig, ax = plt.subplots()
    ax.set_title('Слово творог')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/cotcheese.png')
    plt.clf()
    plt.close()

    labels = ['свЕкла', 'свеклА']
    counts = [all_info['Свекла']['свЕкла'], all_info['Свекла']['свеклА']]
    fig, ax = plt.subplots()
    ax.set_title('Слово свекла')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/beet.png')
    plt.clf()
    plt.close()

    labels = ['вклЮчит', 'включИт']
    counts = [all_info['Включит']['вклЮчит'], all_info['Включит']['включИт']]
    fig, ax = plt.subplots()
    ax.set_title('Слово включит')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/turnon.png')
    plt.clf()
    plt.close()

    labels = ['диспАнсер', 'диспансЕр']
    counts = [all_info['Диспансер']['диспАнсер'], all_info['Диспансер']['диспансЕр']]
    fig, ax = plt.subplots()
    ax.set_title('Слово диспансер')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/disp.png')
    plt.clf()
    plt.close()

    labels = ['жАлюзи', 'жалюзИ']
    counts = [all_info['Жалюзи']['жАлюзи'], all_info['Жалюзи']['жалюзИ']]
    fig, ax = plt.subplots()
    ax.set_title('Слово жалюзи')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/blind.png')
    plt.clf()
    plt.close()

    labels = ['щАвель', 'щавЕль']
    counts = [all_info['Щавель']['щАвель'], all_info['Щавель']['щавЕль']]
    fig, ax = plt.subplots()
    ax.set_title('Слово щавель')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/sorrel.png')
    plt.clf()
    plt.close()

    labels = ['катАлог', 'каталОг']
    counts = [all_info['Каталог']['катАлог'], all_info['Каталог']['каталОг']]
    fig, ax = plt.subplots()
    ax.set_title('Слово каталог')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/catalogue.png')
    plt.clf()
    plt.close()

    labels = ['грАффити', 'граффИти']
    counts = [all_info['Граффити']['грАффити'], all_info['Граффити']['граффИти']]
    fig, ax = plt.subplots()
    ax.set_title('Слово граффити')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/graph.png')
    plt.clf()
    plt.close()

    labels = ['облЕгчить', 'облегчИть']
    counts = [all_info['Облегчить']['облЕгчить'], all_info['Облегчить']['облегчИть']]
    fig, ax = plt.subplots()
    ax.set_title('Слово облегчить')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/obl.png')
    plt.clf()
    plt.close()

    labels = ['тУфля', 'туфлЯ']
    counts = [all_info['Туфля']['тУфля'], all_info['Туфля']['туфлЯ']]
    fig, ax = plt.subplots()
    ax.set_title('Слово туфля')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/shoe.png')
    plt.clf()
    plt.close()

    labels = ['танцОвщица', 'танцовщИца']
    counts = [all_info['Танцовщица']['танцОвщица'], all_info['Танцовщица']['танцовщИца']]
    fig, ax = plt.subplots()
    ax.set_title('Слово танцовщица')
    ax.pie(counts, labels=labels, autopct='%.0f%%', colors=['#DE3163', '#FF7F50'])
    fig.savefig('C:/Users/gigab/PycharmProjects/flask/static/images/dancer.png')
    plt.clf()
    plt.close()
    return render_template('statistics.html', all_info=all_info)


if __name__ == '__main__':
    app.run()
