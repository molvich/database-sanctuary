from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="sanctuary_db"
    )
    return connection


# Home page
@app.route('/')
def index():
    return render_template("index.html")

# Animals list view
@app.route('/animals')
def animal_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SELECT with JOIN - pulls resident rows with species + exhibit names
    query = """
            SELECT a.animal_id,
                   a.name,
                   a.age,
                   a.sex,
                   a.health_status,
                   a.date_acquired,
                   s.common_name,
                   e.name AS exhibit_name
            FROM animal a
                     LEFT JOIN species s ON a.species_id = s.species_id
                     LEFT JOIN exhibit e ON a.exhibit_id = e.exhibit_id
            ORDER BY a.animal_id
            """

    cursor.execute(query)
    list_animals = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("animal.html", animals=list_animals)

# Exhibits list view
@app.route('/exhibits')
def exhibit_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SELECT without JOIN for Exhibit
    query = "SELECT exhibit_id, name, type, capacity FROM exhibit ORDER BY exhibit_id"

    cursor.execute(query)
    list_exhibits = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("exhibit.html", exhibits=list_exhibits)

# Species list view
@app.route('/species')
def species_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SELECT without JOIN for Species
    query = "SELECT species_id, common_name, scientific_name, diet_type FROM species ORDER BY species_id"

    cursor.execute(query)
    list_species = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("species.html", species=list_species)


@app.route('/keepers')
def keeper_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    error = request.args.get('error')

    # SELECT with JOIN on keepers and their total assigned residents
    query = """
            SELECT k.keeper_id,
                   k.name,
                   k.phone,
                   k.shift,
                   COUNT(a.animal_id) AS animal_count
            FROM keeper k
                     LEFT JOIN animal a ON a.keeper_id = k.keeper_id
            GROUP BY k.keeper_id, k.name, k.phone, k.shift
            ORDER BY k.name
            """

    cursor.execute(query)
    list_keepers = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("keeper.html", keepers=list_keepers, error=error)


@app.route('/keepers/<int:keeper_id>')
def keeper_detail(keeper_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SELECT without JOIN on keepers
    cursor.execute("""
                   SELECT keeper_id, name, phone, shift
                   FROM keeper
                   WHERE keeper_id = %s
                   """, (keeper_id,))
    keeper = cursor.fetchone()

    if keeper is None:
        cursor.close()
        db.close()
        return render_template("not_found.html", thing="Keeper"), 404

    # SELECT with JOIN for animals assigned to this keeper
    cursor.execute("""
                   SELECT a.animal_id,
                          a.name,
                          a.age,
                          a.sex,
                          a.health_status,
                          s.common_name,
                          e.name AS exhibit_name
                   FROM animal a
                            LEFT JOIN species s ON a.species_id = s.species_id
                            LEFT JOIN exhibit e ON a.exhibit_id = e.exhibit_id
                   WHERE a.keeper_id = %s
                   ORDER BY a.name
                   """, (keeper_id,))
    assigned = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("keeper_detail.html", keeper=keeper, assigned=assigned)


# Details view for each animal
@app.route('/animals/<int:animal_id>')
def animal_detail(animal_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SELECT with JOIN for residents
    cursor.execute("""
                   SELECT a.animal_id,
                          a.name,
                          a.age,
                          a.sex,
                          a.health_status,
                          a.date_acquired,
                          s.common_name,
                          s.scientific_name,
                          s.diet_type,
                          e.name AS exhibit_name,
                          e.type AS exhibit_type,
                          k.name AS keeper_name,
                          k.phone AS keeper_phone,
                          k.shift AS keeper_shift
                   FROM animal a
                            LEFT JOIN species s ON a.species_id = s.species_id
                            LEFT JOIN exhibit e ON a.exhibit_id = e.exhibit_id
                            LEFT JOIN keeper k ON a.keeper_id = k.keeper_id
                   WHERE a.animal_id = %s
                   """, (animal_id,))
    animal = cursor.fetchone()

    if animal is None:
        cursor.close()
        db.close()
        return render_template("not_found.html", thing="Animal"), 404

    # SELECT without JOIN for feeding history
    cursor.execute("""
                   SELECT log_id, fed_date, food_type, quantity, notes
                   FROM feeding_log
                   WHERE animal_id = %s
                   ORDER BY fed_date DESC
                   """, (animal_id,))
    feedings = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("animal_detail.html", animal=animal, feedings=feedings)


@app.route('/exhibits/<int:exhibit_id>')
def exhibit_detail(exhibit_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SELECT without JOIN for exhibits
    cursor.execute("""
                   SELECT exhibit_id, name, type, capacity, species_id
                   FROM exhibit
                   WHERE exhibit_id = %s
                   """, (exhibit_id,))
    exhibit = cursor.fetchone()

    if exhibit is None:
        cursor.close()
        db.close()
        return render_template("not_found.html", thing="Exhibit"), 404

    # Residents living in this exhibit
    cursor.execute("""
                   SELECT a.animal_id, a.name, a.age, a.sex, a.health_status, s.common_name
                   FROM animal a
                            LEFT JOIN species s ON a.species_id = s.species_id
                   WHERE a.exhibit_id = %s
                   ORDER BY a.name
                   """, (exhibit_id,))
    residents = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("exhibit_detail.html", exhibit=exhibit, residents=residents)


@app.route('/species/<int:species_id>')
def species_detail(species_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SELECT without JOIN for species
    cursor.execute("""
                   SELECT species_id, common_name, scientific_name, diet_type
                   FROM species
                   WHERE species_id = %s
                   """, (species_id,))
    species = cursor.fetchone()

    if species is None:
        cursor.close()
        db.close()
        return render_template("not_found.html", thing="Species"), 404

    # All residents of this species
    cursor.execute("""
                   SELECT a.animal_id, a.name, a.age, a.sex, a.health_status, e.name AS exhibit_name
                   FROM animal a
                            LEFT JOIN exhibit e ON a.exhibit_id = e.exhibit_id
                   WHERE a.species_id = %s
                   ORDER BY a.name
                   """, (species_id,))
    residents = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("species_detail.html", species=species, residents=residents)


# Add animal
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

        try:
            # Validate that the species matches the selected exhibit
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

            if exhibit and exhibit['current_count'] >= exhibit['capacity']:
                cursor.execute("SELECT species_id, common_name FROM species")
                list_species = cursor.fetchall()
                cursor.execute("SELECT exhibit_id, name, capacity FROM exhibit")
                list_exhibits = cursor.fetchall()
                cursor.execute("SELECT keeper_id, name FROM keeper")
                list_keepers = cursor.fetchall()

                return render_template('admission_form.html',
                                       species=list_species,
                                       exhibits=list_exhibits,
                                       keepers=list_keepers,
                                       error="That exhibit is at full capacity.")

            # INSERT function for new residents
            sql = """
                  INSERT INTO animal (name, age, sex, health_status, date_acquired,
                                      species_id, exhibit_id, keeper_id)
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

    # GET the dropdowns
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


# Edit animal info
@app.route('/edit_animal/<int:animal_id>', methods=['GET', 'POST'])
def edit_animal(animal_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        health = request.form.get('health')
        species_id = request.form.get('species_id')
        exhibit_id = request.form.get('exhibit_id')
        keeper_id = request.form.get('keeper_id')

        try:
            # Validate exhibit must match chosen species
            cursor.execute("""
                           SELECT exhibit_id
                           FROM exhibit
                           WHERE exhibit_id = %s AND species_id = %s
                           """, (exhibit_id, species_id))
            if cursor.fetchone() is None:
                raise ValueError("Exhibit does not match selected species.")

            # Capacity check
            cursor.execute("""
                           SELECT e.capacity,
                                  SUM(CASE WHEN a.animal_id <> %s THEN 1 ELSE 0 END) AS others
                           FROM exhibit e
                                    LEFT JOIN animal a ON a.exhibit_id = e.exhibit_id
                           WHERE e.exhibit_id = %s
                           GROUP BY e.exhibit_id
                           """, (animal_id, exhibit_id))
            row = cursor.fetchone()
            if row and row['others'] is not None and row['others'] >= row['capacity']:
                raise ValueError("That exhibit is at full capacity.")

            # UPDATE command
            cursor.execute("""
                           UPDATE animal
                           SET name          = %s,
                               age           = %s,
                               sex           = %s,
                               health_status = %s,
                               species_id    = %s,
                               exhibit_id    = %s,
                               keeper_id     = %s
                           WHERE animal_id = %s
                           """,
                           (name, age, sex, health, species_id, exhibit_id, keeper_id, animal_id))
            db.commit()

            cursor.close()
            db.close()
            return redirect(url_for('animal_detail', animal_id=animal_id))

        except ValueError as e:
            error_msg = str(e)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            cursor.close()
            db.close()
            return "There was an issue updating the animal."
    else:
        error_msg = None

    # GET/POST to load current record + dropdowns
    cursor.execute("""
                   SELECT animal_id, name, age, sex, health_status,
                          species_id, exhibit_id, keeper_id
                   FROM animal
                   WHERE animal_id = %s
                   """, (animal_id,))
    animal = cursor.fetchone()

    if animal is None:
        cursor.close()
        db.close()
        return render_template("not_found.html", thing="Animal"), 404

    cursor.execute("SELECT species_id, common_name FROM species")
    list_species = cursor.fetchall()
    cursor.execute("SELECT exhibit_id, name, capacity FROM exhibit")
    list_exhibits = cursor.fetchall()
    cursor.execute("SELECT keeper_id, name FROM keeper")
    list_keepers = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('edit_form.html',
                           animal=animal,
                           species=list_species,
                           exhibits=list_exhibits,
                           keepers=list_keepers,
                           error=error_msg)


# Delete animal
@app.route('/delete_animal/<int:animal_id>', methods=['POST'])
def delete_animal(animal_id):
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM feeding_log WHERE animal_id = %s", (animal_id,))

        # DELETE function
        cursor.execute("DELETE FROM animal WHERE animal_id = %s", (animal_id,))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "There was an issue deleting the animal."
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('animal_list'))


# Feeding log
@app.route('/add_feeding', methods=['GET', 'POST'])
def add_feeding():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        animal_id = request.form.get('animal_id')
        keeper_id = request.form.get('keeper_id')
        food_type = request.form.get('food_type')
        quantity = request.form.get('quantity')
        notes = request.form.get('notes')

        try:
            cursor.execute("""
                           INSERT INTO feeding_log (animal_id, keeper_id, food_type, quantity, notes)
                           VALUES (%s, %s, %s, %s, %s)
                           """, (animal_id, keeper_id, food_type, quantity, notes))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "There was an issue recording the feeding."
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('animal_detail', animal_id=animal_id))

    preselect = request.args.get('animal_id', type=int)

    cursor.execute("""
                   SELECT a.animal_id, a.name, s.common_name
                   FROM animal a
                            LEFT JOIN species s ON a.species_id = s.species_id
                   ORDER BY a.name
                   """)
    list_animals = cursor.fetchall()
    cursor.execute("SELECT keeper_id, name FROM keeper")
    list_keepers = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('feeding_form.html',
                           animals=list_animals,
                           keepers=list_keepers,
                           preselect=preselect)


# Add new keeper
@app.route('/add_keeper', methods=['GET', 'POST'])
def add_keeper():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        shift = request.form.get('shift')

        try:
            # INSERT function for new keeper
            sql = """
                  INSERT INTO keeper (name, phone, shift)
                  VALUES (%s, %s, %s)
                  """
            cursor.execute(sql, (name, phone, shift))
            db.commit()

        except ValueError as e:
            return render_template('keeper_form.html', error=str(e))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "There was an issue adding the keeper."
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('keeper_list'))

    cursor.execute("SELECT keeper_id, name FROM keeper")
    list_keepers = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('keeper_form.html', keepers=list_keepers)



# Delete keeper
@app.route('/delete_keeper/<int:keeper_id>', methods=['POST'])
def delete_keeper(keeper_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # Validate that the keeper isn't assigned to any animals
        cursor.execute("SELECT 1 FROM animal WHERE keeper_id = %s LIMIT 1", (keeper_id,))
        if cursor.fetchone():
           return redirect(url_for('keeper_list',error='Keeper assignments must be removed.'))

        # DELETE functions
        cursor.execute("DELETE FROM feeding_log WHERE keeper_id = %s", (keeper_id,))

        cursor.execute("DELETE FROM animal WHERE keeper_id = %s", (keeper_id,))

        cursor.execute("DELETE FROM keeper WHERE keeper_id = %s", (keeper_id,))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "There was an issue deleting the keeper."
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('keeper_list'))


if __name__ == '__main__':
    app.run(debug=True)