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
        'SELECT * FROM groupe WHERE id IN (SELECT groupe_id FROM conection WHERE user_id = ?)',(session.get('user_id'),)
    ).fetchall()

    return render_template('home/index.html', posts=posts)

# グループを作成
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        db = get_db()
        groupe_name = request.form['groupe_name']
        groupe_explain = request.form['groupe_explain']
        # TODO:グループコードがかぶらないようにする
        groupe_code = str(random.randint(0, 10000))

        user_id = session.get('user_id')

        db.execute(
            'INSERT INTO groupe (groupe_name, groupe_explain, groupe_code) VALUES (?, ?, ?);',(groupe_name, groupe_explain, groupe_code)
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
                'INSERT INTO conection (user_id, groupe_id) VALUES (?, ?);',(session.get('user_id'), int(groupe_id[0]))
            )
            db.commit()
            return redirect(url_for('home.index'))

    return render_template('home/join.html')

# タスクを表示させる
@bp.route('/task/<int:id>', methods=('POST','GET'))
@login_required
def task(id):
    # if request.method == 'POST':
    db = get_db()
    tasks = db.execute(
        'SELECT * FROM task WHERE groupe_id = ? ORDER BY state ASC', (id,)
    ).fetchall()

    groupe = db.execute(
        'SELECT * FROM groupe WHERE id = ?', (id,)
    ).fetchone()

    return render_template('home/task.html', id = id, tasks = tasks, groupe = groupe)

# タスクを追加する
@bp.route('/add/<int:id>', methods=('GET', 'POST'))
@login_required
def add(id):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if not body:
            error = 'body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (groupe_id, title, body) VALUES (?, ?, ?)',(id, title, body)
            )
            db.commit()

            return redirect(url_for('home.task', id = id))

    return render_template('home/add.html', id = id)

# タスクの修正
@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    db = get_db()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        state = request.form['state']
        error = None

        if state == 0:
            db.execute(
                'UPDATE task SET title = ?, body = ?, state = ? WHERE id = ?',(title, body, state, id)
            )
            db.commit()
        else:
            db.execute(
                'UPDATE task SET title = ?, body = ?, state = ?, username = ? WHERE id = ?',(title, body, state, session.get('user_name'), id)
            )
            db.commit()

        return redirect(url_for('home.index'))
    else:
        tasks = db.execute(
            'SELECT * FROM task WHERE id = ?',(id,)
        ).fetchone()

    return render_template('home/edit.html', tasks=tasks)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('home.index'))
