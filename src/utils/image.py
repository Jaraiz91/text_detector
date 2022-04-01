from sqlalchemy import  Column, Integer, String, BINARY, TIMESTAMP
from sqlalchemy.orm import declarative_base
import numpy as np
import datetime


Base = declarative_base()

class image_object(Base):
    __tablename__ = 'container_images'

    id = Column(Integer, primary_key=True)
    container_id = Column(String)
    date = Column(TIMESTAMP)
    image_array= Column(BINARY)

    def __repr__(self) -> str:
        return "<User(container_id='%s', date='%s', image_array='%s')>" % (
            self.container_id, self.date, self.image_array
        )




class image_loader:

    def __init__(self,image, name, session):
        self.image = image
        self.name = name
        self.session = session

    def upload_to_postgres(self):
        print('uploading')
        photo_array = np.asfarray(self.image)                                                                                                                                                    
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        thread_session = self.session()
        container_id = self.name
        image_data = image_object(container_id=container_id, date=now, image_array=photo_array)
        thread_session.add(image_data)
        thread_session.commit()
        print('PHOTO UPLOADED:', container_id)

        return 
