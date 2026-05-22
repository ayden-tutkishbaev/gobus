import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool
from src.config import config
from src.admin.permissions import require_role
from src.admin.schemas.contracts import ContractCreate, ContractUpdate, ContractResponse, ContractsListResponse
from src.dependencies import db_connection
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.parents.models import Contract
from src.admin.file_utils import process_document, delete_document


admin_contract = APIRouter()


ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
}


@admin_contract.post(
    path="/contracts",
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_contract(
    db: db_connection,
    parent_data: ContractCreate,
):
    new_contract = Contract(
        parent_id=parent_data.parent_id,
        signed_at=parent_data.signed_at,
        date_of_payment=parent_data.date_of_payment,
        expires_at=parent_data.expires_at,
        type_of_payment=parent_data.type_of_payment,
        tariff=parent_data.tariff,
        cost=parent_data.cost
    )
    
    db.add(new_contract)
    await db.commit()
    await db.refresh(new_contract)
    
    return new_contract


@admin_contract.patch(
    path='/contracts/{contract_id}/document',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_contract_document(
    db: db_connection,
    contract_id: uuid.UUID,
    uploaded_file: UploadFile
):
    if uploaded_file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {uploaded_file.content_type}"
        )

    content = await uploaded_file.read()

    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )

    query = await db.execute(select(Contract).where(Contract.id == contract_id))
    chosen_contract = query.scalars().first()

    if not chosen_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )

    try:
        new_filepath = await run_in_threadpool(
            process_document, "contracts", content, uploaded_file.filename
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error

    old_filepath = chosen_contract.document_url

    chosen_contract.document_url = new_filepath

    await db.commit()
    await db.refresh(chosen_contract)

    if old_filepath:
        delete_document("contracts", old_filepath) 

    return chosen_contract


@admin_contract.patch(
    path="/contracts/{contract_id}",
    dependencies=[Depends(require_role("superadmin", "admin"))]

)
async def edit_contract(
    db: db_connection,
    data_edited: ContractUpdate, 
    contract_id: uuid.UUID
):
    query = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = query.scalars().first()
    
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Contract not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(contract, field, value)
        
    await db.commit()
    await db.refresh(contract)
    return contract


@admin_contract.get(
    path="/contracts",
    response_model=list[ContractsListResponse],
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def get_all_contracts(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(Contract).where(Contract.is_active).limit(limit).offset(offset))
    return result.scalars().all()


@admin_contract.get(
    path="/contracts/{contract_id}",
    response_model=ContractResponse,
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def get_contract(
    contract_id: uuid.UUID,
    db: db_connection, 
):
    result = await db.execute(select(Contract).options(selectinload(Contract.parents)).where(Contract.id == contract_id))
    contract = result.scalars().first()
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    return contract


@admin_contract.patch(
    path="/parents/{parent_id}/deactivate",
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def deactivate_contract(
    db: db_connection,
    contract_id: uuid.UUID
):
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = result.scalars().first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            path="Parent not found"
        )
    contract.is_active = False
    await db.commit()
    return {"detail": "Contract has been deactivated"}