import json
import pathlib

import natsort
import quart

app = quart.Quart('app')

with open('config.json') as f:
    config = json.load(f)

fs = pathlib.Path(config['work-path'])

dirs = [i for i in list(fs.iterdir()) if i.is_dir()]


@app.route('/static_fs/<string:author>/<string:post>/<string:image>')
async def static_fs(author, post, image):
    if author in [i.name for i in dirs]:
        img = fs / author / post / image
        if img.exists():
            return await quart.send_file(img)


def construct_posts(author: pathlib.Path):
    author_posts = {}
    for post in author.iterdir():
        author_posts[post.name] = []
        for file in post.iterdir():
            if file.suffix.lower().endswith('jpg') or file.suffix.lower().endswith('png') or \
                    file.suffix.lower().endswith('jpeg') or file.suffix.lower().endswith('gif'):
                author_posts[post.name].append(file.name)
    sorted = natsort.os_sorted(author_posts, reverse=True)
    a = {}
    for s_key in sorted:
        a[s_key] = author_posts[s_key]
    return a


@app.route('/author/<string:author>')
async def author_route(author):
    if author in [i.name for i in dirs]:
        posts_data = construct_posts(fs / author)
    else:
        raise Exception
    print(posts_data)
    return await quart.render_template('author.html', posts=posts_data, author=author)


@app.route('/')
async def root():
    return await quart.render_template('root.html', dirs=dirs)


if __name__ == '__main__':
    app.run("0.0.0.0")
