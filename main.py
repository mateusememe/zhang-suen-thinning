import cv2
import numpy as np


def openImage(path):
    img = cv2.imread(path)
    return img

# retorna imagem preto e branco passando uma imagem colorida por parametro
def getBlackWhiteImage(img):
    lin, col = img.shape
    img2 = np.zeros((lin,col,1), dtype=np.uint8)
    for i in range(lin):
        for j in range(col):
            if img[i][j] < 200:
                img2[i][j] = 0
            else:
                img2[i][j] = 255
    return img2

# Verifica se a conectividade 1 (transições de branco para preto)
def connections(image, p):
    transictions = 0
    for index in range(1,len(p)-1,1):
        if image[p[index]] > 127 and image[p[index + 1]] < 127:
            transictions += 1
    if image[p[len(p) - 1]] > 127 and image[p[1]] < 127:
        transictions += 1
    return transictions == 1


# Verifica se a qtde de pixels pretos vizinhos são >= 2 e <= 6
def blackPixels(img, p):
    pixelsCount = 0
    for index in range(1,9,1):
        if img[p[index]] < 127:
            pixelsCount += 1
    return 2 <= pixelsCount <= 6


# Ao  menos  um  dos pixels  imagem[row, col+1],  imagem[row-1,col]  e  imagem[row,  col-1]  são  fundo branco
def topWhite(img, p):
    return img[p[1]] > 127 or img[p[3]] > 127 or img[p[7]] > 127


# Ao  menos  um  dos pixels  imagem[row, col+1],  imagem[row+1,col]  e  imagem[row,  col-1]  são  fundo branco
def bottomWhite(img, p):
    return img[p[7]] > 127 or img[p[5]] > 127 or img[p[3]] > 127


# Ao  menos  um  dos pixels  imagem[row-1, col],  imagem[row+1,col]  e  imagem[row,  col-1]  são  fundo branco
def leftWhite(img, p):
    return img[p[1]] > 127 or img[p[5]] > 127 or img[p[7]] > 127


# Ao  menos  um  dos pixels  imagem[row-1, col],  imagem[row,col+1]  e  imagem[row+1,  col]  são  fundo branco
def rightWhite(img, p):
    return img[p[1]] > 127 or img[p[3]] > 127 or img[p[5]] > 127


def zhang_suen(img):
    rows, cols, _ = img.shape
    print("Linhas: ",rows,"Colunas: ",cols)
    count = 1
    Side = True
    excludedPixels = []
    while count > 0:
        count = 0
        for row in range(1, rows - 1, 1):
            for col in range(1, cols - 1, 1):
                p = [
                    (row, col),
                    (row - 1, col),
                    (row - 1, col + 1),
                    (row, col + 1),
                    (row + 1, col + 1),
                    (row + 1, col),
                    (row + 1, col - 1),
                    (row, col - 1),
                    (row - 1, col - 1),
                ]
                if img[row][col] < 127:
                    if connections(img, p) and blackPixels(img, p):
                        if Side:
                            if topWhite(img, p) and leftWhite(img, p):
                                excludedPixels.append((row, col))
                                count += 1
                        else:
                            if bottomWhite(img, p) and rightWhite(img, p):
                                excludedPixels.append((row, col))
                                count += 1
        for index in range(len(excludedPixels)):
            img[excludedPixels[index]] = 255
            Side = not Side
        excludedPixels.clear()

    return img


def main():
    originalImage = openImage("images/letraforma.jpg")
    grayImage = cv2.cvtColor(originalImage,cv2.COLOR_BGR2GRAY)
    BWimage = getBlackWhiteImage(grayImage)
    thinningImage = zhang_suen(BWimage)
    cv2.imshow("Original Image", originalImage)
    cv2.imshow("Black and White Image", BWimage)
    cv2.imshow("Thinning Image", thinningImage)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
