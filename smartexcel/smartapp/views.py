from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import textwrap
from django.conf import settings
from django.http import HttpResponse
from smartapp.models import FormData
from openpyxl import Workbook
from .utils import pdf_to_excel
import os
import io
import datetime
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import pandas as pd


def index(request): 
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        user = authenticate(request, username = userid, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully.')
            return redirect('dashboard/')
        else:
            context = {
                'show': False
            }
            messages.error(request, 'Invalid credencial.')
            return render(request, 'index.html', context)
    context = {
        'show': False
    }
    return render(request, 'index.html', context)

def dashboard(request):
    records = FormData.objects.all().values()
    data = list(records)
    total_records = len(data)
    context = {
        'show': False,
        'data': data[::-1],
        'total_records': total_records,
    }
    if not request.user.is_authenticated:
        return redirect('/', context)
 
    return render(request, 'dashboard.html', context)

def bulkAction(request):
    if request.method == 'POST':
        attachmentCount = int(request.POST.get('rows'))
        bulk_dir = os.path.join(settings.BASE_DIR, 'bulk-files')
        os.makedirs(bulk_dir, exist_ok=True)

        # List to store dictionaries representing each row of the combined DataFrame
        data_list = []

        # Iterate over each uploaded file
        for i in range(1, attachmentCount + 1):
            file_object = request.FILES.get(f'attachment_{i}')
            if file_object:
                file_path = os.path.join(bulk_dir, file_object.name)
                
                # Save uploaded file to disk
                with open(file_path, 'wb') as destination:
                    for chunk in file_object.chunks():
                        destination.write(chunk)

                # Read Excel file into a DataFrame
                df = pd.read_excel(file_path)

                # Transform DataFrame to a dictionary and add the 'Sheet Name' column
                row_dict = {'Sheet Name': f'Sheet {i}'}
                for _, row in df.iterrows():
                    row_dict[row['Field']] = row['Value']
                
                data_list.append(row_dict)

                # Optionally, remove the file from disk after reading
                os.remove(file_path)
        
        # Convert the list of dictionaries to a DataFrame
        combined_df = pd.DataFrame(data_list)

        # Write combined DataFrame to a new Excel file
        combined_file_path = os.path.join(bulk_dir, 'combined.xlsx')
        combined_df.to_excel(combined_file_path, index=False)

        if os.path.exists(combined_file_path):
            with open(combined_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=combined.xlsx'
            return response

    return redirect('dashboard')

def update(request, form_id):
    if request.method == 'POST':
        #spec_details = datetime.datetime.strptime(spec_details, '%Y-%m-%d').date()
        form = get_object_or_404(FormData, id=form_id) 
        form.objective = request.POST.get('objective', '')
        form.scope = request.POST.get('scope', '')
        form.concentration = request.POST.get('concentration', '')
        form.volums = request.POST.get('volums', '')
        form.ingradient = request.POST.get('ingradient', '')
        form.spec_io = request.POST.get('spec_io', '')
        form.spec_details = request.POST.get('spec_details', '')
        form.procedure = request.POST.get('procedure', '')
        form.calculation_details = request.POST.get('calculation_details', '')
        form.conclusion = request.POST.get('conclusion', '')
        form.save()

        return redirect('dashboard')
    
    form = FormData.objects.get(id=form_id) 
    context = {
        'form': form
    }

    return render(request, 'edit.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def form(request):
    if FormData.objects.last():
        record_number = FormData.objects.last().id + 1
    else:
        record_number =  1

    context = {
        'show': False,
        'record_number': record_number
    }
    if not request.user.is_authenticated:
        return redirect('/', context)

    if request.method == 'POST':
        objective = request.POST.get('objective')
        scope = request.POST.get('scope')
        concentration = request.POST.get('concentration')
        volums = request.POST.get('volums')
        ingradient = request.POST.get('ingradient')
        spec_io = request.POST.get('spec_io')
        spec_details = request.POST.get('spec_details')
        procedure = request.POST.get('procedure')
        calculation_details = request.POST.get('calculation_details')
        conclusion = request.POST.get('conclusion')
        initiation_date = timezone.now().date()

        form = FormData(
            objective=objective, 
            scope=scope, 
            concentration=concentration, 
            volums=volums, 
            ingradient=ingradient, 
            spec_io=spec_io,
            spec_details=spec_details,
            procedure=procedure,
            calculation_details=calculation_details,
            conclusion=conclusion,
            initiation_date=initiation_date
        )
        form.save()
        return redirect('/dashboard/')

    return render(request, 'form.html', context)

def display(request, form_id):
    if not request.user.is_authenticated:
        return redirect('/')

    form = FormData.objects.get(id=form_id) 
    context = {
        'form': form
    }

    return render(request, 'view.html', context)

def generate_pdf(request, form_id):
    form = FormData.objects.get(id=form_id)
    data = {
        'Objective': form.objective,
        'Scope': form.scope,
        'Concentration': form.concentration,
        'Volumes': form.volums,
        'Ingredient': form.ingradient,
        'Spec. IO': form.spec_io,
        'Spec. Details': form.spec_details,
        'Procedure': form.procedure,
        'Calculation Details': form.calculation_details,
        'Conclusion': form.conclusion,
    }

    for key, value in data.items():
        if isinstance(value, datetime.date):
            data[key] = value.strftime('%Y-%m-%d')

    for key, value in data.items():
        if value is None:
            data[key] = ""

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="form_{form_id}.pdf"'

    # Create PDF document
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Define margins
    margin = 50
    usable_width = width - 2 * margin

    # Calculate center of the page
    center_x = width / 2

    # Set the title
    p.setFont("Helvetica-Bold", 16)
    title = "OCR Form Data"
    title_width = p.stringWidth(title, "Helvetica-Bold", 18)
    p.drawString(center_x - title_width / 2, height - margin, title)

    # Set initial y coordinate for content
    y = height - 2 * margin

    # Loop through data and add to PDF
    for key, value in data.items():
        if y < margin:  # Check if we need to add a new page
            p.showPage()  # Create a new page
            p.setFont("Helvetica-Bold", 16)
            p.drawString(center_x - title_width / 2, height - margin, title)
            y = height - 2 * margin  # Reset y coordinate for new page

        # Draw heading
        p.setFont("Helvetica-Bold", 14)
        p.drawString(margin + 20, y, f"{key}:")
        y -= 20

        # Wrap and draw content
        p.setFont("Helvetica", 12)
        wrapped_value = textwrap.wrap(value, width=int(usable_width / 6))  # Adjust width as needed
        for line in wrapped_value:
            if y < margin:  # Check if we need to add a new page
                p.showPage()  # Create a new page
                p.setFont("Helvetica-Bold", 16)
                p.drawString(center_x - title_width / 2, height - margin, title)
                y = height - 2 * margin  # Reset y coordinate for new page
            
            p.drawString(margin + 40, y, line)
            y -= 15  # Move y coordinate up for next row of content

        y -= 10  # Additional space between sections

    p.save()
    return response

def generate_excel(request, form_id):
    form = FormData.objects.get(id=form_id)
    data = {
        'Objective': form.objective,
        'Scope': form.scope,
        'Concentration': form.concentration,
        'Volumes': form.volums,
        'Ingredient': form.ingradient,
        'Spec. IO': form.spec_io,
        'Spec. Details': form.spec_details,
        'Procedure': form.procedure,
        'Calculation Details': form.calculation_details,
        'Conclusion': form.conclusion,
    }

    # Create a new Excel workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Form Data"

    # Set headers
    worksheet.cell(row=1, column=1, value="Field")
    worksheet.cell(row=1, column=2, value="Value")

    # Write data to Excel
    for index, (field, value) in enumerate(data.items(), start=2):
        worksheet.cell(row=index, column=1, value=field)  # Field
        worksheet.cell(row=index, column=2, value=value)  # Value

    # Adjust column width
    worksheet.column_dimensions['A'].width = 30
    worksheet.column_dimensions['B'].width = 60

    # Save the workbook to a BytesIO object
    excel_file = io.BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)

    # Create HTTP response with Excel file
    response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="form_data.xlsx"'
    
    return response

def export_excel(request, form_id):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        
        # Save the uploaded PDF file temporarily
        temp_dir = os.path.join(settings.BASE_DIR, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_pdf_path = os.path.join(temp_dir, pdf_file.name)
        
        with open(temp_pdf_path, 'wb') as temp_pdf:
            for chunk in pdf_file.chunks():
                temp_pdf.write(chunk)
        
        # Convert PDF to Excel
        workbook = pdf_to_excel(temp_pdf_path)
        
        # Remove the temporary PDF file
        os.remove(temp_pdf_path)
        
        # Create HTTP response with Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{pdf_file.name.split(".")[0]}.xlsx"'
        
        # Save the workbook to response
        excel_file = io.BytesIO()
        workbook.save(excel_file)
        excel_file.seek(0)
        response.write(excel_file.getvalue())
        
        return response
    return redirect('form', form_id=form_id)