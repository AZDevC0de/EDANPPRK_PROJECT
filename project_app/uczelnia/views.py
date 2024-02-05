from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from random import randint
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Education, Subject, News, CustomUser
from .forms import SignupForm, SubjectUpdateForm, SubjectCreateForm, NewsUpdateForm, NewsCreateForm, EducationUpdateForm
from django.db.models import Avg
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def round_half_up(n):
    # Zaokrąglam do najbliższej połówki
    return round(n * 2) / 2
#na korzyść studenta




class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_anonymous:
            return context

        if self.request.user.is_employee:
            context['subjects'] = Subject.objects.filter(teacher=self.request.user)
        else:
            educations = Education.objects.filter(student=self.request.user)
            context['educations'] = educations
            total_grades = []
            subjects_details = {}

            for education in educations:
                subject = education.subject
                if subject not in subjects_details:
                    subjects_details[subject] = {
                        'effects_grades': [],
                        'ects_points': subject.ects_points
                    }
                grade_info = {
                    'effect': education.effect,
                    'grade': education.grade
                }
                subjects_details[subject]['effects_grades'].append(grade_info)
                total_grades.append(education.grade)

            # Oblicz ogólną średnią ocen
            if total_grades:
                overall_average = round_half_up(sum(total_grades) / len(total_grades))
                context['overall_average'] = overall_average
            else:
                context['overall_average'] = None

            # Oblicz średnią dla każdego przedmiotu
            for details in subjects_details.values():
                grades = [eg['grade'] for eg in details['effects_grades']]
                if grades:
                    subject_average = round_half_up(sum(grades) / len(grades))
                    details['average_grade'] = subject_average
                else:
                    details['average_grade'] = None

            context['subjects_details'] = subjects_details

        return context


class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news'  # Nazwa zmiennej kontekstowej, pod którą lista obiektów będzie dostępna w szablonei


class NewsDetailsView(DetailView): #tu mam szczegóły pojedynczego obiektu mojej aktualnosci
    model = News
    template_name = 'news_details.html'
    context_object_name = 'news'


class NewsCreateView(CreateView):
    model = News
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list') ## URL do ktorego użytkownik zostanie przekierowany po
    # pomyślnym utworzeniu obiektu.
    form_class = NewsCreateForm #klasa formularza używana do tworzenia nowego obiektu mojich aktualnosci


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news_update.html'
    success_url = reverse_lazy('news_list')
    form_class = NewsUpdateForm


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class EducationCreateView(CreateView):
    model = Education
    template_name = 'education_create.html'
    success_url = reverse_lazy('education_list') ## URL, na który zostanie przekierowany użytkownik
    # po udanym utworzeniu obiektu
    fields = ['subject'] #jest to pole modelu, które mają być wyświetlone w formularzu

    def get_form(self, form_class=None):

        form = super().get_form(form_class) #tą metodą dostosowuje sobie  formularz przed jego wyświetleniem.
        form.fields['subject'].queryset = Subject.objects.filter( #ograniczam queryset dla pola 'subject'
            # do przedmiotów z semestru i wydziału użytkownika.
            Q(semester=self.request.user.semester) & Q(teacher__department=self.request.user.department))
        return form
    #zatwierdzam form
    def form_valid(self, form):
        subject = form.cleaned_data['subject'] #wywołuje  po zatwierdzeniu formularz

        effects = form.cleaned_data['subject'].effects.split(";")

        for effect in effects: #tworze te efekty
            e = Education()
            e.student = self.request.user
            e.subject = subject
            e.effect = effect
            e.grade = 0
            e.save()

        f = form.save(commit=False) # jeszcze go nie zapisuje w bazie
        # bo dzieki temu moge wprowadzić do obiektu dodatkowe zmiany przed jego zapisaniem
        f.student = self.request.user #automatycznie przypisuje studenta do nowo tworzonych rekordów
        f.save() #tera zapis
        return super().form_valid(form)
        #koncze proces przetwarzania formularza


class EducationDetailsView(DetailView):
    model = Education
    template_name = 'education_details.html'
    context_object_name = 'education'

    # zwracam obiekty związane z tą edukacją
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        education = self.get_object()
        student = education.student
        context['educations'] = Education.objects.filter(subject=education.subject, student=student).exclude(effect="")
        context['purpose'] = education.subject.purpose
        grades = [education.grade for education in context['educations']]
        if grades:
            average_grade = sum(grades) / len(grades)
            # Zaokrąglij średnią do najbliższej połówki
            context['rounded_average'] = round_half_up(average_grade)
        else:
            context['rounded_average'] = None
        return context


class EducationListView(ListView):
    model = Education
    template_name = 'education_list.html'
    context_object_name = 'educations'

    # zwracam tylko obiekty, których efekty ==""
    def get_queryset(self):

        if self.request.user.is_employee == False:
            educations = Education.objects.filter(Q(student=self.request.user) & Q(effect=""))
        else:
            educations = Education.objects.filter(Q(subject__teacher=self.request.user) & Q(effect=""))
        return educations


class EducationUpdateView(UpdateView):
    model = Education
    template_name = 'education_update.html'
    success_url = reverse_lazy('education_list') #przekierowauje pod ten url po auktualizacji
    form_class = EducationUpdateForm

   #Znajduje obiekt edukacyjny, który ma ten sam przedmiot i ucznia,
    # co aktualny obiekt, gdzie efekt jest równy "" i podnieś ocenę."
    def form_valid(self, form):
        f = form.save()
        #znajduje powiązany rekord Education (main_e), który ma ten sam przedmiot (subject) i
        # studenta (student), ale z pustym polem effect.
        main_e = Education.objects.get(Q(subject=f.subject) & Q(student=f.student) & Q(effect=""))
        avg_grade = Education.objects.filter(Q(subject=f.subject) & Q(student=f.student)).exclude(effect="").aggregate(
            Avg('grade')).get('grade__avg')
        main_e.grade = avg_grade
        main_e.save()
        return super().form_valid(form)


class EducationDeleteView(DeleteView):
    model = Education
    template_name = 'education_delete.html'
    success_url = reverse_lazy('education_list')

class OnlyAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class UserVerificationListView(OnlyAdminMixin, ListView):
    model = CustomUser
    template_name = 'registration/verification_list.html'
    context_object_name = 'users_to_verify'
    queryset = CustomUser.objects.filter(is_verified=False)
class UserListView(ListView):
    model = CustomUser
    template_name = 'user_list.html'

    def get_queryset(self):

        users = CustomUser.objects.filter(
            Q(department=self.request.user.department) & Q(education__subject__teacher=self.request.user)).distinct()
        return users
        # filtruje użytkowników na podstawie ich wydziału (department) oraz tego, czy są nauczycielami
        # w jakimś rekordzie Education. distinct() zapewnia,
        # że każdy użytkownik pojawi się na liście tylko raz, nawet jeśli spełnia kryteria wielokrotnie.

class UserDetailsView(DetailView):
    model = CustomUser
    template_name = 'user_details.html'
    context_object_name = 'customuser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        educations = Education.objects.filter(student=user)

        subjects_details = {}
        for education in educations:
            if education.subject not in subjects_details:
                subjects_details[education.subject] = {
                    'effects_grades': [],
                    'ects_points': education.subject.ects_points
                }
            subjects_details[education.subject]['effects_grades'].append((education.effect, education.grade))

        for subject, details in subjects_details.items():
            grades = [grade for effect, grade in details['effects_grades']]
            average_grade = sum(grades) / len(grades) if grades else 0
            details['average_grade'] = round_half_up(average_grade)

        context['subjects_details'] = subjects_details.items()
        return context

# używam do wyświetlania szczegółów użytkownika w formacie PDF

class UserPdfView(DetailView):
    model = CustomUser
    template_name = 'user_pdf.html'
    context_object_name = 'customuser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        educations = Education.objects.filter(student=user)
        subjects_details = {}

        for education in educations:
            subject = education.subject
            if subject not in subjects_details:
                subjects_details[subject] = {
                    'effects_grades': [],
                    'ects_points': subject.ects_points
                }
            subjects_details[subject]['effects_grades'].append({
                'effect': education.effect,
                'grade': education.grade
            })

        for subject, details in subjects_details.items():
            grades = [eg['grade'] for eg in details['effects_grades']]
            average_grade = sum(grades) / len(grades) if grades else 0
            details['average_grade'] = round_half_up(average_grade)

        context['subjects_details'] = [
            {
                'subject': subject,
                'ects_points': details['ects_points'],
                'effects_grades': details['effects_grades'],
                'average_grade': details['average_grade']
            }
            for subject, details in subjects_details.items()
        ]

        return context

#umożliwiam użytkownikom edycję określonych pól (tutaj tylko semester) w ich profilach CustomUser.
class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'user_update.html'
    success_url = reverse_lazy('user_list')
    fields = ['semester'] #określam, które pola modelu mają być wyświetlane i edytowane w formularzu

    def form_valid(self, form):
        f = form.save(commit=False)
        f.save()
        return super().form_valid(form)


class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'user_delete.html' #wyświetlenie strony z prośbą o potwierdzenie usunięcia użytkownika
    success_url = reverse_lazy('user_list')


class SubjectListView(ListView):
    model = Subject
    template_name = 'subject_list.html' #renderowanie listy przedmiotów
    context_object_name = 'subjects' #nazwa zmiennej kontekstowej dla listy przedmiotów w szablonie


    def get_queryset(self):
        #filtruje przedmioty na podstawie wydziału, do którego należy nauczyciel (w tym przypadku zalogowany użytkownik)
        subjects = Subject.objects.filter(teacher__department=self.request.user.department)
        return subjects


class SubjectDetailsView(DetailView):
    model = Subject
    template_name = 'subject_details.html'
    context_object_name = 'subject'


class SubjectCreateView(CreateView):
    model = Subject
    template_name = 'subject_create.html'
    form_class = SubjectCreateForm #klasa formularza używana do tworzenia nowego przedmiotu.

    def form_valid(self, form):
        f = form.save(commit=False) #tworze obiekt ale jeszcze go nie zapisuje
        #Przypisuje zalogowanego użytkownika (nauczyciela) do właściwości teacher nowo tworzonego przedmiotu
        f.teacher = self.request.user
        f.save()
        return super().form_valid(form)


class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'subject_update.html'
    form_class = SubjectUpdateForm


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'subject_delete.html' #potwierdzenie usunięcia przedmiotu
    success_url = reverse_lazy('subject_list')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False  # Upewnij się, że nowy użytkownik nie jest jeszcze zweryfikowany
            user.save()
            # Wyślij e-mail do administratora z prośbą o weryfikację nowego użytkownika
            # send_verification_request_to_admin(user)
            return redirect('registration_success')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def verify_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponse("Brak uprawnień.")
    user_to_verify = get_object_or_404(CustomUser, id=user_id)
    user_to_verify.is_verified = True
    user_to_verify.save()

    # send_confirmation_email(user_to_verify)
    # return HttpResponse("Konto użytkownika zostało zweryfikowane.")
    return render(request, 'registration/user_verification_success.html')


def logout_view(request):
    logout(request)
    return redirect('home')


class EditProfile(LoginRequiredMixin, UpdateView): # tylko zalogowani użytkownicy mają dostęp do tego widoku,aktualizacja
    model = CustomUser
    template_name = 'registration/edit_profile.html' #html do renderowania formularza edycji
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'avatar'] #lista pol do edycji edit_profile.html

    def get_object(self, queryset=None): #edytuje zalogowanego usera
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('home') #po edycji ide do strony głównej

def registration_success(request):
    return render(request, 'registration/registration_success.html')


def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_home(request):
    # Twoja logika dla strony głównej administratora
    return render(request, 'admin_home.html')

def user_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_home')  # Nazwa URL dla strony głównej administratora
    else:
        return redirect('home')  # Nazwa URL dla standardowej strony głównej