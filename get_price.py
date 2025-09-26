from requests import get as req_get;
from requests.packages.urllib3 import disable_warnings;
from urllib3.exceptions import InsecureRequestWarning;
from sys import argv;
import pathlib;
from os import path as os_path;
import re;
from html.parser import HTMLParser;

""""@todo: Falta el filtro por fecha (al dejarlo vacio se obtiene el precio de hoy) y como guardar en formato especifico
@TODO: Hacer una nueva pagina y mostrar el promedio.""";
URL="http://www.bcv.org.ve/cambiaria/export/tasas-informativas-sistema-bancario";
DEFAULT_NAME_FILE="tasa del dolar actual.html";
ILLEGAL_NTFS_CHARS = r'[<>:/\\|?*\"]|[\0-\31]';

def get_bcv_file():
  """Obtiene los precio del dolar del BCV""";
  with req_get(URL, verify=False) as response:
    return {
      "text":response.text if response.ok else response.reason,
      "ok":response.ok
    };

def void_f(*args, **kwargs):
  pass;

def verify_file_name(name):
  """Verifica que el nombre de archivo tenga un caracter no válido.
  Return:
    Bool: ¿Tiene un caracter inválido?
  """;
  return re.search(ILLEGAL_NTFS_CHARS, name);

def html_to_type(html,type):
  """Convierte el string html a tipo de dato.
    Param:
      html (str): El dato a convertir.
      type (str): A qie convertir los datos válidos son:
        - XML
        - JSON
    Return:
      str: Dato ya convertido.
  """;

def main(name_file, url_out, type_file, date):
  """Obtiene el precio del dolar y lo guarda en el archivo
  Especificado.
  
  Param:
    name_file (str): Nombre conque se guardará el archivo.
    url_out (str): Donde se guardará el archivo.
    type_file (str): En que convertir el archivo.
    date (str): El filtro que se usará para saber que datos guardar.
  Return:
    Bool: ¿La operación fue exitosa?
  """;
  print("Conectando con BCV");
  disable_warnings(category=InsecureRequestWarning);
  req_file=get_bcv_file();
  if req_file["ok"]:
    print("Conexión con el Banco Central de Venezuela fue exitosa.");
    print(f"Guardando los resultados en: {url_out}/{name_file}...");
    with open(f"{url_out}/{name_file}",'w') as f:
      f.write(req_file["text"]);
  else:
    print("No fue exitosa la operación:");
    print(req_file["text"]);
  return req_file["ok"];

if __name__=="__main__":
  name_file=DEFAULT_NAME_FILE;
  url_out=pathlib.Path(__file__).parent.absolute();
  type_file="html";
  date=None;# Dejamos el filtro por fecha vacío por defecto.
  for now_arg in argv:
    if len(now_arg)>2 and now_arg[0]=="-":
      if now_arg[1] in ["D","d","F","f"] and now_arg[2]=="=":
        select_opt=now_arg[1];
        value=now_arg[3:]
        if select_opt=="D":# Change out dir
          if os_path.isdir(value):
            url_out=value;
          else:
            print("Error: Directorio no válido.");
            exit(2);
        elif select_opt=="F":# Change name file
          if not verify_file_name(value):
            name_file=value;
          else:
            print("Error: El nombre del archivo no debe contener los siguientes caracteres: "+" ".join(ILLEGAL_NTFS_CHARS[1:12]));
            print("O ser unos de los caracteres invisible en un rango de 0-31.");
            exit(3);
        elif select_opt=="d":
          validate=r"^\d{1,2}/\d{1,2}/\d{4}$";
          date=value.split();
          if (not re.search(validate,date[0])) or (len(date)>2 and not re.search(validate,date[2])):
            print("Error: Formato o fecha no válida.");
            print("Por favor usar el formato Dia/Mes/Año");
            exit(4);
        elif select_opt=="f":
          if value.lower() in ("xml","html","json"):
            type_file=value.lower();
          else:
            print("Error: Formato de archivo no valido. Por favor elegir los siguientes formatos:");
            print("- XML");
            print("- HTML");
            print("- JSON");
            exit(5);
      elif now_arg=="-DISABLE_IO_OUT":
        print=void_f;
      else:
        print("Parámetro no conocido, por favor usar los siguientes.");
        help();
        exit(1);
  if main(name_file, url_out, type_file, date):
    print("El programa ha sido exitoso.");
  else:
    input("Presione enter para terminar.");

def help():
  print(f"""get_price.py -D=[DIR_PATH] -F=[FILE_NAME] -DISABLE_IO_OUT -d=[date]
Obtenemos el precio del dolar y guardamos en DIR_PATH con el archivo FILE_NAME.
Parámetros:
  -D=[DIR_PATH] : Es el directorio donde guardar la salida del archivo. En caso de no especificar, se guardará en el directorio donde se guarda el programa.
  -F=[FILE_NAME] : Es el nombre que tendrá la salida, en caso de no especificar se llamará "{DEFAULT_NAME_FILE}" 
  -DISABLE_IO_OUT : Deshabilita la entrada/salida por consola.
  -d=[date] : Especifica un filtro para la fecha que se quiere ver el precio. Nota: Se usa formato Dia/Mes/Año.
  -endDate=[date] : Fecha ultima fecha a mostrar.
  -f=[FORMAT_FILE] : Especifica el formato que tendrá el archivo, que pueden ser ("xml","html","json").

Ejemplos:
echo "-D=directorio -F=NombreArchivo -d=Ficha inicio - fecha final"              
get_price.py -D=/home/user/desktop/ -F=Dollar_price.html "-d=01/04/2024 - 01/05/2024"
echo "-F=NombreArchivo -d=Desde 01/04/2025 - hasta hoy"
get_price.py -F=Dollar_price.html "-d=01/04/2024"
echo "Sin salida por consola." y obtener en formato xml."
get_price.py -DISABLE_IO_OUT -f=xml
  """);