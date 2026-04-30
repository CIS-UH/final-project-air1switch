import flask
import mysql.connector
from flask import request, jsonify, make_response

# create app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# connect to AWS database
def getDb():
    return mysql.connector.connect(
        host="cis2368-database.c1oqo2o88zpa.us-east-2.rds.amazonaws.com",   # AWS endpoint link
        user="admin",           # username
        password="eaortiz6",    # password
        database="ticketsystem" # database name
    )

levelMap = {
    "Bronze": 1,
    "Silver": 2,
    "Gold": 3
}

# routing
@app.route("/")
def home():
    return {"message": "Event manager API running"}


# member apis
# creating a member
@app.route("/members", methods=["POST"])
def createMember():
    data = request.json
    db = getDb()
    cursor = db.cursor()
    query = """
    INSERT INTO member (name, details, title, level)
    VALUES (%s,%s,%s,%s)
    """
    cursor.execute(query, (
        data["name"],
        data["details"],
        data["title"],
        data["level"]
    ))
    db.commit()
    return jsonify({"message": "Member created"})


# getting all members
@app.route("/members", methods=["GET"])
def getMembers():
    db = getDb()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM member")
    return jsonify(cursor.fetchall())


# getting a member
@app.route("/members/<int:memberId>", methods=["GET"])
def getMember(memberId):
    db = getDb()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM member WHERE id=%s", (memberId,))
    return jsonify(cursor.fetchone())


# updating a member
@app.route("/members/<int:memberId>", methods=["PUT"])
def updateMember(memberId):
    data = request.json
    db = getDb()
    cursor = db.cursor()
    query = """
    UPDATE member
    SET name=%s, details=%s, title=%s, level=%s
    WHERE id=%s
    """
    cursor.execute(query, (
        data["name"],
        data["details"],
        data["title"],
        data["level"],
        memberId
    ))
    db.commit()
    return jsonify({"message": "Member updated"})


# deleting a member
@app.route("/members/<int:memberId>", methods=["DELETE"])
def deleteMember(memberId):
    db = getDb()
    cursor = db.cursor()
    cursor.execute("DELETE FROM member WHERE id=%s", (memberId,))
    db.commit()
    return jsonify({"message": "Member deleted"})


# event apis

# creating an event
@app.route("/events", methods=["POST"])
def createEvent():
    data = request.json
    db = getDb()
    cursor = db.cursor()
    query = """
    INSERT INTO event (name, capacity, level, date)
    VALUES (%s,%s,%s,%s)
    """
    try:
        cursor.execute(query, (
            data["name"],
            data["capacity"],
            data["level"],
            data["date"]
        ))
        db.commit()
    except mysql.connector.Error:
        return jsonify({"error": "Event already exists on that date"}), 400
    return jsonify({"message": "Event created"})


# getting all events
@app.route("/events", methods=["GET"])
def getEvents():
    db = getDb()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM event")
    return jsonify(cursor.fetchall())


# getting an event
@app.route("/events/<int:eventId>", methods=["GET"])
def getEvent(eventId):
    db = getDb()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM event WHERE id=%s", (eventId,))
    return jsonify(cursor.fetchone())


# updating an event
@app.route("/events/<int:eventId>", methods=["PUT"])
def updateEvent(eventId):
    data = request.json
    db = getDb()
    cursor = db.cursor()
    query = """
    UPDATE event
    SET name=%s, capacity=%s, level=%s, date=%s
    WHERE id=%s
    """
    cursor.execute(query, (
        data["name"],
        data["capacity"],
        data["level"],
        data["date"],
        eventId
    ))
    db.commit()
    return jsonify({"message": "Event updated"})


# deleting an event
@app.route("/events/<int:eventId>", methods=["DELETE"])
def deleteEvent(eventId):
    db = getDb()
    cursor = db.cursor()
    cursor.execute("DELETE FROM event WHERE id=%s", (eventId,))
    db.commit()
    return jsonify({"message": "Event deleted"})


# registration apis

# signing up for an event
@app.route("/registrations", methods=["POST"])
def createRegistration():
    data = request.json
    db = getDb()
    cursor = db.cursor(dictionary=True)
    memberId = data["memberId"]
    eventId = data["eventId"]

    # member level
    cursor.execute("SELECT level FROM member WHERE id=%s", (memberId,))
    member = cursor.fetchone()

    # event level and capacity
    cursor.execute("SELECT level, capacity FROM event WHERE id=%s", (eventId,))
    event = cursor.fetchone()
    if not member or not event:
        return jsonify({"error": "member/event not found"}), 404
    
    # level check
    if levelMap[member["level"]] < levelMap[event["level"]]:
        return jsonify({"error": "member level too low"}), 400
    
    # capacity check
    cursor.execute(
        "SELECT COUNT(*) AS total FROM registration WHERE event_id=%s",
        (eventId,)
    )
    count = cursor.fetchone()["total"]

    if count >= event["capacity"]:
        return jsonify({"error": "event is full"}), 400
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO registration (event_id, member_id) VALUES (%s,%s)",
            (eventId, memberId)
        )
        db.commit()
    except mysql.connector.Error:
        return jsonify({"error": "Member already registered"}), 400
    return jsonify({"message": "Registration complete"})


# getting all registrations with their details
@app.route("/registrations", methods=["GET"])
def getRegistrations():
    db = getDb()
    cursor = db.cursor(dictionary=True) 
    query = """
    SELECT registration.id,
           member.name AS member,
           event.name AS event
    FROM registration
    JOIN member ON registration.member_id = member.id
    JOIN event ON registration.event_id = event.id
    """
    cursor.execute(query)
    return jsonify(cursor.fetchall())


# deleting a registration
@app.route("/registrations/<int:registrationId>", methods=["DELETE"])
def deleteRegistration(registrationId):
    db = getDb()
    cursor = db.cursor()
    cursor.execute("DELETE FROM registration WHERE id=%s", (registrationId,))
    db.commit()
    return jsonify({"message": "Registration deleted"})

# run the server
if __name__ == "__main__":
    app.run(debug=True)