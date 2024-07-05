from image import Image
from pixel import Pixel

class Encoder:
    
    def __init__(self, img: 'Image', version : int = 1, **kwargs):
        self.img = img
        self.version = version 
        self.head_len = 12 
        self.depth = kwargs.get('depth', 24)
        self.rle = kwargs.get('rle', True)
        """
        initialze the encoder object
        args:
            img(image): the image object to encode
            version(int): the version of the encoding format
            **kwargs: additional argument including'depth' and 'rle' for specific versions
        
        """
        
    def _encode_version_4(self, pixels: list[Pixel]) -> bytearray:
        text__data = bytearray()
        last_pixel = Pixel(0, 0, 0)
        for p in pixels:
            delta_red = p.red - last_pixel.red
            delta_green = p.green - last_pixel.green
            delta_blue = p.blue - last_pixel.blue
            
            delta_red_green = delta_red - delta_green
            delta_blue_green = delta_blue - delta_green
            delta_green_red = delta_green - delta_red
            delta_blue_red = delta_blue - delta_red
            delta_red_blue = delta_red - delta_blue
            delta_green_blue = delta_green - delta_blue
            
            if -2 <= delta_red <= 1 and -2 <= delta_green <= 1 and -2 <= delta_blue <= 1:
                # Small difference
                red = delta_red + 2 << 4
                green = delta_green + 2 << 2
                blue = delta_blue + 2
                small_diff = red | green | blue
                text__data.extend(small_diff.to_bytes(length=1))

            elif -32 <= delta_green <= 31 and -8 <= delta_red_green <= 7 and -8 <= delta_blue_green <= 7:
                # Intermediate difference
                red = delta_red_green + 8 << 4
                green = delta_green + 32 << 8
                blue = delta_blue_green + 8
                intermediate_diff = green | red | blue
                intermediate_diff = (0b01 << 14) + intermediate_diff
                print(green | red | blue, intermediate_diff, format(intermediate_diff, "b"))
                text__data.extend(intermediate_diff.to_bytes(length=2))

            elif -128 <= delta_red <= 127 and -32 <= delta_green_red <= 31 and -32 <= delta_blue_red <= 31:
                # Big difference red
                red = delta_red + 128 << 12
                green = delta_green_red + 32 << 6
                blue = delta_blue_red + 32
                big_diff_red = red | green | blue
                big_diff_red =  (0b1000 << 20) + big_diff_red 
                text__data.extend(big_diff_red.to_bytes(length=3))
            elif -128 <= delta_green <= 127 and -32 <= delta_red_green <= 31 and -32 <= delta_blue_green <= 31:
                # Big difference green
                green = delta_green + 128 << 12
                red = delta_red_green + 32 << 6
                blue = delta_blue_green + 32
                big_diff_green = green | red | blue
                big_diff_green =  (0b1001 << 20) + big_diff_green 
                text__data.extend(big_diff_green.to_bytes(length=3))
            elif -128 <= delta_blue <= 127 and -32 <= delta_red_blue <= 31 and -32 <= delta_green_blue <= 31:
                # Big difference blue
                blue = delta_blue + 128 << 12
                red = delta_red_blue + 32 << 6
                green = delta_green_blue + 32
                big_diff_blue = blue | red | green
                big_diff_blue =  (0b1010 << 20) + big_diff_blue
                text__data.extend(big_diff_blue.to_bytes(length=3))
            else:
                # New pixel
                red_bin = p.red << 16
                green_bin = p.green << 8
                blue_bin = p.blue

                new_pixel = (255 << 24) | red_bin | green_bin | blue_bin
                text__data.extend(new_pixel.to_bytes(length=4))
            
            last_pixel = p
        return text__data
        """
        Encode the pixels using the version 4 enconding
        args: 
            pixels(list[pixel]): list of pixel object to encode
        return:
            bytearray: encoded data
        
        """
    def _encode_version_rle3(self, pixels: list[Pixel], palette: list[Pixel]) -> bytearray:
        text__data = bytearray()
        
        temp_bits = ""
                        
        for pixel in pixels:
            index = palette.index(pixel)
            temp_bits += format(index, "01b")
            
            if len(temp_bits) == 8:
                text__data.append(int(temp_bits[::-1], 2))
                temp_bits = ""
                            
        text__data.append(int(temp_bits.zfill(8)[::-1], 2))
        
        return text__data
        """
        encode the pixels using 3 rle encoding
        args: 
            pixels(list[pixel]): list of pixel object to encode
            palette(list[pixel]): lsit of colors in the palette
        return:
            bytearray: encoded data
        
        """
        
    def _encode_version_rle(self, pixels: list[Pixel]) ->  bytearray:
        text__data = bytearray()
        text__data += self.version.to_bytes(length=1, byteorder = "big")
        text__data += self.head_len.to_bytes(length=2, byteorder= "little")
        text__data += self.img.width.to_bytes(length=2, byteorder= "little")
        text__data += self.img.height.to_bytes(length=2, byteorder= "little")
        
        elm = pixels[0]
        counts = 0
        for i in range(1, len(pixels)):
            counts += 1
            if pixels[i] == elm:
                if counts == 255:
                    text__data += counts.to_bytes(length=1, byteorder= "big")
                    text__data += elm.red.to_bytes(length=1, byteorder= "big")
                    text__data += elm.green.to_bytes(length=1, byteorder= "big")
                    text__data += elm.blue.to_bytes(length=1, byteorder= "big")
                    counts = 0

            else:
                text__data += counts.to_bytes(length=1, byteorder= "big")
                text__data += elm.red.to_bytes(length=1, byteorder= "big")
                text__data += elm.green.to_bytes(length=1, byteorder= "big")
                text__data += elm.blue.to_bytes(length=1, byteorder= "big")
                elm = pixels[pixels.index(elm) + 1]
                counts = 0
                
        counts += 1
        text__data += counts.to_bytes(length=1, byteorder= "big")
        text__data += elm.red.to_bytes(length=1, byteorder= "big")
        text__data += elm.green.to_bytes(length=1, byteorder= "big")
        text__data += elm.blue.to_bytes(length=1, byteorder= "big")
        
        return text__data
        """
        encode the pixels using version 1 rle encoding
        args:
            pixels(list[pixel]): list of pixel object to encode
        return:
            bytearray: encoded data
        """
                   
    def save_to(self, path: str) -> None:
        text__head = b'ULBMP'
        text__data = bytearray()
        
        if self.version == 3:
            self.pixelsv3 = self.img.get_pixels()
            self.palette = list(set(self.pixelsv3))
            self.head_len += (len(self.palette) * 3) + 2
        
        text__data += self.version.to_bytes(length=1, byteorder = "big")
        text__data += self.head_len.to_bytes(length=2, byteorder = "little")
        text__data += self.img.width.to_bytes(length= 2, byteorder = "little")
        text__data += self.img.height.to_bytes(length=2, byteorder = "little")
        
        if self.version == 3:
            text__data += self.depth.to_bytes(length=1, byteorder= "big")
            text__data += self.rle.to_bytes(length=1, byteorder= "big")
            
        if self.version == 1 or (self.version == 3 and self.depth == 24 and self.rle == False):
            pixels = self.img.get_pixels()
            for pixel in self.img.pixels:
                for colors in pixel.get_colors():
                    text__data += colors.to_bytes(length=1, byteorder= "big")
        elif self.version == 2 or (self.version == 3 and self.depth == 24 and self.rle == True):
            pixels = self.img.get_pixels()
            text__data = self._encode_version_rle(pixels) 
        elif self.version == 3:          
            temp_palette_byte = bytearray()
            
            for p in self.palette:
                for colors in p.get_colors():
                    temp_palette_byte += colors.to_bytes(length=1, byteorder= "big")
            
            text__data.extend(temp_palette_byte[::-1])
                        
            text__data.extend(self._encode_version_rle3(self.pixelsv3, self.palette)) 
              
        elif self.version == 4:
            pixels = self.img.get_pixels()
            text__data.extend(self._encode_version_4(pixels))
        
        with open(path, 'wb') as f:
            f.write(text__head + text__data)
        return None 
        """
        Save the encoded image data to file a file
        args:
            path (str): the file path to save the encoded data
        """
    
class Decoder:
    
    @staticmethod
    def load_from(path: str) -> Image:
        with open(path, "rb") as f:
            head_len = f.read(12)
            version = head_len[5] 
            type = head_len[:5]
            datalen = int.from_bytes(head_len[6:8], byteorder= "little")
            width = int.from_bytes(head_len[8:10], byteorder= "little")
            height = int.from_bytes(head_len[10:12], byteorder= "little")
                        
            if version == 3:
                depth = int.from_bytes(f.read(1))
                rle = int.from_bytes(f.read(1))
            else:
                depth = 0
                rle = 0
            
            pixels_data = []
            if version == 1 or (version == 3 and depth == 24 and rle == 0):
                pixels = f.read(3)
                while pixels:
                    pixels_data.append(Pixel(pixels[0], pixels[1], pixels[2]))
                    pixels = f.read(3)
            elif version == 2 or (version == 3 and depth == 24 and rle == 1):
                text__data = f.read()
                pixels_data = Decoder.decode_pixels_rle(text__data, width, height)
            elif version == 3 :
                palette_byte = f.read(datalen - 14)
                palette = Decoder.decode_palette(palette_byte)
                text__data = f.read()
                
                if depth < 8:
                    pixels_data = Decoder.decode_pixels_palette(text__data, width, height, palette, depth)
                elif depth == 8:
                    pixels_data = Decoder.decode_pixels_rle_8(text__data, width, height, palette, rle)
                elif depth == 24 and rle == 1:
                    pixels_data = Decoder.decode_pixels_rle(text__data, width, height)
            elif version == 4:
                pixels_data = Decoder.decode_version_4(f.read(), width, height)

                    
            return Image(width, height, pixels_data)
        
        """
        load the encoded image data from a  file and decode it into an image object
        args: 
            path(str): the file path to load the encode data from
        
        returns:
            image the decoded image object
        """
    @staticmethod
    def decode_palette(palette) -> list[Pixel]:
        pixel = []
        
        for i in range(0, len(palette), 3):
            pixel.append(Pixel(palette[i], palette[i+1], palette[i+2]))
        
        return pixel
        """
        decode the palette from encoded data
        args:
            palette(bytes): the encoded palette data
        return: 
            list[pixel]: the decoded palette
        """
    
    @staticmethod
    def decode_pixels_palette(text__data, width, height, palette, depth) -> list[Pixel]:
        img: list[pixel] = []
                
        for byte in text__data:
            bits = format(byte, "08b")
                        
            for i in range(0, len(bits), depth):
                bit = bits[i:i+depth]
                index = int(bit, 2)
                img.append(palette[index])
                
                if len(img) == width*height:
                    break
            
            if len(img) == width*height:
                    break
        
        return img
        """
        decode pixel data using a palette
        args:
            text__data(bytes): the encoded pixel data
            width(int): the width of the image
            height(int): the height of the image
            palette(list[pixel]): the palette used for decoding
            depth(int): the bit depth of the image
        retun: 
            list[pixel]: the decoced pixels
        """
    @staticmethod
    def decode_pixels_rle_8(text__data, width, height, palette, rle) -> list[Pixel]:
        rle = True if rle == 1 else False
        
        img: list[Pixel] = []
        j = 0
        
        if rle:
            for i in range(0, len(text__data), 2):
                byte = text__data[i:i+2]
                
                repetition = byte[0]

                for _ in range(repetition):
                    img.append(palette[byte[1]])
        else:
            for byte in text__data:                
                img.append(palette[byte])
                
        return img
        """
        decode pixel data encoded with 8-bit rle compression
        args:
            width(int): the width of the image
            height(int): the height of the image
            palette(list[pixel]): the palette used for decoding
            rle(int): rle flag
        return:
            list[pixel]: the decoced pixels
        
        
        """
    @staticmethod
    def decode_pixels_rle(text__data, width, height) -> list[Pixel]:
        
        img: list[Pixel] = []
        j = 0
        
        for i in range(0, len(text__data), 4):
            byte = text__data[i:i+4]
            
            repetition = byte[0]

            for _ in range(repetition):
                img.append(Pixel(byte[1], byte[2], byte[3]))
        
        return img
        """
        decode pixel data encoded with rle compression
        args:
            text__data(bytes): the encoded pixel data
            width(int): the width of the image
            height(int): the height of the image
        return:
            list[pixel]: the decoded pixels
        
        """
    @staticmethod
    def decode_version_4(text__data, width, height) -> list[Pixel]:
        pixels_list = [Pixel(0, 0, 0)]
        index_pixels = 0
        while index_pixels != len(text__data):
            
            if text__data[index_pixels] == 255:
                red = text__data[index_pixels + 1]
                green = text__data[index_pixels + 2]
                blue = text__data[index_pixels + 3]
                
                new_pixels = Pixel(red, green, blue)
                pixels_list.append(new_pixels)
                index_pixels += 4    
                
                         
            elif text__data[index_pixels] & 0b11000000 == 0:
                previous_pixels = pixels_list[-1]
                pixels = text__data[index_pixels]
                delta_red = ((pixels & 0b110000) >> 4) - 2
                delta_green = ((pixels & 0b1100) >> 2) - 2
                delta_blue = (pixels & 0b11) - 2
                
                red = previous_pixels.red + delta_red
                green = previous_pixels.green + delta_green
                blue = previous_pixels.blue + delta_blue
                
                new_pixels = Pixel(red, green, blue)
                pixels_list.append(new_pixels)
                index_pixels += 1
                
                
            elif (text__data[index_pixels] & 0b11000000) >> 6 == 1:
                previous_pixels = pixels_list[-1]
                
                delta_green = (text__data[index_pixels] & 0b111111) - 32
                delta_red = (text__data[index_pixels + 1] & 0b11110000) - 8 + delta_green
                delta_blue = (text__data[index_pixels + 1] & 0b1111) - 8 + delta_green
                
                red = previous_pixels.red + delta_red
                green = previous_pixels.green + delta_green
                blue = previous_pixels.blue + delta_blue
                
                new_pixels = Pixel(red, green, blue)
                pixels_list.append(new_pixels)
                index_pixels += 2
                

            elif (text__data[index_pixels] & 0b11110000) >> 4 == 8:
                previous_pixels = pixels_list[-1]
                
                delta_red = ((text__data[index_pixels] & 0b1111) << 4 | (text__data[index_pixels + 1] & 0b11110000) >> 4  ) - 128
                delta_green = ((text__data[index_pixels + 1] & 0b1111) << 2 | (text__data[index_pixels + 2] & 0b11000000) >> 6 ) - 32 + delta_red
                delta_blue = (text__data[index_pixels + 2] & 0b111111) - 32 + delta_red
                
                red = previous_pixels.red + delta_red
                green = previous_pixels.green + delta_green
                blue = previous_pixels.blue + delta_blue
                
                new_pixels = Pixel(red, green, blue) 
                pixels_list.append(new_pixels)
                index_pixels += 3
                
                
            elif (text__data[index_pixels] & 0b11110000) >> 4 == 9:
                previous_pixels = pixels_list[-1]
                
                delta_green = ((text__data[index_pixels] & 0b1111) << 4 | (text__data[index_pixels + 1] & 0b11110000) >> 4  ) - 128
                delta_red = ((text__data[index_pixels + 1] & 0b1111) << 2 | (text__data[index_pixels + 2] & 0b11000000) >> 6 ) - 32 + delta_green
                delta_blue = (text__data[index_pixels + 2] & 0b111111) - 32 + delta_green
                
                red = previous_pixels.red + delta_red
                green = previous_pixels.green + delta_green
                blue = previous_pixels.blue + delta_blue
                
                new_pixels = Pixel(red, green, blue) 
                pixels_list.append(new_pixels)
                index_pixels += 3
                
                
            elif (text__data[index_pixels] & 0b11110000) >> 4 == 10:
                previous_pixels = pixels_list[-1]
                
                delta_blue = ((text__data[index_pixels] & 0b1111) << 4 | (text__data[index_pixels + 1] & 0b11110000) >> 4  ) - 128
                delta_red = ((text__data[index_pixels + 1] & 0b1111) << 2 | (text__data[index_pixels + 2] & 0b11000000) >> 6 ) - 32 + delta_blue
                delta_green= (text__data[index_pixels + 2] & 0b111111) - 32 + delta_blue
                
                red = previous_pixels.red + delta_red
                green = previous_pixels.green + delta_green
                blue = previous_pixels.blue + delta_blue
                
                new_pixels = Pixel(delta_red + 1, delta_green, delta_blue + 1) 
                pixels_list.append(new_pixels)
                index_pixels += 3
        pixels_list.pop(0)
        return pixels_list
        """
        decode pixel data encoded with version 4 compression 
        args:
            text__data(bytes): encoded pixel data
            width(int): the encoded pixel 
            height(int): the height of the image
        return:
            list[pixel]: the decoded pixels
        """