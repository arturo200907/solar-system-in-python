from raylib import* 
from pyray import * 
import math
from math import sqrt  

time_scale = 0.33
'''TOMAREMOS M=10 como la masa del sol, DISTANCIA = 10 como la distancia de la tierra al sol y T=10 como el período de la tierra alrededor de sol 
Observe que m*ac = (GM*m)r**2 -> v**2 = G*M/r -> (2*pi*r/T)**2 = G*M/r -> G = 4*pi**2*r**3/(T**2*M) -> G = 394.8

'''
#ACLARACIÓN PARA ESTE NÚMERO: 
#SI TIME SCALE=1 EL PERÍODO DE LA TIERRA ES DE 3 segundos. Luego 30 seg * 0.33 = 10 segundos. Cada 10 segundos se dará una vuelta a la tierra




class Celestial_body(): 
    def __init__(self, coordinates, radius, color, mass):
        self.coordinates = coordinates 
        self.radius = radius 
        self.color = color  
        self.mass = mass  
        self.G_MASS = 394.8*mass  #G*M donde M es la masa del planeta que está tirando

    def draw(self):
        draw_sphere(self.coordinates, self.radius, self.color )

class Planet(Celestial_body): 
    def __init__(self, coordinates, radius, color, mass): 
        super().__init__(coordinates, radius, color, mass)  
        self.speed = Vector3(0,0,0)
        self.trail = [] 

    def get_atracted_to(self, other):

        
        global time_scale

        dt = GetFrameTime() * time_scale
        #Evitamos que el usuario acelere demasiado
        if dt >0.15: 
            dt=0.15  
            time_scale = 9 #EN LA CONSOLA NOS DAMOS CUENTA DE QUE SI DT=0.15, TIME_SCALE ES 9
            print(time_scale)
        
        G_MASS = other.G_MASS

        #CÁLCULO DE DIRECCIÓN 
        dx = other.coordinates.x - self.coordinates.x
        dy = other.coordinates.y - self.coordinates.y 
        dz = other.coordinates.z - self.coordinates.z 

        #Calcula la distancia de un cuerpo a otro (el radio en esta elipse)
        radio = sqrt(dx**2 + dy**2 + dz**2)

        if radio <1: 
            radio =1 
        #Si se acerca demasiado fijamos radio en 1 para evitar divisiones por cero 
        '''
        Observe que: 
        F == m*a 
        G*M*m/r**2 == m*a <-> a = G*M/r**2    
        '''
        aceleracion = G_MASS / (radio**2) 
        

        #Normalizamos los vectores de dirección y escalamos con la aceleración
        #dx/radio nos dice como se mueve el componente vectorialmente y la aceleración nos dice cuanto
        aceleracion_x = dx/radio * aceleracion
        aceleracion_y = dy/radio * aceleracion 
        aceleracion_z = dz/radio * aceleracion 

        #Multiplicamos por dt para que la simulación sea más suave y no dependa de la velocidad de la computadora
        self.speed.x += aceleracion_x*dt 
        self.speed.y += aceleracion_y *dt
        self.speed.z += aceleracion_z *dt

        self.coordinates.x+= self.speed.x*dt
        self.coordinates.y+= self.speed.y *dt
        self.coordinates.z += self.speed.z *dt


        #VAMOS A IR GUARDANDO EL MOVIMIENTO DE LOS PLANETAS PARA DIBUJAR SU TRAIL 
        self.trail.append(Vector3(
        self.coordinates.x,
        self.coordinates.y,
        self.coordinates.z
            ))

        # LIMITAMOS EL TAMAÑO POR SI ALGO
        if len(self.trail) > 5000:
            self.trail.pop(0)

def draw_trail(planet, color):
    for i in range(1, len(planet.trail)):
        draw_line_3d(planet.trail[i-1], planet.trail[i], color)


def main(): 
    global time_scale 
    
    #---------------------------------------------------------------
    #-------------------CONFIGURACIÓN DE CAMARA --------------------
    #---------------------------------------------------------------
    init_window(800, 800, b"Simulacion Fisica: Orbita Real")  
    # Define the camera to look into our 3d world
    camera = Camera3D()
    camera.position = Vector3(10.0, 50.0, 0.0 ); # Camera position
    camera.target = Vector3(0.0, 0.0, 0.0 );      # Camera looking at point
    camera.up = Vector3(0.0, 1.0, 0.0 );          # Camera up vector (rotation towards target)
    camera.fovy = 45.0;                                # Camera field-of-view Y
    camera.projection = CAMERA_PERSPECTIVE;             # Camera projection type
    disable_cursor() 
    set_target_fps(60) 

    #--------------------------------------------------------------
    #---------------------------VARIABLES ÚTILES------------------- 
    #--------------------------------------------------------------  
    
    aphelions = {
        "mercury": 4.67,
        "venus": 7.28,
        "earth": 10.17,
        "mars": 16.66,
        "jupiter": 54.58,
        "saturn": 101.16,
        "uranus": 201.1,
        "neptune": 303.3
    }

    excentricities = {
        "mercury": 0.2056,
        "venus": 0.0067,
        "earth": 0.0167,
        "mars": 0.0934,
        "jupiter": 0.0489,
        "saturn": 0.0565,
        "uranus": 0.0457,
        "neptune": 0.0113
    }
    #------------------------------------------------------------
    #Distancia al sol, excentricidad y cálculo de semieje mayor
    #-----------------------------------------------------------
    
    r_mercury = aphelions["mercury"] 
    e_mercury = excentricities["mercury"]
    a_mercury = r_mercury / (1 + e_mercury) 

    r_venus = aphelions["venus"]
    e_venus = excentricities["venus"]           
    a_venus = r_venus / (1 + e_venus) 

    r_earth = aphelions["earth"]
    e_earth = excentricities["earth"]
    #Calculamos el semieje mayor de la elipse utilizando la fórmula a = r/(1+e) 
    a_earth = r_earth / (1 + e_earth) 

    r_mars = aphelions["mars"] 
    e_mars = excentricities["mars"]     
    a_mars = r_mars / (1 + e_mars) 

    r_jupiter = aphelions["jupiter"]
    e_jupiter = excentricities["jupiter"]
    a_jupiter = r_jupiter / (1 + e_jupiter) 

    r_saturn = aphelions["saturn"] 
    e_saturn = excentricities["saturn"]
    a_saturn = r_saturn / (1 + e_saturn) 

    r_uranus = aphelions["uranus"]
    e_uranus = excentricities["uranus"]
    a_uranus = r_uranus / (1 + e_uranus)

    r_neptune = aphelions["neptune"]
    e_neptune = excentricities["neptune"]
    a_neptune = r_neptune / (1 + e_neptune)



    #---------------------------------------------------------------
    #-------------------CREACIÓN DE OBJETOS ------------------------
    #---------------------------------------------------------------
    sun = Celestial_body(Vector3(0,0,0), 2.5, YELLOW, 10)

    mercury = Planet(Vector3(r_mercury,0,0), 1, GRAY, 1)
    venus = Planet(Vector3(r_venus,0,0), 1, ORANGE, 1)
    earth = Planet(Vector3(r_earth,0,0),1, BLUE,1)   
    mars = Planet(Vector3(r_mars,0,0), 1, RED, 1)
    jupiter = Planet(Vector3(r_jupiter,0,0), 2, BROWN, 1)
    saturn = Planet(Vector3(r_saturn,0,0), 2, BEIGE, 1) 
    uranus = Planet(Vector3(r_uranus,0,0), 2, LIGHTGRAY, 1) 
    neptune = Planet(Vector3(r_neptune,0,0), 2, DARKBLUE, 1)


    #VELOCIDADES INICIALES

    mercury.speed = Vector3(0, 0, sqrt(sun.G_MASS * (2/r_mercury - 1/a_mercury))) 
    venus.speed = Vector3(0, 0, sqrt(sun.G_MASS * (2/r_venus - 1/a_venus)))
    earth.speed = Vector3(0, 0, sqrt(sun.G_MASS * (2/r_earth - 1/a_earth)))  
    mars.speed = Vector3(0, 0, sqrt(sun.G_MASS * (2/r_mars - 1/a_mars)))
    jupiter.speed = Vector3(0, 0, sqrt(sun.G_MASS   * (2/r_jupiter - 1/a_jupiter)))
    saturn.speed = Vector3(0, 0, sqrt(sun.G_MASS    * (2/r_saturn - 1/a_saturn)))
    uranus.speed = Vector3(0, 0, sqrt(sun.G_MASS    * (2/r_uranus - 1/a_uranus)))
    neptune.speed = Vector3(0, 0, sqrt(sun.G_MASS    * (2/r_neptune - 1/a_neptune)))

    #----------------------------------------------------------------
    #---------------------BUCLE PRINCIPAL---------------------------- 
    #----------------------------------------------------------------  

    while not window_should_close():  
        #Cambia el objeto camara utilizando el otro parametro camera free
        update_camera(camera, CAMERA_FREE) 
        if is_key_down(KEY_UP):
            time_scale *= 1.01

        if is_key_down(KEY_DOWN):
            time_scale *= 0.99
        

        earth.get_atracted_to(sun) 
        venus.get_atracted_to(sun) 
        mercury.get_atracted_to(sun)
        mars.get_atracted_to(sun)
        jupiter.get_atracted_to(sun)
        saturn.get_atracted_to(sun) 
        uranus.get_atracted_to(sun)
        neptune.get_atracted_to(sun)
        #DIBUJO 

        begin_drawing()
        #Comienza el modo 3d

        BeginMode3D(camera) 
        
        #Limpia el fondo
        ClearBackground(BLACK);
        sun.draw()
        earth.draw()
        venus.draw()
        mercury.draw() 
        mars.draw()
        jupiter.draw()  
        saturn.draw() 
        uranus.draw()
        neptune.draw()
        #DrawGrid(1000, 1.0) 

        draw_trail(mercury, GRAY) 
        draw_trail(venus, ORANGE)
        draw_trail(earth, BLUE)
        draw_trail(mars, RED)
        draw_trail(jupiter, BROWN)
        draw_trail(saturn, BEIGE)
        draw_trail(uranus, LIGHTGRAY)
        draw_trail(neptune, DARKBLUE)
        EndMode3D()

        #Se calcula el tiempo real teniendo en cuenta que si time_scale = 0.33, cada segundo equivale a 0.1 años. Luego se hace regla de 3
        tiempo_real = (time_scale*0.1)/0.33


        #Rectangulos de leyendas
        #draw_rectangle(10, 10, 220, 70, WHITE) 
        draw_text(f"{round(tiempo_real,4)} años/s", 10, 720, 34, WHITE)
        draw_fps(10,770)
        end_drawing() 


    CloseWindow() 


main()