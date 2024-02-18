#!/usr/bin/env python3
"""
 Entry point of the command interpreter
"""


import cmd
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models import storage
import re
import uuid


class HBNBCommand(cmd.Cmd):
    """Our Console Class"""

    prompt = "(hbnb) "
    __classes = ["BaseModel", "User", "State", "City", "Place", "Amenity",
                 "Review"]

    def do_quit(self, args):
        """
        quit command to exit the program
        Usage: quit
        """
        return True

    def do_EOF(self, args):
        """
        EOF command to exit the program
        Usage: Ctrl+d
        """
        return True

    def emptyline(self):
        """Emptyline handler that does nothing with Enter key"""
        pass

    def do_create(self, args):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Usage: $ create BaseModel
        """
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        new_instace = eval(args[0])()  # to create an instance
        new_instace.save()
        print(new_instace.id)

    def do_show(self, args):
        """
        Prints the string representation of an
        instance based on the class name and id.
        Usage: show <Class Name> <ID>
        """
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        print(f'{args[0]}.{args[1]}')
        if f'{args[0]}.{args[1]}' not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[f'{args[0]}.{args[1]}'])

    def do_destroy(self, args):
        """
        Deletes an instance based on the class name and id
        Usage: destroy <Class Name> <ID>
        """
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if f'{args[0]}.{args[1]}' not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[f'{args[0]}.{args[1]}']
        storage.save()

    def do_all(self, args):
        """
        Prints all string representation of all instances based
        or not on the class name
        Usage: $ all BaseModel or $ all
        """
        if not args:
            print([str(obj) for obj in storage.all().values()])
            return
        args = args.split()
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        out_list = []
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                out_list.append(str(obj))
        print(out_list)

    def do_update(self, args):
        """
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        Ex: $ update
        """
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if f'{args[0]}.{args[1]}' not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        # casting value to the correct type, trying int then float and string
        if args[3].isdigit():
            new_value = int(args[3])
        else:
            try:
                new_value = float(args[3])
            except ValueError:
                new_value = args[3].replace('"', "")
        for key, obj in storage.all().items():
            if f'{args[0]}.{args[1]}' == key:
                setattr(obj, args[2], new_value)
                storage.save()
                return

    def do_count(self, args):
        """
        retrieve the number of instances of a class
        Usage: <class name>.count().
        """
        if not args:
            print("** class doesn't exist **")
        objects = storage.all()
        args = args.split()
        count = 0
        for obj in objects.values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def default(self, line):
        """
        handle dot notaion commands
        functions:
        - update, all, show, destroy, count
        """
        if '.' in line:
            objects = storage.all()
            cls, method = line.split('.')

            if method == 'all()':
                self.do_all(cls)
            if method == 'count()':
                self.do_count(cls)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
