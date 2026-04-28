from fastapi import APIRouter, HTTPException, status, UploadFile
from api.dependecies import db_connection
from api.admin.dependencies import IsSuperAdmin, IsAdmin
from sqlalchemy import select, func, insert
from sqlalchemy.orm import selectinload
from database.models import Kid, Parent, Staff, Transport, Contract, School, Teacher
from api.auth.models import User
from api.auth.schemas import *
from api.admin.schemas import *
from PIL import UnidentifiedImageError
from starlette.concurrency import run_in_threadpool
from api.tools import process_profile_image, delete_profile_image
from config_manager import config
import uuid


admin = APIRouter()


@admin.patch(
    "/edit-rights/{user_id}",
    response_model=UserAdminResponse
)
async def assign_admin(
    super_admin: IsSuperAdmin,
    user_id: uuid.UUID,
    user_data: UserUpdate,
    db: db_connection
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
        
    await db.commit()
    await db.refresh(user)
    
    message = f"Пользователь {user.username} назначен админом" if user.is_admin else f"Пользователь {user.username} снят с админа"
    
    return UserAdminResponse(
        message=message,
        user=UserAdminPublic.model_validate(user)
    )
    
    

@admin.post(
    path='/add-parent',
)
async def add_parent(
    admin: IsAdmin,
    db: db_connection,
    parent_data: ParentCreate
):
    new_parent = Parent(
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        family_name=parent_data.family_name,
        phone_number=parent_data.phone_number,
        document_id=parent_data.document_id,
        active=True
    )
    db.add(new_parent)
    await db.commit()
    await db.refresh(new_parent)
    
    return new_parent


@admin.post(
    path='/add-staff'
)
async def add_staff(
    admin: IsAdmin,
    db: db_connection,
    parent_data: StaffBase,
    uploaded_file: UploadFile
):    
    new_staff = Staff(
        family_name=parent_data.family_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        profile_picture='PICTURE',
        staff_type=parent_data.staff_type,
        birth_date=parent_data.birth_date,
        salary=parent_data.salary,
    )
    
    db.add(new_staff)
    await db.commit()
    await db.refresh(new_staff)
    
    return new_staff


@admin.patch(
    path='/add-staff-picture'
)
async def add_staff_picture(
    admin: IsAdmin,
    db: db_connection,
    parent_data: StaffBase,
    uploaded_file: UploadFile
):
    content = await uploaded_file.read()
    
    
    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )
        
    
    try:
        new_filename = await run_in_threadpool(process_profile_image, content)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file."
        ) from error
    



@admin.post(
    path='/add-transport'
)
async def add_transport(
    admin: IsAdmin,
    db: db_connection,
    parent_data: TransportBase,
):
    
    
    new_transport = Transport(
        unique_transport_id=parent_data.unique_transport_id,
        transport_picture=parent_data.transport_picture,
        driver=parent_data.driver,
        babysitter=parent_data.babysitter,
        registered_at=parent_data.registered_at,
        status=parent_data.status
    )
    
    db.add(new_transport)
    await db.commit()
    await db.refresh(new_transport)
    
    return new_transport


@admin.post(
    path="/add-contract"
)
async def add_contract(
    admin: IsAdmin,
    db: db_connection,
    parent_data: ContractBase,
):
    new_contract = Contract(
        date_of_payment=parent_data.date_of_payment,
        date_of_end=parent_data.date_of_end,
        type_of_payment=parent_data.type_of_payment,
        tariff=parent_data.tariff,
        cost=parent_data.cost,
        document=parent_data.document
    )
    
    db.add(new_contract)
    await db.commit()
    await db.refresh(new_contract)
    
    return new_contract


@admin.post(
    path='/add-school'
)
async def add_school(
    admin: IsAdmin,
    db: db_connection,
    parent_data: SchoolBase,
):
    new_school = School(
        name=parent_data.name
    )
    
    db.add(new_school)
    await db.commit()
    await db.refresh(new_school)
    
    return new_school
    
    
@admin.post(
    path='/add-teacher'
)
async def add_teacher(
    admin: IsAdmin,
    db: db_connection,
    parent_data: TeacherBase,
):
    new_teacher = Teacher(
        family_name=parent_data.family_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        school=parent_data.school,
        active=True #remove after migrations
    )
    
    db.add(new_teacher)
    await db.commit()
    await db.refresh(new_teacher)
    
    return new_teacher


@admin.post(
    path='/add-kid',
)
async def add_kid(
    admin: IsAdmin,
    db: db_connection,
    parent_data: KidBase,
):
    
    new_kid = Kid(
        family_name=parent_data.family_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        home_address=parent_data.home_address,
        school=parent_data.school,
        contract=parent_data.contract,
        driver=parent_data.driver,
        babysitter=parent_data.babysitter,
        teacher=parent_data.teacher,
        birth_date=parent_data.birth_date,
        active=True, #remove after migrations
        transport=1, #remove after migrations
        profile_picture='(blank).jpg'
    )
    
    if parent_data.parents:
        parents = await db.execute(
            select(Parent).where(Parent.id.in_(parent_data.parents))
        )
        new_kid.parents = parents.scalars().all()
    
    db.add(new_kid)
    await db.commit()
    await db.refresh(new_kid)
    
    return new_kid


@admin.patch(
    path="/edit-parent/{parent_id}"
)
async def edit_parents(
    admin: IsAdmin,
    db: db_connection,
    data_edited: ParentUpdate, 
    parent_id: int
):
    query = await db.execute(select(Parent).where(Parent.id == parent_id))
    parent = query.scalars().first()
    
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Parent not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(parent, field, value)
        
    await db.commit()
    await db.refresh(parent)
    return parent


@admin.patch(
    path="/edit-staff/{staff_id}"
)
async def edit_staff(
    admin: IsAdmin,
    db: db_connection,
    data_edited: StaffUpdate, 
    staff_id: int
):
    query = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = query.scalars().first()
    
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Staff member not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(staff, field, value)
        
    await db.commit()
    await db.refresh(staff)
    return staff


@admin.patch(
    path="/edit-transport/{transport_id}"
)
async def edit_transport(
    admin: IsAdmin,
    db: db_connection,
    data_edited: TransportUpdate, 
    transport_id: int
):
    query = await db.execute(select(Transport).where(Transport.id == transport_id))
    transport = query.scalars().first()
    
    if not transport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Transport not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(transport, field, value)
        
    await db.commit()
    await db.refresh(transport)
    return transport


@admin.patch(
    path="/edit-contract/{contract_id}"
)
async def edit_contract(
    admin: IsAdmin,
    db: db_connection,
    data_edited: ContractUpdate, 
    contract_id: int
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


@admin.patch(
    path="/edit-school/{school_id}"
)
async def edit_school(
    admin: IsAdmin,
    db: db_connection,
    data_edited: SchoolUpdate, 
    school_id: int
):
    query = await db.execute(select(School).where(School.id == school_id))
    school = query.scalars().first()
    
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='School not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(school, field, value)
        
    await db.commit()
    await db.refresh(school)
    return school


@admin.patch(
    path="/edit-teacher/{teacher_id}"
)
async def edit_teacher(
    admin: IsAdmin,
    db: db_connection,
    data_edited: TeacherUpdate, 
    teacher_id: int
):
    query = await db.execute(select(Teacher).where(Teacher.id == teacher_id))
    teacher = query.scalars().first()
    
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Teacher not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(teacher, field, value)
        
    await db.commit()
    await db.refresh(teacher)
    return teacher



@admin.patch('/kid/{kid_id}')
async def update_kid(
    kid_id: int,
    data_edited: KidUpdate,
    admin: IsAdmin,
    db: db_connection,
):
    query = await db.execute(
        select(Kid)
        .options(selectinload(Kid.parents))
        .where(Kid.id == kid_id)
    )
    kid = query.scalars().first()
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")

    update_data = data_edited.model_dump(exclude_unset=True, exclude={'parents'})
    for field, value in update_data.items():
        setattr(kid, field, value)

    if 'parents' in data_edited.model_fields_set:
        if data_edited.parents == []:
            kid.parents = []
        else:
            result = await db.execute(
                select(Parent).where(Parent.id.in_(data_edited.parents))
            )
            kid.parents = result.scalars().all()

    await db.commit()
    await db.refresh(kid)
    return kid