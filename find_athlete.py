import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

class Athelete(Base):

    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

    def say(self):
        print("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(self.id, self.age, self.birthdate, self.gender, self.height, self.name, self.weight,
            self.gold_medals, self.silver_medals, self.bronze_medals, self.total_medals, self.sport, self.country))


def connect_db():

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(id, session):
    fff = session.query(User).filter(User.id == id).first()
    return (fff)

def convert_date(line):
    parts = line.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def parse_DB(user, session):

    goal_height = user.height
    goal_date = user.birthdate

    atheletes = session.query(Athelete).all()

    min1 = 10000000000000
    min2 = None


    for one in atheletes:
        if min2 is None:
            min2 = abs(convert_date(goal_date) - convert_date(one.birthdate))
            found_date = one

        if (one.height is not None and abs(goal_height - one.height) < min1):
            min1 = abs(goal_height - one.height)
            found_height = one

        if (one.birthdate is not None and abs(convert_date(goal_date) - convert_date(one.birthdate)) < min2):
            min2 = abs(convert_date(goal_date) - convert_date(one.birthdate))
            found_date = one
    return found_height, found_date


def main():
    session = connect_db()

    find_id = int(input("Введи ID человека и если он есть в базе данных я найду спортсменов, похожих на него!: "))
    user = find(find_id, session)
    if user is None:
        print("Такого ID нет в базе данных!")
        return
    first, second = parse_DB(user, session)
    print("-----------------------------------------")
    print("У этого спортсмена самый близкий рост!")
    first.say()
    print("-----------------------------------------")
    print("У этого спортсмена самая близкая дата рождения!")
    second.say()



if __name__ == "__main__":
    main()