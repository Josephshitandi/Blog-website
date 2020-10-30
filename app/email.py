@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))