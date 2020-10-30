# Bulk Image Resizer

Python script that utilizes PIL and glob packages in order to resize all the images of given format at the designated path folder as well as in it's subfolders. Images can be both upscaled and downscaled, however since the program uses LANCZOS filter, upscaling can be exceptionally slow for large amount of images.

Supported image formats are: .png, .ico, .jpeg, .jpg, .bmp and .icns.

When calling the script 3 or 4 positional arguments are necessary. First being the path to root folder from which the images are taken, second the image format of the images to be resized and third and fourth parameter represent dimensions for resizal. If 3 positional arguments are given, the height and width of the image would be equal to the last argument. Example call would be:

```
pipenv python run bulkResizer.py Path/To/Folder .png 250 250
```

After the call is executed, resized images are stored in a new folder that is created next to root folder at the given path.
