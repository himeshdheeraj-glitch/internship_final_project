import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.logging import logger

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        # Log request receipt
        client_host = request.client.host if request.client else "unknown"
        logger.info(f"Incoming: {request.method} {request.url.path} - Host: {client_host}")
        
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            
            # Log response status
            log_msg = f"Completed: {request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time:.2f}ms"
            if response.status_code >= 400:
                logger.warning(log_msg)
            else:
                logger.info(log_msg)
                
            response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
            return response
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"Failed: {request.method} {request.url.path} - Error: {str(e)} - Duration: {process_time:.2f}ms", exc_info=True)
            raise
