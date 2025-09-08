import sys
import os
import re
from enum import Enum
from typing import Union, Tuple, List, Dict
from database import Database, FieldType

class CommandType(Enum):
    """Enumeration of all supported command types in the ULDB interpreter."""
    OPEN = 1                # Open a database
    CREATE_TABLE = 2         # Create a new table
    DELETE_TABLE = 3         # Delete an existing table
    LIST_TABLES = 4          # List all tables in the database
    INSERT_TO = 5            # Insert data into a table
    FROM_IF_GET = 6          # Conditional query (SELECT with WHERE)
    FROM_DELETE_WHERE = 7    # Conditional deletion (DELETE with WHERE)
    FROM_UPDATE_WHERE = 8    # Conditional update (UPDATE with WHERE)
    QUIT = 9                 # Exit the interpreter

class ULDBInterpreter:
    """
    Main interpreter class for the ULDB command language.
    Handles both interactive and script-based execution of database commands.
    """

    def __init__(self):
        """Initialize the interpreter with no active database."""
        self._db: Database = None      # Currently open database instance
        self._running = True           # Flag for main loop control
        self._prompt = "uldb:: "       # Command prompt for interactive mode

    def run(self) -> None:
        """
        Run the interpreter in either script or interactive mode.
        Determines the mode based on command-line arguments:
        - With script filename: executes commands from the file
        - Without arguments: starts interactive command prompt
        """
        if len(sys.argv) > 1:
            self._run_script(sys.argv[1])
        else:
            self._run_interactive()

    def _run_interactive(self) -> None:
        """
        Run the interpreter in interactive mode.
        Continuously prompts for user input and processes commands until
        the user quits or an interrupt signal is received.
        """
        while self._running:
            try:
                command = input(self._prompt).strip()
                if not command:
                    continue
                self._process_command(command)
            except EOFError:
                print()  # Print newline on EOF (Ctrl+D)
                break
            except KeyboardInterrupt:
                print("\nInterrupted")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

    def _run_script(self, filename: str) -> None:
        """
        Execute commands from a script file.
        Args: filename: Path to the script file containing ULDB commands
        Exits the program if the file cannot be read or contains errors.
        """
        try:
            if not os.path.exists(filename):
                print(f"Error: Script file '{filename}' not found")
                sys.exit(1)

            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self._process_command(line)
        except Exception as e:
            print(f"Error reading script: {str(e)}")
            sys.exit(1)

    def _process_command(self, command: str) -> None:
        """
        Process a single command string.
        Args: command: The raw command string to process
        Handles special cases (like quit) and dispatches to command parsers.
        """
        # Handle quit commands
        if command.lower() in ('quit', 'q'):
            self._running = False
            return

        # Parse and execute the command
        try:
            cmd_type, args = self._parse_command(command)
            self._execute_command(cmd_type, args)
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

    def _parse_command(self, command: str) -> Tuple[CommandType, dict]:
        """
        Parse a command string into its type and arguments.
        Args: command: The command string to parse
        Returns: Tuple of (CommandType, arguments_dict)
        Raises: ValueError: If the command format is invalid or unknown
        """
        # Validate basic command structure (name(args))
        if not re.fullmatch(r'^[a-zA-Z_]+\([^)]*\)$', command):
            raise ValueError("Invalid command format")

        # Extract command name and arguments string
        cmd_name, args_str = command.split('(', 1)
        args_str = args_str.rstrip(')')
        cmd_name = cmd_name.lower()

        # Dispatch to specific command parsers
        if cmd_name == 'open':
            return CommandType.OPEN, self._parse_open(args_str)
        elif cmd_name == 'create_table':
            return CommandType.CREATE_TABLE, self._parse_create_table(args_str)
        elif cmd_name == 'delete_table':
            return CommandType.DELETE_TABLE, self._parse_delete_table(args_str)
        elif cmd_name == 'list_tables':
            return CommandType.LIST_TABLES, {}
        elif cmd_name == 'insert_to':
            return CommandType.INSERT_TO, self._parse_insert_to(args_str)
        elif cmd_name == 'from_if_get':
            return CommandType.FROM_IF_GET, self._parse_from_if_get(args_str)
        elif cmd_name == 'from_delete_where':
            return CommandType.FROM_DELETE_WHERE, self._parse_conditional(args_str)
        elif cmd_name == 'from_update_where':
            return CommandType.FROM_UPDATE_WHERE, self._parse_update(args_str)
        else:
            raise ValueError(f"Unknown command: {cmd_name}")

    def _parse_open(self, args_str: str) -> Dict[str, str]:
        """
        Parse arguments for the OPEN command.
        Args:  args_str: The arguments string (should contain just the database name)
        Returns: Dictionary with 'db_name' key
        Raises: ValueError: If database name is missing
        """
        if not args_str:
            raise ValueError("Missing database name")
        return {'db_name': args_str}

    def _parse_create_table(self, args_str: str) -> Dict[str, Union[str, List[Tuple[str, FieldType]]]]:
        """
        Parse arguments for the CREATE_TABLE command.
        Format: create_table(table_name,name1=type1,name2=type2,...)
        Args: args_str: The arguments string containing table definition
        Returns: Dictionary with 'table_name' and 'fields' keys
        Raises: ValueError: If syntax is invalid or field types are unknown
        """
        parts = [p.strip() for p in args_str.split(',')]
        if len(parts) < 2:
            raise ValueError("Invalid table creation syntax")

        table_name = parts[0]
        fields = []
        
        for field_def in parts[1:]:
            try:
                name, type_str = field_def.split('=')
                name = name.strip()
                type_str = type_str.strip().upper()
                
                try:
                    field_type = FieldType[type_str]
                except KeyError:
                    raise ValueError(f"Invalid field type: {type_str}")
                
                fields.append((name, field_type))
            except ValueError:
                raise ValueError(f"Invalid field definition: {field_def}")
        
        return {'table_name': table_name, 'fields': fields}

    def _parse_delete_table(self, args_str: str) -> Dict[str, str]:
        """
        Parse arguments for the DELETE_TABLE command.
        Args: args_str: The arguments string (should contain just the table name)
        Returns: Dictionary with 'table_name' key
        Raises: ValueError: If table name is missing
        """
        if not args_str:
            raise ValueError("Missing table name")
        return {'table_name': args_str}

    def _parse_insert_to(self, args_str: str) -> Dict[str, Union[str, Dict[str, Union[str, int]]]]:
        """
        Parse arguments for the INSERT_TO command.
        Format: insert_to(table_name,name1=value1,name2=value2,...)
        Args: args_str: The arguments string containing insertion data
        Returns: Dictionary with 'table_name' and 'entry' keys
        Raises: ValueError: If syntax is invalid or values are malformed
        """
        parts = [p.strip() for p in args_str.split(',')]
        if len(parts) < 2:
            raise ValueError("Invalid insert syntax")

        table_name = parts[0]
        entry = {}
        
        for field_def in parts[1:]:
            try:
                name, value_str = field_def.split('=')
                name = name.strip()
                value_str = value_str.strip()
                
                # Parse string values (quoted) or integer values
                if value_str.startswith('"') and value_str.endswith('"'):
                    value = value_str[1:-1]
                else:
                    try:
                        value = int(value_str)
                    except ValueError:
                        raise ValueError(f"Invalid integer value: {value_str}")
                
                entry[name] = value
            except ValueError:
                raise ValueError(f"Invalid field assignment: {field_def}")
        
        return {'table_name': table_name, 'entry': entry}

    def _parse_from_if_get(self, args_str: str) -> Dict[str, Union[str, List[str]]]:
        """
        Parse arguments for the FROM_IF_GET (conditional query) command.
        Format: from_if_get(table_name,cond_name=cond_value,name1,name2,...)
        Special case: '*' selects all fields except id
        Args: args_str: The arguments string containing query parameters
        Returns: Dictionary with table name, condition, and fields to select
        Raises: ValueError: If syntax is invalid or values are malformed
        """
        parts = [p.strip() for p in args_str.split(',')]
        if len(parts) < 2:
            raise ValueError("Invalid from_if_get syntax")

        table_name = parts[0]
        
        # Parse condition (name=value)
        try:
            cond_name, cond_value_str = parts[1].split('=')
            cond_name = cond_name.strip()
            cond_value_str = cond_value_str.strip()
            
            # Parse condition value (string or integer)
            if cond_value_str.startswith('"') and cond_value_str.endswith('"'):
                cond_value = cond_value_str[1:-1]
            else:
                try:
                    cond_value = int(cond_value_str)
                except ValueError:
                    raise ValueError(f"Invalid condition value: {cond_value_str}")
        except ValueError:
            raise ValueError(f"Invalid condition: {parts[1]}")

        # Parse fields to select (or handle '*' wildcard)
        fields = []
        for field in parts[2:]:
            field = field.strip()
            if field == '*':
                fields = ['*']
                break
            fields.append(field)
        
        return {
            'table_name': table_name,
            'cond_name': cond_name,
            'cond_value': cond_value,
            'fields': fields
        }

    def _parse_conditional(self, args_str: str) -> Dict[str, Union[str, int, str]]:
        """
        Parse arguments for conditional commands (DELETE/UPDATE).
        Format: command(table_name,cond_name=cond_value)
        Args: args_str: The arguments string containing condition
        Returns: Dictionary with table name and condition parameters
        Raises: ValueError: If syntax is invalid or values are malformed
        """
        parts = [p.strip() for p in args_str.split(',')]
        if len(parts) != 2:
            raise ValueError("Invalid conditional syntax")

        table_name = parts[0]
        
        # Parse condition (name=value)
        try:
            cond_name, cond_value_str = parts[1].split('=')
            cond_name = cond_name.strip()
            cond_value_str = cond_value_str.strip()
            
            # Parse condition value (string or integer)
            if cond_value_str.startswith('"') and cond_value_str.endswith('"'):
                cond_value = cond_value_str[1:-1]
            else:
                try:
                    cond_value = int(cond_value_str)
                except ValueError:
                    raise ValueError(f"Invalid condition value: {cond_value_str}")
        except ValueError:
            raise ValueError(f"Invalid condition: {parts[1]}")

        return {
            'table_name': table_name,
            'cond_name': cond_name,
            'cond_value': cond_value
        }

    def _parse_update(self, args_str: str) -> Dict[str, Union[str, int, str]]:
        """
        Parse arguments for the FROM_UPDATE_WHERE command.
        Format: from_update_where(table_name,cond_name=cond_value,name=new_value)
        Args: args_str: The arguments string containing update parameters
        Returns: Dictionary with table name, condition, and update parameters
        Raises: ValueError: If syntax is invalid or values are malformed
        """
        parts = [p.strip() for p in args_str.split(',')]
        if len(parts) != 3:
            raise ValueError("Invalid update syntax")

        table_name = parts[0]
        
        # Parse condition (name=value)
        try:
            cond_name, cond_value_str = parts[1].split('=')
            cond_name = cond_name.strip()
            cond_value_str = cond_value_str.strip()
            
            # Parse condition value (string or integer)
            if cond_value_str.startswith('"') and cond_value_str.endswith('"'):
                cond_value = cond_value_str[1:-1]
            else:
                try:
                    cond_value = int(cond_value_str)
                except ValueError:
                    raise ValueError(f"Invalid condition value: {cond_value_str}")
        except ValueError:
            raise ValueError(f"Invalid condition: {parts[1]}")

        # Parse update (name=new_value)
        try:
            update_name, update_value_str = parts[2].split('=')
            update_name = update_name.strip()
            update_value_str = update_value_str.strip()
            
            # Parse update value (string or integer)
            if update_value_str.startswith('"') and update_value_str.endswith('"'):
                update_value = update_value_str[1:-1]
            else:
                try:
                    update_value = int(update_value_str)
                except ValueError:
                    raise ValueError(f"Invalid update value: {update_value_str}")
        except ValueError:
            raise ValueError(f"Invalid update: {parts[2]}")

        return {
            'table_name': table_name,
            'cond_name': cond_name,
            'cond_value': cond_value,
            'update_name': update_name,
            'update_value': update_value
        }

    def _execute_command(self, cmd_type: CommandType, args: dict) -> None:
        """
        Execute a parsed command by dispatching to the appropriate method.
        Args:- cmd_type: The type of command to execute
             - args: Dictionary of parsed arguments for the command
        """
        if cmd_type == CommandType.OPEN:
            self._execute_open(args)
        elif cmd_type == CommandType.CREATE_TABLE:
            self._execute_create_table(args)
        elif cmd_type == CommandType.DELETE_TABLE:
            self._execute_delete_table(args)
        elif cmd_type == CommandType.LIST_TABLES:
            self._execute_list_tables()
        elif cmd_type == CommandType.INSERT_TO:
            self._execute_insert_to(args)
        elif cmd_type == CommandType.FROM_IF_GET:
            self._execute_from_if_get(args)
        elif cmd_type == CommandType.FROM_DELETE_WHERE:
            self._execute_from_delete_where(args)
        elif cmd_type == CommandType.FROM_UPDATE_WHERE:
            self._execute_from_update_where(args)

    def _execute_open(self, args: dict) -> None:
        """
        Execute the OPEN command to open a database.
        Args: args: Dictionary containing 'db_name' key
        """
        if self._db is not None:
            print("Error: A database is already open")
            return
        
        try:
            self._db = Database(args['db_name'])
        except Exception as e:
            print(f"Error opening database: {str(e)}")

    def _execute_create_table(self, args: dict) -> None:
        """
        Execute the CREATE_TABLE command to create a new table.
        Args: args: Dictionary containing 'table_name' and 'fields' keys
        """
        if self._db is None:
            print("Error: No database is open")
            return
        
        try:
            self._db.create_table(args['table_name'], *args['fields'])
        except ValueError as e:
            print(f"Error creating table: {str(e)}")

    def _execute_delete_table(self, args: dict) -> None:
        """
        Execute the DELETE_TABLE command to remove a table.
        Args: args: Dictionary containing 'table_name' key
        """
        if self._db is None:
            print("Error: No database is open")
            return
        
        try:
            self._db.delete_table(args['table_name'])
        except ValueError as e:
            print(f"Error deleting table: {str(e)}")

    def _execute_list_tables(self) -> None:
        """Execute the LIST_TABLES command to display all tables."""
        if self._db is None:
            print("Error: No database is open")
            return
        
        tables = self._db.list_tables()
        for table in tables:
            print(table)

    def _execute_insert_to(self, args: dict) -> None:
        """
        Execute the INSERT_TO command to add data to a table.
        Args: args: Dictionary containing 'table_name' and 'entry' keys
        """
        if self._db is None:
            print("Error: No database is open")
            return
        
        try:
            self._db.add_entry(args['table_name'], args['entry'])
        except ValueError as e:
            print(f"Error adding entry: {str(e)}")

    def _execute_from_if_get(self, args: dict) -> None:
        """
        Execute the FROM_IF_GET command to query data with a condition.
        Args: args: Dictionary containing table name, condition, and fields
        """
        if self._db is None:
            print("Error: No database is open")
            return
        
        try:
            # Handle special case for * (all fields)
            if args['fields'] == ['*']:
                # Get all fields except id
                signature = self._db.get_table_signature(args['table_name'])
                fields = [name for name, _ in signature]
                entries = self._db.select_entries(
                    args['table_name'],
                    fields,
                    args['cond_name'],
                    args['cond_value']
                )
            else:
                entries = self._db.select_entries(
                    args['table_name'],
                    tuple(args['fields']),
                    args['cond_name'],
                    args['cond_value']
                )
            
            # Format output as specified
            for entry in entries:
                if isinstance(entry, tuple):
                    if len(entry) == 1:
                        print(entry[0])
                    else:
                        print(entry)
                else:
                    print(entry)
        except ValueError as e:
            print(f"Error retrieving entries: {str(e)}")

    def _execute_from_delete_where(self, args: dict) -> None:
        """
        Execute the FROM_DELETE_WHERE command to delete matching entries.
        Args: args: Dictionary containing table name and condition
        """
        if self._db is None:
            print("Error: No database is open")
            return
        
        try:
            self._db.delete_entries(
                args['table_name'],
                args['cond_name'],
                args['cond_value']
            )
        except ValueError as e:
            print(f"Error deleting entries: {str(e)}")

    def _execute_from_update_where(self, args: dict) -> None:
        """
        Execute the FROM_UPDATE_WHERE command to update matching entries.
        Args: args: Dictionary containing table name, condition, and update data
        """
        if self._db is None:
            print("Error: No database is open")
            return
        
        try:
            self._db.update_entries(
                args['table_name'],
                args['cond_name'],
                args['cond_value'],
                args['update_name'],
                args['update_value']
            )
        except ValueError as e:
            print(f"Error updating entries: {str(e)}")

def main():
    """Main entry point for the ULDB interpreter."""
    interpreter = ULDBInterpreter()
    interpreter.run()

if __name__ == "__main__":
    main()
