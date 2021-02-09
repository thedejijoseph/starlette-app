from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import uvicorn

# util: helper methods
# common responses

async def success(message, data=None, status_code=200):
    response = {'success': True, 'message': message}
    if data:
        response['data'] = data
    
    return JSONResponse(response, status_code=status_code)

async def error(message, errors=None, status_code=500):
    response = {'success': False, 'message': message}
    if errors:
        response['errors'] = errors
    
    return JSONResponse(response, status_code=status_code)



async def root(request):
    response = await success('Clipboard API Root. (https://clipboard-app.netlify.app')
    return response

async def hello(request):
    name = request.query_params.get('name', 'Johnn Doe')
    response = await success(f'Hello there, {name}')
    return response

async def room(request):
    room_id = request.path_params['room_id']
    respomse = await success(f'You are now in Room {room_id}.')
    return respomse


async def not_found(request, exc):
    response = {
        'success': False,
        'message': 'Not found',
        'errors': [{
            'message': f'URL {request.url.path} is not on this server.'
        }]
    }
    return JSONResponse(response, status_code=404)

async def server_error(request, exc):
    response = {
        'success': False,
        'message': 'Server error',
        'errors': [{
            'message': str(exc),
            'details': repr(exc)
        }]
    }
    return JSONResponse(response, status_code=500)

exception_handlers = {
    404: not_found,
    500: server_error
}

routes = [
    Route('/', root),
    Route('/hello', hello),
    Route('/room/{room_id}', room)
]

app = Starlette(
    debug=False,
    routes=routes,
    exception_handlers=exception_handlers
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
