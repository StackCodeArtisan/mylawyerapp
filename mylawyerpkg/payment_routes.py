import requests, random
from flask import render_template,request,redirect,flash,session
from mylawyerpkg import app
from mylawyerpkg.models import db, Client, Payment



#pay routes begins

@app.route('/pay/', methods=['POST', 'GET'])
def make_payment():
    loggedin_biz = session.get('loggedin')
    if loggedin_biz != None:
        price = db.session.query(Payment).first()
        if request.method == 'GET': 
            biz_deets = db.session.query().get(loggedin_biz)
            return render_template('user/pay.html', biz_deets=biz_deets, price=price)
        else: 
            amt = price.price_amt
            ref = int(random.random() * 10000000000) 
            session['refno'] = ref
            pay = Payment(payment_bizid=loggedin_biz, payment_amt=amt,payment_ref=ref) #insert into db
            db.session.add(pay)
            db.session.commit()
            return redirect('/pay/confirm/') 
    else:
        flash('errormsg', 'you must be logged in')
        return redirect('/login/')

#pay routes ends