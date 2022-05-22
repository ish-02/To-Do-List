from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    menu_options = {'1': "Today's tasks",
                    '2': "Week's tasks",
                    '3': "All tasks",
                    '4': "Missed tasks",
                    '5': "Add task",
                    '6': "Delete task",
                    '0': "Exit"}


    def menu(opts):
        """

        :type opts: dict
        """
        for item in opts:
            print(f"{item}) {opts.get(item)}")


    def print_list(lis, show_dead=False):
        """
        :type show_dead: bool
        :type lis: list
        """
        if len(lis) == 0:
            print("Nothing to do!")
        else:
            for item in lis:
                print(f"{lis.index(item) + 1}. {item.task}. {item.deadline.strftime('%#d %b') if show_dead is True else ''}".strip())
        print()


    while True:
        menu(menu_options)
        opted = input()
        if opted in menu_options:
            if opted == '0':
                print("\nBye!")
                exit()
            else:
                if opted == '1':
                    date = datetime.today().date()
                    rows = session.query(Table).filter(Table.deadline == date).all()
                    print(f"\nToday {date.strftime('%d %b')}:")
                    print_list(rows)

                elif opted == '2':
                    print()
                    for i in range(7):
                        date = (datetime.today() + timedelta(days=i)).date()
                        rows = session.query(Table).filter(Table.deadline == date).all()
                        print(f"{date.strftime('%A %d %b')}:")
                        print_list(rows)

                elif opted == '3':
                    rows = session.query(Table).order_by(Table.deadline.asc()).all()
                    print("\nAll tasks:")
                    print_list(rows, show_dead=True)

                elif opted == '4':
                    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline.asc()).all()
                    print("\nMissed tasks:")
                    if len(rows) == 0:
                        print("Nothing is missed!")
                    else:
                        print_list(rows, show_dead=True)

                elif opted == '5':
                    task = input("Enter task\n")
                    date = input("Enter deadline\n")
                    try:
                        new_row = Table(task=task, deadline=datetime.strptime(date, '%Y-%m-%d'))
                        session.add(new_row)
                        session.commit()
                    except Exception as e:
                        print(e)
                    else:
                        print("The task has been added!\n")
                elif opted == '6':
                    rows = session.query(Table).order_by(Table.deadline.asc()).all()
                    print("\nChoose the number of the task you want to delete:")
                    print_list(rows, show_dead=True)
                    task_no = int(input())
                    try:
                        session.delete(rows[task_no - 1])
                        session.commit()
                    except Exception as e:
                        print(e)
                    else:
                        print("The task has been deleted!")


        else:
            print("Invalid option!")
