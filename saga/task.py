# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Andre Merzky"
__copyright__ = "Copyright 2012, The SAGA Project"
__license__   = "MIT"

""" SAGA task interface
"""

import time
import traceback

import saga.exceptions
import saga.attributes


SYNC     = 'Sync'
ASYNC    = 'Async'
TASK     = 'Task'

UNKNOWN  = 'Unknown'
NEW      = 'New'
RUNNING  = 'Running'
DONE     = 'Done'
FAILED   = 'Failed'
CANCELED = 'Canceled'

STATE    = 'State'
RESULT   = 'Result'



class Async :
    '''
    tagging interface for SAGA classes which implement asynchronous methods.
    '''
    pass


class Task (saga.attributes.Attributes) :


    def __init__ (self) :

        # set attribute interface properties
        self._attributes_extensible  (False)
        self._attributes_camelcasing (True)

        # register properties with the attribute interface
        self._attributes_register   (RESULT,  None,    self.ANY, self.SCALAR, self.READONLY)
        self._attributes_set_getter (RESULT,  self.get_result)
        self._attributes_set_setter (RESULT,  self._set_result)

        self._attributes_register   (STATE,   UNKNOWN, self.ENUM, self.SCALAR, self.READONLY)
        self._attributes_set_enums  (STATE,  [UNKNOWN, NEW, RUNNING, DONE, FAILED, CANCELED])
        self._attributes_set_getter (STATE,   self.get_state)
        self._attributes_set_setter (STATE,   self._set_state)
              
        self._set_state (NEW)


    def _set_result (self, result) :
        self._attributes_i_set (self._attributes_t_underscore (RESULT), result, force=True)
        self._attributes_i_set (self._attributes_t_underscore (STATE),  DONE,   force=True)


    def get_result (self) :
        
        if not state in [DONE, FAILED, CANCELED] :
            wait ()
        
        if state == FAILED :
            re_raise ()
            return

        if state == CANCELED :
            raise saga.exceptions.IncorrectState \
                    ("task.get_result() cannot be called on cancelled tasks")

        if state == DONE :
            return self.result


    def _set_state (self, state) :
        if not state in [UNKNOWN, NEW, RUNNING, DONE, FAILED, CANCELED] :
            raise saga.exceptions.BadParameter ("attempt to set invalid task state '%s'" % state)
        self._attributes_i_set (self._attributes_t_underscore (STATE), state, force=True)


    def get_state (self) :
        return self.state


    def wait (self, timeout=-1) :
        # FIXME: implement timeout, more fine grained wait, attribute notification
        while self_.state not in [DONE, FAILED, CANCELED] :
            time.sleep (1)


    def run (self) :
        pass


    def cancel (self) :
        self._set_state (CANCELED)
