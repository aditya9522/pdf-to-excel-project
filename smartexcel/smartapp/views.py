from django.shortcuts import render, redirect
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import textwrap
from django.http import HttpResponse
from smartapp.models import FormData
from .utils import convert_pdf_to_excel
import io

def index(request):
    return render(request, 'index.html')

def form(request):
    if request.method == 'POST':
        objective = request.POST.get('objective')
        scope = request.POST.get('scope')
        concentration = request.POST.get('concentration')
        volums = request.POST.get('volums')
        ingradient = request.POST.get('ingradient')
        spec_io = request.POST.get('spec_io')
        spec_dates = request.POST.get('spec_dates')
        procedure = request.POST.get('procedure')
        calculation_details = request.POST.get('calculation_details')
        conclusion = request.POST.get('conclusion')
        
        form = FormData(
            objective=objective, 
            scope=scope, 
            concentration=concentration, 
            volums=volums, 
            ingradient=ingradient, 
            spec_io=spec_io,
            spec_dates=spec_dates,
            procedure=procedure,
            calculation_details=calculation_details,
            conclusion=conclusion
        )
        form.save()
        return redirect('display', form_id=form.id)

    return render(request, 'form.html')

def display(request, form_id):
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
        'Spec. Dates': form.spec_dates,
        'Procedure': form.procedure,
        'Calculation Details': form.calculation_details,
        'Conclusion': form.conclusion,
    }

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

def export_excel(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        excel_file = convert_pdf_to_excel(pdf_file)

        response = HttpResponse(
            excel_file.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
        return response

    return redirect('index')