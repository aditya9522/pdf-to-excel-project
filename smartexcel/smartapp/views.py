from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from . forms import FormDataForm

def default(request):
    return render(request, 'welcome.html')

def index(request):
    return render(request, 'form.html')

def display(request):
    if request.method == 'POST':
        objective = request.POST.get('objective', '')
        scope = request.POST.get('scope', '')
        concentration = request.POST.get('concentration', '')
        volums = request.POST.get('volums', '')
        ingradient = request.POST.get('ingradient', '')
        spec_io = request.POST.get('spec_io', '')
        spec_dates = request.POST.get('spec_dates', '')
        procedure = request.POST.get('procedure', '')
        calculation_details = request.POST.get('calculation_details', '')
        conclusion = request.POST.get('conclusion', '')
        
        form = FormDataForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
        
        return render(request, 'display.html', {
                'objective': objective,
                'scope': scope,
                'concentration': concentration,
                'volums': volums,
                'ingradient': ingradient,
                'spec_io': spec_io,
                'spec_dates': spec_dates,
                'procedure': procedure,
                'calculation_details': calculation_details,
                'conclusion': conclusion,
            })
    
    else:
        form = FormDataForm()
        context = {
            'form': form,
        }
        return render(request, 'form.html', context)

def generate_pdf(request):
    # Your data - replace with actual data retrieval logic
    data = {
        'Sample Objective': 'objective',
        'Sample Scope': 'scope',
        'Sample Concentration': 'concentration',
        'Sample Volumes': 'volums',
        'Sample Ingredient': 'ingradient',
        'Sample Spec. IO': 'spec_io',
        'Sample Spec. Dates': 'spec_dates',
        'Sample Procedure': 'procedure',
        'Sample Calculation Details': 'calculation_details',
        'Sample Conclusion': 'conclusion',
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ocr_data.pdf"'

    # Create PDF document
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "OCR Data")

    # Set initial y coordinate for table
    y = 750

    # Loop through data and add to PDF
    for key, value in data.items():
        p.setFont("Helvetica", 12)
        p.drawString(100, y, key + ":")
        p.drawString(250, y, value)
        y -= 20  # Move y coordinate up for next row

    p.save()
    return response