
from flask import Blueprint, redirect, url_for, flash, render_template, request

import logging

from app.extensions import limiter
from app.service.face import detectFace, findFace

face_bp = Blueprint("face", __name__, url_prefix="/face")


@face_bp.route("/detect", methods=["GET", "POST"])
@limiter.limit("30/minute")
def handle_face_request():
    request.timeout = 120
    return detectFace(request)

@face_bp.route("/find", methods=["GET", "POST"])
@limiter.limit("30/minute")
def find():
    return findFace(request)