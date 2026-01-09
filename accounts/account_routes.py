from fastapi import APIRouter, Depends, HTTPException
from accounts.schemas import AccountCreate, AccountUpdate
from auth.routes import get_current_user
from models import accounts_db

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/")
def create_account(account: AccountCreate, user: str = Depends(get_current_user)):
    new_account = {
        "id": len(accounts_db) + 1,
        "user": user,
        "name": account.name,
        "balance": account.balance,
        "currency": account.currency
    }
    accounts_db.append(new_account)
    return new_account


@router.get("/")
def get_accounts(user: str = Depends(get_current_user)):
    return [acc for acc in accounts_db if acc["user"] == user]


@router.put("/{account_id}")
def update_account(account_id: int, data: AccountUpdate, user: str = Depends(get_current_user)):
    for acc in accounts_db:
        if acc["id"] == account_id and acc["user"] == user:
            if data.name:
                acc["name"] = data.name
            if data.balance is not None:
                acc["balance"] = data.balance
            return acc
    raise HTTPException(status_code=404, detail="Account not found")


@router.delete("/{account_id}")
def delete_account(account_id: int, user: str = Depends(get_current_user)):
    for acc in accounts_db:
        if acc["id"] == account_id and acc["user"] == user:
            accounts_db.remove(acc)
            return {"message": "Account deleted"}
    raise HTTPException(status_code=404, detail="Account not found")