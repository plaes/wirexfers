from flask import Flask, render_template, url_for
from wiretransfers import PaymentInfo, utils
from wiretransfers.providers import ProviderBase

private_key = utils.load_key('../_keys_/private_key.pem')
public_key = utils.load_key('../_keys_/public_key.pem')
provider = ProviderBase('uid217657', private_key, public_key,
                        'https://pangalink.net/banklink/008/ipizza')

app = Flask(__name__)

@app.route('/')
def index():
    info = PaymentInfo('1.00', 'Test transfer', utils.ref_731('123'))
    urls = {'return': url_for('index', _external=True)}
    payment = provider(info, urls)
    return render_template('form.html', payment=payment)

if __name__ == '__main__':
    app.run(debug=True)
