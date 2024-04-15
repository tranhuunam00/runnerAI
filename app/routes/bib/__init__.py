
from flask import Blueprint, redirect, url_for, flash, render_template, request

import logging

from app.extensions import limiter
from app.service.bib import detectTextFromImage

bib_bp = Blueprint("bib", __name__, url_prefix="/bib")


@bib_bp.route("/", methods=["GET", "POST"])
@limiter.limit("30/minute")
def login():
  return detectTextFromImage(request)