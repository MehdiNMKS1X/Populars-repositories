from typing import BinaryIO

class BinaryFile:
    def __init__(self, file: BinaryIO):
        '''
        Initialize the BinaryFile with a file object.
        Args: file (BinaryIO): A binary file object opened in binary mode.
        '''
        self.file = file
    
    def goto(self, pos: int) -> None:
        '''
        Move the file pointer to a specific position.
        Args: pos(int): Position to seek to. If positive, seeks from beginning.
               If negative, seeks from end of file.
        '''
        if pos >= 0:
            self.file.seek(pos, 0)  # From beginning
        else:
            self.file.seek(pos, 2)  # From end
    
    def get_size(self) -> int:
        '''
        Get the total size of the file in bytes.
        Returns: int: The size of the file in bytes.
        '''
        current_pos = self.file.tell()
        self.file.seek(0, 2)  # Go to the end
        size = self.file.tell()
        self.file.seek(current_pos, 0)  # Restore position
        return size
    
    def write_integer(self, n: int, size: int) -> int:
        '''
        Write an integer to the current file position.
        Args:- n (int): The integer to write.
             - size (int): Number of bytes to use for storage.
            
        Returns:int: Number of bytes written.
        '''
        return self.file.write(n.to_bytes(size, byteorder='little', signed=True))
    
    def write_integer_to(self, n: int, size: int, pos: int) -> int:
        '''
        Write an integer at a specific file position.
        Args:- n (int): The integer to write.
             - size (int): Number of bytes to use for storage.
             - pos (int): Position in file to write at.
            
        Returns: int: Number of bytes written.
        '''
        current_pos = self.file.tell()
        self.goto(pos)
        bytes_written = self.write_integer(n, size)
        self.file.seek(current_pos, 0)  # Restore position
        return bytes_written
    
    def write_string(self, s: str) -> int:
        '''
        Write a string to the current file position.
        The string is prefixed with its length (2 bytes).
        Args: s (str): The string to write.
        Returns: int: Total bytes written (length + string).
        '''
        encoded = s.encode('utf-8')
        length_bytes = self.write_integer(len(encoded), 2)
        string_bytes = self.file.write(encoded)
        return length_bytes + string_bytes
    
    def write_string_to(self, s: str, pos: int) -> int:
        '''
        Write a string at a specific file position.
        Args:- s (str): The string to write.
             - pos (int): Position in file to write at.
            
        Returns: int: Total bytes written (length + string).
        '''
        current_pos = self.file.tell()
        self.goto(pos)
        bytes_written = self.write_string(s)
        self.file.seek(current_pos, 0)  # Restore position
        return bytes_written
    
    def read_integer(self, size: int) -> int:
        '''
        Read an integer from the current file position.
        Args: size (int): Number of bytes to read.
        Returns: int: The integer value read.
        '''
        return int.from_bytes(self.file.read(size), byteorder='little', signed=True)
    
    def read_integer_from(self, size: int, pos: int) -> int:
        '''
        Read an integer from a specific file position.
        Args:- size (int): Number of bytes to read.
             - pos (int): Position in file to read from.
            
        Returns: int: The integer value read.
        '''
        current_pos = self.file.tell()
        self.goto(pos)
        value = self.read_integer(size)
        self.file.seek(current_pos, 0)  # Restore position
        return value
    
    def read_string(self) -> str:
        '''
        Read a string from the current file position.
        The string is expected to be prefixed with its length (2 bytes).
        Returns: str: The string read.
        '''
        length = self.read_integer(2)
        return self.file.read(length).decode('utf-8')
    
    def read_string_from(self, pos: int) -> str:
        '''
        Read a string from a specific file position.
        Args: pos (int): Position in file to read from.
        Returns: str: The string read.
        '''
        current_pos = self.file.tell()
        self.goto(pos)
        value = self.read_string()
        self.file.seek(current_pos, 0)  # Restore position
        return value
