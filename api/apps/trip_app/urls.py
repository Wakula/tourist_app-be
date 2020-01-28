from . import views


urls = {
    '/v1/trip/<int:trip_id>': views.TripView.as_view('trip'),
    '/v1/trip': views.TripView.as_view('create_trip'),
}
