from flask import Flask, render_template, redirect, request, url_for
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
    urls = {'cancel': url_for('cancel', _external=True),
            'reject': url_for('reject', _external=True),
            'return': url_for('finish', _external=True)}
    payment = provider(info, urls)
    return render_template('form.html', payment=payment)

@app.route('/cancel')
def cancel():
    payment = provider.parse_response(request.args)
    if payment.is_valid:
        return 'Payment cancelled!'
    return redirect(url_for('invalid'))

@app.route('/reject')
def reject():
    payment = provider.parse_response(request.args)
    if payment.is_valid:
        return 'Payment rejected!'
    return redirect(url_for('invalid'))

@app.route('/finish')
def finish():
    payment = provider.parse_response(request.args)
    if payment.is_valid:
        return 'Payment successful!'
    return redirect(url_for('invalid'))

@app.route('/invalid')
def invalid():
    return 'INVALID PAYMENT'

if __name__ == '__main__':
    app.run(debug=True)
