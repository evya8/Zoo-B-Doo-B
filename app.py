import sqlite3
from flask import Flask, redirect, render_template, render_template_string, request, session, url_for


app = Flask(__name__, static_url_path='/static')
con = sqlite3.connect("zoob.db" ,check_same_thread=False)
cur = con.cursor()
global logged





@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists in the database
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            # If the username already exists, display an error message
            alert_message = f'The username "{username}" is already taken. Please choose a different username.'
            return render_template('register.html')

        # Insert user data into the database
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists in the database
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        
        if user:
            logged=True
            return redirect(url_for('get_animals'))
            # Redirect to the 'get_animals' route upon successful login
            
        else:
            return "Invalid credentials. Please try again."
    return render_template("login.html")

# Modify your add route to handle both GET and POST requests
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        species = request.form['species']
        animal_name = request.form['animal_name']
        age = request.form['age']
        sex = request.form['sex']
        enclosure_number = request.form['enclosure_number']
        date_acquired = request.form['date_acquired']
        health_status = request.form['health_status']
        last_vet_visit = request.form['last_vet_visit']
        diet = request.form['diet']
        conservation_status = request.form['conservation_status']
        image_url = request.form['image_url']
        genetic_information = request.form['genetic_information']
        notes = request.form['notes']
            # Insert data into the database using placeholders
        cur.execute("""
                INSERT INTO animals 
                (species, name, age, sex, enclosure_number, date_acquired, health_status, 
                last_vet_visit, diet, conservation_status, image_url, genetic_information, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (species, animal_name, age, sex, enclosure_number, date_acquired, health_status, 
                  last_vet_visit, diet, conservation_status, image_url, genetic_information, notes))
        con.commit()    
    return render_template ('add.html')


@app.route('/get_animals')
def get_animals():
    
    # Fetch data from the database
    cur.execute("SELECT * FROM animals")
    animals = cur.fetchall()  # Fetch all rows
    
    # Render the template and pass the retrieved data
    return render_template("animals.html", animals=animals)


@app.route('/delete_animal/<int:animal_id>', methods=['GET', 'POST'])
def delete_animal(animal_id):
    if request.method == 'GET':
        # Fetch the details of the animal
        cur.execute("SELECT * FROM animals WHERE animal_id=?", (animal_id,))
        animal_tuple = cur.fetchone()

        if animal_tuple:
            # Convert the tuple to a dictionary
            animal = {
                'animal_id': animal_tuple[0],
                'species': animal_tuple[1],
                'name': animal_tuple[2],
            }

            # Render the confirmation page
            return render_template('delete_animal.html', animal=animal)

        # If the animal is not found, redirect to get_animals
        return redirect(url_for('get_animals'))

    elif request.method == 'POST':
        # Delete the specified animal from the database
        cur.execute("DELETE FROM animals WHERE animal_id=?", (animal_id,))
        con.commit()

        print("Deletion successful")

        return redirect(url_for('get_animals'))




@app.route('/update_animal/<int:animal_id>', methods=['GET', 'POST'])
def update_animal(animal_id):
    if request.method == 'POST':
        species = request.form['new_species']
        animal_name = request.form['new_name']
        age = request.form['new_age']
        sex = request.form['new_sex']
        enclosure_number = request.form['new_enclosure_number']
        date_acquired = request.form['new_date_acquired']
        health_status = request.form['new_health_status'] 
        last_vet_visit = request.form['new_last_vet_visit']
        diet = request.form['new_diet']
        conservation_status = request.form['new_conservation_status']
        image_url = request.form['new_image_url']
        genetic_information = request.form['new_genetic_information']
        notes = request.form['new_notes']

        # Update data in the database
        cur.execute("""
            UPDATE animals SET
            species=?, name=?, age=?, sex=?, enclosure_number=?, date_acquired=?,
            health_status=?, last_vet_visit=?, diet=?, conservation_status=?, image_url=?, genetic_information=?, notes=?
            WHERE animal_id=?
        """, (species, animal_name, age, sex, enclosure_number, date_acquired, health_status,last_vet_visit, diet,conservation_status,image_url,genetic_information,notes, animal_id))
        con.commit()
        
        return render_template('animals.html')

    # Fetch the existing data for the specified animal_id
    cur.execute("SELECT * FROM animals WHERE animal_id=?", (animal_id,))
    animal_tuple = cur.fetchone()

    if animal_tuple:
        # Convert the tuple to a dictionary
        animal = {
            'animal_id': animal_tuple[0],
            'species': animal_tuple[1],
            'name': animal_tuple[2],
            'age': animal_tuple[3],
            'sex': animal_tuple[4],
            'enclosure_number': animal_tuple[5],
            'date_acquired': animal_tuple[6],
            'health_status': animal_tuple[7],
            'last_vet_visit' : animal_tuple[8],
            'diet' : animal_tuple[9],
            'conservation_status' : animal_tuple[10],
            'image_url': animal_tuple[11],
            'genetic_information' : animal_tuple[12],
            'notes' : animal_tuple[13]
        }

        # Render the update template and pass the existing data
        return render_template("update_animal.html", animal=animal)
    
if __name__ == '__main__':
    app.run(debug=True)

