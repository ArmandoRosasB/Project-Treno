import mysql.connector
import webbrowser
import time

from selenium import webdriver

FILENAME = "Index.html"

def getConnection():
    link = mysql.connector.connect(user = 'root', password = '', host = 'localhost', database = 'Treno')

    if link:
        print("Connected Successfully")
        return link
    else:
        print("Connection Not Established")


def queries(device, link):
#Query
    select_input = f"""SELECT * FROM  input WHERE device_key = {device} AND {device} BETWEEN %s AND %s ORDER BY num_signal DESC LIMIT 10;"""
    select_times = """SELECT COUNT(num_signal) FROM input WHERE device_state = 1 ;"""

    cursor = link.cursor() 
    '''
    cursor(): Is an object that is used to make
    the connection for executing SQL queries
    '''

    cursor.execute(select_input, ("1", "3000")) #Ejecutamos el query
    query = cursor.fetchall() # En nuestro query tenemos a todos los objetos

    p = ""

    for row in query:
        a = "<tr><td>%s</td>"%row[0]
        p += a
        b = "<td>%s</td>"%row[1]
        p += b
        c = "<td>%s</td>"%row[2]
        p += c
        d = "<td>%s</td>"%row[3]
        p += d
        e = "<td>%s</td>"%row[4]
        p += e

    cursor.execute(select_times)
    query = cursor.fetchall()

    q = ""
    for row in query:
        a = "%s"%row[0]
        q += a
    
    if(link.is_connected()):
       cursor.close()
       link.close()
       print("MySQL connection is closed.")

    return [p, q]

def modifyHtml(p, q, i):
    html_template =f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="Style.css">
        <title>Treno</title>
        
    </head>

    <body>
        <nav>
            <p class="logo">Treno</p>
            <p class = "username">User<span class="Color_primario">name</span></p>
        </nav>

        <section id="Inicio">
            <h1><span class="Color_primario">Treno</span> Activado</h1>
            <h2><br>Ultimas notificaciones del dispositivo: </h2>
            <button class="stats"> <p>El perrito entro a la habitacion hoy un total de: {q}</p></button>
        </section>

        <section id = "Data">
            <table>
                <thead>
                    <tr>
                        <th>Num_Signal</th>
                        <th>Date</th>
                        <th>Device Key</th>
                        <th>Distance</th>
                        <th>State</th>
                    </tr>
                </thead>

            <tbody>
                {p}
            </tbody>
            </table>
        </section>

    </body>
    </html>
    ''' 
    
    with open(FILENAME, 'w') as output:
        output.write(html_template)




def main():
    link = getConnection()
    key = input("Type the key of your device: ")
    queries_list = queries(key, link)

    modifyHtml(queries_list[0],queries_list[1], 0)

    x = "localhost/Treno/index.html"
    refreshrate = 10

    driver = webdriver.Edge()
    driver.get("http://"+x)

    while (True):
       time.sleep(refreshrate)
       link = getConnection()
       queries_list = queries(key, link)
       modifyHtml(queries_list[0],queries_list[1], 1)
       driver.refresh()


main()

      
    




