import os
import zipfile
import base64
import io
import shutil
import warnings
import logging
import pandas as pd

from pathlib import Path
from sqlalchemy import text
from numpy.dtypes import ObjectDType

from config.settings import TRUELINK_SSH_KEY_BASE64
from config.settings import Types, Routes
from utils.custom_data_api import post_to_custom_data_connector
from utils.climateDb import get_connection

warnings.simplefilter("ignore", UserWarning)


def format_text(string):
    trans_dict = dict.fromkeys(' -/', '_')
    trans_dict.update({'ø' : 'oe', 'å' : 'aa', 'æ' : 'ae'})
    return string.lower().translate(str.maketrans(trans_dict))


def write_key_file(path='.', name='key'):
    key_data = base64.b64decode(TRUELINK_SSH_KEY_BASE64).decode('utf-8')
        
    with open(os.path.join(path, name), 'w') as key_file:
        key_file.write(key_data)

    return os.path.abspath(os.path.join(path, name))


def route_files(filelist, connection):
    track_types = []
    for t in list(Types):
        t.value['files'] = []
        track_types.append(t.value)
    
    for f in filelist:
        for t in Types:
            if t.value['keyword'] in f:
                current_tt = next(tt for tt in track_types if tt['keyword'] == t.value['keyword'])
                current_tt['files'].append(f)

    for tt in track_types:
        match tt['route']:
            case Routes.CLIMATE_DB:
                handle_climate_db(tt['files'], connection, tt['prefix'], tt['keyword'])
                pass
            case Routes.BI_SYS:
                handle_bi_sys(tt['files'], connection, tt['prefix'])
                pass
            case _:
                raise TypeError('Unknown route')


def handle_climate_db(files, connection, prefix, keyword):
    with io.BytesIO() as outfile:
        for i, filename in enumerate(files):

            file = connection.open(filename)
            zip = zipfile.ZipFile(file, 'r')

            # Assume just ONE csv file 
            csv_file = [ f for f in zip.namelist() if f.endswith( ('.csv') ) ][0]
            with zip.open(csv_file, 'r') as f:
                if i != 0:
                    f.readline()
                shutil.copyfileobj(f, outfile)

        outfile.seek(0)
        decoded_string = io.StringIO(outfile.read().decode('cp1252'))
        data = pd.read_csv(decoded_string, sep=';')   
        df = pd.DataFrame(data)
        df.columns = [format_text(c) for c in list(df)]
        for col in df.columns:
            if df.dtypes[col] == ObjectDType:
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

                try:
                    df[col] = pd.to_numeric(df[col].str.replace(',','.'))
                except:
                    pass
        
        df['opdateret'] = pd.Timestamp.now()
        df.index.names = ['id']

        table_name = format_text(prefix + '_' + keyword)

        with get_connection() as conn:
            df.to_sql(table_name, con=conn, if_exists='replace')
            conn.execute(text(f'ALTER TABLE `{table_name}` ADD PRIMARY KEY (`id`);'))

    logging.info(f'Updated {keyword}')


def handle_bi_sys(files, connection, prefix):
    for filename in files:
        file = connection.open(filename)
        zip = zipfile.ZipFile(file, 'r')

        # Assume just ONE csv file 
        csv_file = [ f for f in zip.namelist() if f.endswith( ('.csv') ) ][0]
        with zip.open(csv_file, 'r') as f:
            all_lines = f.readlines()

        for i in range(len(all_lines)):
            line = all_lines[i].decode('cp1252')
            
            # Strips leading equal signs from all lines
            if(line[0] == '='):
                line = line[1:]
            line = line.replace(';=', ';')
            line = line.replace('"','')

            # Adds 'n/a' to empty columns in first row - assumes empty columns should be strings
            if i == 1:
                first_line_arr = line.split(';')
                line = ';'.join(['"n/a"' if not e.strip() else e for e in first_line_arr]) + '\n'

            all_lines[i] = line.strip()

        with io.BytesIO() as outfile:
            #file.write('\n'.join(all_lines))
            encoded_outfile = io.TextIOWrapper(outfile, 'utf-8', newline='')
            encoded_outfile.write('\n'.join(all_lines))

            new_filename = Path(filename).stem.replace(' ', '_')
            post_to_custom_data_connector(prefix + new_filename, outfile.getbuffer())

            logging.info(f'Updated {prefix + new_filename}')