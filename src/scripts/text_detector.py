import os, sys
import json
import cv2
import pytesseract
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import numpy as np
import psycopg2
from psycopg2.extensions import register_adapter
from threading import Thread



route = os.getcwd()
new_route = os.path.dirname(route)
sys.path.append(new_route)


from utils import psycopg_functions 
from utils import image

# Setting psycopg2 to upload numpy arrays as binary data
register_adapter(np.ndarray, psycopg_functions.adapt_array)
ARRAY = psycopg2.extensions.new_type(psycopg2.BINARY.values, 
                                    'ARRAY', psycopg_functions.typecast_array)
psycopg2.extensions.register_type(ARRAY)

# Creating Database Engine
#for i in range(2):
    
#    sys.path.append(os.path.dirname(new_route))
print('new path:',sys.path)

with open('../../secrets.json', 'r') as json_file:
    db_secrets = json.load(json_file)
engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(
    user=db_secrets['user'],
    password= db_secrets['password'],
    host = db_secrets['host'],
    db= db_secrets['db']
)
)   
    


# Making a scoped_session for multithreading purposes

session_factory= sessionmaker(bind=engine)
Session= scoped_session(session_factory)


def main():
    #camera settings
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:

        ret, frame = cap.read()
        #RGB colour image for the database
        uploading_image= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)

        n_boxes= len(boxes['text'])
        tags= [x for x in boxes['text'] if x.strip() != '']
        if len(tags) > 0:
            image_name= ' '.join(tags).strip()
            print('Name:', image_name)
            image_class = image.image_loader(image=uploading_image, name=image_name, session= Session)
            image_thread = Thread(target=image_class.upload_to_postgres)
            image_thread.start()
        
        for i in range(n_boxes):
            if boxes['text'][i].strip() != '':
                text, x, y, w, h= boxes['text'][i], boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                frame = cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.0 , (0,0,255), 3)            

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()