import json
from tabulate import tabulate
def read_file(file):
    with open('materias.txt','r') as f:

        f = f.readlines()
        f = [i.encode("ascii", errors="ignore").decode() for i in f if i!= '\n']
        return f


def make_json():
    dict = {}
    f = read_file('materias.txt')
    f = [i.split('**') for i in f]


    count = 0
    materia_dict = {}
    for i in f:
        materias = i[1].split(',')
        for materia in materias:
            try:
                materia = materia.split('\n')[0]
            except:materia =materia
            materia_dict[materia] = {}
            count += 1
        dict[i[0]] = materia_dict
        count = 0
        materia_dict = {}

    with open('materias.json','w') as f:
        json.dump(dict,f,indent=4)


def read_json(jsonn):
    with open(jsonn,'r') as f:
        a = json.load(f)
        return a


def yes_or_no(prompt):
    chosen = input(prompt)
    if chosen =='y':
        return True

    elif chosen == 'n':
        return False

    else:
        return yes_or_no(prompt)


def cleaning():
    print('\n\n\n\n\n\n\n\n\n\n\n')

def write_to_json(jason,dict):
    with open(f'{jason}.json','w') as f:
        json.dump(dict,f,indent=4)

def prettyfy(alumno):
    headers = []
    headers.insert(0, 'Nombre')

    jason = read_json('alumnos.json')
    for i in jason:
        for keys in jason[i]:
            headers.append(keys)
        break
    to_tabulate = []
    for i in jason:
        if i == alumno:
            key_list = []
            key_list.append(i)
            for evr in jason[i]:
                key_list.append(jason[i][evr])

            to_tabulate.append(key_list)


    print(tabulate([i for i in to_tabulate], headers=headers, tablefmt='orgtbl'))

def display_indices_with_key_name(list_to_loop):
    '''return indices_list, indices_list_name_key_dict'''
    indices_list = []
    key_dict_indices = {}
    index = 0
    for key in list_to_loop:
        indices_list.append(str(index))
        key_dict_indices[str(index)] = key

        print(f'({index}){key}')

        indices_list.append(str(index))
        index += 1



    print(f'({index})Abandonar')
    if len(list_to_loop) > 1:
        indices_list.append(str(index + 1))
        print(f'({index+1})Print all')

    return (indices_list,key_dict_indices,index)


def validate_int(promt):
    is_int = False
    while not is_int:
        num = input(promt)

        if (num).isdigit() == True:
            return  int(num)


def check_if_abandonar(palabra,otra_palabra,func):
    if palabra.lower() == 'abandonar':
        cleaning()
        return func()




if __name__ == "__main__":
    pass


















