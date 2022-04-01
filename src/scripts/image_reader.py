import sys, os
import json
import psycopg2
from typing import Text
from sqlalchemy import create_engine
import numpy as np
from PIL import Image
from psycopg2.extensions import register_adapter


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

def get_image(id):
	
	with engine.begin() as conn:
		query= " SELECT image_array"\
				" FROM container_images"\
				" WHERE id= %(id)s"
		result= conn.execute(Text(query), id= id).all()[0]
	reshaped_result= result[0].reshape(720,960,3)	
	final_result= reshaped_result.astype(np.uint8)
	display_image= Image.fromarray(final_result, 'RGB')
	display_image.show()
	
if __name__ == '__main__':
	
	print('Displaying image')
	get_image(*sys.argv[1:])
		 
		
