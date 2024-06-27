from django.shortcuts import render, redirect,get_object_or_404
from .models import Book, Category
from django.contrib.auth.forms import UserCreationForm
from  .forms import CreateUserForm
from django.contrib import messages
from django.http import HttpResponse,Http404,FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .recommendationsys import SkillPredictor
import os
from django.conf import settings
from .summariser import find_summary
from fpdf import FPDF
from io import BytesIO
from django.views import View
from django.conf import settings
# from .summariser import find_summary
# Create your views here.
def home(request):
    recommended_books = Book.objects.filter(recommended_books = True)
    fiction_books = Book.objects.filter(fiction_books = True)
    business_books = Book.objects.filter(business_books = True)
    return render(request, 'home.html', {'recommended_books': recommended_books,
    'business_books': business_books, 'fiction_books': fiction_books
    })

def all_books(request):
    books = Book.objects.all()
    return render(request, 'all_books.html', {'books':books})

def recommend_starting(request):
     skills1 = ["Spreadsheet", "Generator", "Asset Management", "Reinforcement Learning Model Development", "Random Forest", "Postgresql", "Tensorflow", "Eigenvalues And Eigenvectors", "Data Collection", "Statistical Analysis", "Probabilistic Neural Network", "Logistic Regression", "Describe fundamental principles of machine learning on Azure", "Database (DBMS)", "Statistics", "SciPy and scikit-learn", "Geographic Information System (GIS)", "MySQL", "Data Manipulation","Professional", "Email Writing", "Presentation"
]
     skills2 = ["Asset Management", "Reinforcement Learning Model Development", "Basic Tensor Functionality", "Random Forest", "Postgresql", "SAS Visual Analytics", "Eigenvalues And Eigenvectors", "Data Collection", "Custom and Exotic Models with Functional API", "StyleGANs", "Gradient Descent", "Describe fundamental principles of machine learning on Azure", "Database (DBMS)", "Statistics", "Geographic Information System (GIS)", "Data Manipulation", "option pricing and risk management", "Storyboarding", "User-Centered Design (Create basic visualizations that match data and user needs)", "Stakeholder Management", "Machine Learning Concepts", "Markov Model", "Interactivity", "Delta Lake", "Bioconductor", "Machine Learning Model Evaluation and Optimization","Teaching", "English Language", "Lesson Plan"

]
     skills3 = ["Reinforcement Learning Trading Strategy Development", "Reports", "Markov Chain Monte Carlo (MCMC)", "Basic Tensor Functionality", "Random Forest", " Cloud Databases", "Q-learning using financial problems", "Tensorflow", "SAS Visual Analytics", "Data Collection", "Custom and Exotic Models with Functional API", " Big Data", "Database (DBMS)", "MySQL", " Financial Accounting", "Alteryx", "Teradata", "User-Centered Design (Create basic visualizations that match data and user needs)","English Grammar", "Perfect Tenses", "English Language"

]

     return render(request,'recommendation.html',{'skills1': skills1,"skills2":skills2,"skills3":skills3})

def recommend_category(request):
    skills1 = ["Spreadsheet", "Generator", "Asset Management", "Financial Analysis", "Market Research", "Strategic Planning","Information Engineering", " Python Programming", " Extraction","Software Architecture", " Java", " Software Design Pattern","Visual Communication", " Branding Communication", " Graphic Design","Professional", "Email Writing", "Presentation","goal setting", "Persuasion", "Delegation","Statistics", "Punctuation", "Music","wellbeing", "Whole Genome Sequencing", "Emergency Medicine","Artificial Intelligence (AI)", "Presentation", "Arduino","Differential Equations", "R Programming", "Bayes' Theorem"
]
    skills2 = ["Asset Management","Basic Tensor Functionality","Data Manipulation","Strategic Leadership", "Financial Risk Management", "Financial Technology","Operating System Security", " database vulnerabilities", " Cybersecurity","Scala Programming", " Parallel Computing", " Apache Spark","Short Story Writing", " Fiction Writing", " Creativity","Teaching", "English Language", "Lesson Plan","Happiness", "Creativity", "Leadership","Statistical Inference", "Essay Writing", "Music production","patient-centered care", "Viterbi Algorithm", "Emergency Medical Technician","Digital Design", "Data Analysis", "Python Programming","Vector Calculus", "Linear Regression", "Bayesian Probability"
]
    skills3 = ["Reports", "Markov Chain Monte Carlo (MCMC)"," Cloud Databases","Algorithmic Trading", "Design Thinking", "Performance Management","Devops", " Python Programming", " Node.Js","Graph Theory", " Number Theory", " Cryptography","Photography", " Design", " Art","English Grammar", "Perfect Tenses", "English Language","Personality Development", "Communication", "Coaching","R Programming", "Academic Writing", "Improvisation","improved symptom management", "Suffix Tree", "EMT","Manufacturing Engineer", "Sustainability", "Internet Of Things (IOT)","Matrix Algebra", "Statistical Hypothesis Testing", "Probability"
]
    if request.method == 'POST':
        # Get user input from the form
        skill1 = request.POST.get('skill1')
        skill2 = request.POST.get('skill2')
        skill3 = request.POST.get('skill3')
        
        # Initialize the SkillPredictor object
        predictor = SkillPredictor()
        
        # Call the predict_category_from_skills method with user input
        result = predictor.predict_category_from_skills(skill1, skill2, skill3)
        
        # Pass the result to the template
        return render(request, 'recommendation.html', {'skills1': skills1,"skills2":skills2,"skills3":skills3,'result': result})
    else:
        return render(request, 'recommendation.html',{"skills1":skills1,"skills2":skills2,"skills3":skills3})


def category_detail(request, slug):
    category = Category.objects.get(slug = slug)
    return render(request, 'genre_detail.html', {'category': category})

def cat_detail(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)
        print(f"Category found: {category}")
    except Category.DoesNotExist:
        print(f"Category with slug '{slug}' does not exist.")
        return render(request, '404.html', {'error': f"Category '{slug}' not found."})

    print(f"Slug passed: {slug}")
    return render(request, 'genre_detail.html', {'category': category})

@login_required(login_url='login')
def book_detail(request, slug):
    book = Book.objects.get(slug = slug)
    book_category = book.category.first()
    similar_books = Book.objects.filter(category__name__startswith = book_category)
    return render(request, 'book_detail.html', {'book': book, 'similar_books': similar_books})

def search_book(request):
    searched_books = Book.objects.filter(title__icontains = request.POST.get('name_of_book'))
    return render(request, 'search_book.html', {'searched_books':searched_books})

def register_page(request):
    register_form = CreateUserForm()
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.info(request, "Account Created Successfully!")
            return redirect('login')
           
    return render(request, 'register.html', {'register_form': register_form})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid Credentials")
        
    
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')
    
def target_view(request):
    return render(request, 'home.html')

def summarise_pdf(request):
    if request.method == 'POST':
        pdf_filename = request.POST.get('pdf_path', '')  # Get the PDF path from POST data
        pdf_path_c = pdf_filename.replace('media/', '', 1)
        pdf_filenam = os.path.basename(pdf_path_c)
        
        # Extract the filename without the extension
        filename_without_extension = os.path.splitext(pdf_filenam)[0]
        
        # Construct the new filename
        new_filename = f"{filename_without_extension}_summary.pdf"
        
        # Construct the full path to the new summary file
        new_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf', new_filename)
        
        # Construct the full path to the original PDF file
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path_c.lstrip('/'))
        
        # Debug output for constructed paths
        # Check if the summary file exists
        if os.path.exists(new_file_path):
        
            # Optionally, provide the file for download
            # response = FileResponse(open(new_file_path, 'rb'), as_attachment=True, filename=new_filename)
            # return response
            response = FileResponse(open(new_file_path, 'rb'), as_attachment=True, filename=os.path.basename(new_file_path))
            return response
        else:
            
        
        # Your summarizer logic here
            sum_path=find_summary(pdf_path)  # Call your summarizer function with pdf_path
        # return HttpResponse(summary)  # Return a response with the summary (or redirect as needed)
            if os.path.exists(sum_path):
                # File exists, provide the file for download
                response = FileResponse(open(sum_path, 'rb'), as_attachment=True, filename=os.path.basename(sum_path))
                return response
        return render(request, 'book_detail.html')
    else:
        return HttpResponse('Method not allowed', status=405)





    
'/Users/indulekhaag/Downloads/Django-Book-WebSite-main/media/1-1_summary.pdf'
'/Users/indulekhaag/Downloads/Django-Book-WebSite-main/media/pdf/1-1_summary.pdf'