import os
import sys
from glob import glob
from PIL import Image
from tqdm import tqdm

def main(start, format, size):
    supportedFormats = ['png', 'ico', 'jpeg', 'jpg', 'bmp', 'icns']
    globExtensions = ['[pP][nN][gG]', '[iI][cC][oO]', '[jJ][pP][eE][gG]', '[jJ][pP][gG]', '[bB][mM][pP]', '[iI][cC][nN][sS]']
    if format[0] == '.':
        format = format[1:]
    if format.lower() not in supportedFormats:
        sys.exit('Error: Image format not supported by the program. Try one of the following formats instead: ' + ', '.join(supportedFormats))
    imageFolders = []
    index = supportedFormats.index(format.lower())
    getImageFolders(start, imageFolders, globExtensions[index])
    lastDir = start.split('/')[-1]
    if lastDir == '':
        lastDir = start.split('/')[-2]
    print('Image folders resizing progress:')
    for imageFolder in tqdm(imageFolders):
        saveLocation = imageFolder.replace(lastDir, 'ResizedImages', 1)
        if not os.path.exists(saveLocation):
            os.makedirs(saveLocation)
        path = imageFolder
        if path[-1] != '/':
            path = path + '/*.' + globExtensions[index]
        else:
            path = path + '*.' + globExtensions[index]

        for imageFile in glob(path):
            file, ext = os.path.splitext(imageFile)
            filename = file.split('/')[-1]
            im = Image.open(imageFile)
            im = im.crop(im.getbbox())
            if size[0] < im.size[0] and size[1] < im.size[1]:
                im.thumbnail(size, Image.LANCZOS)
            else:
                if (im.size[0] < im.size[1]):
                    smallerSide = round((im.size[0]/im.size[1]) * size[1])
                    newsize = (smallerSide, size[1])
                elif (im.size[1] < im.size[0]):
                    smallerSide = round((im.size[1]/im.size[0]) * size[0])
                    newsize = (size[0], smallerSide)
                else:
                    newsize = (size[0], size[1])
                im = im.resize(newsize, Image.LANCZOS)
            driver = format.lower()
            if format.lower() == 'jpg':
                driver = 'jpeg'
            im.save(saveLocation + filename + '.' + format.lower(), driver)

    print('All done. Thank you for waiting.')


def getImageFolders(path, imageFolders, extension):
    new_path = path
    if new_path[-1] != '/':
        new_path = path + '/*/'
    else:
        new_path = path + '*/'
    if glob(new_path) != []:
        for folder in glob(new_path):
            result = getImageFolders(folder, imageFolders, extension)

    if (glob(new_path[:-1] + '.' + extension)!= []):
        imageFolders.append(path)


    return imageFolders

if __name__ == '__main__':
    size = ()
    if not os.path.exists(sys.argv[1]):
        sys.exit('Error: Folder at the path to images does not exist.')
    if (len(sys.argv) > 5):
        sys.exit('Error: Too many arguments.')
    elif (len(sys.argv) == 5):
        try:
            size = (int(sys.argv[3]), int(sys.argv[4]))
        except ValueError:
            sys.exit('Error: Resize Width and Resize Height need to be proper integer numbers!')
    elif (len(sys.argv) == 4):
        try:
            size = (int(sys.argv[3]), int(sys.argv[3]))
        except ValueError:
            sys.exit('Error: Resize Width and Resize Height need to be proper integer numbers!')
    else:
        sys.exit('Error: Too few arguments. Please input path to images, file format, resize width and resize height.')
    main(sys.argv[1], sys.argv[2], size)
