from PIL import Image, ImageOps,ImageFilter
from os import remove
def image_filter(filename, preset, username):
    '''
    processes files stored in .../media/unprocessed_photos, and stores in .../media/processed_photos<username>/
    deletes file saved at .../media/unprocessed_photos/<username>/
    returns filename of processed photo stored at .../media/processed_photos
    '''

    inputfile = '/home/ubuntu/Project1/flaskr/media/unprocessed_photos/' + filename

    f=filename.split('.')
    outputfilename = f[0] + '_'+ preset + '.jpg'

    outputfile = '/home/ubuntu/Project1/flaskr/media/processed_photos/' +username+'/' + outputfilename

    im = Image.open(inputfile)
    if preset=='gray':
        im = ImageOps.grayscale(im)

    if preset=='solar':
        im = ImageOps.solarize(im, threshold=20)

    if preset=='blur':
        im = im.filter(ImageFilter.BLUR)
        
        
    im.save(outputfile)
    remove(inputfile)
    return outputfilename
