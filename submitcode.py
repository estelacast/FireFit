from graphics import *
import time
import json
import pandas as pd
import matplotlib.pyplot as plt


class LoginSystem:
    def __init__(self):
        self.database = {}
        self.load_database()

    def load_database(self):
        """Load the database from a JSON file if it exists"""
        try:
            with open("database.json", "r") as file:
                self.database = json.load(file)
        except FileNotFoundError:
            print("No database found, starting with an empty one.")
            self.database = {}

    def save_database(self):
        """Save the current database to a JSON file"""
        with open("database.json", "w") as file:
            json.dump(self.database, file, indent=4)

    def add_user(self, username, password, name, surname, gender, height, weight, dob):
        """Add a new user to the database"""
        if username in self.database:
            print("Username already exists.")
            return False
        # Save user data in database
        self.database[username] = {
            "Password": password,
            "Name": name,
            "Surname": surname,
            "Gender": gender,
            "Height (cm)": height,
            "Weight (kg)": weight,
            "Date of Birth": dob
        }
        self.save_database()
        print(f"User {username} added successfully.")
        return True

    def validate_login(self, username, password):
        """Validate the user's login credentials"""
        if username not in self.database:
            return "No account with such username."
        elif self.database[username]["Password"] != password:
            return "Wrong password."
        else:
            return "Login successful!"

# Button Class
class Button:
    def __init__(self, x, y, width, height, offset, outline, fill=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.offset = offset
        self.outline = outline
        self.fill = fill
        self.rectangle = None

    def create_rectangle(self):
        top_left = Point(720 / 2 + self.x - self.width / 2, 1000 / 2 + self.y - self.height / 2 + self.offset)
        bottom_right = Point(720 / 2 + self.x + self.width / 2, 1000 / 2 + self.y + self.height / 2 + self.offset)
        rectangle = Rectangle(top_left, bottom_right)
        rectangle.setWidth(4)
        rectangle.setOutline(self.outline)
        if self.fill:
            rectangle.setFill(self.fill)
        self.rectangle = rectangle

    def draw(self, win):
        self.create_rectangle()
        self.rectangle.draw(win)

    def get_center(self):
        return self.rectangle.getCenter()

    def get_bounds(self):
        return self.rectangle.getP1(), self.rectangle.getP2()


# TextLabel Class
class TextLabel:
    def __init__(self, position, text, font="helvetica", size=13, style="normal", color="black"):
        self.text = Text(position, text)
        self.text.setFace(font)
        self.text.setSize(size)
        self.text.setStyle(style)
        self.text.setTextColor(color)

    def draw(self, win):
        self.text.draw(win)

    def set_text(self, new_text):
        self.text.setText(new_text)

    def get_text(self):
        return self.text.getText()

    def set_color(self, color):
        self.text.setTextColor(color)

    def set_style(self, style):
        self.text.setStyle(style)

def frames(letter, range1, range2, window):
    # Animated frames
    frames = [Image(Point(window.getWidth() / 2, 500), f"{letter}{i}.png") for i in range(range1, range2)]
    for frame in frames:
        frame.draw(window)
        time.sleep(0.1)
        frame.undraw()

# Create the login window
def create_login_window(login_system, transition):
    win = GraphWin("Phone - Login", 720, 1000)

    if transition != "":
        frames("", 1,25, win)

    # Background
    background_image = Image(Point(win.getWidth() / 2, win.getHeight() / 2), "b4.png")
    background_image.draw(win)

    # Username box
    button1 = Button(x=0, y=-120, width=300, height=50, offset=50, outline="#ff3e00")
    button1.draw(win)

    # Password box
    button2 = Button(x=0, y=-50, width=300, height=50, offset=50, outline="#ff3e00")
    button2.draw(win)

    # Login button
    button3 = Button(x=-100, y=50, width=200, height=50, offset=50, outline="#ff3e00", fill="#ff3e00")
    button3.draw(win)

    # Sign-Up button (without outline)
    signup_button = Button(x=100, y=50, width=200, height=50, offset=50, outline="#f6f4f0", fill="#f6f4f0")
    signup_button.draw(win)

    # Placeholder Text using TextLabel
    username_text = TextLabel(button1.get_center(), "Username", style="italic", color="gray")
    username_text.draw(win)

    password_text = TextLabel(button2.get_center(), "Password", style="italic", color="gray")
    password_text.draw(win)

    login_text = TextLabel(button3.get_center(), "Log In", style="bold", color="white")
    login_text.draw(win)

    # Sign-Up text
    signup_text = TextLabel(signup_button.get_center(), "Sign Up", style="bold", color="#ff3e00")
    signup_text.draw(win)

    # Exit button
    exit_button = Button(x=300, y=-500, width=80, height=40, offset=50, outline="#f6f4f0")
    exit_button.draw(win)

    exit_text = TextLabel(exit_button.get_center(), "Exit", color="red")
    exit_text.draw(win)

    username = ""
    password = ""

    def clear_placeholder(box_text, placeholder):
        if box_text.get_text() == placeholder:
            box_text.set_text("")
            box_text.set_color("black")
            box_text.set_style("normal")

    def handle_input(box_text, is_password=False):
        nonlocal username, password
        placeholder = "Password" if is_password else "Username"
        clear_placeholder(box_text, placeholder)
        user_input = ""
        while True:
            key = win.checkKey()
            if key == "Return":
                break
            elif key == "BackSpace":
                user_input = user_input[:-1]
            elif key.isprintable():
                user_input += key

            box_text.set_text(user_input if not is_password else "*" * len(user_input))

        if is_password:
            password = user_input
            return password
        else:
            username = user_input
            return username

    username1 = ""
    password1 = ""
    while True:
        pt = win.getMouse()
        if pt:
            if button1.rectangle.getP1().getX() < pt.getX() < button1.rectangle.getP2().getX() and \
                    button1.rectangle.getP1().getY() < pt.getY() < button1.rectangle.getP2().getY():
                username1 = handle_input(username_text, is_password=False)

            elif button2.rectangle.getP1().getX() < pt.getX() < button2.rectangle.getP2().getX() and \
                    button2.rectangle.getP1().getY() < pt.getY() < button2.rectangle.getP2().getY():
                password1 = handle_input(password_text, is_password=True)

            elif button3.rectangle.getP1().getX() < pt.getX() < button3.rectangle.getP2().getX() and \
                    button3.rectangle.getP1().getY() < pt.getY() < button3.rectangle.getP2().getY():
                username = username1
                password = password1

                # Validate login inputs
                if not username or not password:
                    error_text = TextLabel(Point(720 / 2, 1000 / 2 + 250), "Please fill in all fields!", color="red")
                    error_text.draw(win)
                else:
                    login_result = login_system.validate_login(username, password)
                    if login_result == "Login successful!":
                        print(login_result)
                        win.close()
                        return ["dashboard", login_system, username]
                    else:
                        error_text = TextLabel(Point(720 / 2, 1000 / 2 + 250), login_result, color="red")
                        error_text.draw(win)

            # Check if Sign-Up button is clicked
            elif signup_button.rectangle.getP1().getX() < pt.getX() < signup_button.rectangle.getP2().getX() and \
                    signup_button.rectangle.getP1().getY() < pt.getY() < signup_button.rectangle.getP2().getY():
                print("Navigating to Sign-Up page...")
                win.close()  # Close the login window
                return ["signup", login_system]

            elif exit_button.rectangle.getP1().getX() < pt.getX() < exit_button.rectangle.getP2().getX() and \
                    exit_button.rectangle.getP1().getY() < pt.getY() < exit_button.rectangle.getP2().getY():
                print("Application exited.")
                win.close()
                return ["exit"]


def create_signup_page(login_system):
    signup_win = GraphWin("Phone - Sign Up", 720, 1000)

    frames("t", 1,24, signup_win)

    # Background
    background_image = Image(Point(signup_win.getWidth() / 2, signup_win.getHeight() / 2), "b1.png")
    background_image.draw(signup_win)

    # Text fields for the user's information
    fields = ["Name", "Surname", "Username", "Password", "Gender", "Height (cm)", "Weight (kg)"]
    dob_fields = ["Day", "Month", "Year"]  # For Date of Birth
    boxes = {}
    dob_boxes = {}

    # Box dimensions
    box_width = 300
    box_height = 36

    # Create input fields for each item in `fields`
    for idx, field in enumerate(fields):
        top_y = 264 + idx * 60

        # Label for the field (aligned with the input box)
        label = TextLabel(
            position=Point(150, top_y + box_height / 2),  # Vertically align with box center
            text=field,
            font="helvetica",
            size=13,
            style="bold",
            color="#333333"
        )
        label.draw(signup_win)

        # Input box using Button class
        box = Button(
            x=50, y=-219 + idx*60,  # Same y-coordinate as the label
            width=box_width, height=box_height,
            offset=0,
            outline="#ff3e00"
        )
        box.draw(signup_win)

        # Placeholder text for the field using TextLabel class (centered in the box)
        field_text = TextLabel(
            position=box.get_center(),
            text=field,
            font="helvetica",
            size=13,
            style="italic",
            color="gray"
        )
        field_text.draw(signup_win)

        # Store the box and text for later interaction
        boxes[field] = (box, field_text)

    # Add Date of Birth fields (aligned with labels and boxes)
    dob_label = TextLabel(
        position=Point(150, 264 + 7 * 60 + 18),
        text="Date of Birth",
        font="helvetica",
        size=13,
        style="bold",
        color="#333333"
    )
    dob_label.draw(signup_win)

    for idx, field in enumerate(dob_fields):
        top_left = Point(-50+idx*125, 202)

        # Date of Birth input box using Button class
        dob_box = Button(
            x=top_left.x, y=top_left.y,  # Ensure proper alignment
            width=100, height=box_height,
            offset=0,
            outline="#ff3e00"
        )
        dob_box.draw(signup_win)

        # Placeholder text for Date of Birth field using TextLabel class (centered in the box)
        dob_field_text = TextLabel(
            position=dob_box.get_center(),
            text=field,
            font="helvetica",
            size=13,
            style="italic",
            color="gray"
        )
        dob_field_text.draw(signup_win)

        dob_boxes[field] = (dob_box, dob_field_text)

    # Submit button using Button class
    submit_button = Button(
        x=0, y=310,
        width=200, height=50,
        offset=0,
        outline="#ff6914",
        fill="#ff6914"
    )
    submit_button.draw(signup_win)

    submit_text = TextLabel(
        position=submit_button.get_center(),
        text="Submit",
        font="helvetica",
        size=13,
        style="bold",
        color="white"
    )
    submit_text.draw(signup_win)

    # Add return button using Button class (for going back to the main page or dashboard)
    return_button = Button(
        x=320, y=-470,
        width=100, height=50,
        offset=0,
        outline="#ff6914",
        fill="#ff6914"
    )
    return_button.draw(signup_win)

    return_text = TextLabel(
        position=return_button.get_center(),
        text="Return",
        font="helvetica",
        size=13,
        style="bold",
        color="white"
    )
    return_text.draw(signup_win)

    # Function to clear placeholder text
    def clear_placeholder(box_text, placeholder):
        if box_text.get_text() == placeholder:
            box_text.set_text("")
            box_text.set_color("black")
            box_text.set_style("normal")

    # Function to handle input dynamically with validation
    def handle_input(box_text, placeholder, field_name, max_length=None, allowed_chars=None):
        clear_placeholder(box_text, placeholder)
        user_input = ""
        while True:
            key = signup_win.checkKey()
            click = signup_win.checkMouse()

            if click:
                break
            if key:
                if key == "BackSpace":
                    user_input = user_input[:-1]
                elif len(user_input) < max_length and (key in allowed_chars if allowed_chars else key.isprintable()):
                    user_input += key
                box_text.set_text(user_input)

    # Allowed character sets for validation
    allowed_characters = {
        "Name": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        "Surname": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        "Username": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-",
        "Password": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-",
        "Gender": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        "Height (cm)": "0123456789",
        "Weight (kg)": "0123456789",
        "Day": "0123456789",
        "Month": "0123456789",
        "Year": "0123456789",
    }

    max_lengths = {
        "Name": 50,
        "Surname": 50,
        "Username": 20,
        "Password": 20,
        "Gender": 6,
        "Height (cm)": 3,
        "Weight (kg)": 3,
        "Day": 2,
        "Month": 2,
        "Year": 4,
    }

    # Main event loop for the sign-up page
    while True:
        pt = signup_win.checkMouse()

        # Check if the user clicked on input boxes
        if pt:
            for field, (box, box_text) in boxes.items():
                if box.rectangle.getP1().getX() < pt.getX() < box.rectangle.getP2().getX() and \
                        box.rectangle.getP1().getY() < pt.getY() < box.rectangle.getP2().getY():
                    handle_input(box_text, field, field, max_length=max_lengths[field],
                                 allowed_chars=allowed_characters[field])

            for field, (box, box_text) in dob_boxes.items():
                if box.rectangle.getP1().getX() < pt.getX() < box.rectangle.getP2().getX() and \
                        box.rectangle.getP1().getY() < pt.getY() < box.rectangle.getP2().getY():
                    handle_input(box_text, field, field, max_length=max_lengths[field],
                                 allowed_chars=allowed_characters[field])

            if return_button.rectangle.getP1().getX() < pt.getX() < return_button.rectangle.getP2().getX() and \
                    return_button.rectangle.getP1().getY() < pt.getY() < return_button.rectangle.getP2().getY():
                signup_win.close()
                return ["login", login_system, ""]

            if submit_button.rectangle.getP1().getX() < pt.getX() < submit_button.rectangle.getP2().getX() and \
                    submit_button.rectangle.getP1().getY() < pt.getY() < submit_button.rectangle.getP2().getY():
                print("Submit clicked!")

                # Extract user data from input fields
                username = boxes["Username"][1].get_text()
                password = boxes["Password"][1].get_text()
                name = boxes["Name"][1].get_text()
                surname = boxes["Surname"][1].get_text()
                gender = boxes["Gender"][1].get_text()
                height = boxes["Height (cm)"][1].get_text()
                weight = boxes["Weight (kg)"][1].get_text()
                dob = {
                    "Day": dob_boxes["Day"][1].get_text(),
                    "Month": dob_boxes["Month"][1].get_text(),
                    "Year": dob_boxes["Year"][1].get_text()
                }

                # Validate required fields
                if not username or not password or not name or not surname:
                    error_text = TextLabel(Point(720 / 2, 1000 / 2 + 250), "Please fill in all required fields!",
                                           color="red")
                    error_text.draw(signup_win)
                else:
                    # Add user to the login system
                    if login_system.add_user(username, password, name, surname, gender, height, weight, dob):
                        print("Registration successful!")
                        signup_win.close()
                        return ["login", login_system, ""]
                    else:
                        error_text = TextLabel(Point(720 / 2, 1000 / 2 + 250), "Username already exists.", color="red")
                        error_text.draw(signup_win)

                signup_win.close()
                return ["login", login_system, ""]

def create_dashboard_page(login_system, username):

    dashboard_win = GraphWin("User Dashboard", 720, 1000)

    frames("t", 1,24, dashboard_win)

    background_image = Image(Point(dashboard_win.getWidth() / 2, dashboard_win.getHeight() / 2), "b2.png")
    background_image.draw(dashboard_win)

    heading = TextLabel(Point(720 / 2, 113), f"Welcome {username}", font="helvetica", size=32, style="bold", color="#f6f4f0")
    heading.draw(dashboard_win)

    # Create buttons using the Button class
    best_exercise_button = Button(0, -72, 300, 70, 0, "#ff3e00", "#ff3e00")
    best_exercise_button.draw(dashboard_win)
    best_exercise_text = TextLabel(best_exercise_button.get_center(), "Best Exercise", font="helvetica", size=15, style="bold", color="white")
    best_exercise_text.draw(dashboard_win)

    statistics_button = Button(0, 63, 300, 70, 0, "#ff3e00", "#ff3e00")
    statistics_button.draw(dashboard_win)
    statistics_text = TextLabel(statistics_button.get_center(), "Statistics", font="helvetica", size=15, style="bold", color="white")
    statistics_text.draw(dashboard_win)

    edit_profile_button = Button(0, 198, 300, 70, 0, "#ff3e00", "#ff3e00")
    edit_profile_button.draw(dashboard_win)
    edit_profile_text = TextLabel(edit_profile_button.get_center(), "Edit Profile", font="helvetica", size=15, style="bold", color="white")
    edit_profile_text.draw(dashboard_win)

    exit_button = Button(x=300, y=-500, width=80, height=40, offset=50, outline="#ff6914")
    exit_button.draw(dashboard_win)

    exit_text = TextLabel(exit_button.get_center(), "Exit", color="white")
    exit_text.draw(dashboard_win)

    # Event loop for dashboard
    while True:
        pt = dashboard_win.checkMouse()

        if pt:
            # Check if any of the buttons is clicked
            if best_exercise_button.get_bounds()[0].getX() < pt.getX() < best_exercise_button.get_bounds()[1].getX() and \
               best_exercise_button.get_bounds()[0].getY() < pt.getY() < best_exercise_button.get_bounds()[1].getY():
                print("Best Exercise Page selected")
                dashboard_win.close()
                return ["best_exercise", login_system, username]

            if statistics_button.get_bounds()[0].getX() < pt.getX() < statistics_button.get_bounds()[1].getX() and \
               statistics_button.get_bounds()[0].getY() < pt.getY() < statistics_button.get_bounds()[1].getY():
                print("Statistics Page selected")
                dashboard_win.close()
                return ["create_chart", login_system, username]

            if edit_profile_button.get_bounds()[0].getX() < pt.getX() < edit_profile_button.get_bounds()[1].getX() and \
               edit_profile_button.get_bounds()[0].getY() < pt.getY() < edit_profile_button.get_bounds()[1].getY():
                print("Edit Profile Page selected")
                dashboard_win.close()
                return ["edit_profile", login_system, username]

            elif exit_button.rectangle.getP1().getX() < pt.getX() < exit_button.rectangle.getP2().getX() and \
                    exit_button.rectangle.getP1().getY() < pt.getY() < exit_button.rectangle.getP2().getY():
                print("Application exited.")
                dashboard_win.close()
                return ["exit"]


def create_best_exercise_page(login_system, username):
    best_exercise_win = GraphWin("Workout Suggestion", 720, 1000)

    frames("t", 1, 24, best_exercise_win)

    best_exercise_win.setBackground("#f6f4f0")

    # Background
    background_image = Image(Point(best_exercise_win.getWidth() / 2, best_exercise_win.getHeight() / 2), "b3.png")
    background_image.draw(best_exercise_win)

    # Time Available Input
    time_label = TextLabel(
        position=Point(180, 300),
        text="Time Available:",
        font="helvetica",
        size=15,
        color="#333333"
    )
    time_label.draw(best_exercise_win)

    time_box = Button(
        x=10, y=-200,
        width=200, height=40,
        offset=0,
        outline="#ff3e00"
    )
    time_box.draw(best_exercise_win)

    time_input = TextLabel(
        position=time_box.get_center(),
        text="Enter time (min)",
        font="helvetica",
        size=13,
        style="italic",
        color="gray"
    )
    time_input.draw(best_exercise_win)

    # Intensity Options
    intensity_label = TextLabel(
        position=Point(130, 370),
        text="Intensity:",
        font="helvetica",
        size=15,
        color="#333333"
    )
    intensity_label.draw(best_exercise_win)

    intensity_buttons = []
    intensity_options = ["Low", "Medium", "High", "Super High"]

    for i, option in enumerate(intensity_options):
        button = Button(
            x=-100 + i * 100,
            y=-130,
            width=90, height=40,
            offset=0,
            outline="#ff3e00"
        )
        button.draw(best_exercise_win)

        label = TextLabel(
            position=button.get_center(),
            text=option,
            font="helvetica",
            size=12,
            color="#333333"
        )
        label.draw(best_exercise_win)

        intensity_buttons.append((button, option))

    # Generate Button
    generate_button = Button(
        x=0, y=-50,
        width=200, height=50,
        offset=0,
        outline="#ff3e00",
        fill="#ff3e00"
    )
    generate_button.draw(best_exercise_win)

    generate_label = TextLabel(
        position=generate_button.get_center(),
        text="Generate Workout Plan",
        font="helvetica",
        size=13,
        style="bold",
        color="white"
    )
    generate_label.draw(best_exercise_win)

    # Workout Result Display
    workout_result = TextLabel(
        position=Point(360, 550),
        text="",
        font="helvetica",
        size=15,
        color="#333333"
    )
    workout_result.draw(best_exercise_win)

    bpm_result = TextLabel(
        position=Point(360, 625),
        text="",
        font="helvetica",
        size=15,
        color="#007bff"
    )
    bpm_result.draw(best_exercise_win)

    return_button = Button(
        x=320, y=-470,
        width=100, height=50,
        offset=0,
        outline="#ff6914",
        fill="#ff6914"
    )
    return_button.draw(best_exercise_win)

    return_text = TextLabel(
        position=return_button.get_center(),
        text="Return",
        font="helvetica",
        size=13,
        style="bold",
        color="white"
    )
    return_text.draw(best_exercise_win)

    # Placeholder Variables
    selected_intensity = None
    time_value = None

    # Function to Clear Placeholder Text
    def clear_placeholder(box_text, placeholder):
        if box_text.get_text() == placeholder:
            box_text.set_text("")
            box_text.set_color("black")
            box_text.set_style("normal")

    # Function to Handle Text Input
    def handle_input(box_text, is_password=False):
        nonlocal time_value
        placeholder = "Enter time (min)"
        clear_placeholder(box_text, placeholder)
        user_input = ""
        while True:
            key = best_exercise_win.checkKey()
            if key == "Return":
                break
            elif key == "BackSpace":
                user_input = user_input[:-1]
            elif key.isdigit():
                user_input += key

            box_text.set_text(user_input)
        time_value = user_input.strip()

    # Function to Display Workout Plan
    def display_workout_plan():
        nonlocal selected_intensity, time_value
        if not time_value or not selected_intensity:
            workout_result.set_text("Please input time and select intensity.")
            bpm_result.set_text("")
            return

        # Example logic for workout suggestion
        if selected_intensity == "Low":
            workout_type = "Yoga"
            avg_bpm = "Avg BPM: 80-100"
            image = Image(Point(best_exercise_win.getWidth() / 2, 750), 'i4.png')
        elif selected_intensity == "Medium":
            workout_type = "Strength Training"
            avg_bpm = "Avg BPM: 110-130"
            image = Image(Point(best_exercise_win.getWidth() / 2, 750), 'i1.png')
        elif selected_intensity == "High":
            workout_type = "Cardio"
            avg_bpm = "Avg BPM: 130-150"
            image = Image(Point(best_exercise_win.getWidth() / 2, 750), 'i2.png')
        else:  # Super High
            workout_type = "HIIT"
            avg_bpm = "Avg BPM: 150-180"
            image = Image(Point(best_exercise_win.getWidth() / 2, 750), 'i3.png')

        workout_result.set_text(f"Workout: {workout_type}")
        bpm_result.set_text(avg_bpm)
        image.draw(best_exercise_win)

    # Event Loop
    while True:
        pt = best_exercise_win.getMouse()

        if pt:
            # Time Input Box
            if time_box.rectangle.getP1().getX() < pt.getX() < time_box.rectangle.getP2().getX() and \
                    time_box.rectangle.getP1().getY() < pt.getY() < time_box.rectangle.getP2().getY():
                handle_input(time_input)

            # Check if the Return Button is clicked
            if return_button.rectangle.getP1().getX() < pt.getX() < return_button.rectangle.getP2().getX() and \
                    return_button.rectangle.getP1().getY() < pt.getY() < return_button.rectangle.getP2().getY():
                best_exercise_win.close()
                return ["dashboard", login_system, username]

            # Intensity Buttons
            for button, option in intensity_buttons:
                if button.rectangle.getP1().getX() < pt.getX() < button.rectangle.getP2().getX() and \
                        button.rectangle.getP1().getY() < pt.getY() < button.rectangle.getP2().getY():
                    # Update the selected intensity
                    selected_intensity = option

                    # Clear all button highlights
                    for b, _ in intensity_buttons:
                        b.rectangle.setFill("#f6f4f0")  # Set to default background color

                    # Highlight the selected button
                    button.rectangle.setFill("#ffcccb")

            # Generate Button
            if generate_button.rectangle.getP1().getX() < pt.getX() < generate_button.rectangle.getP2().getX() and \
                    generate_button.rectangle.getP1().getY() < pt.getY() < generate_button.rectangle.getP2().getY():
                display_workout_plan()


def create_chart_interface(login_system, username, window_title="Gym Interface", window_size=(720, 1000)):

    # Load the data
    data = pd.read_csv('gym_members_exercise.csv')

    # Create the main window
    graph_win = GraphWin(window_title, *window_size)

    frames("t", 1, 24, graph_win)

    bg_image = Image(Point(window_size[0] / 2, window_size[1] / 2), "b5.png")
    bg_image.draw(graph_win)

    return_button = Button(
        x=320, y=-470,
        width=100, height=50,
        offset=0,
        outline="#ff6914",
        fill="#ff6914"
    )
    return_button.draw(graph_win)

    return_text = TextLabel(
        position=return_button.get_center(),
        text="Return",
        font="helvetica",
        size=13,
        style="bold",
        color="white"
    )
    return_text.draw(graph_win)

    def draw_pie_chart(filtered_data, filename="piechart.png", bg_color="#f6f4f0"):
        gender_count = filtered_data["Gender"].value_counts()
        plt.figure(figsize=(4.6, 4.6))
        plt.pie(
            gender_count,
            labels=gender_count.index,
            autopct='%1.1f%%',
            colors=["#ff883c", "#ed460f"]
        )
        plt.gca().set_facecolor(bg_color)
        plt.savefig(filename, bbox_inches='tight', dpi=100, facecolor=bg_color)
        plt.close()

    def draw_bar_chart(filtered_data, filename="barchart.png", bg_color="#f6f4f0"):
        experience_frequency = filtered_data.groupby("Experience_Level")["Workout_Frequency (days/week)"].sum()
        plt.figure(figsize=(3.9, 3.5))
        plt.bar(
            experience_frequency.index,
            experience_frequency.values,
            color=["#ff883c", "#ed460f", "#ffc888"]
        )
        plt.gca().set_facecolor(bg_color)
        plt.xlabel("Experience Level")
        plt.ylabel("Training Days")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(filename, bbox_inches='tight', dpi=100, facecolor=bg_color)
        plt.close()

    def display_chart(win, chart_type, bg_image=None):

        if chart_type == "pie":
            pie_chart = Image(Point(400, 441), "piechart.png")
            pie_chart.draw(win)
        elif chart_type == "bar":
            bar_chart = Image(Point(400, 441), "barchart.png")
            bar_chart.draw(win)


    # Buttons for chart selection
    pie_button = Button(-280, -94, 100, 50, offset=0, outline="#ff6914", fill="#ff6914")
    pie_button.draw(graph_win)
    pie_text = TextLabel(pie_button.get_center(), "Pie chart", style="bold", color="#f6f4f0")
    pie_text.draw(graph_win)

    bar_button = Button(-280, -24, 100, 50, offset=0, outline="#ff6914", fill="#ff6914")
    bar_button.draw(graph_win)
    bar_text = TextLabel(bar_button.get_center(), "Bar chart", style="bold", color="#f6f4f0")
    bar_text.draw(graph_win)

    # Buttons for workout filters
    buttons = {}
    button_labels = ["Yoga", "HIIT", "Cardio", "Strength", "All"]
    button_file_map = {
        "Yoga": "yoga.png",
        "HIIT": "hiit.png",
        "Cardio": "cardio.png",
        "Strength": "strength.png",
        "All": "all.png"
    }
    button_width = 100
    button_spacing = 20
    start_x = (window_size[0] - ((len(button_labels) * button_width) + ((len(button_labels) - 1) * button_spacing))) // 2
    y_pos = 700

    for i, label in enumerate(button_labels):
        x_pos = start_x + i * (button_width + button_spacing)
        button_image = Image(Point(x_pos + button_width // 2, y_pos + 20), button_file_map[label])
        button_image.draw(graph_win)
        buttons[label] = button_image

    # Initial charts
    draw_pie_chart(data, bg_color="#f6f4f0")
    draw_bar_chart(data, bg_color="#f6f4f0")
    display_chart(graph_win, chart_type="", bg_image=bg_image)

    # Event loop for interaction
    current_chart = "pie"
    while True:
        click = graph_win.getMouse()

        # Handle pie chart and bar chart buttons
        if pie_button.get_bounds()[0].getX() < click.getX() < pie_button.get_bounds()[1].getX() and \
                pie_button.get_bounds()[0].getY() < click.getY() < pie_button.get_bounds()[1].getY():
            current_chart = "pie"
            display_chart(graph_win, chart_type="pie", bg_image=bg_image)

        elif bar_button.get_bounds()[0].getX() < click.getX() < bar_button.get_bounds()[1].getX() and \
                bar_button.get_bounds()[0].getY() < click.getY() < bar_button.get_bounds()[1].getY():
            current_chart = "bar"
            display_chart(graph_win, chart_type="bar", bg_image=bg_image)

        # Handle workout filter buttons
        for label, button_image in buttons.items():
            x_center = button_image.getAnchor().getX()
            y_center = button_image.getAnchor().getY()
            width = 100
            height = 40

            if (x_center - width / 2 <= click.getX() <= x_center + width / 2 and
                    y_center - height / 2 <= click.getY() <= y_center + height / 2):
                if label == "All":
                    filtered_data = data
                else:
                    filtered_data = data[data["Workout_Type"] == label]

                draw_pie_chart(filtered_data, bg_color="#f6f4f0")
                draw_bar_chart(filtered_data, bg_color="#f6f4f0")
                display_chart(graph_win, chart_type=current_chart, bg_image=bg_image)
                break
        # Check if the Return Button is clicked
        if return_button.rectangle.getP1().getX() < click.getX() < return_button.rectangle.getP2().getX() and \
                return_button.rectangle.getP1().getY() < click.getY() < return_button.rectangle.getP2().getY():
            graph_win.close()
            return ["dashboard", login_system, username]


def edit_profile_page(login_system, username):
    edit_win = GraphWin("Edit Profile", 720, 1000)

    frames("t", 1,24, edit_win)

    # Background
    background_image = Image(Point(edit_win.getWidth() / 2, edit_win.getHeight() / 2), "b6.png")
    background_image.draw(edit_win)

    # Fields to edit
    fields = ["Name", "Surname", "Password", "Gender", "Height (cm)", "Weight (kg)"]
    dob_fields = ["Day", "Month", "Year"]
    boxes = {}
    dob_boxes = {}

    user_data = login_system.database[username]

    # Box dimensions
    box_width = 300
    box_height = 36

    # Display fields for editing
    for idx, field in enumerate(fields):
        top_y = 264 + idx * 60

        # Label for each field
        label = TextLabel(
            position=Point(150, top_y + box_height / 2),
            text=field,
            font="helvetica",
            size=13,
            style="bold",
            color="#333333"
        )
        label.draw(edit_win)

        # Editable input box
        box = Button(
            x=50, y=-219 + idx*60,
            width=box_width, height=box_height,
            offset=0,
            outline="#ff3e00"
        )
        box.draw(edit_win)

        # Populate current value into text
        field_value = user_data[field] if field != "Password" else "********"
        box_text = TextLabel(
            position=box.get_center(),
            text=field_value,
            font="helvetica",
            size=13,
            style="normal",
            color="black"
        )
        box_text.draw(edit_win)
        boxes[field] = (box, box_text)

    # Date of Birth Fields
    dob_label = TextLabel(
        position=Point(150, 264 + len(fields) * 60 + 18),
        text="Date of Birth",
        font="helvetica",
        size=13,
        style="bold",
        color="#333333"
    )
    dob_label.draw(edit_win)

    for idx, field in enumerate(dob_fields):
        top_left = Point(-50 + idx * 125, 141)

        dob_box = Button(
            x=top_left.x, y=top_left.y,
            width=100, height=box_height,
            offset=0,
            outline="#ff3e00"
        )
        dob_box.draw(edit_win)

        # Populate DOB values
        field_value = user_data["Date of Birth"][field]
        dob_text = TextLabel(
            position=dob_box.get_center(),
            text=field_value,
            font="helvetica",
            size=13,
            style="normal",
            color="black"
        )
        dob_text.draw(edit_win)
        dob_boxes[field] = (dob_box, dob_text)

    # Submit Button
    submit_button = Button(
        x=0, y=310,
        width=200, height=50,
        offset=0,
        outline="#ff6914",
        fill="#ff6914"
    )
    submit_button.draw(edit_win)

    submit_text = TextLabel(
        position=submit_button.get_center(),
        text="Save Changes",
        font="helvetica",
        size=13,
        style="bold",
        color="white"
    )
    submit_text.draw(edit_win)

    # Return Button
    return_button = Button(
        x=320, y=-470,
        width=100, height=50,
        offset=0,
        outline="#ff6914",
        fill="#ff6914"
    )
    return_button.draw(edit_win)

    return_text = TextLabel(
        position=return_button.get_center(),
        text="Return",
        font="helvetica",
        size=13,
        style="bold",
        color="white"
    )
    return_text.draw(edit_win)

    # Event handling for updating fields
    def handle_input(box_text, placeholder, max_length=None, allowed_chars=None):
        user_input = box_text.get_text()
        while True:
            key = edit_win.checkKey()
            click = edit_win.checkMouse()
            if click:
                break
            if key:
                if key == "BackSpace":
                    user_input = user_input[:-1]
                elif len(user_input) < max_length and (key in allowed_chars if allowed_chars else key.isprintable()):
                    user_input += key
                box_text.set_text(user_input)

    # Allowed characters and max lengths
    allowed_characters = {
        "Name": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        "Surname": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        "Password": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ",
        "Gender": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        "Height (cm)": "0123456789",
        "Weight (kg)": "0123456789",
        "Day": "0123456789",
        "Month": "0123456789",
        "Year": "0123456789",
    }
    max_lengths = {
        "Name": 50,
        "Surname": 50,
        "Password": 20,
        "Gender": 6,
        "Height (cm)": 3,
        "Weight (kg)": 3,
        "Day": 2,
        "Month": 2,
        "Year": 4,
    }

    # Main event loop
    while True:
        pt = edit_win.checkMouse()

        if pt:
            # Input fields
            for field, (box, box_text) in boxes.items():
                if box.rectangle.getP1().getX() < pt.getX() < box.rectangle.getP2().getX() and \
                        box.rectangle.getP1().getY() < pt.getY() < box.rectangle.getP2().getY():
                    handle_input(box_text, field, max_length=max_lengths[field],
                                 allowed_chars=allowed_characters[field])

            for field, (box, box_text) in dob_boxes.items():
                if box.rectangle.getP1().getX() < pt.getX() < box.rectangle.getP2().getX() and \
                        box.rectangle.getP1().getY() < pt.getY() < box.rectangle.getP2().getY():
                    handle_input(box_text, field, max_length=max_lengths[field],
                                 allowed_chars=allowed_characters[field])

            # Return button
            if return_button.rectangle.getP1().getX() < pt.getX() < return_button.rectangle.getP2().getX() and \
                    return_button.rectangle.getP1().getY() < pt.getY() < return_button.rectangle.getP2().getY():
                edit_win.close()
                return ["dashboard", login_system, username]

            # Save Changes
            if submit_button.rectangle.getP1().getX() < pt.getX() < submit_button.rectangle.getP2().getX() and \
                    submit_button.rectangle.getP1().getY() < pt.getY() < submit_button.rectangle.getP2().getY():
                updated_data = {
                    "Password": boxes["Password"][1].get_text(),
                    "Name": boxes["Name"][1].get_text(),
                    "Surname": boxes["Surname"][1].get_text(),
                    "Gender": boxes["Gender"][1].get_text(),
                    "Height (cm)": boxes["Height (cm)"][1].get_text(),
                    "Weight (kg)": boxes["Weight (kg)"][1].get_text(),
                    "Date of Birth": {
                        "Day": dob_boxes["Day"][1].get_text(),
                        "Month": dob_boxes["Month"][1].get_text(),
                        "Year": dob_boxes["Year"][1].get_text()
                    }
                }

                # Update the user's data in the database
                login_system.database[username].update(updated_data)
                login_system.save_database()
                print("Profile updated successfully!")
                edit_win.close()
                return ["dashboard", login_system, username]



def main():
    # Initialize the login system
    login_system = LoginSystem()

    actualScreen = create_login_window(login_system= login_system, transition="yes")
    while actualScreen[0] != "exit":
        if actualScreen[0] == "dashboard":
            actualScreen = create_dashboard_page(actualScreen[1], actualScreen[2])
        elif actualScreen[0] == "signup":
            actualScreen = create_signup_page(actualScreen[1])
        elif actualScreen[0] == "best_exercise":
            actualScreen = create_best_exercise_page(actualScreen[1], actualScreen[2])
        elif actualScreen[0] == "create_chart":
            actualScreen = create_chart_interface(actualScreen[1], actualScreen[2])
        elif actualScreen[0] == "edit_profile":
            actualScreen = edit_profile_page(actualScreen[1], actualScreen[2])
        elif actualScreen[0] == "login":
            actualScreen = create_login_window(login_system=actualScreen[1], transition=actualScreen[2])


if __name__ == "__main__":
    main()