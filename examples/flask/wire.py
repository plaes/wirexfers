from flask import Flask, render_template, url_for
from wirexfers import PaymentInfo, utils
from wirexfers.providers.tupas import SoloKeyChain, NordeaEEProvider

app = Flask(__name__)

# Replace the '<mac>' argument below!
keychain = SoloKeyChain(<mac>)
# Replace the <user> and <endpoint> arguments below!
provider = NordeaEEProvider(<user>, keychain, <endpoint>)

@app.route('/')
def index():
    info = PaymentInfo('1.00', 'Test transfer', utils.ref_731('123'))
    urls = {'cancel': url_for('index', _external=True),
            'reject': url_for('index', _external=True),
            'return': url_for('index', _external=True)}
    payment = provider(info, urls)
    return render_template('form.html', payment=payment)

if __name__ == '__main__':
    app.run(debug=True)
