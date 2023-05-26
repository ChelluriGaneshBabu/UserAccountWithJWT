from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import models,oauth2
from app.database import get_db
import pdfkit,jinja2
import os


router = APIRouter()

# pdf creation
@router.get("/profile_pdf", status_code= status.HTTP_201_CREATED)
def generate_profile_pdf(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # check whether the user profile exist or not
    profile_data = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if profile_data is None:
        raise HTTPException(status_code=404, detail= "Profile not found")
    
    first_name = profile_data.first_name
    last_name = profile_data.last_name
    date_of_birth= profile_data.date_of_birth.strftime("%d %b, %Y")
    phone_number = profile_data.phone_number
    address = profile_data.address
    highest_qualification = profile_data.highest_qualification

    # assigning the python variables to html placeholders
    context = {"first_name":first_name, "last_name":last_name, "date_of_birth":date_of_birth, "phone_number":phone_number, "address":address, "highest_qualification":highest_qualification}
    
    #The Jinja2 template loader is configured to load templates from the specified directory 
    template_loader = jinja2.FileSystemLoader("C:/Users/CS0142303/Desktop/Python/UserAccountWithJWT/app/routers/")
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template("profile_template.html")
    output_text = template.render(context)

    # configuring pdfkit to point to our installation of wkhtmltopdf  
    config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")  

    # Generate PDF from HTML using pdfkit
    pdf_content = pdfkit.from_string(output_text, False, configuration = config)


# Save the PDF to a file
    output_filename = "output.pdf"
    output_filepath = os.path.abspath(output_filename)
    with open(output_filepath, "wb") as file:
        file.write(pdf_content)

    # Return the PDF file as a response with filename and location
    return {
        "filename":output_filename,
        "file_path":output_filepath
    }

