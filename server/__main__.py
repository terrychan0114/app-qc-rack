#!/usr/bin/env python3

import connexion

from server import encoder
from flask_cors import CORS

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'QC rack Microservice'}, pythonic_params=True)
    CORS(app.app)
    app.run(port=8083)


if __name__ == '__main__':
    main()
