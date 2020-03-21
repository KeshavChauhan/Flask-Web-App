from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# engine = create_engine("postgres://my_username:my_password@localhost:5432/lecture3")
engine = create_engine('mysql+mysqlconnector://sqlalchemy:root@localhost:3306/actors_db')
db = scoped_session(sessionmaker(bind=engine))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def insert():
    name = request.form.get("name")
    groupType = request.form.get("groupType")

    results = db.execute("SELECT id, name, groupType FROM actors_db.groups where name = :name AND groupType = "
                          ":groupType", {"name": name, "groupType": groupType}).fetchall()

    if not results:
        # INSERT QUERY
        db.execute("INSERT INTO actors_db.groups (name, groupType) VALUES (:name, :groupType)", {"name": name, "groupType": groupType})
        db.commit()

        # Results for the given query.
        results = db.execute("SELECT id, name, groupType FROM actors_db.groups where name = :name AND groupType = "
                             ":groupType", {"name": name, "groupType": groupType}).fetchall()
        return render_template("insert_results.html", results=results)
    else:
        # Show results for existing user.
        results = db.execute("SELECT id, name, groupType FROM actors_db.groups where name = :name AND groupType = "
                             ":groupType", {"name": name, "groupType": groupType}).fetchall()
        return render_template("read_results.html", results=results)


if __name__ == "__main__":
    app.run()
