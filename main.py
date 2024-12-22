from os.path import isfile
import pandas as pd 
import matplotlib.pyplot as plt
import json 
import argparse

DEFAULT_FILEPATH = './data'
DEFAULT_MSG_FILE = 'message_1.json'
DEFAULT_WRITE_FILE = 'data.csv'

def messages_mode(file):
    data = []
    participants = []

    try:
        # TODO: maybe make this less weird? 
        if isfile(file):
            # INFO: test if file specified by user exists
            with open(file,'r') as f:
                json_data = json.load(f)
                data.extend(json_data['messages'])

                for i in json_data['participants']:
                    participants.append(i['name'])
        else:
            print('User did not specify file! using defaults')
            # INFO: defaults to default path and filename
            with open(f'{file}/{DEFAULT_MSG_FILE}') as f:
                json_data = json.load(f)
                data.extend(json_data['messages'])

                for i in json_data['participants']:
                    participants.append(i['name'])

    except Exception as e:
        print(f'Error! {e}')
        raise e

    df = pd.DataFrame(data)
    df['timestamp_ms'] = pd.to_datetime(df['timestamp_ms'],unit='ms')

    print(f'análise de mensagens de {" - ".join(participants)}')    

    total_msg = df['sender_name'].count()

    print(f'Total de mensagens: {total_msg}')

    print('Número de mensagens por participante')
    print(df['sender_name'].value_counts().to_string(header=False))

    month_groups = df.groupby(df['timestamp_ms'].dt.month).size()

    plt.figure(figsize=(10,6))
    plt.title(f'Número de mensagens por mês (conversa de {" ".join(participants)})')
    month_groups.plot(kind='bar')
    plt.xlabel('Month')
    plt.ylabel('datapoints')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    for i,v in enumerate(month_groups):
        plt.text(i,v +0.5 , str(v),ha='center')
    plt.show()
    #
    # save data to csv
    # df.to_csv('dados.csv')


# def read_dir(path): # TODO: implement a instagram data dir analyser
#
#     directory = os.fsencode(path)
#     for file in os.listdir(directory):
#         filename = os.fsdecode(file)
#         if filename.endswith('.json'):
#             with open(f'{path}/{filename}') as fread:
#                 json_data = json.load(fread)
#                 data.extend(json_data['messages'])

def write_to_file():
    with open(DEFAULT_WRITE_FILE,'w') as fwrite:
        #TODO: implement file writer helper func

        pass

def main(mode:str,file=DEFAULT_FILEPATH):
    match mode:
        case 'm':
            # INFO: passing specified file 
            messages_mode(file)
        # add mode script modes here

if __name__ == '__main__':
    f = DEFAULT_FILEPATH
    parser = argparse.ArgumentParser(description='Instagram data analyser')
    parser.add_argument('-m',action='store_true',help='Read messages file (defaults to ./data/message_1.json)')
    parser.add_argument('-f',type=str,help='Specify file (message_01.json) to be read, defaults to ./data/message_01.json')
    args = parser.parse_args()

    if not args.f:
        print(f'No file specifies, defaulting to {DEFAULT_FILEPATH}/{DEFAULT_MSG_FILE}')
    else:
        f = args.f

    if args.m: 
        print('Script set to Read Messages mode')
        main('m',f)


