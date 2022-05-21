from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import random

bp = Blueprint('home', __name__)

# 自分の登録しているグループ一覧を表示
@bp.route('/')
@login_required
def index():
    db = get_db()

    posts = db.execute(
        'SELECT groupe_name FROM groupe WHERE id IN (SELECT groupe_id FROM conection WHERE user_id = ?)',(session.get('user_id'),)
    ).fetchall()

    return render_template('home/index.html', posts=posts)

# グループを作成
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        groupe_name = request.form['groupe_name']
        # TODO:グループコードがかぶらないようにする
        groupe_code = str(random.randint(0, 10000))
        error = None

        if not groupe_name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_id = session.get('user_id')
            db.execute(
                'INSERT INTO groupe (groupe_name, groupe_code) VALUES (?, ?);',(groupe_name, groupe_code)
            )
            db.commit()

            # 先ほど作成したグループのidを取得
            groupe_id = db.execute(
                'SELECT id FROM groupe WHERE groupe_code = ?',(groupe_code,)
            ).fetchone()

            # 自分をそのグループに招待
            db.execute(
                'INSERT INTO conection (user_id, groupe_id) VALUES (?, ?);',(user_id, int(groupe_id[0])),
            )
            db.commit()
            return redirect(url_for('home.index'))

    return render_template('home/create.html')

# グループに加入
@bp.route('/join', methods=('GET', 'POST'))
@login_required
def join():
    if request.method == 'POST':
        db = get_db()

        groupe_code = request.form['groupe_code']
        error = None

        groupe_id = db.execute(
            'SELECT id FROM groupe WHERE groupe_code = ?',(groupe_code,)
        ).fetchone()

        if not groupe_code:
            error = 'code is required.'

        if groupe_id is None:
            error = 'code is noting.'

        if error is not None:
            flash(error)
        else:
            # 自分をそのグループに招待
            db.execute(
                'INSERT INTO conection (user_id, groupe_id) VALUES (?, ?);',(session.get('user_id'), int(groupe_id[0])),
            )
            db.commit()
            return redirect(url_for('home.index'))

    return render_template('home/join.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('home.index'))

    return render_template('home/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('home.index'))