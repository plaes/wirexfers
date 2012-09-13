from flask import Flask
from wiretransfers import PaymentInfo, utils
from wiretransfers.providers import ProviderBase

private_key = utils.load_key('../_keys_/private_key.pem')
public_key = utils.load_key('../_keys_/public_key.pem')
provider = ProviderBase('uuid217657', private_key, public_key,
                        'https://pangalink.net/banklink/008/ipizza')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello!'

if __name__ == '__main__':
    app.run()
