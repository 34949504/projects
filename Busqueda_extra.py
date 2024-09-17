from funcs import read_json,display_indices_with_key_name,prettyfy
import main
from funcs import yes_or_no,cleaning,validate_int
import admin
class Busqueda():
    def __init__(self):
        self.meses = {
            '0':'enero',
            '1':'febrero','2':'marzo','3':'abril','4':'mayo','5':'junio','6':'julio','7':'agosto','8':'septiembre','9':'octubre','10':'diciembre'
        }

        self.mayor =0
        self.menor = 0


    def askin(self):
        print('--------------\nBUSQUEDA EXTRA\n--------------')
        chose = input("Escoge como quieres buscar\n(1)Nombre\n(2)Matricula\n(3)Edad\n(4)Mes\n(5)Abandonar\nchoose: ")

        if chose == '1':
            self.cleainng()
            return self.busqueda_nombre('nombre','el')

        elif chose =='2':
            return self.busqueda_nombre('matricula', 'la')


        elif chose =='3':
            return self.busqueda_nombre('edad', 'la')


        elif chose =='4':
            return self.busqueda_nombre('mes de nacimiento', 'el')



        elif chose == '5':
            self.cleainng()
            return admin.Admin().update()


        else:
            cleaning()
            self.askin()


    def busqueda_nombre(self,atributo,lale):
        chose = 'bruh'
        cleaning()
        jason = read_json('alumnos.json')

        if atributo.lower() == 'mes de nacimiento':
            mes = self.print_meses()
        elif atributo.lower() == 'edad':
            edad = self.asking_rango_edad()
        else:

            chose = input(f'Entra {lale} {atributo} del alumno o escribe abandonar: ').lower()

        if chose == 'abandonar':
            cleaning()
            return Busqueda().update()
        alumnos_with_same_name = []
        alumnos_with_same_name_index = []

        if atributo.lower() == 'nombre':
            for i in jason:
                if i.split('_')[0].lower() == chose:
                    alumnos_with_same_name.append(i)

        if atributo.lower() == 'matricula':
            for i in jason:
                if jason[i]['matricula'] == chose:
                    alumnos_with_same_name.append(i)

        if atributo.lower() == 'mes de nacimiento':
            for i in jason:
                if jason[i]['fecha_nacimiento'].split('/')[1] == mes:
                    alumnos_with_same_name.append(i)

        if atributo.lower() == 'edad':
            for i in jason:
                if str(edad) != 'bruh':
                    if jason[i]['edad'].__floor__() == edad:
                        alumnos_with_same_name.append(i)
                else:
                    age = jason[i]['edad'].__floor__()
                    if age > self.mayor and age < self.menor:
                        alumnos_with_same_name.append(i)






        index = 0

        if len(alumnos_with_same_name) == 0:
            self.cleainng()
            print(f'No matching {atributo} found')
            return self.askin()

        else:
            nombre = chose.lower()

            broly = display_indices_with_key_name(alumnos_with_same_name)
            indices_list= broly[0]
            indices_key_name = broly[1]
            index = broly[2]





            chose = input('Choose: ')
            cleaning()

            if chose == index:
                cleaning()
                print('Abandoning')
                return Busqueda().update()

            elif chose == str(int(index)+1):
                if atributo.lower() == 'nombre':
                    admin.Sorting().print_everything(nombre_especifico=nombre)

                elif atributo.lower() == 'edad':
                    admin.Sorting().print_everything(edad_rango=(self.mayor,self.menor))

                if yes_or_no('Return to Busqueda extra hub(y/n): ') == True:
                    cleaning()
                    return Busqueda().update()

                else:
                    cleaning()
                    return admin.Admin().update()



            elif chose not in indices_list:
                cleaning()
                print('Index not available')
                return self.busqueda_nombre()

            else:
                prettyfy(indices_key_name[chose])
                return admin.Admin().askingv1(current_key=indices_key_name[chose])










    def busqueda_matricula(self):
        pass


    def busqueda_edad(self):
        pass


    def cleainng(self):
        print('\n\n\n\n\n\n\n')



    def print_meses(self):

        index_list = []
        index = 0
        for i in self.meses:
            print(f'({i}){self.meses[i]}')
            index_list.append(i)
            index += 1

        print(f'({index})Regresar a Busqueda extra')
        chose = input('Choose: ')

        if chose == str(index):
            cleaning()
            return Busqueda().update()

        elif chose not in index_list:
            cleaning()
            print(f'Index {chose} not found')
            return self.print_meses()

        else:
            cleaning()
            print(f'Mes: {self.meses[chose]}')
            return str(int(chose)+1)


    def asking_rango_edad(self):

        chose = input('(1)Edad especifica\n(2)Rango\n(3)Abandonar\nChoose: ')

        if chose == '1':
            cleaning()
            chose = validate_int('Entra la edad: ')
            cleaning()
            return chose

        elif chose == '2':
            cleaning()
            mayor_a = validate_int('Rango mayor a (like this: 17): ')
            menor_a = validate_int('Rango menor a (like this 20): ')

            if menor_a == mayor_a:
                return chose

            elif mayor_a > menor_a:
                temp = menor_a
                menor_a = mayor_a
                mayor_a = temp

            self.mayor = mayor_a
            self.menor = menor_a
            return 'bruh'



        elif chose == '3':
            cleaning()
            return Busqueda().update()


    def update(self):

        self.askin()









