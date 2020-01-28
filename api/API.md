# trip_app
> /trip/v1/trip/<int:trip_id>
    PUT: update trip data  
    PATCH: refresh trip uuid  
    GET: get trip data fields  
> /trip/v1/trip  
    POST: create new trip  
  
# user_app  
> user/v1/user  
    POST: create new user  
    GET: get user data fields  
    DELETE: delete user from trip  
    PATCH: edit user data  
> user/v1/user/avatar  
    POST: update user avatar  
    GET: get user avatar  
> user/v1/login  
    POST: user login  
> user/v1/logout  
    POST: user logout  
  
# role_app  
> /role/v1/role/<int:role_id>  
    GET: get role data  
    DELETE: delete role from db  
    PUT: (un)assign role to user  
> /role/v1/role  
    POST: create new role  
  
# equipment_app  
> equipment/v1/equipment/<int:equipment_id>  
    GET: get equipment data  
    PATCH: edit equipment data  
    DELETE: delete equipment from db  
> equipment/v1/equipment  
    POST: create new equipment  
  
  
  