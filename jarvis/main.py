import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyaudio
import requests
import webbrowser
import os
from openai import OpenAI

r = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

activado = True

def prender():
    global activado
    hablar('Buenas señor, los comando son prender, apagar, reproduce y hora')
    activado = True

def apagar():
    global activado
    hablar('Adios señor.')
    activado = False

def hablar(texto):
    print(texto)
    engine.say(texto)
    engine.runAndWait()

def detectarComandos():
    with sr.Microphone() as source:
        hablar('En que puedo ayudarlo señor.')
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='es')
        hablar('Comando detectado.')
        return texto.lower()
    except sr.UnknownValueError:
        return ''

def ejecutarComandos(comando):
    if (comando == ""):
        hablar('No detecto ningun comando ...')
        return True
    elif ('apagar' in comando):
        apagar()
        return False
    else:
        chat = chatGPT(comando)
        print(chat)
        if 'reproduce' in chat.split(' ')[0]:
            cancion = chat.replace('reproduce', '')
            hablar('Reproduciondo ' + cancion)
            pywhatkit.playonyt(cancion)
            return True
        elif 'hora' in chat.split(' ')[0]:
            horaActual = datetime.datetime.now().strftime('%H:%M:%S')
            hablar('La hora actual es ' + horaActual)
            return True
        elif 'clima' in chat.split(' ')[0]:
            comando.replace('clima en', '')
            hablar(obtener_info_clima(comando))
            return True
        elif 'abrir' in comando:
            comando.replace('abrir', '')
            abrir_aplicacion(comando)
            hablar('Se ha abierto ' + comando)
            return True
        elif 'buscar' in chat.split(' ')[0]:
            chat.replace('buscar', '')
            buscar_en_web(chat)
            return True
        else:
            hablar(chat)
            return True

def chatGPT(mensaje):
    client = OpenAI(
        api_key='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',
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": "Tu eres una interprete de comandos, vas a interpretar los mensajes que te llegen y responderme solo con las instrucciones que te diga a continuacion. Si del mensaje interpretas que quiere poner una cancion, contestame con el mensaje 'reproduce {cancion}', si del mensaje interpretas que quiere buscar algo en google, contestame con el mensaje 'buscar {cosa a buscar en google}', si del mensaje interpretas que quiere la hora actual, contestame con el mensaje 'hora', si del mensaje interpretas que quiere el clima de un lugar, contestame con el mensaje 'clima en {lugar}', si no interpretas ninguna de las anteriores, simplemente contesta a lo que diga con lo que quieras, pero que no sea mas largo que 50 palabras."
            },
            {
                "role": "user",
                "content": mensaje,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content
def obtener_info_clima(ciudad):
    api_key = '3e8c3b3d635dd2e6f55695980e512223'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es'
    respuesta = requests.get(url)
    datos_clima = respuesta.json()

    if datos_clima['cod'] == '404':
        return 'Ciudad no encontrada. Verifica el nombre.'
    print(datos_clima)
    temperatura = datos_clima['main']['temp']
    descripcion_clima = datos_clima['weather'][0]['description']

    return f'La temperatura en {ciudad} es de {temperatura} grados Celsius. {descripcion_clima}.'

def buscar_en_web(consulta):
    url = f'https://www.google.com/search?q={consulta}'
    webbrowser.open(url)

def abrir_aplicacion(nombre_aplicacion):
    aplicaciones = {
        'navegador': 'chrome.exe',
        'editor': 'notepad.exe',
        'calculadora': 'calc.exe',
    }

    if nombre_aplicacion in aplicaciones:
        os.system(f'start {aplicaciones[nombre_aplicacion]}')
        return f'Abriendo {nombre_aplicacion.capitalize()}.'
    else:
        return f'No conozco la aplicación {nombre_aplicacion}.'


hablar('Di iniciar.')
while True:
    comandoInicial = detectarComandos()
    print(comandoInicial)
    if ('iniciar' in comandoInicial):
        prender()
        while activado:
            comando = detectarComandos()
            print(f'Comando: {comando}.')
            ejecucion = ejecutarComandos(comando)
            if (ejecucion == False):
                break
            hablar('¿Puedo hacer algo mas por usted?')







