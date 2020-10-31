from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile
from ..models import User,Opinion,Comment
from ..request import get_quote
from flask_login import login_required,current_user
from .. import db,photos
import markdown2

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''


    title = 'Home - Shitandi blog website'
    content = "WELCOME TO SHITANDI BLOG WEBSITE"
    quote = get_quote()

    return render_template('index.html', title = title,content = content,quote = quote)



@main.route('/user/<uname>')
def profile(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, quote=quote)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form, quote=quote)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/opinion/', methods = ['GET','POST'])
@login_required
def new_opinion():

    form = OpinionForm()

    if form.validate_on_submit():
        opinion= form.description.data
        title=form.opinion_title.data

        # Updated opinion instance
        new_opinion = Opinions(title=title,opinion= opinion,user_id=current_user.id)

        title='New opinion'

        new_opinion.save_opinion()

        return redirect(url_for('main.index'))

    return render_template('opinion.html',form= form)


