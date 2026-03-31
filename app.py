from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ReverseMollusk@2",
        database="sanctuary_db"
    )
    return connection


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/animals')
def animal_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Select without join for Animal
    query = """
            SELECT a.name, a.age, a.sex, a.health_status a.date_acquired, s.common_name, e.name AS exhibit_name
            FROM Animal a
                     LEFT JOIN species s on a.species_id = s.species_id
                     LEFT JOIN exhibit e on a.exhibit_id = e.exhibit_id \
            """

    cursor.execute(query)
    list_animals = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("animal.html", animals=list_animals)


@app.route('/exhibits')
def exhibit_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Select without join for Exhibit
    query = "SELECT name, type, capacity FROM Exhibit"

    cursor.execute(query)
    list_exhibits = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("exhibit.html", exhibits=list_exhibits)


@app.route('/species')
def species_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Select without join for Species
    query = "SELECT common_name, scientific_name, diet_type FROM Species"

    cursor.execute(query)
    list_species = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("species.html", species=list_species)


@app.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    date = datetime.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        health = request.form.get('health')
        species_id = request.form.get('species_id')
        exhibit_id = request.form.get('exhibit_id')
        keeper_id = request.form.get('keeper_id')

        # Try except loop for input validation
        try:
            # Validating that the species is allowed in the selected exhibit
            cursor.execute("""
                           SELECT exhibit_id
                           FROM exhibit
                           WHERE exhibit_id = %s
                             AND species_id = %s
                           """, (exhibit_id, species_id))
            valid = cursor.fetchone()

            if not valid:
                raise ValueError("Exhibit does not match selected species.")

            # Check capacity
            cursor.execute("""
                           SELECT e.capacity, COUNT(a.animal_id) AS current_count
                           FROM exhibit e
                                    LEFT JOIN animal a ON a.exhibit_id = e.exhibit_id
                           WHERE e.exhibit_id = %s
                           GROUP BY e.exhibit_id
                           """, (exhibit_id,))
            exhibit = cursor.fetchone()

            # If exhibit exists and current count exceeds exhibits capacity
            if exhibit and exhibit['current_count'] >= exhibit['capacity']:
                cursor.execute("SELECT species_id, common_name FROM species")
                list_species = cursor.fetchall()
                cursor.execute("SELECT exhibit_id, name, capacity FROM exhibit")
                list_exhibits = cursor.fetchall()
                cursor.execute("SELECT keeper_id, name FROM keeper")
                list_keepers = cursor.fetchall()

                # render_template returns an error
                return render_template('admission_form.html',
                                       species=list_species,
                                       exhibits=list_exhibits,
                                       keepers=list_keepers,
                                       error="That exhibit is at full capacity.")

            # SQL command to add new animal to table based on inputs
            sql = """
                  INSERT INTO animal (name, age, sex, health_status, date_acquired, species_id, exhibit_id, keeper_id)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                  """
            cursor.execute(sql, (name, age, sex, health, date, species_id, exhibit_id, keeper_id))
            db.commit()

        except ValueError as e:
            return render_template('admission_form.html', error=str(e))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "There was an issue adding the animal."
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('animal_list'))

    # Getting information for the dropdown selectors
    cursor.execute("SELECT species_id, common_name FROM species")
    list_species = cursor.fetchall()
    cursor.execute("SELECT exhibit_id, name, capacity FROM exhibit")
    list_exhibits = cursor.fetchall()
    cursor.execute("SELECT keeper_id, name FROM keeper")
    list_keepers = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('admission_form.html',
                           species=list_species,
                           exhibits=list_exhibits,
                           keepers=list_keepers)


if __name__ == '__main__':
    app.run(debug=True)
