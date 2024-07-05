class Pixel:
    def __init__(self, red, green, blue)-> None:
        if not(0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError
        self.__red = red 
        self.__green = green
        self.__blue = blue
        self.__colors = (red,green,blue) 
    """ 
    Initialize a pixel object with given rgb values
    Args:
        red(int): Value of red component (0 to 255)
        green(int): also
        blue(int): also
    Raise:
        ValueError: if any rgb  values are out of range.
    """
    
    def __hash__(self):
        return hash((self.red, self.green, self.blue))
        """
        compute hash value of the pixel object
        return:
            int: hash value of the object based on its rgb values.
        """
    @property
    def red(self) -> int:
        return self.__red
        """
        get the value of the red component 
        return:
            int: value of red component
        """
    
    @property
    def green(self) -> int:
        return self.__green
        """
        get the value of the red component 
        return:
            int: value of green component
        """
    
    @property
    def blue(self) -> int:
        return self.__blue
    """
        get the value of the red component 
        return:
            int: value of blue component
        """
    def get_colors(self) -> tuple[int, int, int]:
        return self.__colors
        """
        get the rgb values of the pixel.
        return:
            tuple[int, int, int]: rgb values of the pixel
        
        """
    def __eq__(self, other: 'Pixel') -> bool:
        if not isinstance(other, Pixel):
            raise NotImplemented
        return self.__red == other.__red and self.__green == other.__green and self.__blue == other.__blue
        """
        compare two pixel object for equality
        args:
            other (pixel): another piuxel object to compare with.
        return:
            bool: true if both pixel object have the same rgb values, false otherwise
        raise:
            Notimplemented: if the other object is not a pixel
        """
    def __repr__(self):
        return f"Pixel({self.red}, {self.green}, {self.blue})"
    
        """
        get a string representation of the pixel object
        return:
            str : string representation of the pixel object
        """