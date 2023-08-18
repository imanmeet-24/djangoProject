'''
Team Members
Manmeet Kaur - C0884039
Angrej Singh - C0884026
Riya Sidhu - C0886435
Dheepasri Ravichandran - C0883900
'''
from datetime import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.utils import timezone
from django.shortcuts import redirect
from .models import Quiz, Question, Answer
from django.shortcuts import render
from django.views import View


# View for user registration
class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm() # Instantiate the UserRegisterForm
        return render(request, 'register.html', {'form': form})  # Render the registration form template

    def post(self, request):
        form = UserRegisterForm(request.POST) # Instantiate the UserRegisterForm with form data
        if form.is_valid(): # Check if the form data is valid
            print(form.cleaned_data)  # Print the cleaned form data for reference
            user = form.save()  # Save the user instance
            print("Success message being generated")  # Print a success message
            messages.success(request, 'Your account has been successfully registered. You can now log in.')
            return redirect('login')  # Redirect the user to the login page
        else:
            print("Form is not valid") # Print an error message if the form is not valid
            messages.error(request, 'There was an error in the registration form. Please check your inputs.')
        return render(request, 'register.html', {'form': form}) # Re-render the registration form template



# View for the quiz
class QuizView(View):
    def get(self, request):
        questions = Question.objects.order_by('?')[:5]  # Get 5 random questions
        return render(request, 'quiz.html', {'questions': questions})   # Render the quiz template with the questions

    def post(self, request):
        user = request.user  # Get the current user

        total_score = 0  # Initialize the total score
        answers = []   # Initialize a list to store answers

        quiz = Quiz(user=user, score=total_score, quiz_taken_datetime=timezone.now())   # Create a new quiz instance
        quiz.save()   # Save the quiz instance to the database

        for question, answer in request.POST.items():  # Loop through POST data
            if 'question' in question:   # Check if the item is a question
                question_id = question.lstrip('question_')   # Get the question ID from the POST item
                correct_answer = Question.objects.get(id=question_id).correct_choice   # Get the correct answer for the question
                if answer == correct_answer:   # Check if the submitted answer is correct
                    total_score += 1   # Increment the total score
                answers.append(Answer(quiz=quiz, question_id=question_id, selected_choice=answer))  # Append the answer to the answers list

        quiz.score = total_score # Set the quiz score to the total score
        quiz.save()   # Save the updated quiz instance to the database

        Answer.objects.bulk_create(answers)  # Bulk create the answers in the database

        response = redirect('/PROJECT_SAMPLE1/score/')  # Redirect the user to the score page
        return response


# View for the user's score
class ScoreView(View):
    def get(self, request):
        user = request.user  # Get the current user
        quizzes = Quiz.objects.filter(user=user)  # Get all quizzes for the current user

        total_quizzes = quizzes.count()  # Get the total number of quizzes taken
        if total_quizzes > 0:   # Check if quizzes have been taken
            total_score = sum(quiz.score for quiz in quizzes)   # Calculate the scores
            average_score = (total_score / total_quizzes)
            highest_score = max(quiz.score for quiz in quizzes)
            lowest_score = min(quiz.score for quiz in quizzes)
        else:
            total_score = 0   # Set default values
            average_score = 0
            highest_score = 0
            lowest_score = 0

        answers = Answer.objects.filter(quiz__in=quizzes)   # Get all answers for the quizzes

        context = {
            'total_score': total_score,
            'average_score': average_score,
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'quizzes': quizzes,
            'answers': answers,
        }
        return render(request, 'score.html', context)  # Render the score template with context


# View for custom login
class CustomLoginView(LoginView):
    template_name = 'login.html'   # Set the template name for the login view

    def form_valid(self, form):   # Override the form_valid method
        remember_me = form.cleaned_data.get('remember_me')  # Get the remember_me field value
        if not remember_me:   # Check if remember_me is not checked
            self.request.session.set_expiry(0)  # Set the session expiry to 0 (no remembering)
        return super().form_valid(form)   # Call the parent form_valid method

    def get_success_url(self):   # Override the get_success_url method
        return reverse_lazy('main-page')  # Return the URL of the main page


# View for the main page
class MainPageView(View):
    template_name = 'main_page.html'   # Set the template name for the main page

    def get(self, request):  # Override the get method
        return render(request, self.template_name)  # Render the main page template


# View for user logout
def logout_view(request):   # Define the logout view
    logout(request)  # Log the user out
    return redirect('main-page')  # Redirect the user to the main page


# View for the base template
def base_view(request):  # Define the base view
    return render(request, 'base.html')  # Render the base template


# View for reviewing quiz
class ReviewQuizView(View):
    template_name = 'review_quiz.html'   # Set the template name for the review quiz page

    def get(self, request, quiz_id):  # Override the get method
        quiz = get_object_or_404(Quiz, id=quiz_id)   # Get the quiz instance based on quiz_id
        answers = Answer.objects.filter(quiz=quiz)  # Get all answers for the quiz
        return render(request, self.template_name, {'quiz': quiz, 'answers': answers})   # Render the review quiz template with context
