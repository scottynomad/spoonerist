from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
import itertools

from spoonerist import pairs


app = Flask('spoonerist')
CORS(app)
api = Api(app)


class SpoonerismPairs(Resource):
    def get(self, word):
        count = int(request.args.get('count', 5))
        shuffle = request.args.get('shuffle', False)
        return list(itertools.islice(pairs(word), count))


api.add_resource(SpoonerismPairs, '/<string:word>/pairs')


key = '0LpcKiPyeG3ScFONl3gownnvTUZh1ctubzTVaqreyMc'
value = ('0LpcKiPyeG3ScFONl3gownnvTUZh1ctubzTVaqreyMc.0ana0d6lzmt-Y'
         '-jEARBOXKrIX--I_9V_E7m-pbYIuXA')


@app.route('/.well-known/acme-challenge/' + key,
           methods=['GET'])
def acme_challenge():
    return value


if __name__ == '__main__':
    app.run(debug=True)
