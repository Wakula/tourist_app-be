from flask.views import MethodView
from flask import jsonify, make_response, current_app, g
from datetime import datetime

request_counter = 0

class BaseView(MethodView):
    def _get_response(self, data, *, status_code=200):
        response = {
            'data': self._serialize(data),
            'date': datetime.now().__str__(),
        }
        global request_counter
        request_counter += 1
        print('request_counter=' + str(request_counter))
        return make_response(jsonify(response), status_code)

    def _serialize(self, data):
        if isinstance(data, list):
            return [self._serialize(item) for item in data]

        elif isinstance(data, dict):
            data_dict = dict(data)
            # will delete private methods from dict
            for key in data:
                if key.startswith(('_')):
                    del data_dict[key]
            return {key:self._serialize(value) for (key, value) in data_dict.items()}
    
        elif isinstance(data, current_app.db.Model):
            data_dict = dict(data.__dict__)
            return self._serialize(data_dict)

        try:
            return data.__dict__
        except AttributeError:
            return data


