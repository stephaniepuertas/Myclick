from ensurepip import bootstrap
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bcrypt= Bcrypt(app)
app.secret_key = '92f09598141f32847rewr9fhudhvsiduu4893u58uf8disj757f5eghjdsgdhjsgfhjsdgafhjgsdkfgsdhshdjkgsdgf47tb2'