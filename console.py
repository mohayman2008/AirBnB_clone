#!/usr/bin/python3
'''This module contains the definition of the command interpreter class
'HBNBCommand' in the AirBnB clone app and contains the entry point of the
command interpreter
'''
import cmd


class HBNBCommand(cmd.Cmd):
    '''the command interpreter class in the AirBnB clone app'''
    prompt = "(hbnb) "

    def do_quit(self, line):
        '''\tquit: exits the program'''
        return True

    def do_EOF(self, line):
        '''\tEOF (CTRL+D) command to exit the program'''
        return True

    def emptyline(self):
        return


if __name__ == '__main__':
    HBNBCommand().cmdloop()
