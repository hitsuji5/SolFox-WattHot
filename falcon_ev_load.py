# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 10:56:10 2016

@author: Tak
"""

import falcon
import json
import logging
import get_ev_load_profile as ev
 
class EvResource:
    def __init__(self):
        self.logger = logging.getLogger('evapp.' + __name__)
        
    def on_get(self, req, resp):
        distance = req.get_param_as_int('distance') or 0
        maker = req.get_param('maker') or ''
        model = req.get_param('model') or ''
        year = req.get_param_as_int('year') or 2016
        charger = req.get_param_as_int('charger') or 0
        
        try:
            result = ev.get_ev_load_profile(distance, maker, model, year, charger)
        except Exception as ex:
            self.logger.error(ex)
            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                description,
                30)
        resp.body = json.dumps(result)
 
app = falcon.API()
app.add_route('/ev', EvResource())