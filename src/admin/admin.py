import uuid

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from src.admin.permissions import require_role
from src.admin.schemas import ContractBase, ContractUpdate, KidBase, KidUpdate, ParentCreate, ParentUpdate, RouteBase, RouteUpdate, SchoolBase, SchoolUpdate, StaffBase, StaffUpdate, TeacherBase, TeacherUpdate, TransportBase, TransportUpdate, UserAdminPublic, UserAdminResponse, UserUpdate
from src.dependencies import db_connection
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.kids.models import Kid
from src.parents.models import Parent, Contract
from src.staff.models import Staff
from src.routes.models import Route, Transport
from src.schools.models import School, Teacher
from src.auth.models import User
from PIL import UnidentifiedImageError
from starlette.concurrency import run_in_threadpool
from src.admin.image_utils import process_image, delete_profile_image
from src.config import config


admin = APIRouter()


@admin.post(
    path='/add-parent',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_parent(
    db: db_connection,
    parent_data: ParentCreate
):
    new_parent = Parent(
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        last_name=parent_data.last_name,
        phone_number=parent_data.phone_number,
        document_id=parent_data.document_id,
        home_address=parent_data.home_address,
    )
    db.add(new_parent)
    await db.commit()
    await db.refresh(new_parent)
    
    return new_parent


@admin.post(
    path='/add-staff',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_staff(
    db: db_connection,
    parent_data: StaffBase,
):    
    new_staff = Staff(
        last_name=parent_data.last_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        staff_type=parent_data.staff_type,
        date_of_birth=parent_data.date_of_birth,
        salary=parent_data.salary,
    )
    
    db.add(new_staff)
    await db.commit()
    await db.refresh(new_staff)
    
    return new_staff


@admin.patch(
    path='/{staff_id}/add-staff-picture',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_staff_picture(
    db: db_connection,
    staff_id: uuid.UUID,
    uploaded_file: UploadFile
):
    content = await uploaded_file.read()
    
    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )
        
    query = await db.execute(select(Staff).where(Staff.id == staff_id))
    chosen_staff = query.scalars().first()
    
    if not chosen_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    
    try:
        new_filename = await run_in_threadpool(process_image, "staff", content)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file."
        ) from error
        
    old_filename = chosen_staff.profile_photo_url
    
    chosen_staff.profile_photo_url = new_filename

    await db.commit()
    await db.refresh(chosen_staff)

    delete_profile_image("staff", old_filename)

    return chosen_staff


@admin.post(
    path='/add-transport',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_transport(
    db: db_connection,
    parent_data: TransportBase,
):
    
    new_transport = Transport(
        unique_transport_id=parent_data.unique_transport_id,
        model=parent_data.model,
        capacity=parent_data.capacity,
        status=parent_data.status
    )
    
    db.add(new_transport)
    await db.commit()
    await db.refresh(new_transport)
    
    return new_transport


@admin.patch(
    path='/{transport_id}/add-transport-picture',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_transport_picture(
    db: db_connection,
    transport_id: uuid.UUID,
    uploaded_file: UploadFile
):
    content = await uploaded_file.read()
    
    query = await db.execute(select(Transport).where(Transport.id == transport_id))
    chosen_transport = query.scalars().first()
    
    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )
        
    try:
        new_filename = await run_in_threadpool(process_image, "transport", content, False)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file."
        ) from error
        
    old_filename = chosen_transport.photo_url
    
    chosen_transport.photo_url = new_filename

    await db.commit()
    await db.refresh(chosen_transport)

    if chosen_transport.photo_url:
        delete_profile_image("transport", old_filename)

    return chosen_transport


@admin.post(
    path="/add-contract",
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_contract(
    db: db_connection,
    parent_data: ContractBase,
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




@admin.post(
    path='/add-school',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_school(
    db: db_connection,
    parent_data: SchoolBase,
):
    new_school = School(
        name=parent_data.name,
        address=parent_data.address,
        geo_latitude=parent_data.geo_latitude,
        geo_longitude=parent_data.geo_longitude
    )
    
    db.add(new_school)
    await db.commit()
    await db.refresh(new_school)
    
    return new_school
    
    
@admin.post(
    path='/add-teacher',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_teacher(
    db: db_connection,
    parent_data: TeacherBase,
):
    new_teacher = Teacher(
        last_name=parent_data.last_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        school_id=parent_data.school,
    )
    
    db.add(new_teacher)
    await db.commit()
    await db.refresh(new_teacher)
    
    return new_teacher


@admin.post(
    path='/add-kid',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_kid(
    db: db_connection,
    parent_data: KidBase,
):
    
    new_kid = Kid(
        last_name=parent_data.last_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        home_address=parent_data.home_address,
        school_id=parent_data.school_id,
        route_id=parent_data.route_id,
        contract_id=parent_data.contract_id,
        teacher_id=parent_data.teacher_id,
        date_of_birth=parent_data.date_of_birth,
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
    path='/{kid_id}/add-kid-picture',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_kid_picture(
    db: db_connection,
    kid_id: uuid.UUID,
    uploaded_file: UploadFile
):
    content = await uploaded_file.read()
    
    query = await db.execute(select(Kid).where(Kid.id == kid_id))
    chosen_kid = query.scalars().first()
    
    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )
        
    try:
        new_filename = await run_in_threadpool(process_image, "kids", content)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file."
        ) from error
        
    old_filename = chosen_kid.profile_photo_url
    
    chosen_kid.profile_photo_url = new_filename

    await db.commit()
    await db.refresh(chosen_kid)

    if chosen_kid.profile_photo_url:
        delete_profile_image("kids", old_filename)

    return chosen_kid


@admin.post(
    path='/add-route',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_route(
    db: db_connection,
    route_data: RouteBase,
):
    
    new_route = Route(
        name=route_data.name,
        estimated_duration_minutes=route_data.estimated_duration_minutes,
        driver_id=route_data.driver_id,
        babysitter_id=route_data.babysitter_id,
        transport_id=route_data.transport_id
    )
    
    db.add(new_route)
    await db.commit()
    await db.refresh(new_route)
    
    return new_route


@admin.patch(
    path="/edit-parent/{parent_id}",
    dependencies=[Depends(require_role("superadmin", "admin"))]

)
async def edit_parents(
    db: db_connection,
    data_edited: ParentUpdate, 
    parent_id: uuid.UUID
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
    path="/edit-staff/{staff_id}",
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def edit_staff(
    db: db_connection,
    data_edited: StaffUpdate, 
    staff_id: uuid.UUID
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
    path="/edit-transport/{transport_id}",
    dependencies=[Depends(require_role("superadmin", "admin"))]

)
async def edit_transport(
    db: db_connection,
    data_edited: TransportUpdate, 
    transport_id: uuid.UUID
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
    path="/edit-contract/{contract_id}",
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


@admin.patch(
    path="/edit-school/{school_id}",
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def edit_school(
    db: db_connection,
    data_edited: SchoolUpdate, 
    school_id: uuid.UUID
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
    path="/edit-teacher/{teacher_id}",
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def edit_teacher(
    db: db_connection,
    data_edited: TeacherUpdate, 
    teacher_id: uuid.UUID
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



@admin.patch(path='/kid/{kid_id}',
             dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def update_kid(
    kid_id: uuid.UUID,
    data_edited: KidUpdate,
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


@admin.patch(
    path="/edit-route/{route_id}",
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def edit_route(
    db: db_connection,
    data_edited: RouteUpdate, 
    route_id: uuid.UUID
):
    query = await db.execute(select(Route).where(Route.id == route_id))
    route = query.scalars().first()
    
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Route not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(route, field, value)
        
    await db.commit()
    await db.refresh(route)
    return route