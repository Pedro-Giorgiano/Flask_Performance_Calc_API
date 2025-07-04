import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# SQLite database connection
engine = create_engine('sqlite:///database.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, ForeignKey('employees.id'), primary_key=True)  # Same ID as employee
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

    employee = relationship("Employee", back_populates="user")


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(String, primary_key=True)  # Same ID as user
    name = Column(String)
    job_level = Column(String)           # Intern, Junior, Mid, etc.
    career_track = Column(String)        # Technical or Management
    time_in_company = Column(Integer)    # In months
    time_in_current_role = Column(Integer)  # In months

    # Relationships
    user = relationship("User", uselist=False, back_populates="employee")
    evaluations = relationship("Evaluation", back_populates="employee")


class Evaluation(Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey('employees.id'))
    semester = Column(String)  # ex: '2023.1', '2024.2'
    scores = Column(JSON)      # Structure: { "Category": { "Item": "Frequency" } }

    employee = relationship("Employee", back_populates="evaluations")


# create the database with initial data
def init_db():
    Base.metadata.create_all(engine)

    if not session.query(User).first():
        # Employees
        emp1 = Employee(
            id='emp001',
            name='João Silva',
            job_level='Mid',
            career_track='Technical',
            time_in_company=30,
            time_in_current_role=12
        )
        emp2 = Employee(
            id='emp002',
            name='Maria Oliveira',
            job_level='Senior',
            career_track='Technical',
            time_in_company=48,
            time_in_current_role=24
        )
        emp3 = Employee(
            id='emp003',
            name='Carlos Director',
            job_level='Director',
            career_track='Management',
            time_in_company=72,
            time_in_current_role=36
        )
        emp4 = Employee(
            id='emp004',
            name='Lucas Martins',
            job_level='Junior',
            career_track='Technical',
            time_in_company=12,
            time_in_current_role=6
        )
        emp5 = Employee(
            id='emp005',
            name='Aline Costa',
            job_level='Tech Lead',
            career_track='Menagement',
            time_in_company=60,
            time_in_current_role=18
        )

        # Users
        users_data = [
            {'id': 'emp001', 'username': 'joao', 'password': '123', 'role': 'collaborator'},
            {'id': 'emp002', 'username': 'maria', 'password': '456', 'role': 'manager'},
            {'id': 'emp003', 'username': 'carlos', 'password': '789', 'role': 'director'},
            {'id': 'emp004', 'username': 'lucas', 'password': 'abc', 'role': 'collaborator'},
            {'id': 'emp005', 'username': 'aline', 'password': 'xyz', 'role': 'manager'}
        ]
        users = []

        for user_data in users_data:
            # generating bcrypt hash
            hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())

            # creating user after encrypting password with bcrypt
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                password=hashed_password.decode('utf-8'),  # ensure that hash is a string
                role=user_data['role']
            )
            users.append(user)



        # Evaluations
        evals = [
            Evaluation(
                employee_id='emp001',
                semester='2023.1',
                scores={
                    "Teamwork": {
                        "Collaborates with peers": "Frequently",
                        "Shares knowledge": "Rarely"
                    },
                    "Technical Quality": {
                        "Delivers with quality": "Rarely"
                    }
                }
            ),
            Evaluation(
                employee_id='emp001',
                semester='2023.2',
                scores={
                    "Teamwork": {
                        "Collaborates with peers": "Almost always",
                        "Shares knowledge": "Almost always"
                    },
                    "Technical Quality": {
                        "Delivers with quality": "Frequently"
                    }
                }
            ),
            Evaluation(
                employee_id='emp002',
                semester='2023.2',
                scores={
                    "Leadership": {
                        "Provides clear direction": "Almost always",
                        "Gives constructive feedback": "Frequently"
                    },
                    "Teamwork": {
                        "Fosters collaboration": "Always"
                    }
                }
            ),
            Evaluation(
                employee_id='emp004',
                semester='2024.1',
                scores={
                    "Teamwork": {
                        "Collaborates with peers": "Rarely",
                        "Shares knowledge": "Never"
                    },
                    "Technical Quality": {
                        "Delivers with quality": "Rarely"
                    }
                }
            ),
            Evaluation(
                employee_id='emp005',
                semester='2023.2',
                scores={
                    "Leadership": {
                        "Supports team growth": "Frequently",
                        "Manages complexity": "Almost always"
                    },
                    "Technical Quality": {
                        "Delivers with quality": "Always"
                    }
                }
            ),
            Evaluation(
                employee_id='emp005',
                semester='2024.1',
                scores={
                    "Leadership": {
                        "Supports team growth": "Always",
                        "Manages complexity": "Always"
                    },
                    "Teamwork": {
                        "Shares knowledge": "Always"
                    }
                }
            ),
        ]

        session.add_all([emp1, emp2, emp3, emp4, emp5])
        session.add_all(users)
        session.add_all(evals)
        session.commit()
