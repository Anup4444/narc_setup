from setup.dbsetup import db


class BaseModel(db.Model):
    __abstract__ = True  # This ensures that a table for BaseModel isn't created

    @classmethod
    def update(cls, filter, data):
        cls.query.filter_by(**filter).update(data)
        db.session.commit()

    @classmethod
    def search(cls, filter):
        return cls.query.filter_by(**filter).all()

    @classmethod
    def addData(cls, data):
        new_record = cls(**data)
        db.session.add(new_record)
        db.session.commit()
        return new_record


class Host(BaseModel):
    __tablename__ = 'host'  # Explicitly setting table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class DiagnosticTest(BaseModel):
    __tablename__ = 'diagnostictest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class SuspectedProblem(BaseModel):
    __tablename__ = 'suspectedproblem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class SampleMaterialsSubmitted(BaseModel):
    __tablename__ = '
    '
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)
