import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CARGO_DEFAULT = 'Developer'
UBICACION_DEFAULT = 'Mendoza,Argentina'


def initial_setup():
    #Creo el driver de firefox
    driver = webdriver.Firefox()
    #Dirijo a web de linkedin
    driver.get("https://www.linkedin.com")
    #deserializo las cookies,que se deben encontrar en el directorio raíz
    cookies = pickle.load(open("cookies.pkl", "rb"))
    #cargo las cookies de sesión
    for cookie in cookies:
        driver.add_cookie(cookie)
    #actualizo la página
    driver.get("http://www.linkedin.com")
    return driver



def obtener_empleos(cargo="",ubicacion=""):
    driver = initial_setup()
    driver.get("https://www.linkedin.com/jobs/")
    busqueda_por_cargo = driver.find_elements_by_id("jobs-search-box-keyword-id-ember44")
    busqueda_por_ubicacion = driver.find_elements_by_id("jobs-search-box-location-id-ember44")

    if cargo != "":
        busqueda_por_cargo[0].send_keys(cargo)
    else:
        busqueda_por_cargo[0].send_keys(CARGO_DEFAULT)
    if ubicacion != "":
        busqueda_por_ubicacion[0].send_keys(ubicacion)
    else:
        busqueda_por_ubicacion[0].send_keys(UBICACION_DEFAULT)

    boton_enviar = driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/section/section[1]/div/div/div[2]/button")
    boton_enviar.click()

    #Continuar con el procesamiento de los datos retornados

obtener_empleos("", "")
