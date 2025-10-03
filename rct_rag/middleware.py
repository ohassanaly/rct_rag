from fastapi import Request
from fastapi.responses import Response
from logger import logger
import time

# async def log_middleware(request: Request, call_next):
#     start_time = time.time()

#     response = await call_next(request)

#     # Retrieving the response body
#     body = b"" #initializes an empty bytes accumulator
#     if hasattr(response, "body_iterator"): #StreamingResponse objects don’t have a .body property
#         async for chunk in response.body_iterator:
#             body += chunk
#         # Rebuild the response so the client still receives it
#         response = Response(
#             content=body,
#             status_code=response.status_code,
#             headers=dict(response.headers),
#             media_type=response.media_type
#         )
#     else:
#         # If the response wasn’t streaming it already has .body
#         body = response.body


#     process_time = time.time() - start_time
#     log_dict = {
#         'url' : request.url.path,
#         'method' : request.method,
#         'params' : request.query_params,
#         'process_time' : round(process_time,4),
#         "status_code": response.status_code,
#         "response_body": body.decode("utf-8", errors="replace")
#     }
#     logger.info(log_dict, extra = log_dict) #extra parameter is supposed to retrieve the log_dict parameters as keys in the log message
    
#     return(response)

#content logs are maanged in query_vector_db now, so we only monitor latency
async def log_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    log_dict = {
        'url' : request.url.path,
        'method' : request.method,
        'process_time' : round(process_time,4)
    }
    logger.info(log_dict)
    
    return(response)