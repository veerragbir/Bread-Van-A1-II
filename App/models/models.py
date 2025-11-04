from App.database import db

# Resident Model
class Resident(db.Model):
    __tablename__ = "residents"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("streets.id"), nullable=False)

    # Relationships
    street = db.relationship("Street", back_populates="residents")
    stop_requests = db.relationship("StopRequest", back_populates="resident", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Resident {self.username} on {self.street.name}>"

# Driver Model
class Driver(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default="Idle")  # Idle, EnRoute, Delivering for future additions/modifications 

    schedules = db.relationship("Schedule", back_populates="driver", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Driver {self.username} | Status: {self.status}>"

# Street Model
class Street(db.Model):
    __tablename__ = "streets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    residents = db.relationship("Resident", back_populates="street", cascade="all, delete-orphan")
    schedules = db.relationship("Schedule", back_populates="street", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Street {self.name}>"

# Schedule Model
class Schedule(db.Model):
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("streets.id"), nullable=False)
    scheduled_time = db.Column(db.String(50), nullable=False)  

    # Relationships
    driver = db.relationship("Driver", back_populates="schedules")
    street = db.relationship("Street", back_populates="schedules")
    stop_requests = db.relationship("StopRequest", back_populates="schedule", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Schedule Driver:{self.driver.username} Street:{self.street.name} at {self.scheduled_time}>"

# StopRequest Model
class StopRequest(db.Model):
    __tablename__ = "stop_requests"

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("residents.id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False)
    note = db.Column(db.String(200))
    status = db.Column(db.String(20), default="Pending")  # Pending, Accepted, Rejected for future additions/modifications

    # Relationships
    resident = db.relationship("Resident", back_populates="stop_requests")
    schedule = db.relationship("Schedule", back_populates="stop_requests")

    def __repr__(self):
        return f"<StopRequest Resident:{self.resident.username} Schedule:{self.schedule.id} Status:{self.status}>"
