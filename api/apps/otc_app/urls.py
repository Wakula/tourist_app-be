from . import views

urls = {
    '/v1/otc/<string:uuid>': views.OtcView.as_view('otc')
}
