from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///DB.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Summary(Base):
    _tablename_ = 'summaries'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    uploads = relationship('Uploads', back_populates='summary')

class Uploads(Base):
    _tablename_ = 'uploads'
    upload_id = Column(Integer, primary_key=True)
    name_of_regulation = Column(String, unique=True)
    latest_version = Column(Integer, ForeignKey('summaries.id'))
    summary = relationship('Summary', back_populates='uploads')

class Graph(Base):
    _tablename_ = 'graphs'
    id = Column(Integer, primary_key=True)
    path = Column(String)

Base.metadata.create_all(engine)


def upload_regulation(name_of_regulation, new_summary_path, new_graph_path):
    existing_upload = session.query(Uploads).filter_by(name_of_regulation=name_of_regulation).first()

    if existing_upload:

        current_summary = session.query(Summary).filter_by(id=existing_upload.latest_version).first()
        current_graph = session.query(Graph).filter_by(id=existing_upload.latest_version).first()

        print("Existing regulation found.")
        print(f"Current Summary Path: {current_summary.path}")
        print(f"Current Graph Path: {current_graph.path if current_graph else 'Not Found'}")


        new_summary = Summary(path=new_summary_path)
        session.add(new_summary)
        session.flush()

        new_graph = Graph(path=new_graph_path)
        session.add(new_graph)


        existing_upload.latest_version = new_summary.id

        session.commit()
        print(f"Updated regulation '{name_of_regulation}' with new summary ID {new_summary.id}.")
    else:

        new_summary = Summary(path=new_summary_path)
        session.add(new_summary)
        session.flush()

        new_graph = Graph(path=new_graph_path)
        session.add(new_graph)

        new_upload = Uploads(
            name_of_regulation=name_of_regulation,
            latest_version=new_summary.id
        )
        session.add(new_upload)

        session.commit()
