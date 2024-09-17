import json
import datetime
from tabulate import tabulate
from funcs import yes_or_no,cleaning,prettyfy
import Busqueda_extra

import main
import cambiar_carrera
admin_password = '123'
from funcs import  read_json
class Admin():
    def __init__(self):
        self.current_alumno_key = ''

        self.alumnos_dict_storage = {}
        self.new_dict = {}

        self.alumnos_materias_storage = {}

        alumnos = read_json('alumnos.json')
        self.alumnos_dict_storage = alumnos
        try:
            self.debaja_dict =read_json('Debaja.json')
        except:
            self.debaja_dict = {}
            #print('bruh')


    def main_menu(self):
        '''Admin main hub'''
        print('-----\nADMIN\n-----')
        chose = input("Que quieres hacer\nVer alumnos(1)\nBusqueda extra(2)\nAbandonar(3)\nEscoge: ")

        if chose == '1':
            return self.view_alumnos() #calls func


        elif chose == '2':
            self.cleaning()
            return Busqueda_extra.Busqueda().askin() #calls func

        elif chose == '3':
            self.cleaning()
            return main.Materias().update() #Te regresa a main hub

        else:
            self.cleaning()
            return self.main_menu()

    def view_alumnos(self):
        '''Reads alumnos.json, displays an index beside name to select the student
            You can choose to abandon, You can choose to view all students or a single student'''
        self.cleaning()
        alumnos = read_json('alumnos.json')
        alumnos_dict_with_index = {}
        index = 0

        for alumno in alumnos:
            alumnos_dict_with_index[index] = {alumno:alumnos[alumno]}

            print(f'({index}){alumno}')
            index += 1

        print(f'({index})View all their information') #ALL INFORMATION
        print(f'({index+1})Abandonar') #ABANDONAR

        chose = input('escoge: ')
        chose_a_int = False

        ###ADMIN HUB
        if chose == str(index+1):
            cleaning()
            return Admin().update()
            #return self.anything_else()


        '''AQUI HICE ALGO EXTRANNO EN CHECAR SI LA OPCION ES UN INT, YA DESPUES
        ME DI CUENTA QUE PODIA ALMACENAR LOS INDICES COMO STRING EN UNA LISTA Y COMPARAR
        SI EL STRING DE CHOSE ESTA EN LA LISTA DE STR INDICES. SI NO ESTA, PUES VOLVER A LLAMAR
        A LA FUNC, ETC
        
        SE SUPONE QUE LA FUNCION DE ESTO ES ASEGURAR QUE SEA INT'''
        while not chose_a_int:
            self.cleaning()
            if chose == str(index):
                chose_a_int = True

                return self.view_all_information(alumnos)

            else:

                try:

                    '''HICE ALGO EXTRANNO AQUI, PERO FUNCIONAR'''
                    for i in alumnos_dict_with_index[int(chose)]: #Places index and gets alumno key
                        for x in self.ultimate_json_modifier(alumno=i, extra_information='yes'): #CREO QUE ESTO NO HACE NADA

                            cleaning()
                            prettyfy(i) #LLAMA LA FUNC PRETTIFY DE FUNCS PARA IMPRIMIR INFORMACION CON TABULAR


                    for i in alumnos_dict_with_index[int(chose)]: #Saves the key of the alumno to then later use it
                        self.current_alumno_key = i
                    chose_a_int = True
                except:
                    #SE REPITE EL LOOP SI NO ES INDEX
                    index = 0
                    for alumno in alumnos:
                        print(f'{alumno}({index})')
                        index += 1
                    print(f'View all their information({index})')

                    chose = input('escoge: ')

        if chose != str(index):
            return self.askingv1() #PREGUNTA SOBRE MODIFCAR COSAS DEL ALUMNO
        else:
            return self.anything_else() #PREGRUNTA SI ONO

    def check_student_list_len(self):
        '''Checks length of alumnos.json'''
        jason = read_json('alumnos.json')
        return len(jason)
    def view_all_information(self,dict):

        if (self.check_student_list_len()) != 0: #Esto es para no llamar la func sorting cuando no hay alumnos
            return Sorting().update()

        else:
            cleaning()
            print('There are no students :(')
            return Admin().update()  #Return to admin hub




    def Debaja(self):
        '''Guarda a los alumnos que se dan debaja en debaja.json

        Se podria implementar otra clase para recuperar y transferir alguien debaja  a alumnos.json'''
        self.new_dict = {}
        self.putting_together_debaja_dict() #Pone la informacion de debaja en self.debaja_dict


        '''AQUI SE USA SELF.CURRENT ALUMNO DICT,
        LOOPEA EL DICT DE ALUMNOS, SI LA KEY COINCIDE
        CON CURRENT, SE PONE EN DEBAJAS A ESA PERSONA'''
        for i in self.alumnos_dict_storage:
            if i == self.current_alumno_key:

                with open('Debaja.json','w') as f:
                    self.debaja_dict[i] = self.alumnos_dict_storage[i]
                    json.dump(self.debaja_dict,f,indent=4)
            else:
                self.ultimate_json_modifier(alumno=i) #ESTO DEBE DE HACER ALGO

        self.reescribiendo_todo_en_el_json() #Reescribe a alumnos.json
        self.cleaning()
        print(f'{self.current_alumno_key} has been removed')
        return Admin().update()

    def putting_together_debaja_dict(self):
        '''Funcion innecesaria que solamente ocupan espacio
        Pone en debaja dict la informacion de debaja.json'''
        try:
            debajas = read_json('Debaja.json')
            for i in debajas:
                self.debaja_dict[i] = debajas[i]
        except:pass



    def cleaning(self):
        print('\n\n\n\n\n\n\n\n\n\n\n\n')


    def anything_else(self):
        '''Pregunta si o no '''
        chose = input('Anything else(y/n):').lower()
        if chose == 'y':
            self.cleaning()
            return Admin().update()

        elif chose == 'n':
            self.cleaning()
            return print('Exiting')

        else:
             return self.anything_else()

    def askingv1(self,current_key = None):
        '''Pregunta modificar materias, Dar de baja al alumno, y cambiar de carrera'''
        if current_key != None:
            self.current_alumno_key = current_key
        chose = input('(1)Modificar materias\n(2)Dar de baja\n(3)Cambiar de carrera\n(4)Abandonar\nchoose: ')

        if chose == '1':
            return self.modificar_materia() #llama func

        elif chose == '2':
            return self.Debaja() #llama func

        elif chose == '3':
            return cambiar_carrera.Cambiar_Carrera(self.current_alumno_key,self.alumnos_dict_storage[self.current_alumno_key]['carrera'])
            # Llama la clase del documento cambiar carrera, y le pasa los datos necesarios para que pueda trabajar
            #alumno key y nombre de carrera

        elif chose == '4':
            cleaning()
            return Admin().update() #Te manda al admin hub

        else:
            cleaning()
            return self.askingv1() #Volver a preguntar

    def modificar_materia(self):
        '''Me he dado cuenta que he llamado varias que he leido en varias
        funciones el mismo documento, cuando pude haber usado self.alumnos bruh'''

        '''Guarda las materias del alumno en self.alumnos_materias y luego da la opcion de escoger si agregar, o 
        eliminar materias'''
        self.cleaning()
        alumnos = read_json('alumnos.json')
        index = 0

        alumno = alumnos[self.current_alumno_key]
        for materia in (alumno['materias']):
            self.alumnos_materias_storage[index] = materia

            #print(f'{materia}({index})')
            index += 1

        chose = input('Agregar materia(1),Eliminar materia(2)\nchoose: ')

        if chose == '1':
            return self.agregar_materia() #Calls func agregar

        elif chose == '2':
            return self.eliminar_materia(alumno) #calls func eliminar


        else:
            return self.modificar_materia() #recurssion


    def agregar_materia(self):
        mawiki = read_json('materias.json')
        carrera = self.alumnos_dict_storage[self.current_alumno_key]['carrera']
        if len(self.alumnos_dict_storage[self.current_alumno_key]['materias']) == len(mawiki[carrera]):
            cleaning()
            print('There are no more subjects to be added, he has all of them')
            return Admin().update()


        alumno = self.alumnos_dict_storage[self.current_alumno_key]
        carrera = alumno['carrera']
        carrera_materiasjson = []
        materias_lista = []
        #print(carrera)

        jocobo = read_json('materias.json') #lee el json de materias

        for i in jocobo:
            if i == carrera:
                carrera_materiasjson = jocobo[i] #Guarda las materias de la carrera aqui
                break

        index = 0
        index_list = []

        '''Displays materias que no tiene el alumno'''
        for materia in carrera_materiasjson:
            if materia not in alumno['materias']:
                materias_lista.append(materia)
                index_list.append(str(index))
                print(f'({index}){materia}')
                index += 1



        indices = input("Escoge que materias agregar de esta forma 1 3 8 etc o abandonar: ")
        if indices == 'abandonar':
            cleaning()
            return Admin().update()

        desired_format=False

        materias_to_add = [] #Guarda las materias para agregar

        '''Todo esto es para verificar que se haya escogido algo '''
        while not desired_format:
            try:
                indices.split(' ')
                desired_format = True

            except:
                print('Cannot understand the provided format')
                indices = input("Escoge que materias agregar de esta forma 1 3 8 etc: ")




        #print(index_list) #palabraclave

        if desired_format ==True:
            for i in indices.split(' '):
                if i not in index_list:
                    print(f'{i} is not found')
                else:
                    materias_to_add.append(materias_lista[int(i)]) #aqui agrega a las materias para agregar
        #print(carrera_materiasjson)
        tuk = False

        '''Luego aqui checa si se agrego o no se agrego nada a materias_to_ass'''
        while not tuk:
            if len(materias_to_add) == 0:
                chose = input('You chose zero subjects.Would you like to do it again(y) or exit(n): ')

                '''Do it again'''
                if chose == 'y':
                    tuk =True
                    return self.agregar_materia()


                elif chose == 'n': #Returns to admin hub
                    tuk =True
                    #return self.admin()
                    return Admin().update()
                    #return self.main_menu()

                else:
                    print('Choose y or n')

            else:
                #breaks of second loop
                tuk = True

        '''Continues with main loop'''

        alumno_materias = alumno['materias']
        alumno_materias = alumno_materias + materias_to_add #Megers alumno materias with materias to add

        cleaning()

        gender_palabra = 'alumno'
        if self.alumnos_dict_storage[self.current_alumno_key]['genero'].lower() == 'mujer':
            gender_palabra = 'alumna'
        print(f'Se ha agregado al {gender_palabra} {self.current_alumno_key}:')
        [print(i,end=',')for i in materias_to_add]
        print('')
        print('------------------------------------------------------------------------')
        self.new_dict = {}

        '''This is supposed to write everything back to alumnos.json'''
        for i in self.alumnos_dict_storage:
            self.ultimate_json_modifier(alumno=i,materias=alumno_materias)
            self.reescribiendo_todo_en_el_json()

        return Admin().update()
        #return self.anything_else()











    def eliminar_materia(self,alumno):
        if len(self.alumnos_dict_storage[self.current_alumno_key]['materias']) == 0:
            cleaning()
            print(f'{self.current_alumno_key} does not have any subject to be  remove')
            return Admin().update()
        index = 0
        self.cleaning()

        indices_list = []
        indices_dict = {}

        print(f"Materias de {self.current_alumno_key}\n---------------------------------------------")
        for materia in (alumno['materias']):
            self.alumnos_materias_storage[index] = materia

            print(f'({index}){materia}')
            indices_list.append(str(index))
            indices_dict[str(index)] = materia

            index += 1

        print(f'({index})Eliminar todas,({index+1})Abandonar sin borrar nada')
        print("---------------------------------------------")

        print('Example: 0 3 4')
        chose = input("Escoge: ")


        if chose == str(index+1):
            return Admin().update()

        elif chose == str(index):
            #print(self.alumnos_dict_storage)
            cleaning()
            print(f'Se ha eliminado todas las materias de {self.current_alumno_key}')
            self.reescribiendo_materias()
            self.reescribiendo_todo_en_el_json()
            return Admin().update()


        chose = chose.split()
        keys_list = []
        for i in chose:
            if i in indices_list:
                keys_list.append(indices_dict[i])

        if len(keys_list) == 0:
            cleaning()
            print('You have chosen 0 indices')
            return self.eliminar_materia(self.current_alumno_key)

        else:


            materias = self.eliminar_materia_por_index(keys_list)
            self.reescribiendo_materias(materias)
            self.reescribiendo_todo_en_el_json()

            cleaning()
            print(f'Successfully deleted {[i for i in keys_list]}')
            return Admin().update()



    def eliminar_todas(self):
        self.alumnos_materias_storage = []

    def eliminar_materia_por_index(self,materias_to_eliminate):
        new_materias = []
        materias_to_eliminate = materias_to_eliminate
        for i in self.alumnos_materias_storage:
            print(i)
            if self.alumnos_materias_storage[i] not in materias_to_eliminate:
                new_materias.append(self.alumnos_materias_storage[i] )

        print(new_materias)
        return new_materias






    def reescribiendo_materias(self,elminar_una_materia=None,agregar_materias = None): #Eliminando materia?

        for i in self.alumnos_dict_storage:

            base = self.alumnos_dict_storage[i]




            # carrera = base['carrera']
            if i != self.current_alumno_key:
                materias = base['materias']
            else:
                if elminar_una_materia != None:
                    materias = elminar_una_materia
                else:
                    materias = []

            self.ultimate_json_modifier(alumno=i,materias=materias)

        #print(self.new_dict)

    def reescribiendo_todo_en_el_json(self):
        with open('alumnos.json','w') as f:
            json.dump(self.new_dict,f,indent=4)


    def ultimate_json_modifier(self,alumno,edad=None,carrera=None,materias=None,matricula=None,genero=None,
                               apellido_materno=None,apellido_paterno=None,curp=None,full_name=None,extra_information=None,dict_for_some_reason=None,fecha_nacimiento=None):
        '''I will try to make everything modifiable in this function
        Si pones yes en extra stuff, te regresa una lista con informacion'''
        alumno = alumno
        #for i in self.alumnos_dict_storage:

        base = self.alumnos_dict_storage[alumno]
        dict_of_things = {
            'edad': self.calculando_edad(base['fecha_nacimiento']),
            'carrera': base['carrera'],
            'materias': base['materias'],
            'matricula': base['matricula'],
            'genero': base['genero'],
            'apellido_materno': base['apellido_materno'],
            'apellido_paterno': base['apellido_paterno'],
            'curp': base['curp'],
            'full_name': base['full_name'],
            'fecha_nacimiento':base['fecha_nacimiento']
        }
        if extra_information != None:
            listof = [f'{i}:{dict_of_things[i]}' for i in dict_of_things]
            listof.insert(0,f'Nombre:{alumno}')
            return [listof]
        #print('bruh')
        if alumno == self.current_alumno_key:
            if edad != None:
                dict_of_things['edad'] = edad


            if carrera != None:
                dict_of_things['carrera'] = carrera

            if materias != None:
                dict_of_things['materias'] = materias

            if matricula != None:
                dict_of_things['matricula'] = matricula

            if genero != None:
                dict_of_things['genero'] = genero

            if apellido_materno != None:
                dict_of_things['apellido_materno'] = apellido_materno

            if apellido_paterno != None:
                dict_of_things['apellido_paterno'] = apellido_paterno

            if curp != None:
                dict_of_things['curp'] = curp

            if full_name != None:
                dict_of_things['full_name'] = full_name

            if fecha_nacimiento != None:
                dict_of_things['fecha_nacimiento'] = fecha_nacimiento

        self.new_dict[alumno] = dict_of_things


    def calculando_edad(self,fecha):
        fecha = fecha.split('/')
        base = datetime.date.today()
        year = base.year - int(fecha[2])
        mes = base.month - int(fecha[1]) # if this + = means i substract from year else, I add to the year else = 0, i dont add
        dia = base.day - int(fecha[0] )  #same month principle i think

        mes = mes / 12
        if mes < 0:
            year += mes

        elif mes > 0:
            year -= mes

        elif mes == 0:
            pass

        dia = dia / 365
        if dia < 0:
            year += dia

        elif dia > 0:
            year -= dia

        elif dia == 0:
            pass

        edad = year

        return edad

    def update(self):
        self.main_menu()







class Sorting():

    def __init__(self,individual=None):
        self.individual = individual

    def main_menu(self):
        chose = input("(1)Print all atributes\n(2)Filter\n(3)Abandonar\nChoose: ")

        if chose == '1':
            return self.print_everything()

        elif chose =='2':
            return self.filtering()

        elif chose == '3':
            return Admin().update()




    def print_everything(self,nombre_especifico=None,edad_rango=None):
        '''Nombre especifico se va a usar en el modulo de Busqueda extra'''
        headers = []
        headers.insert(0, 'Nombre')


        jason = read_json('alumnos.json')
        for i in jason:
            for keys in jason[i]:
                headers.append(keys)
            break
        to_tabulate = []

        #Prints everything without filter
        if nombre_especifico == None and edad_rango ==None:
            for i in jason:

                key_list = []
                key_list.append(i)
                for evr in jason[i]:
                    key_list.append(jason[i][evr])

                to_tabulate.append(key_list)

        elif edad_rango != None:
            for i in jason:
                edad = jason[i]['edad'].__floor__()

                if edad > edad_rango[0] and edad < edad_rango[1]:
                    key_list = []
                    key_list.append(i)
                    for evr in jason[i]:
                        key_list.append(jason[i][evr])

                    to_tabulate.append(key_list)


        else:
            for i in jason:

                if i.split('_')[0].lower() == nombre_especifico.lower():
                    key_list = []
                    key_list.append(i)
                    for evr in jason[i]:
                        key_list.append(jason[i][evr])

                    to_tabulate.append(key_list)
            return print(tabulate([i for i in to_tabulate], headers=headers, tablefmt='orgtbl'))

        print(tabulate([i for i in to_tabulate], headers=headers, tablefmt='orgtbl'))
        if yes_or_no('Would you like to do it again(y/n): ') == True:
            cleaning()
            return Admin().view_alumnos()

        else:
            cleaning()
            return Admin().update()

    def printing_keys(self):
        jason = read_json('alumnos.json')
        # [[print(key) for key in (jason[i])] for i in jason]
        indexxed_keys = {}

        index = 0
        for i in jason:
            size = 0
            for key in jason[i]:
                print(f'({index}){key}')
                indexxed_keys[str(index)] = key
                index += 1

            break

        print('Example 0 2 3')
        chose = input('Enter the indexes to view: ')

        chose = chose.split()
        chose = [i for i in chose if i in indexxed_keys]  # Checks whether index in indexes
        keys_filterd_list = [indexxed_keys[i] for i in chose]


        return keys_filterd_list


    def filtering(self):
        jason = read_json('alumnos.json')
        bruh = self.printing_keys()
        keys_filterd_list = bruh

        if len(keys_filterd_list) != 0:
            to_tabulate = []
            for i in jason:
                key_list = []
                key_list.append(i)
                for key in keys_filterd_list:
                    key_list.append(jason[i][key])

                to_tabulate.append(key_list)



            keys_filterd_list.insert(0,'nombre')

            # print(keys_filterd_list)
            cleaning()
            print(tabulate([i for i in to_tabulate], headers=keys_filterd_list, tablefmt='orgtbl'))

            if yes_or_no('Would you like to do it again(y/n): ') == True:
                cleaning()
                return Admin().view_alumnos()

            else:
                cleaning()
                return Admin().update()

        else:
            if yes_or_no('You have entered 0 indices\nWould you like to try again(y/n): ') == True:
                return self.filtering()
            else:
                pass























    def update(self):
        Sorting().main_menu()



#Sorting().update()

