import cv2
import os
import easygui as eg

#Se define un arreglo que contiene los caracteres ascii que se utilizaran para la conversion a ascii
ascii_caracter = ['@','&','¶','£','#','%','$','ü','Ç','=','ã','?','(',')','|','!','+','/','*',
                   ';',':',',','.','-','.','"','°','^','¨',' ']
#Se calcula el factor de conversión para establecer la cuantización del video con relación
#al nivel de intensidad de cada pixel del video
factor = 255/(len(ascii_caracter)-1)
#Tamaño de los caracteres ascii
font_size = 0.4
#Valor de separacion horizontal y vertical de los caracteres
vertical_factor = 9
horizontal_factor = 6

#Abrimos una ventana para escoger el video que será convertido a ascii
def open_file():
	archivo = eg.fileopenbox(msg="",title="Seleccione video a transformar.",default='',filetypes='')
	return archivo

#Se calcula la posicion en el array ascii diviendo la intensidad del pixel entre el factor de conversión 
def to_ascii(frame):
  for i in range(width):
    for j in range(height):
      pixel=frame[i][j]
      position=pixel/factor
      caracter=ascii_caracter[int(position)]
      to_image(caracter,(j,i))
    
#Se dibuja el caracter ascii en la imagen utilizada como lienzo 
def to_image(string_ascii, position):
  cv2.putText(background, string_ascii, (position[0]*horizontal_factor, position[1]*vertical_factor+1), cv2.FONT_HERSHEY_PLAIN, font_size,  
              (255, 255, 255), 1)

#Abrimos el archivo de video y la imagen de lienzo que se utiliza como fondo
path = open_file()
video = cv2.VideoCapture(path)
background = cv2.imread("C:/Users/John Eduard/Documents/Python/Video to ascii/lienzo.bmp")
#Obtenemos el tamaño del lienzo y el framerate del video a convertir
fps = video.get(5)
height_full, width_full = background.shape[:2]
fps_counter = 0
#Se establece un tamaño estándar para redimensionar el video original, para obtener un mejor resultado
#con el video en ascii 
width = 120
height = 240
dsize = (height, width)
os.system("cls")
#Se establece el formato de salida con igual framerate del video original y tamaño del lienzo
salida = cv2.VideoWriter('videoSalida.avi',cv2.VideoWriter_fourcc(*'DIVX'),fps,(width_full,height_full))

while (video.isOpened()):
  ret, imagen = video.read()
  if ret == True:
    fps_counter += 1
    #Se convierte el frame a escala de grises y se redimensiona para poder realizar la conversión
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(imagen, dsize)
    #Realizamos la conversion del frame a ascii
    to_ascii(img_resize)
    #Se abre una vista previa del video convertido
    cv2.imshow('video', background)
    #Se guarda la imagen con los caracteres ascii como un frame del video convertido
    salida.write(background)
    #Se calculan los segundos de video renderizados
    seconds = fps_counter/fps
    print("\033[0;0H","[",seconds, "s  renderizados]")
    #Se restablece el lienzo como un fondo negro para borrar los caracteres anteriores
    background = background*0
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
  else: break
video.release()
salida.release()
cv2.destroyAllWindows()



 