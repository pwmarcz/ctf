from flask import Flask, render_template, request, Response, url_for
import os

app = Flask(__name__)


def guess_type(path):
    if os.path.isdir(path):
        return 'directory'

    _, ext = os.path.splitext(path)
    return {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.html': 'text/html',
    }.get(ext, 'text/plain')


@app.route('/gallery/')
def gallery(path=None):
    path = request.args.get('path')
    if not path:
        path = '.'

    full_path = os.path.join(os.path.dirname(__file__), 'photos', path)

    if os.path.isfile(full_path):
        with open(full_path, 'rb') as f:
            content = f.read()
        return Response(content, mimetype=guess_type(full_path))

    if os.path.isdir(full_path):
        files = []
        if path != '.':
            up_path = path.rpartition('/')[0]
            files.append({
                'name': '<up>',
                'path': up_path,
                'type': 'directory',
                'url': url_for('gallery') + '?path=' + up_path,
            })
        for fname in os.listdir(full_path):
            path_fname = os.path.join(path, fname)
            full_path_fname = os.path.join(full_path, fname)
            files.append({
                'name': fname,
                'path': path_fname,
                'type': guess_type(full_path_fname).split('/')[0],
                'url': url_for('gallery') + '?path=' + path_fname,
            })
        return render_template('gallery.html', files=files)
    return Response('Not Found', status=404)
