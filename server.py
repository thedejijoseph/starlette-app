from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

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



async def server_error(request, exc):
    return JSONResponse({'message': 'Server error', 'details':repr(exc)}, status_code=500)

exception_handlers = {
    500: server_error
}

routes = [
    Route('/', root)
]

app = Starlette(
    debug=False,
    routes=routes,
    exception_handlers=exception_handlers
    )
