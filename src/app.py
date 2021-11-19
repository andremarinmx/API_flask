from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app = Flask(__name__)


conexion = MySQL(app)


@app.route('/')
def index():
    return "Bienvenidos"


@app.route('/materias', methods=['GET'])
def listar_materias():
    try:
        cur = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM materias"
        cur.execute(sql)
        datos = cur.fetchall()
        materias = []
        for fila in datos:
            materia = {'codigo': fila[0],
                       'nombre': fila[1], 'creditos': fila[2]}
            materias.append(materia)
        return jsonify({'cursos': materias, 'mensaje': "Materias listadas."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/materia/<codigo>', methods=['GET'])
def leer_materia(codigo):
    try:
        cur = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM materias WHERE codigo = '{0}'".format(
            codigo)
        cur.execute(sql)
        datos = cur.fetchone()
        if datos != None:
            materia = {'codigo': datos[0],
                       'nombre': datos[1], 'creditos': datos[2]}
            return jsonify({'cursos': materia, 'mensaje': "Materia encontrada."})
        else:
            return jsonify({'mensaje': "Materias no encontrada."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/materia/<codigo>', methods=['POST'])
def registrar_materia(codigo):
    try:
        cur = conexion.connection.cursor()
        sql = """INSERT INTO materias (codigo, nombre, creditos) 
        VALUES ('{0}', '{1}', '{2}')""".format(request.json['codigo'],
                                               request.json['nombre'], request.json['creditos'])
        cur.execute(sql)
        conexion.connection.commit()  # confirma la accion de insercion
        return jsonify({'mensaje': "Materia registrada"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/materias/<codigo>', methods=['DELETE'])
def eliminar_materia(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM materias WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de eliminación.
        return jsonify({'mensaje': "Curso eliminado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/materias/<codigo>', methods=['PUT'])
def actualizar_materia(codigo):
    try:
        cur = conexion.connection.cursor()
        sql = """UPDATE materias SET nombre = '{0}', creditos = '{1}' 
        WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
        cur.execute(sql)
        conexion.connection.commit()  # confirma la accion de actualizacion
        return jsonify({'mensaje': "Materia actualizada"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def pagina_no_encontrada(error):
    return "<h1>La pagina que buscas no existe</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    print(app.config['MYSQL_HOST'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
