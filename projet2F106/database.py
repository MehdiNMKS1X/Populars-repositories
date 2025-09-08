import os
from typing import List, Tuple, Dict
from enum import Enum
from binary import BinaryFile

class FieldType(Enum):
    """Enumeration representing the types of fields in the database tables."""
    INTEGER = 1
    STRING = 2

TableSignature = List[Tuple[str, FieldType]]
Field = str | int
Entry = Dict[str, Field]

class Database:
    """A simple database system that stores tables in binary files."""
    
    def __init__(self, name: str):
        """
        Initialize a new database with the given name.
        Args: name: The name of the database directory where tables will be stored.
        """
        self.name = name
        if not os.path.exists(name):
            os.makedirs(name)
        # Store tables that have been modified in memory
        self._filled_tables = set()
        # In-memory cache of table data
        self._table_data = {}

    def list_tables(self) -> List[str]:
        """
        List all tables in the database.
        Returns: A list of table names (without the .table extension).
        """
        tables = []
        for file in os.listdir(self.name):
            if file.endswith('.table'):
                tables.append(file[:-6])
        return tables

    def create_table(self, table_name: str, *fields: TableSignature) -> None:
        """
        Create a new table with the specified fields.
        Args:- table_name: Name of the table to create.
             - *fields: Variable number of field definitions (name, type pairs).
             
        Raises: ValueError: If a table with the same name already exists.
        """
        table_path = os.path.join(self.name, f'{table_name}.table')
        if os.path.exists(table_path):
            raise ValueError(f"Table {table_name} already exists")

        with open(table_path, 'wb') as f:
            bf = BinaryFile(f)
            # Write the header
            bf.file.write(b"ULDB")
            bf.write_integer(len(fields), 4)

            # Write the table signature
            for name, field_type in fields:
                bf.write_integer(field_type.value, 1)
                bf.write_string(name)

            # Write the string buffer offset and the first available place in the buffer 
            bf.write_integer(0x40, 4), bf.write_integer(0x40, 4) # Initially at 64 bytes offset

            # Write the entry buffer offset
            bf.write_integer(0x50, 4)  # Initially at 80 bytes offset

            # Write the initial string buffer (16 bytes)
            bf.file.write(b"\x00" * 16)

            # Write the initial entry buffer mini-header (20 bytes)
            bf.write_integer(0, 4)  # Last ID used
            bf.write_integer(0, 4)  # Number of entries
            bf.write_integer(-1, 4)  # Pointer to the first entry
            bf.write_integer(-1, 4)  # Pointer to the last entry
            bf.write_integer(-1, 4)  # Reserved pointer
            
        # Initialize in-memory table data
        self._table_data[table_name] = []

    def delete_table(self, table_name: str) -> None:
        """
        Delete a table from the database.
        Args: table_name: Name of the table to delete.
        Raises: ValueError: If the table doesn't exist.
        """
        table_path = os.path.join(self.name, f'{table_name}.table')
        if not os.path.exists(table_path):
            raise ValueError(f"Table {table_name} does not exist")
        os.remove(table_path)
        
    def get_table_signature(self, table_name: str) -> TableSignature:
        """
        Get the field definitions (signature) of a table.
        Args: table_name: Name of the table to inspect.
        Returns: A list of (field_name, field_type) tuples representing the table's structure.
        Raises: ValueError: If the table doesn't exist.
        """
        table_path = os.path.join(self.name, f'{table_name}.table')
        if not os.path.exists(table_path):
            raise ValueError(f"Table {table_name} does not exist")

        with open(table_path, 'rb') as f:
            bf = BinaryFile(f)
            bf.goto(4)  # Skip the magic constant
            num_fields = bf.read_integer(4)

            signature = []
            for _ in range(num_fields):
                field_type_value = bf.read_integer(1)
                field_type = FieldType(field_type_value)
                name = bf.read_string()
                signature.append((name, field_type))

            return signature
        
    def add_entry(self, table_name: str, entry: Entry) -> None:
        """
        Add a new entry to the specified table.
        Args:- table_name: Name of the table to modify.
             - entry: Dictionary of field names to values representing the new entry.
            
        Raises: ValueError: If the table doesn't exist or if the entry doesn't match the table's structure.
        """
        table_path = os.path.join(self.name, f"{table_name}.table")
        if not table_name in self.list_tables():
            raise ValueError(f"Table {table_name} does not exist.")
            
        # Get the table signature to validate the entry
        signature = self.get_table_signature(table_name)
        
        with open(table_path, 'r+b') as f:
            bf = BinaryFile(f)
            
            # Find string fields in the entry that need special handling
            string_fields = []
            for name, field_type in signature:
                if field_type == FieldType.STRING and name in entry:
                    string_fields.append((name, entry[name]))
            
            # Calculate string buffer layout
            string_buffer_start = 0x40  # Fixed position of string buffer
            string_positions = {}
            current_pos = string_buffer_start
            
            # Write strings to buffer and track their positions
            for name, value in string_fields:
                string_positions[name] = current_pos
                encoded = value.encode('utf-8')
                bf.goto(current_pos)
                bf.write_integer(len(encoded), 2)
                bf.file.write(encoded)
                current_pos += 2 + len(encoded)
            
            # Calculate new positions after writing strings
            new_available_string_pos = current_pos
            entry_buffer_pos = 0x60  # Fixed position for entry buffer
            entry_data_pos = 0x74    # Position where entry data starts
            
            # Update header pointers
            bf.goto(52)  # Position of string buffer pointer
            bf.write_integer(string_buffer_start, 4)  # String buffer position (unchanged)
            bf.write_integer(new_available_string_pos, 4)  # New available string position
            bf.write_integer(entry_buffer_pos, 4)  # Entry buffer position
            
            # Write entry buffer header
            bf.goto(entry_buffer_pos)
            bf.write_integer(1, 4)  # Current ID
            bf.write_integer(1, 4)  # Number of entries
            bf.write_integer(entry_data_pos, 4)  # First entry pointer
            bf.write_integer(entry_data_pos, 4)  # Last entry pointer
            
            # Write -1 for the first deleted entry pointer (0xFFFFFFFF)
            f.write(b'\xff\xff\xff\xff')
            
            # Write entry data
            bf.goto(entry_data_pos)
            bf.write_integer(1, 4)  # Entry ID
            
            # Write field values according to their types
            for name, field_type in signature:
                if field_type == FieldType.INTEGER:
                    value = entry.get(name, 0)
                    bf.write_integer(value, 4)
                elif field_type == FieldType.STRING:
                    pos = string_positions.get(name, 0)
                    bf.write_integer(pos, 4)
        
        # Update in-memory representation
        if table_name not in self._table_data:
            self._table_data[table_name] = []
        
        # Add ID to the entry and store it
        entry_with_id = entry.copy()
        entry_with_id['id'] = len(self._table_data[table_name]) + 1
        self._table_data[table_name].append(entry_with_id)
        
        # Mark this table as having been modified
        self._filled_tables.add(table_name)
            
    def get_table_size(self, table_name: str) -> int:
        """
        Get the number of entries in a table.
        Args: table_name: Name of the table to inspect.
        Returns: The number of entries in the table.
        Raises: ValueError: If the table doesn't exist.
        """
        table_path = os.path.join(self.name, f"{table_name}.table")
        if not os.path.exists(table_path):
            raise ValueError(f"Table {table_name} does not exist.")
        
        # Check if the table has been modified in memory
        if table_name in self._filled_tables:
            return len(self._table_data.get(table_name, []))
        else:
            # If not modified, read the size from the file
            with open(table_path, 'rb') as f:
                bf = BinaryFile(f)
                # Go to the entry buffer position to read the number of entries
                bf.goto(60)  # Get entry buffer position
                entry_buffer_pos = bf.read_integer(4)
                bf.goto(entry_buffer_pos + 4)  # Skip past the last ID used
                return bf.read_integer(4)  # Read number of entries
        
    def get_complete_table(self, table_name: str) -> List[Entry]:
        """
        Get all entries from a table.
        Args:- table_name: Name of the table to query.
        Returns:- A list of all entries in the table (as dictionaries).
                - Returns an empty list if the table hasn't been modified in memory.
            
        Raises: ValueError: If the table doesn't exist.
        """
        if table_name not in self.list_tables():
            raise ValueError(f"Table {table_name} doesn't exist")
        
        # If the table wasn't modified in memory, return empty list
        if table_name not in self._filled_tables:
            return []
            
        # Return the cached table data
        return self._table_data.get(table_name, [])

    def get_entry(self, table_name: str, field_name: str, field_value: Field) -> Entry | None:
        """
        Get a single entry matching the specified criteria.
        Args:- table_name: Name of the table to query.
             - field_name: Name of the field to match against.
             - field_value: Value to match in the specified field.
            
        Returns: The first matching entry as a dictionary, or None if no match is found.
        """
        # Get all entries from the table
        entries = self.get_complete_table(table_name)
        
        # Find the first matching entry
        for entry in entries:
            if entry.get(field_name) == field_value:
                return entry
        
        # Return None if no match found
        return None

    def get_entries(self, table_name: str, field_name: str, field_value: Field) -> list[Entry]:
        """
        Get all entries matching the specified criteria.
        Args:- table_name: Name of the table to query.
             - field_name: Name of the field to match against.
             - field_value: Value to match in the specified field.
            
        Returns:- A list of all matching entries (as dictionaries).
                - Returns an empty list if no matches are found.
            
        Raises: ValueError: If the table doesn't exist.
        """
        # Check if table exists
        if table_name not in self.list_tables():
            raise ValueError(f"Table {table_name} does not exist")
        
        # Get all entries from the table
        entries = self.get_complete_table(table_name)
        
        # Find all matching entries
        matching_entries = []
        for entry in entries:
            if entry.get(field_name) == field_value:
                matching_entries.append(entry)
        
        return matching_entries

    def select_entry(self, table_name: str, fields: tuple[str], field_name: str, field_value: Field) -> Field | tuple[Field]:
        """
        Get specific fields from a single matching entry.
        Args:- table_name: Name of the table to query.
             - fields: Tuple of field names to retrieve.
             - field_name: Name of the field to match against.
             - field_value: Value to match in the specified field.
            
        Returns:- If one field is requested: the field value.
                - If multiple fields: a tuple of field values.
                - None if no matching entry is found.
        """
        # Get the matching entry
        entry = self.get_entry(table_name, field_name, field_value)
        
        # Return None if no entry found
        if entry is None:
            return None
        
        # Return single value or tuple of values
        if len(fields) == 1:
            return entry.get(fields[0])
        return tuple(entry.get(field) for field in fields)

    def select_entries(self, table_name: str, fields: tuple[str], field_name: str, field_value: Field) -> list[Field | tuple[Field]]:
        """
        Get specific fields from all matching entries.
        Args:- table_name: Name of the table to query.
             - fields: Tuple of field names to retrieve.
             - field_name: Name of the field to match against.
             - field_value: Value to match in the specified field.
            
        Returns: A list of values or tuples of values for the requested fields.
        """
        # Get all matching entries
        entries = self.get_entries(table_name, field_name, field_value)
        
        # Extract requested fields from each entry
        results = []
        for entry in entries:
            if len(fields) == 1:
                results.append(entry.get(fields[0]))
            else:
                results.append(tuple(entry.get(field) for field in fields))
        
        return results
    
    def update_entries(self, table_str: str, cond_name: str, cond_value: Field, update_name: str, update_value: Field) -> bool:
        """
        Update entries matching the specified criteria.
        Args:- table_str: Name of the table to modify.
             - cond_name: Name of the field to match against.
             - cond_value: Value to match in the specified field.
             - update_name: Name of the field to update.
             - update_value: New value for the field.
            
        Returns: True if at least one entry was modified, False otherwise.
        Raises: ValueError: If the table doesn't exist, or if types don't match.
        """
        # Check if table exists
        if table_str not in self.list_tables():
            raise ValueError(f"Table {table_str} does not exist")
        
        # Get the table signature for type validation
        signature = self.get_table_signature(table_str)
        field_types = {name: field_type for name, field_type in signature}
        
        # Validate the update field exists
        if update_name not in field_types:
            raise ValueError(f"Field {update_name} does not exist in table {table_str}")
        
        # Validate the update value type
        expected_type = field_types[update_name]
        if expected_type == FieldType.INTEGER and not isinstance(update_value, int):
            raise ValueError(f"Field {update_name} expects an integer value")
        elif expected_type == FieldType.STRING and not isinstance(update_value, str):
            raise ValueError(f"Field {update_name} expects a string value")
        
        # Get all entries and look for matches
        entries = self.get_complete_table(table_str)
        modified = False
        
        # Update matching entries
        for entry in entries:
            if entry.get(cond_name) == cond_value:
                entry[update_name] = update_value
                modified = True
        
        # Return False if no modifications were made
        if not modified:
            return False
        
        # Update the in-memory representation
        self._table_data[table_str] = entries
        
        return True
    
    def delete_entries(self, table_name: str, field_name: str, field_value: Field) -> bool:
        """
        Delete entries matching the specified criteria.
        Args:- table_name: Name of the table to modify.
             - field_name: Name of the field to match against.
             - field_value: Value to match in the specified field.
            
        Returns: True if at least one entry was deleted, False otherwise.
        Raises: ValueError: If the table doesn't exist or if types don't match.
        """
        # Check if table exists
        if table_name not in self.list_tables():
            raise ValueError(f"Table {table_name} does not exist")
        
        # Get the table signature for type validation
        signature = self.get_table_signature(table_name)
        field_types = {name: field_type for name, field_type in signature}
        
        # Validate the field exists
        if field_name not in field_types and field_name != 'id':
            raise ValueError(f"Field {field_name} does not exist in table {table_name}")
        
        # Validate the field value type
        if field_name in field_types:
            expected_type = field_types[field_name]
            if expected_type == FieldType.INTEGER and not isinstance(field_value, int):
                raise ValueError(f"Field {field_name} expects an integer value")
            elif expected_type == FieldType.STRING and not isinstance(field_value, str):
                raise ValueError(f"Field {field_name} expects a string value")
        
        # Get all entries and filter out matches
        entries = self.get_complete_table(table_name)
        entries_to_keep = []
        deleted_any = False
        
        for entry in entries:
            if entry.get(field_name) == field_value:
                deleted_any = True
            else:
                entries_to_keep.append(entry)
        
        # Return False if no deletions occurred
        if not deleted_any:
            return False
        
        # Update in-memory representation
        self._table_data[table_name] = entries_to_keep
        
        # Update the file to reflect deletions
        table_path = os.path.join(self.name, f"{table_name}.table")
        
        with open(table_path, 'r+b') as f:
            # Update the entry count in the file header
            f.seek(0x64)  # Position of entry count in header
            f.write(len(entries_to_keep).to_bytes(4, byteorder='little'))
        
            # Truncate the file to remove deleted entries
            f.truncate(max(80, 80 + len(entries_to_keep) * 10))

        return True
