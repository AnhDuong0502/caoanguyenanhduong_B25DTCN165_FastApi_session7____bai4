from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

app = FastAPI()


orders_db = {
    1: {"id": 1, "code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    2: {"id": 2, "code": "SP002", "payment_status": "UNPAID", "method": "NONE"},
}


@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int):

    order = orders_db.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đơn hàng"
        )

    return {"payment_status": order["payment_status"], "method": order["method"]}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException):

    return JSONResponse(
        status_code=exception.status_code,
        content={
            "statusCode": exception.status_code,
            "message": exception.detail,
            "data": None,
            "error": exception.detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": request.url.path,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exception: Exception):

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Đã xảy ra lỗi hệ thống",
            "data": None,
            "error": "Internal Server Error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": request.url.path,
        },
    )
