from flask import Flask, request
from flask_restful import Resource, Api
import itertools

from spoonerist import pairs


app = Flask('spoonerist')
api = Api(app)


class SpoonerismPairs(Resource):
    def get(self, word):
        count = request.args.get('count', 5)
        shuffle = request.args.get('shuffle', False)
        return list(itertools.islice(pairs(word), count))


api.add_resource(SpoonerismPairs, '/<string:word>/pairs')


if __name__ == '__main__':
    app.run(debug=True)
