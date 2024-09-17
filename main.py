import json
import os
from funcs import read_json,check_if_abandonar
import subprocess
import random
from admin import Admin,admin_password
import datetime
#from Busqueda_extra import Busqueda
import Busqueda_extra
mensaje_abandonar = 'PARA ABANDONAR SIN GUARDAR ESCRIBE --> ABANDONAR'
class Materias():
    def __init__(self):
        self.json_file = self.reading_alumnos()
        self.alumno_information = {}
        self.carrera = ''
        self.sexo = ''
        self.materias = []
        self.matricula = ''

        self.new_dict = {}

        self.edad = 9
        self.apellido_materno = ''
        self.apellido_paterno = ''
        self.curpp = ''

        self.dia = ''
        self.mes = ''
        self.anno = ''
        self.fecha_attempts = 0
        self.fecha_de_nacimiento_string = ''

        self.current_alumno_key = ''

        self.list_of_dicts_to_write = []

        self.anno  = 0
        self.dia = 0
        self.mes = 0

        self.next_step_of_this = False
        self.weird_symbols =['!',"@","#","$","%","^","&","*","(",")","-","_","=","+","[","]","{","}","|",";",":","'","?",",","<",">","?","/","`","~"," "]
        self.nums = ['1','2','3','4','5','6','7','8','9']






    def alumno_o_admin(self):

        '''Este es el hub'''
        print('--------\nMAIN HUB\n--------')
        chose = input('Alumno(0),Admin(1),Abandonar(2)\nEscoge: ')
        if chose == '0':
             if self.name_edad() != False: #If true
                return self.asking()

        elif chose == '1':
            return self.admin() #Se va al hub de admin
        elif chose == '2':
            print('Exiting')
            exit()

        else:
            self.cleaning()
            print('Escoga 0 o 1')
            return self.alumno_o_admin()

    def asking(self):
        '''Pregunta si quiere inscribirse o abandonar sin guardar los datos pasados'''
        
        chose = (input('Que quieres hacer\nInscribirse(1),Abandonar sin guardar(2)\nEscoger: '))


        if chose == '1':
            return self.inscribirse() #Llama esta func

        elif chose == '2':
            self.cleaning()
            print('Exiting')
            return exit()  #Puse esto aqui porque al inicio tenia problemas trying to end the program when it was supposed to end
                            #Because when i was calling a function, i didnt end the function that called that function with return
                            #So i searched how to terminate a python program, and eso aparecio.


        else:
            self.cleaning()
            print('Porfavor, escoger una de las opciones')
            return self.asking()


    def inscribirse(self):
        '''Imprime las carreras de materias.json, cuando se escoge una carrera
        el programa regresa con ramndom choice 3 materias de la carrera
        Aqui se llama al a funcion que crea la matricula con random module'''
        self.cleaning()
        print('Nuestras carreras son:\n ')

        a = read_json('materias.json')
        for i in a:
            print(i)

        chose = input('Cual escoges?: ').lower()

         #looping through materias
        materias_whole = []
        materias = []
        carreras = [i for i in a]
        if chose in carreras:

            for x in a[chose.lower()]:  #Loops through subjects
                materias_whole.append(x)
                #print(x)


            while len(materias) <3: #3 materias
                materia = random.choice(materias_whole)
                if materia not in materias:
                    materias.append(materia)

            self.materias = materias
            self.carrera = chose
            self.creating_matricula()



            self.data_to_alumnos() #Llama esta cunfion

            self.cleaning()
            print(f'Tus materias son: {self.materias}')
            return self.anything_else() #Si al hub, no bye bye






        else:
            self.cleaning()
            print('No tenemos esa carrera')
            return self.inscribirse() #Volver a llamar

    def data_to_alumnos(self):
        '''Aqui se asigna las keys con los values proporcionados posteriormente'''

        self.alumno_information['edad'] = self.calculando_edad() #Aqui se llama esta func
        self.alumno_information['carrera'] = self.carrera
        self.alumno_information['materias'] = self.materias
        self.alumno_information['matricula'] = self.matricula
        self.alumno_information['genero'] = self.sex
        self.alumno_information['apellido_materno'] = self.apellido_materno.lower() #Lower por si acaso
        self.alumno_information['apellido_paterno'] = self.apellido_paterno.lower()
        self.alumno_information['curp'] = self.curpp
        self.alumno_information['full_name'] = self.name + self.apellido_paterno + self.apellido_materno
        self.alumno_information['fecha_nacimiento'] = f'{self.dia}/{self.mes}/{self.anno}'

        self.putting_evrything_together() #Pone lo que leyOO en el alumnos.json y lo pone en new dict

        self.new_dict[f'{self.name.lower()}_{self.apellido_paterno.lower()}_{self.apellido_materno.lower()}'] = self.alumno_information
        #Guarda Nombre_Apellido_Apellido as key with dict of  rest of information


        with open('alumnos.json','w') as f:
            json.dump(self.new_dict,f,indent=4)
            #Pone el new dict a alumnos.json




    def reading_alumnos(self):
        '''Reads json in try, if there is nothing, returns empty'''
        try:
            with open('alumnos.json','r') as f:
                f = json.load(f)
                return f
        except: return {}


    def creating_matricula(self):
        '''Crea matricula con $ y numeros aleatorios
        Se puede implementar leer las matriculas de los alumnos y verificar que no se repitan
        O se podrian crear matriculas con un significado, tal vez con los datos de la fecha de nacimiento'''

        matricula_length = 6
        matricula = '$'
        nums = [1,2,3,4,5,6,7,8,9]
        for i in range(matricula_length):
            matricula += str(random.choice(nums))

        self.matricula = matricula
        return print(self.matricula)


    def entering_admin_password(self):
        '''Checar si la password es 123 y regresar True, exit = return False'''
        self.cleaning()
        self.cleaning()

        chose = input("Enter password admin or exit: ")
        while chose != admin_password and chose != 'exit':
            chose = input("Enter password admin or exit: ")

        if chose == admin_password:
            return True
        else:
            return False



    def admin(self):
        '''Si la password es correcta, inicia el hub de admin
        Si is_admin = False, regresa main hub'''


        is_admin = self.entering_admin_password()
        print(is_admin)
        if is_admin == True:
            self.cleaning()
            return Admin().update() #aqui bruh


        else:
            self.cleaning()
            print('Eres alumno')
            return Materias().update()


    def cleaning(self):
        '''Limpia'''
        print('\n\n\n\n\n\n\n\n\n\n')

    def name_edad(self):
        self.cleaning()
        '''Asks for full name, calls fecha func,asks for gender'''
        edad,sexos,count= True,True,0
        name_bool,paterno_bool,materno_bool = False,False,False

        ###Test name
        while not name_bool:
            print(mensaje_abandonar)
            self.name = input("Cual es tu nombre: ")
            check_if_abandonar(self.name,mensaje_abandonar,Materias().update)


            name_bool = self.checkif_nombres_have_num(self.name) #Function to try name

            one_word = self.check_if_only_one_word(self.name) #Function to try length of name
            if name_bool and one_word:
                name_bool = True
                self.cleaning()

        ###Lo mismo de arriba
        while not paterno_bool:
            print(mensaje_abandonar)
            self.apellido_paterno = input("Apellido paterno: ")
            check_if_abandonar(self.apellido_paterno,mensaje_abandonar,Materias().update)


            paterno_bool = self.checkif_nombres_have_num(self.apellido_paterno)
            one_word = self.check_if_only_one_word(self.apellido_paterno)
            if paterno_bool and one_word:
                paterno_bool = True
                self.cleaning()

        ###Lo mismo de arriba
        while not materno_bool:
            print(mensaje_abandonar)
            self.apellido_materno = input("Apellido materno: ")
            check_if_abandonar(self.apellido_materno,mensaje_abandonar,Materias().update)

            materno_bool = self.checkif_nombres_have_num(self.apellido_materno)
            one_word = self.check_if_only_one_word(self.apellido_materno)
            if materno_bool and one_word:
                materno_bool = True
                self.cleaning()

        self.current_alumno_key = f'{self.name}_{self.apellido_paterno}_{self.apellido_materno}' # Guarda la key para usar despues


        if self.checar_si_un_nombre_ya_existe(): # Looks into  alumnos.json keys  and checks if there is one with same name,apellido materno paterno
            self.cleaning()
            print('Ese Alumno ya existe en la base de datos')
            return self.alumno_o_admin() #Te regresa al hub
        else:

            self.cleaning()
            self.fecha_de_nacimiento() #Ahora pregunta la fecha

            self.cleaning()

            ###While hasta que se escoja 1 o 2
            while sexos:
                try:
                    sex = input('Sexo\nHombre(1)\nMujer(2)\nEscoger: ').lower()
                except:sex='3'
                if sex == '1':
                    self.sex = 'Hombre'
                    sexos = False
                    self.cleaning()
                elif sex == '2':
                    self.sex = 'Mujer'
                    sexos = False
                    self.cleaning()


                else:
                    self.cleaning()
                    print('Choose (1) or (2)')
            self.next_step_of_this = True
            return True


    def curp(self):
        '''Checks if curp is of length of 18, if greater or less, calls again func
            Checks if curp contains weird symbols, if so, calls again func

            El curp esta compuesto esta formado por la fecha de nacimiento de la persona,
            Yo no implemntee checar si coincide, pero se puede hacer'''
        #weird_symbols =['!',"@","#","$","%","^","&","*","(",")","-","_","=","+","[","]","{","}","|",";",":","'","?",",","<",">","?","/","`","~"," "]
        weird_symbol_count = 0
        ready,all_ready = False,False
        print(mensaje_abandonar)
        curp = input('Entra tu CURP:')
        check_if_abandonar(curp,'bre',Materias().update)
        while not all_ready:
            while not ready:
                for i in curp:

                    if i in self.weird_symbols:
                        weird_symbol_count +=1
                        self.cleaning()
                        print('Simbolo que no es alfanumerico fue detectado')
                if weird_symbol_count == 0:
                    ready = True
                else:
                    print(mensaje_abandonar)
                    curp = input('Entra tu CURP:')

                    weird_symbol_count = 0


            if len(curp)  == 18:
                all_ready = True
                return curp

            else:
                self.cleaning()
                print(mensaje_abandonar)
                print(f'Curp length was of {len(curp)}')
                print(f'Your previous attempt was {curp}')
                curp = input('Entra tu CURP:')
                check_if_abandonar(curp, 'bre', Materias().update)

                ready = False

    def fecha_de_nacimiento(self):
        '''Checar si es muy viejo o muy joven
        Checar si no hay mas dias de los que hay en el mes
        Correr luego el curp'''

        error_anno_texto = 'Parece que el anno que has entrado es ficticio. El anno es muy viejo, muy reciente, o del futuro'
        error_mes = 'Has entrado un mes que no existe'
        error_dia_mes = 'Haz hecho algo mal'

        anno_texto_bool = False
        error_mes_bool = False
        error_dia_mes_bool  = False
        error_count = 0
        count_of_satiety = 0

        every_thing_satisfied = False

        meses = {
        31: [1, 3, 5, 7, 8, 10, 12],
        28: [2],
        30: [4, 6, 9, 11]
        }


        #while not every_thing_satisfied:
        print(mensaje_abandonar)
        chose = input('Entra tu fecha de nacimiento asi dd mm yy\nEjemplo: 14 8 2000\nPon: ')
        check_if_abandonar(chose, mensaje_abandonar, Materias().update)

        try:
            chose = chose.split()
            dia = int(chose[0])
            mes = int(chose[1])
            anno = int(chose[2])

        except:
            dia = 20000
            mes=20000
            anno=20000
        if anno > datetime.date.today().year or anno > (datetime.date.today().year -15) or anno < 1930:
            anno_texto_bool = True
            error_count += 1

        if mes > 12 or mes < 1:
            error_mes_bool = True
            error_count += 1

        #checar dia
        for i in meses:
            if mes in meses[i]:
                if dia > i or dia <1:
                    error_dia_mes_bool = True
                    error_count += 1

                    break
            if dia < 1:
                error_dia_mes_bool =True
                error_count += 1
                break

        if error_count == 0:
            self.cleaning()
            print('good job')
            self.dia = dia
            self.mes = mes
            self.anno = anno
            self.curpp = self.curp() #Hace la funcion curp y regresa curp
            return self.curpp #Modificado aqui


        else:
            self.cleaning()
            print('------------------------------------------------------------------------------------')
            if error_mes_bool:
                print(error_mes)

            if anno_texto_bool:
                print(error_anno_texto)

            if error_dia_mes_bool:
                print(error_dia_mes)
            print(f'errores = {error_count}')
            print('\n')
            return self.fecha_de_nacimiento()




    def anything_else(self):
        '''Pregunta si o no'''
        chose = input('Anything else(y/n): ').lower()
        if chose == 'y':
            self.cleaning()
            return Materias().update()
        elif chose == 'n':
             print('Exiting')
             return exit()

        else:
            return self.anything_else()



        count_of_satiety = 0


    def calculando_edad(self):
        '''Con la fecha de nacimiento dada, calcular la edad de la personas usando datetime'''
        base = datetime.date.today()
        year = base.year - self.anno
        mes = base.month - self.mes # if this + = means i substract from year else, I add to the year else = 0, i dont add
        dia = base.day - self.dia #same month principle i think

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

    def checar_si_un_nombre_ya_existe(self):
        '''Checa nombre completo de los estudiantes de alumnos.json
        con la persona que se esta inscribiendo'''
        try:
            jason = read_json('alumnos.json')

            for i in jason:
                if i == f'{self.name.lower()}_{self.apellido_paterno.lower()}_{self.apellido_materno.lower()}':
                    return True

            return False
        except:pass


    def adding_to_count_of_same_name(self):
        '''No esta en uso por el momento'''
        try:
            jason = read_json("count_of_same_name.json")
        except:pass


    def checkif_nombres_have_num(self,nombre):
        '''This functions makes sures that the nombre y apellidos que no contengan
        numeros, ni simbolodos raros.'''
        error_count = 0
        for i in self.nums:
            if i in nombre:
                error_count += 1

        for i in self.weird_symbols:
            if i in nombre:
                error_count += 1

        if error_count > 0:
            return False

        else:
            return True


    def check_if_only_one_word(self,nombre):
        '''Checks if user entered more than 1 word'''
        if len(nombre.split()) > 1:
            #print('bruh')
            return False

        else:

            return True

    def putting_evrything_together(self):
        '''Por alguna razon decidi to create another dict instead of modifying the
        json that i had already read, my thinking was not on point and
        Lo que hace es guardar json file en new dict'''

        for i in self.json_file:
            self.new_dict[i] = self.json_file[i]

    def update(self):
        '''Esto es para que cuando se llame esto, se cree une nueva instancia
        de Materias y se cierre la otra, para poder escribir en el json sin tener que terminar
        con el programa, ni tener que complicarme en agregar la informacion en una lista con los dicts.'''
        return Materias().alumno_o_admin()



















