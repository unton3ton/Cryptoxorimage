# conda activate DCTWM 
# conda activate iWM

# https://stackoverflow.com/questions/11142851/adding-borders-to-an-image-using-python
# https://learnopencv.com/cropping-an-image-using-opencv/
# https://ru.stackoverflow.com/questions/414593/%D0%9A%D0%B0%D0%BA-%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B8%D1%82%D1%8C-%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0

# pip install opencv-python

import cv2, os.path
import numpy as np
# pip install colorthief
from colorthief import ColorThief

# очень медленный код и не оптимальный
def order_in_reversed_bits(data: np.ndarray) -> np.ndarray:
    tobinary = lambda t: np.binary_repr(t, width=len(np.binary_repr(data.shape[0]-1)))[::-1]
    func = np.vectorize(tobinary)
    a = func(np.arange(0,data.shape[0]))
    t = np.zeros(data.shape,dtype='float64')

    for i,k in enumerate(a):
        t[int(k,2)] = data[i]

    return t

def order_in_reversed_bits_python(lst):
    return order_in_reversed_bits(lst)
    # довольно быстрый, но работает ТОЛЬКО с черно-белыми изображениями
    return [v for _, v in sorted(enumerate(lst), key=lambda k: bin(k[0])[:1:-1])]

def rever(img:cv2.Mat,size:int=0)->cv2.Mat:
    if(size==0):
        size = img.shape[0]
    print(img.shape)
    print(size)
    print(img.shape[0]//size)
    # применим бит-реверсивную перестановку для каждой строки изображения
    for i in range(img.shape[0]):
        #меняем фрагментированно, для голографических свойств
        for j in range(0,img.shape[0]//size): 
            img[i][j*size:j*size+size] = order_in_reversed_bits_python(img[i][j*size:j*size+size])
    return img

def example2(img:cv2.Mat,size:int=0)->cv2.Mat:
    # приминяем бит реверсную перестановку для картинки горизонтально
    img = rever(img,size)
    # транспонируем матрицу(мменяем местами координаты x,y)
    img = cv2.transpose(img)
    # приминяем бит реверсную перестановку для картинки вертикально
    img = rever(img,size)
    # возвращаем матрицу на свое место
    img = cv2.transpose(img)
    return img

if __name__ == "__main__":
    
    # читаем картинку new.png и выводим на экран, ждем действий от пользователя
    name = 'test1.jpg'
    img = cv2.imread(name, cv2.IMREAD_COLOR)
        
    if img.shape[0] != img.shape[1] != 1024:
        if img.shape[1] >= img.shape[0]:
            width = 1024
            left, right = 0, 0 
            height = int(img.shape[0] * 1024 / img.shape[1])
            top = bottom = (1024 - height)//2
        else:
            height = 1024
            top, bottom = 0, 0
            width = int(img.shape[1] * 1024 / img.shape[0])
            left = right = (1024 - width)//2
        
        img = cv2.resize(img, (width, height))

        color_thief = ColorThief(name)
        dominant_color = color_thief.get_color(quality=1)
         
        color = (dominant_color[2], dominant_color[1], dominant_color[0])
           

        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        # cv2.imwrite(f"new.png", img)


    # применяем бит-реверсивную перестановку к изображению, 
    # получаем закодированное изображение, сохраняем в файл corupt.png выводим его на экран и ждем, 
    # если пользователь хочет его попробывать повредить, ждем действий от пользователя
    img = example2(img)
    cv2.imwrite(f"corupt_{name[:-4]}.png",img)
    
    # # Читаем по новой из файла, который пользователь мог изменить, 
    # # выводим изменения на экран, чтобы пользователь убедился, что закодированное изображение повреждено, 
    # # ждем действий от пользователя
    
    if os.path.exists(f'corupt_{name[:-4]}.jpg') == True:
        img = cv2.imread(f'corupt_{name[:-4]}.jpg', cv2.IMREAD_COLOR)
    else:
        print('\nik ben hier\n')
        img = cv2.imread(f'corupt_{name[:-4]}.png', cv2.IMREAD_COLOR)
    

    # # применяем бит-реверсивную перестановку для востановления изображения
    # # раскомментировать, для голографических свойств, а другую строку закомментировать
    
    img = example2(img)

    # # выводим результат и ждем действий от пользователя
    cv2.imwrite(f"result_{name[:-4]}.jpg",img)

    if img.shape[0] != img.shape[1] != 1024:
        crop = img[top:(height+bottom), left:(width+right)]
        cv2.imwrite(f"cropresult_{name[:-4]}.jpg",crop)