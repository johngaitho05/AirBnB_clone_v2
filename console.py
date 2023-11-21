#!/usr/bin/python3
""" Console Module """
import cmd
import re
import sys

from sqlalchemy.exc import IntegrityError

from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = "(hbnb) "

    __classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    # dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }
    __commands = {
        'all': r'^\.all(\(\))$',
        'count': r'^\.count(\(\))$',
        'show': r'^\.show(\(.*?\))$',
        'destroy': r'^\.destroy(\(.*?\))$',
        'update': r'^\.update(\(.*?\))$',
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def _split_dict(self, args):
        """Splits args in to className and kwargs"""

        def parse_value(value):
            if value.startswith('"') and value.endswith('"'):
                # String value
                value = value[1:-1].replace('\\"', '"').replace('_', ' ')
                return value
            elif '.' in value:
                # Float value
                try:
                    return float(value)
                except ValueError:
                    pass
            else:
                # Integer value
                try:
                    return int(value)
                except ValueError:
                    pass
            # If value doesn't match any recognized format, return None
            return None

        # Split the input string into components
        components = args.split()

        if len(components) < 1:
            # Invalid input format
            return None

        class_name = components[0]
        params = {}

        for param in components[1:]:
            key_value = param.split('=')
            if len(key_value) == 2:
                k, v = key_value
                parsed_value = parse_value(v)
                if parsed_value is not None:
                    params[k] = parsed_value

        return class_name, params

    def _split(self, arg):
        """Split the line in to substrings based on double quotes and spaces"""
        pattern = r'("[^"]+"|\{[^}]*\}|\S+)'
        res = re.findall(pattern, arg)
        for i in range(len(res)):
            try:
                v = eval(res[i])
                if type(v) in (int, str, float, dict):
                    res[i] = v
            except (NameError, SyntaxError, TypeError):
                continue
        return res

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        klas, kwargs = self._split_dict(args)
        if klas not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.__classes[klas](**kwargs)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, arg):
        """prints the string representation of an instance"""
        arg = self._split(arg)
        if not arg:
            return print("** class name missing **")
        if arg[0] not in self.__classes:
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        key = "{}.{}".format(arg[0], arg[1])
        instance = storage.all().get(key)
        if not instance:
            return print("** no instance found **")
        print(instance)

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, arg):
        """deletes an instance given a classname and instance id"""
        arg = self._split(arg)
        if not arg:
            return print("** class name missing **")
        if arg[0] not in self.__classes:
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        key = "{}.{}".format(arg[0], arg[1])
        instance = storage.all().get(key)
        if not instance:
            return print("** no instance found **")
        storage.delete(instance)
        storage.save()

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """prints all instances of a given model"""
        arg = self._split(arg)
        if not arg:
            return print([str(instance) for k, instance in
                          storage.all().items()])
        klas = arg[0]
        if klas not in self.__classes:
            return print("** class doesn't exist **")
        instances = [str(instance) for k, instance in
                     storage.all(self.__classes[klas]).items()]
        print(instances)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, arg):
        """Count instances based on className"""
        args = self._split_dict(arg)
        klas = args[0]
        match = list(filter(lambda k: k.startswith('{}.'.format(klas)),
                            storage.all().keys()))
        print(len(match))

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    def _eval(self, value):
        """Adds double quotes to a string"""
        if type(value) is str:
            return '"{}"'.format(value)
        return str(value)

    def do_update(self, arg):
        """updates a model instance"""
        arg = self._split(arg)
        if not arg:
            return print("** class name missing **")
        if arg[0] not in self.__classes:
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        key = "{}.{}".format(arg[0], arg[1])
        instance = storage.all().get(key)
        if not instance:
            return print("** no instance found **")
        if len(arg) < 3:
            return print("** attribute name missing **")
        kw = {}
        if type(arg[2]) is dict:
            kw = arg[2]
        if not kw and len(arg) < 4:
            return print("** value missing **")
        if not kw:
            kw = {arg[2]: arg[3]}
        for k, v in kw.items():
            setattr(instance, k, v)
        instance.save()

    def parse_line(self, line, klas):
        """parse the input string"""

        command = line[len(klas):]
        for c in self.__commands.keys():
            match = re.match(self.__commands[c], command)
            if match:
                args = eval(match.group(1))
                if not args:
                    return "{} {}".format(c, klas)
                if type(args) is not tuple:
                    args = [args]
                args = " ".join([self._eval(arg) for arg in args])
                return "{} {} {}".format(c, klas, args)
        return line

    def onecmd(self, line):
        """Override to handle advanced commands"""
        if line in ['all', '.all()']:
            return self.do_all("")
        pattern = r"([a-zA-Z]*)\.(all|count|show|destroy|update)"
        match = re.search(pattern, line)
        if match:
            klas = match.group(1)
            if not klas:
                return print("** class name missing **")
            elif klas not in self.__classes:
                return print("** class doesn't exist **")
            line = self.parse_line(line, klas)
        return super(HBNBCommand, self).onecmd(line)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
