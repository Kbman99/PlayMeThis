from app import app, models, db, config
from flask import request, jsonify, abort, render_template, flash, redirect, url_for
from app.toolbox import get_ip, webhook, playlist
from flask_login import login_required

from datetime import datetime, timedelta

import pusher

pl = playlist.SongPlaylist()

pusher_client = pusher.Pusher(
  app_id='411577',
  key='d33b6f10de4245953937',
  secret='6d0be1ac11d46d9da60a',
  cluster='us2',
  ssl=True
)


@app.route('/webhook', methods=['GET', 'POST'])
def web_hook():
    if request.method == 'GET':
        verify_token = request.args.get('verify_token')
        print("Sent token: " + verify_token)
        print("Server token: " + app.config["WEBHOOK_VERIFY_TOKEN"])
        clientip = get_ip.get_ip(request)
        client = models.AuthorizedClients.query.filter_by(client_ip=clientip).first()
        if client is not None:
            flash('You have already been authorized to use the webhook feature.', 'info')
            return redirect(url_for('index'))
        if verify_token == app.config["WEBHOOK_VERIFY_TOKEN"]:
            client = models.AuthorizedClients(
                client_ip=get_ip.get_ip(request)
            )
            db.session.add(client)
            db.session.commit()
            flash('You are now authorized to use the webhook feature! Enjoy!', 'positive')
            return redirect(url_for('index'))
        else:
            return jsonify({'status': 'bad token'}), 401

    elif request.method == 'POST':
        print(pl.__dict__)
        clientip = get_ip.get_ip(request)
        print("Client ip: " + str(clientip))
        client = models.AuthorizedClients.query.filter_by(client_ip=clientip).first()
        print("Client object: " + str(client))
        if client:
            if datetime.now() - client.pub_time > timedelta(hours=app.config["CLIENT_AUTH_TIMEOUT"]):
                db.session.delete(client)
                db.session.commit()
                return jsonify({'status': 'authorization timeout'}), 401
            else:
                webhook.process_webhook(request, pusher_client, pl)
                return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'not authorized'}), 401

    else:
        abort(400)


@app.route('/webhook/setup', methods=['GET', 'POST'])
@login_required
def web_hook_setup():
    clientip = get_ip.get_ip(request)
    client = models.AuthorizedClients.query.filter_by(client_ip=clientip).first()
    if client:
        verified = True
    else:
        verified = False
    return render_template('user/webhooksetup.html', token=config.WEBHOOK_VERIFY_TOKEN, verified=verified)
