from flask import Flask, request
from flask_restful import Resource, Api
import itertools

from spoonerist import pairs


app = Flask('spoonerist')
api = Api(app)


class SpoonerismPairs(Resource):
    def get(self, word):
        count = int(request.args.get('count', 5))
        shuffle = request.args.get('shuffle', False)
        return list(itertools.islice(pairs(word), count))


api.add_resource(SpoonerismPairs, '/<string:word>/pairs')


@app.route('.well-known/acme-challenge/L0JbnCYn4E8uGTxjnfn9keJ7hfwTNH19qmyCJnbopAs',
        methods=['GET'])
def acme_challenge():
    return 'L0JbnCYn4E8uGTxjnfn9keJ7hfwTNH19qmyCJnbopAs.0ana0d6lzmt'
        '-Y-jEARBOXKrIX--I_9V_E7m-pbYIuXA'


if __name__ == '__main__':
    app.run(debug=True)
