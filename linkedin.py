import csv
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CARGO_DEFAULT = 'Developer'
UBICACION_DEFAULT = 'Mendoza,Argentina'
XPATH_BUSQUEDA_CARGO = "//input[starts-with (@id,'jobs-search-box-keyword-id-ember')]"
XPATH_BUSQUEDA_UBICACION = "//input[starts-with (@id,'jobs-search-box-location-id-ember')]"
XPATH_BOTON_SUBMIT = "/html/body/div[8]/div[3]/div/section/section[1]/div/div/div[2]/button"
XPATH_CONTENEDOR_RESULTADOS = "/html/body/div[8]/div[3]/div[3]/div/div/section[1]/div/div/ul"
XPATH_VACANTE = "//a[starts-with (@class,'disabled ember-view job-card-container__link job-card-list__title')]"

def initial_setup():
    # Creo el driver de firefox
    driver = webdriver.Firefox()
    # Dirijo a web de linkedin
    driver.get("https://www.linkedin.com")
    # deserializo las cookies,que se deben encontrar en el directorio raíz
    cookies = pickle.load(open("cookies.pkl", "rb"))
    # cargo las cookies de sesión
    for cookie in cookies:
        driver.add_cookie(cookie)
    # actualizo la página
    driver.get("http://www.linkedin.com")
    return driver


def obtener_empleos(cargo="", ubicacion=""):
    driver = initial_setup()
    driver.get("https://www.linkedin.com/jobs/")
    busqueda_por_cargo = driver.find_elements_by_xpath(XPATH_BUSQUEDA_CARGO)
    busqueda_por_ubicacion = driver.find_elements_by_xpath(XPATH_BUSQUEDA_UBICACION)

    if cargo != "":
        busqueda_por_cargo[0].send_keys(cargo)
    else:
        busqueda_por_cargo[0].send_keys(CARGO_DEFAULT)
    if ubicacion != "":
        busqueda_por_ubicacion[0].send_keys(ubicacion)
    else:
        busqueda_por_ubicacion[0].send_keys(UBICACION_DEFAULT)

    boton_enviar = driver.find_element_by_xpath(XPATH_BOTON_SUBMIT)
    boton_enviar.click()

    # Scrolleo hasta el final para encontrar resultados
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    lista_resultados = driver.find_element_by_xpath(XPATH_CONTENEDOR_RESULTADOS)

    data = list()
    data.append(['Descripcion de la vacante', 'url de la vacante'])

    vacantes = lista_resultados.find_elements_by_xpath(XPATH_VACANTE)

    for vacante in vacantes:
        descripcion = vacante.text
        url = vacante.get_property('href')
        data.append([descripcion, url])

    # Continuar con el procesamiento de los datos retornados
    with open('output.csv', 'w') as data_file:
        writer = csv.writer(data_file)
        writer.writerows(data)
    driver.close()


obtener_empleos("", "")
