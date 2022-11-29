#!/usr/bin/python3
"""This module implements the console interpreter"""
import cmd
import sys

from models import engine, storage
classes = engine.classes


class HBNBCommand(cmd.Cmd):
    """The console class"""

    l_c = ['create', 'show', 'update', 'all', 'destroy', 'count']

    def __init__(self, *args, **kwargs):
        """Initiate the console"""
        self.prompt = '(hbnb) '
        if not sys.stdin.isatty():
            self.use_rawinput = False
        cmd.Cmd.__init__(self)

    def precmd(self, arg):
        """parses command input"""
        if '.' in arg and '(' in arg and ')' in arg:
            cls = arg.split('.')
            cnd = cls[1].split('(')
            args = cnd[1].split(')')
            if cls[0] in classes and cnd[0] in HBNBCommand.l_c:
                arg = cnd[0] + ' ' + cls[0] + ' ' + args[0]
            else:
                return arg
            id_rest_of_args = args[0].split(',', 1)
            if len(id_rest_of_args) < 2:
                return arg
            arg2 = id_rest_of_args[1].strip()
            if arg2[0] == '{' and arg2[-1] == '}':
                self.update_from_dict(cls[0], id_rest_of_args[0], arg2)
                return ''

        return arg

    def do_EOF(self, line):
        '''Exits the program'''
        print('')
        return True

    def do_quit(self, line):
        '''\n\tquit:\t\t\tExits the program\n'''
        return True

    def emptyline(self):
        '''Empty line handler'''
        pass

    def get_class(self, line):
        '''Checker for class name'''
        if not line:
            print('** class name missing **')
            return None

        name = line.split()[0]
        if name not in classes:
            print("** class doesn't exist **")
            return None
        else:
            return classes[name]

    def get_index(self, args):
        '''Check if an object which its class name is <cls_name> and
        has id <id> exists and return the associated index if found'''
        if not args:
            args.append('')
        cls = self.get_class(args[0])
        if cls is None:
            return None
        if len(args) < 2:
            print('** instance id missing **')
            return None

        index = '.'.join(args[:2])
        if index in storage.all():
            return index
        print('** no instance found **')
        return None

    def do_create(self, line):
        '''\n\tcreate <class>:\t\tCreates a new instance of <class>\n'''
        cls = self.get_class(line)
        if cls is not None:
            obj = cls()
            obj.save()
            print(obj.id)
        pass

    def do_all(self, line):
        '''Command processor for command "all"'''
        name = ''
        if line:
            cls = self.get_class(line)
            if cls:
                name = cls.__name__
            else:
                return None
        all_list = []
        for obj in storage.all().values():
            if not name or name == obj.__class__.__name__:
                all_list.append(str(obj))
        print(all_list)
        pass

    def do_show(self, line):
        '''Command processor for command "show"'''
        args = line.split()
        index = self.get_index(args)

        if index is not None:
            print(storage.all()[index])
        pass

    def do_count(self, cls_name):
        """ retrieve the number of instances of a class """
        count = 0
        all_objs = storage.all()
        for k, v in all_objs.items():
            clss = k.split('.')
            if clss[0] == cls_name:
                count = count + 1
        print(count)

    def do_destroy(self, line):
        '''Command processor for command "destroy"'''
        args = line.split()
        index = self.get_index(args)

        if index is not None:
            storage.remove(index)
        pass

    def do_update(self, line):
        '''Command processor for command "show"'''
        args = (',').join(line.split(', ')).split(',')
        args = args[0].split() + args[1:]
        index = self.get_index(args)

        if index is None:
            return None
        if len(args) < 3:
            print('** attribute name missing **')
        elif len(args) < 4:
            print('** value missing **')
        else:
            attr = args[2]
            val = args[3]
            if args[3][0] == '\"':
                idx1 = 0
                for i in range(3):
                    idx1 = line.find(' ', idx1 + 1)
                idx1 = line.find('\"', idx1 + 1) + 1
                idx2 = line.find('\"', idx1)
                if idx2 < 0:
                    print('** value missing **')
                    return None
                val = line[idx1:idx2]
            obj = storage.all()[index]
            attrib_old = getattr(obj, attr, None)
            if attrib_old is None:
                attrib_type = str
            else:
                attrib_type = type(attrib_old)
            if attrib_type not in [str, int, float]:
                return None
            setattr(obj, attr, attrib_type(val))
            obj.save()
        pass

    def update_from_dict(self, cls_name, id, attr_dict):
        """Update attributes from dictionary"""
        id = id.strip('\'"')
        index = self.get_index([cls_name, id])
        if index is None:
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

    def help_all(self):
        """Help function for do_show()"""
        s = '\n\tall [<class>]:\t\tPrints the string representation of all '
        s += 'existing instances\n\t\t\t\t'
        s += 'If <class> is provided, it prints the string representation '
        s += 'of all instances of <class>'
        print(s)

    def help_show(self):
        """Help function for do_show()"""
        s = '\n\tshow <class> <id>:\t'
        s += 'Prints the string representation of <class> object that has id '
        s += '<id>\n'
        print(s)

    def help_destroy(self):
        """Help function for do_destroy()"""
        s = '\n\tdestroy <class> <id>:\t'
        s += 'Deletes the instance of <class> object that has id <id>\n'
        print(s)

    def help_update(self):
        """Help function for do_update()"""
        s = '\n\tupdate <class> <id> <attribute name> "<attribute value>":'
        s += '\n\t\t\t\t'
        s += 'Updates the instance of <class> object that has id <id> by '
        s += 'assigning\n\t\t\t\t'
        s += '<attribute value> to the attribute <attribute name>\n'
        print(s)
    pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
