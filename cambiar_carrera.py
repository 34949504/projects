from funcs import cleaning,yes_or_no,read_json,write_to_json
import admin
class Cambiar_Carrera():
    def __init__(self,alumno_key,alumno_carrera):
        self.jason_materias = read_json('materias.json')

        self.alumno_carrera = alumno_carrera
        self.alumno_key = alumno_key

        self.alumno_json = read_json('alumnos.json')

        self.carrera = ''
        self.new_dict = {}
        self.cambio()

    def cambio(self):
        cleaning()
        index = 0
        carreras_jason_with_index = {}
        index_list_for_approval = []
        print(f'CARRERA ACTUAL --> {self.alumno_carrera}')
        for carrera in self.jason_materias:
            if carrera != self.alumno_carrera:
                index_list_for_approval.append(str(index))
                print(f'({index}){carrera}')
                carreras_jason_with_index[str(index)] = carrera
                index += 1

        print(f'({index})Abandonar sin guardar')

        chose = input('Escoge a que carrera a cambiar: ')

        if chose == str(index):
            cleaning()
            return admin.Admin().update()

        elif chose not in index_list_for_approval:
            cleaning()
            'Indice no disponible'
            return self.cambio()

        else:
            carrera = carreras_jason_with_index[chose]
            self.carrera = carrera

            self.chosing_materias(carrera)


    def chosing_materias(self,carrera_chosen):
        cleaning()

        print(f'Materias de {carrera_chosen}')
        materias_index_json = {}
        index_list = []
        index = 0
        for materia in self.jason_materias[carrera_chosen]:
            print(f'({index}){materia}')

            materias_index_json[str(index)] = materia
            index_list.append(str(index))

            index += 1

        print(f'({index})Abandonar sin guardar')

        print('Example: 1 4 6')
        chose = input('Choose: ')

        if chose == str(index):
            cleaning()

            return admin.Admin().update()


        indices_de_materias_escogiadas = chose.split()

        materias_names_para_agregar = []
        for number in indices_de_materias_escogiadas:
            if number == str(index):

                cleaning()
                print('Successfully abandoned')
                return admin.Admin().update()

            if number in index_list:

                name_materia = materias_index_json[number]
                materias_names_para_agregar.append(name_materia)

        if len(materias_names_para_agregar) == 0:
            cleaning()
            return self.chosing_materias(carrera_chosen)


        self.info_to_dict(materias_names_para_agregar)
        cleaning()
        print('Modificacion ha sido exitosa')
        return admin.Admin().update()
        #return (carrera_chosen,materias_names_para_agregar)




    def info_to_dict(self,materias):
        for alumno in self.alumno_json:
            if alumno == self.alumno_key:
                self.alumno_json[alumno]['carrera'] = self.carrera
                self.alumno_json[alumno]['materias'] = materias

            else:
                pass

        write_to_json('alumnos',self.alumno_json)















