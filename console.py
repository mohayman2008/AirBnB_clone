#!/usr/bin/python3
'''This module contains the definition of the command interpreter class
'HBNBCommand' in the AirBnB clone app and contains the entry point of the
command interpreter
'''
import cmd
import re
import sys

from models.base_model import BaseModel
from models import storage

classes = {"BaseModel": BaseModel}


class HBNBCommand(cmd.Cmd):
    '''the command interpreter class in the AirBnB clone app'''

    prompt = "(hbnb) "
    l_c = ['create', 'show', 'update', 'all', 'destroy', 'count']
    if not sys.stdin.isatty():
        use_rawinput = False
    fmt_re = re.compile(r'^[A-Za-z]*\.\w+(.*)$')

    def parse_args(self, line, delimiters=None, enclosings=None):
        """Parse comma separated string of arguments"""
        if enclosings is None:
            enclosings = {"'": "'", '"': '"', '{': '}'}
        if delimiters is None:
            delimiters = ' ,\r\n\t'

        line = line.strip(delimiters)
        args = []
        begin = end = 0
        i, n = 0, len(line)
        while i < n:
            char = line[i]
            if char in enclosings.keys():
                end = begin = i
                endx = i - 1
                i += 1
                while i < n and line[i] != enclosings[char]:
                    if line[i] in delimiters and endx < begin:
                        endx = i
                    end = i
                    i += 1
                if i < n and line[i] == enclosings[char]:
                    end += 1
                    i += 1
                    args.append(line[begin:end + 1])
                else:
                    args.append(line[begin:endx])
                    i = endx
            elif char in delimiters:
                while i < n and line[i] in delimiters:
                    i += 1
            else:
                begin = i
                while i < n and line[i] not in delimiters:
                    end = i
                    i += 1
                args.append(line[begin:end + 1])
        return args

    def onecmd(self, line):
        """Parses a command line"""
        line = line.strip()
        if self.fmt_re.match(line) is None:
            return cmd.Cmd.onecmd(self, line)
        else:
            # Spliting the line arround '.'
            line_split = line.split('.', 1)
            cls_name = line_split[0]
            rest_line_split = line_split[1][:-1].split('(', 1)
            _cmd = rest_line_split[0]
            args = rest_line_split[1].strip()
            args_l = self.parse_args(args)

            id = ''
            args = ''
            if args_l:
                id = args_l[0]
            if len(args_l) > 1:
                args = ' '.join(args_l[1:])

            if _cmd != 'update' or len(args_l) < 2:
                pass
            elif args_l[1][0] == '{' and args_l[1][-1] == '}':
                return self.update_from_dict(cls_name, id, args_l[1])

            if args:
                args = ' ' + args
            if id:
                args = ' ' + id + args

            line = f'{_cmd} {cls_name}{args}'
            return cmd.Cmd.onecmd(self, line)

    def do_quit(self, line):
        '''\tquit: exits the program'''
        return True

    def do_EOF(self, line):
        '''\tEOF (CTRL+D) command to exit the program'''
        return True

    def emptyline(self):
        return

    @staticmethod
    def check_class(line, check_len=True):
        '''Checks if the class argument exists and is valid,
        The 'line' argument is a string that should start with the class name
        Return: The class name string if input is valid and None other wise
        '''
        if len(line) < 1 and check_len:
            print("** class name missing **")
            return None

        cls_name = line.split(' ')[0]
        if cls_name in classes.keys():
            return cls_name
        print("** class doesn't exist **")
        return None

    @staticmethod
    def check_class_id(line):
        '''Checks the validity the class argument using 'check_class(line)',
        then checks that the second argument exists and is valid 'id'
        The 'line' argument is a string that should start with the class name
        followed by an id
        Return: Key index for the object in the storage.all() dictionary
        if the class and id comination is valid and None otherwise
        '''
        cls_name = HBNBCommand.check_class(line)
        if not cls_name:
            return None

        args = line.split(' ')
        if len(args) < 2:
            print("** instance id missing **")
            return None

        id = args[1]
        key = f"{cls_name}.{id}"
        if key in storage.all().keys():
            return key
        print("** no instance found **")
        return None

    def do_create(self, line):
        '''\tcreate: Creates a new instance of a BaseModel class, saves it to
        \tthe storage engine and prints the id'''

        cls_name = self.check_class(line)
        if cls_name:
            cls = classes[cls_name]
        obj = cls()
        obj.save()
        print(obj.id)

    def do_show(self, line):
        '''\tshow: Prints the string representation of an instance based on
        \tthe class name and id'''
        key = self.check_class_id(line)
        if key:
            print(storage.all()[key])

    def do_destroy(self, line):
        '''\tdestroy: Deletes an instance based on the class name and id and
        \tsave the change to the storage engine'''
        key = self.check_class_id(line)
        if key:
            del storage.all()[key]
            storage.save()

    def do_all(self, line):
        '''\tall: Prints all string representation of all instances
        \tbased or not on the class name'''
        if len(line.split(' ')[0]):
            cls_name = self.check_class(line, check_len=False)
            if not cls_name:
                return

            obj_list = []
            for key, val in storage.all().items():
                if key.split('.')[0] == cls_name:
                    obj_list.append(str(val))
        else:
            obj_list = []
            for val in storage.all().values():
                obj_list.append(str(val))
        print(obj_list)

    def do_update(self, line):
        '''\tupdate: Updates an instance based on the class name and id by
        \tadding or updating attribute and save the change into the storage
        \tengine'''
        key = self.check_class_id(line)
        if not key:
            return

        args = (',').join(line.split(', ')).split(',')
        args = args[0].split() + args[1:]

        if len(args) < 3:
            print('** attribute name missing **')
        elif len(args) < 4:
            print('** value missing **')
        else:
            attr = args[2]
            val = args[3]
            if val[0] == '\"':
                idx1 = 0
                for i in range(3):
                    idx1 = line.find(' ', idx1 + 1)
                idx1 = line.find('\"', idx1 + 1) + 1
                idx2 = line.find('\"', idx1)
                if idx2 < 0:
                    print('** value missing **')
                    return None
                val = line[idx1:idx2]
            obj = storage.all()[key]
            attrib_old = getattr(obj, attr, None)
            if attrib_old is None:
                attrib_type = str
            else:
                attrib_type = type(attrib_old)
            if attrib_type not in [str, int, float]:
                return None
            setattr(obj, attr, attrib_type(val))
            obj.save()

    def update_from_dict(self, cls_name, id, attr_dict):
        """Update attributes from dictionary"""
        id = id.strip('\'"')
        key = self.check_class_id(cls_name + id)
        if key is None:
            return None
        updates = attr_dict[1:-1].split(',')
        if not updates:
            print('** attribute name missing **')
            return None

        for update in updates:
            key_val = update.strip().split(":")
            if not update or key_val[0] == '':
                print('** attribute name missing **')
                return None
            if len(key_val) < 2 or key_val[1] == '':
                print('** value missing **')
                return None

            name = key_val[0].strip().strip('\'"')
            value = key_val[1].strip().strip('\'"')
            self.do_update(f'{cls_name} {id} {name} "{value}"')


if __name__ == '__main__':
    HBNBCommand().cmdloop()
