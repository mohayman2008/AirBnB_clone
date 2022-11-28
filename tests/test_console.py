#!/usr/bin/python3
"""Test module for the console"""

import unittest
import os
import sys
from io import StringIO

from models import storage
from models.engine import classes
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """Tests for the console"""

    file_name = storage._FileStorage__file_path
    cmd = HBNBCommand()

    def remove_json(self):
        '''Removes the JSON file and reload'''
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            storage.reload()

    def test_create(self):
        """Tests for <create> command"""
        self.remove_json()

        sys.stdout = StringIO()
        self.cmd.do_create('')
        self.assertEqual(sys.stdout.getvalue(), '** class name missing **\n')

        sys.stdout = StringIO()
        self.cmd.onecmd('create')
        self.assertEqual(sys.stdout.getvalue(), '** class name missing **\n')

        sys.stdout = StringIO()
        self.cmd.do_create('NoClass')
        self.assertEqual(sys.stdout.getvalue(), "** class doesn't exist **\n")

        sys.stdout = StringIO()
        self.cmd.onecmd('create NoClass')
        self.assertEqual(sys.stdout.getvalue(), "** class doesn't exist **\n")

        for cls_name, cls in classes.items():
            self.remove_json()
            sys.stdout = StringIO()
            self.cmd.do_create(cls_name)
            id = sys.stdout.getvalue()[:-1]
            index = '.'.join((cls_name, id))
            self.assertIn(index, storage.all().keys())
            self.assertIsInstance(storage.all()[index], cls)

            sys.stdout = StringIO()
            self.cmd.onecmd(f'create {cls_name}')
            id = sys.stdout.getvalue()[:-1]
            index = '.'.join((cls_name, id))
            self.assertIn(index, storage.all().keys())
            self.assertIsInstance(storage.all()[index], cls)

        sys.stdout = sys.__stdout__
        pass

    def test_show(self):
        """Tests for <show> command"""
        self.remove_json()

        sys.stdout = StringIO()
        self.cmd.onecmd('show')
        self.assertEqual(sys.stdout.getvalue(), '** class name missing **\n')

        sys.stdout = StringIO()
        self.cmd.onecmd('show NoClass')
        self.assertEqual(sys.stdout.getvalue(), "** class doesn't exist **\n")

        for cls_name, cls in classes.items():
            sys.stdout = StringIO()
            self.cmd.onecmd(f'show {cls_name}')
            self.assertEqual(sys.stdout.getvalue(),
                             "** instance id missing **\n")

            sys.stdout = StringIO()
            self.cmd.onecmd(f'show {cls_name} xyz')
            self.assertEqual(sys.stdout.getvalue(),
                             "** no instance found **\n")

            obj = cls()
            sys.stdout = StringIO()
            self.cmd.onecmd(f'show {cls_name} {obj.id}')
            index = '.'.join((cls_name, obj. id))
            self.assertEqual(sys.stdout.getvalue()[:-1], str(obj))

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_destroy(self):
        """Tests for <destroy> command"""
        self.remove_json()

        sys.stdout = StringIO()
        self.cmd.onecmd('destroy')
        self.assertEqual(sys.stdout.getvalue(), '** class name missing **\n')

        sys.stdout = StringIO()
        self.cmd.onecmd('destroy NoClass')
        self.assertEqual(sys.stdout.getvalue(), "** class doesn't exist **\n")

        for cls_name, cls in classes.items():
            sys.stdout = StringIO()
            self.cmd.onecmd(f'destroy {cls_name}')
            self.assertEqual(sys.stdout.getvalue(),
                             "** instance id missing **\n")

            sys.stdout = StringIO()
            self.cmd.onecmd(f'destroy {cls_name} xyz')
            self.assertEqual(sys.stdout.getvalue(),
                             "** no instance found **\n")

            obj = cls()
            index = '.'.join((cls_name, obj. id))
            self.assertIn(index, storage.all().keys())
            # sys.stdout = StringIO()
            self.cmd.onecmd(f'destroy {cls_name} {obj.id}')
            self.assertNotIn(index, storage.all().keys())

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_all(self):
        """Tests for <all> command"""
        self.remove_json()

        sys.stdout = StringIO()
        self.cmd.onecmd('all')
        self.assertEqual(sys.stdout.getvalue()[:-1], '[]')

        sys.stdout = StringIO()
        self.cmd.onecmd('all NoClass')
        self.assertEqual(sys.stdout.getvalue(), "** class doesn't exist **\n")

        for cls_name, cls in classes.items():
            self.remove_json()
            sys.stdout = StringIO()
            self.cmd.onecmd(f'all {cls_name}')
            self.assertEqual(sys.stdout.getvalue()[:-1], '[]')

        all_objs = []
        for cls_name, cls in classes.items():
            n = 5
            objs = [cls() for i in range(n)]
            all_objs += objs

            sys.stdout = StringIO()
            self.cmd.onecmd(f'all {cls_name}')
            out = sys.stdout.getvalue()[:-1]
            for obj in objs:
                self.assertTrue(out.find(str(obj)) > 0)
                self.assertEqual(out[0], '[')
                self.assertEqual(out[-1], ']')

        sys.stdout = StringIO()
        self.cmd.onecmd('all')
        out = sys.stdout.getvalue()[:-1]
        for obj in all_objs:
            self.assertTrue(out.find(str(obj)) > 0)
            self.assertEqual(out[0], '[')
            self.assertEqual(out[-1], ']')

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_update(self):
        """Tests for <update> command"""
        self.remove_json()

        sys.stdout = StringIO()
        self.cmd.onecmd('update')
        self.assertEqual(sys.stdout.getvalue(), '** class name missing **\n')

        sys.stdout = StringIO()
        self.cmd.onecmd('update NoClass')
        self.assertEqual(sys.stdout.getvalue(), "** class doesn't exist **\n")

        for cls_name, cls in classes.items():
            sys.stdout = StringIO()
            self.cmd.onecmd(f'update {cls_name}')
            self.assertEqual(sys.stdout.getvalue(),
                             "** instance id missing **\n")

            sys.stdout = StringIO()
            self.cmd.onecmd(f'update {cls_name} xyz')
            self.assertEqual(sys.stdout.getvalue(),
                             "** no instance found **\n")

            obj = cls()
            cls_id = cls_name + ' ' + obj.id

            sys.stdout = StringIO()
            self.cmd.onecmd(f'update {cls_id}')
            self.assertEqual(sys.stdout.getvalue()[:-1],
                             "** attribute name missing **")

            sys.stdout = StringIO()
            self.cmd.onecmd(f'update {cls_id} attrib')
            self.assertEqual(sys.stdout.getvalue()[:-1],
                             "** value missing **")

            index = '.'.join((cls_name, obj. id))
            # sys.stdout = StringIO()
            self.cmd.onecmd(f'update {cls_id} name value')
            self.assertEqual(obj.name, 'value')
            self.assertIn('name', obj.to_dict())

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass
    pass
