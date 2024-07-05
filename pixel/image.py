from pixel import Pixel

class Image:
    def __init__(self, width: int, height: int, pixels: list[Pixel]):
        if not isinstance(width, int) or width <= 0:
            raise ValueError('le width doit etre un entier positive')
        if not isinstance(height,int) or height <= 0:
            raise ValueError('le height doit etre un entier positive')
        if len(pixels) != width * height:
            print(len(pixels))
            raise ValueError('le nombre de pixels doit etre egal a la taille de width and height')
        if not all(isinstance(p, Pixel) for p in pixels):
            raise ValueError('les pixels doivent etre une liste dinstance de pixels')
        self.width = width
        self.height = height
        self.pixels = pixels 
        """
        Inialisize an image object with given width, height, and pixels
        args:
            width(int): width of the image
            height(int): height of the image
            pixels(list[pixel]): list of pixel object representing the image
        raise:
            ValueError: if width or height are not positive intergers
            or if the number of pixels does not matchthe size of the image
            or if the pixels list contains objects other than pixel
        """
    def __getitem__(self, pos: tuple[int,int]) -> Pixel:
        if not (0 <= pos[0] < self.width and 0 <= pos[1] < self.height):
            raise IndexError
        return self.pixels[pos[1] * self.width + pos[0]]
        """
        get the pixel object at a specified position in the image
        
        args:
            pos(tuple[int,int]): psition(x,y) in the image
        return: 
            Pixel: pixel object at the specified position 
        raise:
            indexError if the position is out of bounds
        
        """
    
    def __setitem__(self, pos: tuple[int,int], pix: 'Pixel') -> None:
        if not (0 <= pos[0] < self.width and 0 <= pos[1] < self.height):
            raise IndexError
        self.pixels[pos[1] * self.width + pos[0]] = pix 
        """
        set the pixel objectat a specified position in the image
        args:
            pos(tuple[int,int]): position(x,y) in the image
            pix(pixel): pixel object to set at the specified position
        raise:
            IndexError: if the position is out of bounds
        
        """
    def get_pixels(self):
        return self.pixels
        """
        get the list of the pixels representing the image
        returns:
                List[pixel]: list of pixel objetc representing the immage
    
        """
        
    def __eq__(self, other: 'Image') -> bool:
        if not isinstance(other, Image):
            return False 
            return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height
        return self.width == other.width and self.height == other.height and self.pixels == other.pixels
        """
        compare two image object for equality
        args:
            other(image): another image object to comaare with
        return:
            bool: true if both image object have the same width, height and pixels, False otherwise
        """